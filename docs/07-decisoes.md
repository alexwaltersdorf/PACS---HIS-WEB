# Registro de decisões de arquitetura

| ADR | Decisão proposta | Motivo e alternativa |
|---|---|---|
| ADR-001 | RIS/PACS/viewer como núcleo; HIS completo fora do MVP | Fechar jornada diagnóstica primeiro; integrar prontuários existentes |
| ADR-002 | Oito funções e perfis clínicos reutilizáveis | Especialização e revisão independente sem disparar todos os especialistas por caso |
| ADR-003 | Orquestração explícita em workflow | Persistência, limites e gates verificáveis; evitar coordenação por texto sem enforcement |
| ADR-004 | FHIR R4 candidato inicial, contratos por parceiro | Compatibilidade a validar; adaptar R4B/R5/HL7v2 conforme requisitos, não presumir versão universal |
| ADR-005 | Termos e mapeamentos versionados | Preservar origem e vigência; não equiparar códigos clínicos, administrativos e regulatórios |
| ADR-006 | Objetos originais preservados | Contexto interoperável não elimina sinais e documentos-fonte |
| ADR-007 | Template, instância e documento assinado separados | Mudanças não reescrevem laudos históricos; adendo rastreável |
| ADR-008 | Imagem e texto em serviços separados | Persona LLM não valida modelo diagnóstico; inferência por finalidade |
| ADR-009 | Corpus técnico, clínico e dados de pacientes isolados | Autonomia de pesquisa sem exposição de dados sensíveis |
| ADR-010 | Modelos, prompts, templates e corpus com avaliação | Cada mudança pode alterar resultado, mesmo sem modificar código |
| ADR-011 | Segurança por controles testados e risco residual | Não declarar blindagem total, conformidade automática ou certificação inexistente |
| ADR-012 | Perfis portáveis e política declarativa neste commit | Planner sustentável; runtime será implementado em incrementos verificáveis |
| ADR-013 | Conselho de Codex, Claude Code e Gemini | Governança solicitada pelo fundador; mensagens, crítica cruzada e decisões compartilhadas, sem simular participantes |
| ADR-014 | Git como meio assíncrono inicial | Protocolo e utilitário local disponíveis; despacho autônomo contínuo depende de adaptadores, permissões e orçamento |

## Decisões necessárias antes da implementação clínica

Finalidade regulatória, responsáveis nominais, modalidade/tarefa piloto, infraestrutura, dados autorizados, integração prioritária, licenças, orçamento, SLOs, assinatura e critérios quantitativos. Cada decisão deve atualizar o contexto, o requisito e os testes afetados.

## Continuidade da base anterior

Este planner amplia a análise funcional do Eden e a revisão do anexo realizadas neste projeto. Mantém: calibração explícita; separação entre geometria e apresentação; unidades por modalidade; registro validado; preservação de evidências; modelos por tarefa; atualização com avaliação. Não publica credenciais, dados de paciente, caminhos pessoais nem conteúdo de conversas privadas anteriores.
