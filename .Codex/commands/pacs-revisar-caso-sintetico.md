---
description: Exercita contratos clínicos com caso exclusivamente sintético, sem emitir laudo clínico.
argument-hint: caminho do caso sintético
---

# Revisar caso sintético

1. Confirmar que a entrada é sintética e atende CaseContext. Se houver dado real, parar a ingestão neste repositório público e encaminhar ao ambiente clínico autorizado.
2. triagem-contexto organiza lacunas, datas e pergunta. Falha de identidade ou contexto impede análise dependente.
3. Selecionar perfil de radiologia-especializada e, quando necessário, discussao-multidisciplinar; cada um produz artefato independente. Não simular que um modelo analisou pixels quando só recebeu texto.
4. pesquisa-cientifica recebe apenas pergunta genérica e verifica fontes para dúvidas delimitadas.
5. qualidade-clinica revisa saídas, evidências, negações, unidades, lateralidade e discordâncias.
6. Sessão principal apresenta resultado de teste, falhas e pendências. Não emitir assinatura ou diagnóstico para paciente; este comando não habilita uso clínico.

Saída: artefatos sintéticos auditáveis e melhorias de contrato.
