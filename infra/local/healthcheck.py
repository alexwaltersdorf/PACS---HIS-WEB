"""Authenticated local health probe; never print credentials or medical data."""
import base64
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

try:
    users = json.loads(Path('/run/secrets/orthanc-users.json').read_text())['RegisteredUsers']
    username, password = next(iter(users.items()))
    token = base64.b64encode(f'{username}:{password}'.encode()).decode()
    request = Request('http://127.0.0.1:8042/system', headers={'Authorization': 'Basic ' + token})
    with urlopen(request, timeout=3) as response:
        sys.exit(0 if response.status == 200 else 1)
except Exception:
    sys.exit(1)
