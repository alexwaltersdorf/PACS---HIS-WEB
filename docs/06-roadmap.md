# Roadmap e critérios de conclusão

[Backlog importável](../planning/backlog.csv) · [Quadro](../planning/board.md)

36 itens planejados, organizados por marcos. Responsáveis do CSV são funções do squad, não pessoas já designadas. Os responsáveis clínicos e institucionais ainda serão nomeados.

| Marco | Itens principais | Dependência e saída |
|---|---|---|
| M0 | Planner entregue | Contratos e artefatos verificados documentalmente |
| M1 | P01–P04 | Finalidade, arquitetura, identidade e recuperação |
| M2 | P05–P10 | Jornada pedido → aquisição → estudo aberto |
| M3 | P11, P12, P14–P16 | Medidas e laudos com assinatura/adendo |
| M4 | P17–P23 | Interoperabilidade e contexto rastreável |
| M5 | P24–P29 | Uma tarefa de IA avaliada e rascunho assistivo |
| M6 | P13, P30–P32, P36 | Expansão seletiva; depende da maturidade dos componentes |
| M7 | P33–P35 | Avaliação, piloto e autorização para a finalidade pretendida |

M6 e M7 não são uma fila rígida: expansões clínicas de P36 dependem do piloto P35; pesquisa/engenharia podem evoluir antes, em sandbox. A coluna dependencies do CSV é a fonte de precedência por item.

## Catálogo inicial de máscaras a desenvolver

- US: bases de abdome, pelve, tireoide, partes moles e Doppler; obstetrícia em protocolo próprio.
- TC: crânio, tórax, abdome/pelve e protocolos vasculares quando aprovados.
- RM: encéfalo, coluna, musculoesquelético, abdome/pelve e protocolos específicos.
- MG: mamografia com técnica, lateralidade, comparação e classificação conforme protocolo/licença.
- RX: tórax, coluna, pelve e segmentos, respeitando incidência e calibração.

As cinco bases JSON entregues são esqueletos de estrutura. Não contêm textos de normalidade, classificações licenciadas nem protocolos completos validados. Subtemplates, regras e vocabulários serão adicionados em P15.

## Definição de pronto

Cada item inclui requisito rastreável, contrato, proprietário, implementação revisada, testes adequados e evidência de aceitação. Mudança clínica acrescenta finalidade, população/técnica, licença, avaliação, responsável humano, limitações e reversão. Documentação, protótipo, implementado, validado e homologado são estados distintos.

Estimativas de prazo/custo dependem de equipe, infraestrutura, volume e integrações. Planejar por marcos aceitos antes de prometer datas. CI de documentação não comprova segurança, capacidade diagnóstica ou conformidade.
