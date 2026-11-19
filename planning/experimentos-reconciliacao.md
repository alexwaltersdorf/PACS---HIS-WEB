# Proposta de experimentos de reconciliação e contratos

Origem: parecer do Claude Code na mensagem 006 e réplica do Codex na mensagem 007. **Estado: proposta para avaliação do conselho, sem implementação nem ensaio executado.** Relaciona-se a P08 (reconciliação), P17 (interfaces), P18 (terminologia) e P38 (piloto).

## Hipótese a testar primeiro

Um núcleo mínimo de pedido, identificadores qualificados, MWL, estados de leitura e fila humana permite integrar aquisição/viewer/laudo sem criar vínculos incorretos silenciosos. O RIS continua no escopo; o uso do RIS existente do parceiro ou do núcleo próprio depende da descoberta do piloto.

## E1 — Reconciliação sob anomalias

Usar exclusivamente dados sintéticos com gabarito conhecido, incluindo casos válidos e inválidos. Registrar eventos recebidos, decisão, vínculo produzido, rejeição/fila e auditoria. Não basta obter JSON válido.

| Caso | Entrada/sequência | Comportamento esperado a especificar/testar |
|---|---|---|
| E1-01 | Estudo chega antes do pedido | Manter pendência; reconciliar após evidência suficiente sem criar pedido fictício |
| E1-02 | Mesmo accession em organizações/emissores diferentes | Não unir por valor textual isolado; respeitar namespace e autorização |
| E1-03 | PatientID ou accession incompatível | Encaminhar conflito; não escolher paciente por similaridade de nome |
| E1-04 | Mesma instância/evento recebido novamente | Processamento idempotente, sem duplicação lógica |
| E1-05 | Série chega após rascunho/preliminar | Criar nova revisão de entrada e pendência de reavaliação; preservar anterior |
| E1-06 | Merge e posterior desfazimento | Histórico e referências recuperáveis; revisão humana quando necessária |
| E1-07 | Pedido cancelado ou corrigido fora de ordem | Aplicar política explícita de versão/estado; não reabrir silenciosamente |
| E1-08 | Cliente tenta forjar tenant_id | Autorização deriva da identidade autenticada; negar acesso fora do escopo |

Medir vínculos corretos automáticos, encaminhamentos corretos à fila, encaminhamentos desnecessários, vínculos errados e vínculos errados silenciosos. No conjunto de teste, qualquer vínculo errado silencioso reprova o experimento. Zero ocorrências nesse conjunto não demonstra risco nulo em produção. Cobertura, volumes e tolerâncias restantes precisam ser definidos antes do ensaio.

## E2 — Segundo parceiro

Dois adaptadores sintéticos com contratos definidos (exemplo candidato: HL7 v2 e FHIR) alimentam o mesmo domínio. Registrar quais arquivos/contratos precisam mudar e **por quê**. Separar vazamento de dialeto do parceiro, descoberta de requisito comum legítimo, correção de defeito e refatoração. Alterar um arquivo do domínio, sozinho, não prova falha arquitetural.

Avaliar isolamento do adaptador, compreensão das fronteiras, repetição de regras, testes de consumidores e custo de mudança. A extração de microsserviço é uma decisão posterior baseada em necessidade operacional observada, não consequência automática de contagem de arquivos.

## E3 — Consistência semântica

Casos de referência por parceiro com unidade, significado do código, autoridade emissora, status, fuso e cronologia conhecidos. Preservar valor original, transformação e origem; verificar equivalência e também não equivalência. Validar estados desconhecidos, resultados corrigidos, enum novo e mensagens parcialmente compreendidas.

Mudanças opcionais/aditivas podem afetar consumidores; versões não substituem testes de contrato e semântica. Definir comportamento para campos/códigos desconhecidos e coexistência de versões sem aceitar perda silenciosa.

## Descoberta do piloto

Confirmar se a instituição já possui RIS, se pretende substituí-lo, interfaces disponíveis e dor prioritária. Observação de poucos centros é exploração, não prova de mercado. Entrevistas, protótipo e condições de piloto devem gerar evidências; nenhuma receita ou disposição a pagar está demonstrada.

## Portão de decisão

Ainda faltam fixtures, executor, contratos por parceiro, responsáveis, métricas com linha de base e avaliação do Gemini sobre o parecer e a réplica. Este documento não altera sozinho o roadmap nem autoriza produção ou uso de dados reais.
