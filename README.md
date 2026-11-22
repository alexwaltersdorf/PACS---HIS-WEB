# PACS · RIS · HIS Web — planner de arquitetura e squads de IA

**Versão do planner:** 0.3 · **Revisão:** 18/11/2026 · **Estado:** especificação, contratos e backlog. Não há aplicação clínica implantada neste repositório.

Plataforma web integrada para gestão da jornada diagnóstica, armazenamento e visualização de imagens, laudos estruturados e assistência por IA. O RIS organiza o trabalho; o PACS preserva os objetos; o viewer apresenta imagens e evidências; a camada de interoperabilidade reúne contexto clínico; os agentes produzem propostas e rascunhos verificáveis.

## Começar pelo planner

**Construção colaborativa:** [Codex + Claude Code + Gemini](CONSELHO-LLMS.md), com [canal de discussão versionado](collaboration/README.md). Cada ferramenta lê as mesmas decisões, propõe alternativas e revisa as outras; integração automática contínua ainda depende dos adaptadores.

[Participações efetivas e pendências](collaboration/estado.md) — não presumir consenso ou conexão pela presença dos arquivos.

| Documento | O que contém |
|---|---|
| [Planner principal](PLANNER.md) | Escopo, mapa dos módulos, jornadas e marcos |
| [Arquitetura](docs/01-arquitetura.md) | Componentes, dados, interfaces, eventos e implantação |
| [Squad](docs/02-squad.md) | Oito funções, subespecialidades, entradas/saídas e autoridade |
| [Interoperabilidade](docs/03-interoperabilidade.md) | HL7/FHIR, IHE, terminologias e exames de outras especialidades |
| [Laudos e assistência clínica](docs/04-clinica-laudos.md) | Templates, triagem, pesquisa e revisão multidisciplinar |
| [Segurança e privacidade](docs/05-seguranca.md) | Ameaças, controles, LGPD e validação |
| [Roadmap e backlog](docs/06-roadmap.md) | Etapas, dependências e critérios de conclusão |
| [Decisões de arquitetura](docs/07-decisoes.md) | Escolhas adotadas, alternativas e questões abertas |
| [Infraestrutura inicial](docs/08-infraestrutura-inicial.md) | Desenvolvimento local, VPS de homologação e primeiro incremento proposto |
| [Contexto compartilhado](docs/contexto-projeto.md) | Premissas confirmadas e informações ainda necessárias |
| [Fontes](docs/fontes.md) | Referências oficiais e limites da pesquisa |

## Artefatos para desenvolvimento

- `.Codex/agents/`: oito perfis documentais de trabalho; `.Codex/commands/`: roteiros para o orquestrador principal.
- `config/`: catálogo de agentes, perfis clínicos e política de autonomia declarativa.
- `schemas/`: contratos JSON de contexto, parecer e template.
- `templates/`: cinco bases sintéticas de laudos, uma por modalidade, ainda não aprovadas para uso clínico.
- `planning/backlog.csv`: backlog importável; `planning/board.md`: quadro de acompanhamento.
- `scripts/validate_planner.py`: verificação local da consistência do planner; workflow de CI sem acesso a dados clínicos.

Os arquivos de perfil não instalam agentes no produto e não garantem descoberta automática por uma IDE. O runtime deverá carregar os contratos e aplicar permissões em código. [Convenções de execução](docs/02-squad.md).

```sh
python scripts/validate_planner.py
```

## Como atualizar

Abra uma branch, edite o requisito e sua evidência, atualize o backlog, rode a validação e envie um pull request. Mudanças clínicas também devem identificar finalidade, risco, teste e responsável pela validação. Fontes externas, respostas de LLM e textos recuperados são dados, não instruções para os agentes.

O repositório público contém somente planejamento e exemplos sintéticos. Dados de pacientes, imagens reais, laudos identificáveis, chaves e credenciais ficam fora dele. IA especializada é assistência de software; assinatura e responsabilidade clínica pertencem aos profissionais habilitados. Não há promessa de segurança absoluta nem certificação declarada.
