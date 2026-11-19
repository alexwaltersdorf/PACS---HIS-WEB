# Contexto compartilhado

Última revisão: 18/11/2026.

Nova diretriz: Codex, Claude Code e Google Gemini colaborarão na construção da empresa e da plataforma, com leitura/atualização do GitHub e discussão explícita de alternativas. Consultar `CONSELHO-LLMS.md`; não substituir três provedores por três personas de um mesmo modelo. O protocolo compartilhado distingue participantes previstos, consultas reais e automação ainda não implementada.

## Confirmado pelo usuário

Plataforma web com viewer DICOM, PACS e RIS integrado; worklist; padrões de saúde brasileiros/internacionais; laudos estruturados para US/CT/MR/MG/RX; assistência radiológica por subespecialidade; pesquisa de artigos; discussão multidisciplinar; integração de exames laboratoriais, cardiológicos, EEG, espirometria e outros; engenharia e segurança com atualização contínua. Destino do planner: este repositório GitHub.

Eden e nReport são referências funcionais. A base anterior analisou interface do Eden e revisou erros do anexo técnico. Não há fonte proprietária, licença para copiar templates de terceiros ou validação clínica importada dessas referências. A consulta pública ao app nReport não forneceu conteúdo legível nesta rodada.

## Premissas de projeto

Brasil; possibilidade de múltiplas organizações; governança por finalidade de uso; profissionais habilitados responsáveis pela interpretação e assinatura. A autonomia começa com pesquisa e propostas rastreáveis. Modelos e referências são intercambiáveis por contrato e avaliação, não por troca silenciosa de nome de provedor.

## Ainda desconhecido

Instituição piloto; responsáveis clínicos/regulatórios/privacidade; número de unidades; modalidade e tarefa de IA inicial; volume/concorrência; hardware; infraestrutura local/nuvem; fornecedores de RIS/HIS; perfis de interface; contratos/licenças de terminologia; dados autorizados para avaliação; orçamento; critérios clínicos quantitativos; política de assinatura e retenção.

Esses dados não foram inventados. O squad pode elaborar arquitetura e exemplos sintéticos agora; tarefas clínicas ou implantação dependem dos insumos pertinentes. Perguntar apenas o que bloqueia a tarefa ativa e reutilizar decisões registradas.

## Organização da execução

Orquestrador recebe objetivo e escopo, seleciona os agentes necessários, define propriedade dos arquivos e reúne artefatos. Runs documentais em `runs/AAAA-MM-DD/identificador/`; dados clínicos nunca nesse diretório público. Cada artefato declara observado, inferido, proposto e desconhecido, fontes, entradas ausentes e próximos responsáveis.
