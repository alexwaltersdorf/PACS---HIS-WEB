"""Validate documentation contracts. Does not assess clinical or regulatory fitness."""
from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from council import load_messages

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def main() -> int:
    json_files = list(ROOT.glob("config/*.json")) + list(ROOT.glob("schemas/*.json"))
    json_files += list(ROOT.glob("templates/*.json")) + list(ROOT.glob("examples/*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError) as exc:
            errors.append(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
    if errors:
        return finish()

    registry = load("config/agents.json")
    agents = registry["agents"]
    ids = {item["id"] for item in agents}
    require(bool(agents) and len(agents) == len(ids), "Agent IDs must be nonempty and unique")
    require(registry["runtime_enabled"] is False, "Planner must not claim an enabled runtime")
    for agent in agents:
        profile = ROOT / agent["profile_file"]
        require(profile.is_file(), f"Missing profile: {profile}")
        if profile.is_file():
            text = profile.read_text(encoding="utf-8")
            require(f"name: {agent['id']}\n" in text, f"Profile/name mismatch: {agent['id']}")
            require("description:" in text and "Acione quando" in text, f"Missing trigger: {agent['id']}")
            require("## Handoff" in text and "Write" in text, f"Missing output contract: {agent['id']}")
        for key in ("input_schema", "output_schema"):
            require((ROOT / agent[key]).is_file(), f"Missing {key}: {agent['id']}")
        require(agent["enabled"] is False, f"Agent unexpectedly enabled: {agent['id']}")
        require(agent["can_sign_report"] is False, f"Agent can sign: {agent['id']}")
        require(agent["can_deploy_production"] is False, f"Agent can deploy: {agent['id']}")
        require(agent["tool_bindings"] == [], f"Planner has unreviewed bindings: {agent['id']}")

    profiles = load("config/profiles.json")["profiles"]
    profile_ids = {item["id"] for item in profiles}
    require(bool(profiles) and len(profile_ids) == len(profiles), "Specialty profile IDs must be unique")
    for profile in profiles:
        require(profile["agent_id"] in ids, f"Unknown agent in profile: {profile['id']}")
        require(profile["clinical_use_enabled"] is False, "Specialty profile claims clinical activation")
    policy = load("config/autonomy-policy.json")
    require(not policy["runtime_enabled"] and not policy["clinical_use_enabled"], "Policy must remain design-only")
    require(policy["defaults"]["deny_agent_report_signature"], "Missing signature restriction")
    require(policy["defaults"]["deny_self_promotion"], "Missing self-promotion restriction")

    council = load("config/llm-council.json")
    participants = council["participants"]
    require({item["id"] for item in participants} == {"codex", "claude-code", "gemini"}, "Missing council participant")
    require(len(participants) == 3, "Council participant IDs must be unique")
    require(council["automatic_dispatch_enabled"] is False, "Automatic dispatch not implemented")
    for item in participants:
        require((ROOT / item["entrypoint"]).is_file(), f"Missing entrypoint: {item['id']}")
    require((ROOT / council["canonical_document"]).is_file(), "Missing shared council document")
    load_messages(ROOT)

    validators = {}
    for path in ROOT.glob("schemas/*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[path.name] = Draft202012Validator(schema, format_checker=FormatChecker())
    examples = {
        "examples/case-synthetic.json": "case-context.schema.json",
        "examples/agent-result-synthetic.json": "agent-result.schema.json",
        "examples/task-synthetic.json": "task-request.schema.json",
    }
    for path, schema_name in examples.items():
        for issue in validators[schema_name].iter_errors(load(path)):
            errors.append(f"{path}: {issue.message}")
    task = load("examples/task-synthetic.json")
    require(task["agent_id"] in ids and task["profile_id"] in profile_ids, "Unresolved sample routing")
    for ref in task["artifact_refs"] + [task["context_ref"]]:
        require((ROOT / ref).is_file(), f"Missing sample artifact: {ref}")

    modalities = set()
    for path in ROOT.glob("templates/*.json"):
        template = json.loads(path.read_text(encoding="utf-8"))
        modalities.add(template["modality"])
        for issue in validators["report-template.schema.json"].iter_errors(template):
            errors.append(f"{path.name}: {issue.message}")
        field_ids = [field["id"] for field in template["fields"]]
        require(len(set(field_ids)) == len(field_ids), f"Duplicate field IDs: {path.name}")
    require(modalities == {"US", "CT", "MR", "MG", "DX"}, "Missing modality template")

    # Negative cases ensure the guard contracts reject signature/activation claims.
    bad_result = copy.deepcopy(load("examples/agent-result-synthetic.json"))
    bad_result["human_review_required"] = False
    bad_result["signed_by"] = "synthetic-agent"
    require(not validators["agent-result.schema.json"].is_valid(bad_result), "Unsafe result passed contract")
    unsupported_finding = copy.deepcopy(load("examples/agent-result-synthetic.json"))
    unsupported_finding["status"] = "completed_draft"
    unsupported_finding["findings"] = [{"statement": None, "evidence_refs": [], "assessment_state": "present"}]
    require(not validators["agent-result.schema.json"].is_valid(unsupported_finding), "Unsupported finding passed contract")
    bad_template = copy.deepcopy(load("templates/us-base.json"))
    bad_template["clinical_use_enabled"] = True
    require(not validators["report-template.schema.json"].is_valid(bad_template), "Enabled template passed draft contract")

    with (ROOT / "planning/backlog.csv").open(encoding="utf-8", newline="") as stream:
        backlog = list(csv.DictReader(stream))
    tasks = {item["id"]: item for item in backlog}
    require(bool(backlog) and len(tasks) == len(backlog), "Backlog IDs must be nonempty and unique")
    edges = {key: [dep for dep in item["dependencies"].split(";") if dep] for key, item in tasks.items()}
    for key, item in tasks.items():
        require(item["owner_role"] in ids, f"Unknown backlog owner: {key}")
        require(item["status"] in {"planned", "ready", "in_progress", "in_review", "validated", "done", "blocked"}, f"Unknown task state: {key}")
        if item["status"] in {"validated", "done"}:
            evidence = item.get("evidence", "")
            evidence_path = (ROOT / evidence).resolve()
            require(bool(evidence) and evidence_path.is_relative_to(ROOT.resolve()) and evidence_path.is_file(), f"Missing implementation evidence: {key}")
        require(all(dep in tasks for dep in edges[key]), f"Missing dependency: {key}")
    visiting, visited = set(), set()

    def visit(key: str) -> None:
        if key in visiting:
            errors.append(f"Backlog dependency cycle: {key}")
            return
        if key in visited:
            return
        visiting.add(key)
        for dep in edges[key]:
            if dep in tasks:
                visit(dep)
        visiting.remove(key)
        visited.add(key)
    for key in tasks:
        visit(key)

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        body = path.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\]\(([^)]+)\)", body):
            link = match.group(1).strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            require(target.is_relative_to(ROOT), f"Link escapes repository: {path.name}: {link}")
            require(target.exists(), f"Broken local link: {path.name}: {link}")
    print(f"Checked {len(json_files)} JSON files, {len(agents)} agents, {len(profiles)} specialty profiles, 5 templates and {len(backlog)} backlog items.")
    return finish()


def finish() -> int:
    if errors:
        print("\n".join(f"ERROR: {message}" for message in errors), file=sys.stderr)
        return 1
    print("Planner checks passed. Clinical validation and runtime execution are not covered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
