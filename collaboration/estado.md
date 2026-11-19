# Estado da colaboração

Registro da primeira rodada em 18/11/2026. Este arquivo descreve o que ocorreu; não representa disponibilidade permanente de provedores.

| Participante | Evidência desta rodada | Estado |
|---|---|---|
| Codex | Elaborou proposta, protocolo, réplica e síntese | Participou |
| Claude Code | CLI consultado, mas sem revisão válida retornada | Parecer pendente na 1ª rodada; respondido depois na mensagem 006 |
| Gemini | Resposta obtida na interface web e retransmitida com autoria/origem declaradas | Participou via web; CLI não conectado |

Não há consenso das três ferramentas nem despacho automático contínuo. Não foi gerada resposta fictícia do Claude Code.

## Mensagens

1. [Proposta do Codex](messages/estrategia-inicial-001.json).
2. [Estado da tentativa de consulta](messages/estrategia-inicial-002.json).
3. [Crítica do Gemini](messages/estrategia-inicial-003.json).
4. [Réplica do Codex](messages/estrategia-inicial-004.json).
5. [Síntese provisória](messages/estrategia-inicial-005.json).
6. [Parecer do Claude Code](messages/estrategia-inicial-006.json) — sessão direta do Claude Code em 19/11/2026, base `cd29471`.

## Atualização de 19/11/2026

O Claude Code respondeu às mensagens 001, 003 e 004 (mensagem 006). O registro acima da primeira rodada permanece como histórico: naquela rodada o parecer estava pendente.

Pontos principais do parecer, para avaliação dos demais: RIS mínimo mantido, mas definido como pedido, accession, MWL, estados de interpretação e fila de reconciliação; contrato canônico único, versionado e agnóstico de parceiro, com diferenças em perfis de adaptador; riscos previstos de sobreajuste ao primeiro parceiro e deriva semântica; experimentos E1 (reconciliação com anomalias sintéticas), E2 (troca de parceiro) e E3 (testes semânticos); decisão entre RIS mínimo próprio e adaptador condicionada a saber se o piloto já tem RIS.

Ainda não há consenso das três ferramentas. Pendente: réplica do Codex e avaliação do Gemini sobre as mensagens 004 e 006, seguidas de síntese revisada e ADR se houver mudança material.

As metas numéricas sugeridas pelo Gemini foram preservadas como proposta do participante e questionadas na réplica. Não se tornaram benchmarks comprovados, SLAs ou metas comerciais aprovadas. A alternativa de piloto não remove o RIS do escopo solicitado.

## Próxima participação

Claude Code deve ler as mensagens 001, 003 e 004 e responder ao problema de contratos compartilhados e prioridade de implementação. Quando uma revisão válida estiver disponível, publicá-la em novo arquivo e atualizar esta síntese sem apagar o histórico. Gemini deve avaliar a réplica do Codex na próxima execução.

A execução autônoma contínua ainda depende de adaptadores, autorização das contas, orçamento e controles previstos no backlog. Credenciais e detalhes privados das contas não fazem parte deste registro público.
