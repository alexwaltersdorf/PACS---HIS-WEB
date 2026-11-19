# Segurança, privacidade e governança da plataforma

**Consulta:** 18/11/2026. **Estado:** arquitetura proposta; nenhum controle foi implantado, nenhum pentest foi executado e não há certificação declarada. **Objetivo:** reduzir riscos com evidências verificáveis, continuidade assistencial e responsabilidade definida. “Blindado contra ataques” não é uma garantia tecnicamente demonstrável.

## 1. Referenciais e responsabilidades

**OBSERVADO:** a OWASP disponibiliza ASVS 5.0.0, publicado em 30/05/2025, como catálogo de requisitos verificáveis de aplicações. A OWASP API Security Top 10 2023 destaca autorização por objeto, autenticação, consumo de recursos e SSRF. **PROPOSTA:** adotar ASVS nível 2 como baseline de planejamento, acrescentando requisitos de maior rigor conforme análise de risco; manter cada controle ligado a teste e evidência, sem anunciar certificação OWASP. [ASVS](https://asvs.owasp.org/), [API Security](https://owasp.org/www-project-api-security/).

A responsabilidade humana deve distinguir: proprietário do produto; responsável clínico; encarregado de proteção de dados; responsável de segurança; operação/SRE; qualidade e regulatório. O agente de segurança identifica problemas, propõe mudanças e organiza evidências; não assume essas responsabilidades institucionais nem aprova a própria exceção.

**OBSERVADO:** a SBIS publica listas de requisitos S-RES, incluindo RIS e exportação de documentos assinados relacionada ao NGS2. **PROPOSTA:** selecionar categoria, modalidade, estágio e versão aplicáveis; construir matriz requisito → implementação → ensaio → evidência. Assinatura digital isolada não demonstra atendimento ao conjunto. A avaliação sanitária por finalidade pretendida é distinta da certificação S-RES: análise diagnóstica e laudos com IA precisam de enquadramento específico, sem presumir dispensa por serem locais ou open source. [SBIS](https://sbis.org.br/certificacoes/certificacao-software/manuais-e-listas-de-requisitos/), [Anvisa — RDC 657/2022](https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2022/software-como-dispositivo-medico-perguntas-e-respostas/perguntas-respostas-rdc-657-de-2022-v1-01-09-2022.pdf).

## 2. Fronteiras de confiança

Separar rede de modalidades/gateway DICOM, aplicação web/API, PACS/armazenamento, processamento de imagens, agentes clínicos, pesquisa pública e administração. Equipamento conhecido não torna um arquivo recebido confiável. Parsers e codecs processam conteúdo potencialmente malformado em workers isolados, com limites de tamanho, memória, tempo, frames e descompressão.

O frontend não acessa diretamente banco, credenciais do PACS ou API administrativa. DICOM DIMSE legado permanece em segmento restrito, com gateways e transporte protegido compatível; não expor portas C-STORE à internet. DICOMweb usa HTTPS, autenticação e autorização em cada operação. TLS deve seguir perfil vigente compatível, e não copiar exemplos históricos: o próprio DICOM marca o antigo perfil Basic TLS como retirado. [DICOM PS3.15, edição observada 2026d](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_B.html).

## 3. Matriz de ameaças e verificações propostas

| Superfície / ameaça | Controle proposto | Evidência exigida |
|---|---|---|
| DICOM malformado, zip/decompression bomb | Quarentena; parser isolado; quotas; codecs fixados; sem execução de conteúdo | Corpus adversarial autorizado, rejeição previsível e ausência de acesso lateral |
| PACS acessível indevidamente | Segmentação; gateway autenticado; autorização por estudo/série/frame | Testes negativos QIDO/WADO/STOW e de APIs administrativas |
| Vazamento entre organizações | Tenant derivado da identidade autenticada; política no serviço e banco; isolamento de objetos/cache | Matriz cruzada de usuários, tenants, exports, jobs e URLs assinadas |
| Troca de paciente/contexto | Reconciliação de identidade; referências consistentes; conflito bloqueia publicação | Caso sintético com identificadores conflitantes não gera laudo vinculado incorretamente |
| Furto de sessão ou privilégio | SSO/OIDC; MFA; sessões revogáveis; RBAC + atributos de vínculo/finalidade | Revogação efetiva, sessão expirada, usuário sem vínculo e escalada negados |
| SSRF por URLs de importação | Egress restrito; destinos permitidos; bloqueio de redes internas/metadados; checagem de redirects | Destinos proibidos não alcançáveis pelo worker |
| Injeção em artigo, laudo ou RAG | Conteúdo tratado como dado; ferramentas estreitas; ACL antes da recuperação | Documentos adversariais não obtêm segredos nem promovem ações |
| Pacote, peso ou plugin comprometido | Revisão de origem/licença; digest; SBOM; scanner; execução isolada | Build reproduzível e artefato desconhecido bloqueado |
| Ransomware ou exclusão em massa | Backup segregado, imutável/offline conforme arquitetura; credenciais separadas | Restauração completa e consistente em ambiente limpo |
| Exfiltração em logs ou LLM externo | Redação/allowlist de campos; retenção; destinos aprovados | Amostragem automatizada sem tokens, texto clínico ou imagens nos logs técnicos |
| Exaustão de GPU, tokens ou API | Orçamentos, rate limits, fila, timeout, cancelamento e circuit breaker | Saturação não derruba fluxos essenciais; custo interrompido no limite |
| Alteração de resultado assinado | Versão imutável; adendo vinculado; integridade e trilha protegida | Edição destrutiva negada; assinatura e proveniência verificáveis |

## 4. Identidade, criptografia e auditoria

Usar identidades individuais, contas de serviço distintas por componente e credenciais de curta duração quando viável. RBAC define função; ABAC restringe organização, relação assistencial, finalidade, contexto e recurso. O identificador de estudo nunca é autorização. Download, exportação, pesquisa vetorial e consultas administrativas obedecem à mesma política.

O acesso emergencial (*break glass*) é explícito, motivado, temporário, limitado e revisado; não é uma conta permanente sem restrições. Segredos ficam em cofre/KMS, fora do Git, prompts, notebooks e imagens de contêiner. Criptografia em trânsito e em repouso inclui backups; acesso às chaves é segregado e sua recuperação é testada.

Separar logs técnicos minimizados da trilha assistencial restrita. Esta última pode exigir identificadores protegidos para rastreabilidade, com acesso, retenção e finalidade próprios. Registrar identidade, recurso, ação, decisão, horário sincronizado e correlação; não guardar raciocínio interno de LLM como substituto de evidência clínica.

## 5. LGPD e circulação dos dados

**OBSERVADO:** informações de saúde vinculadas à pessoa são dados pessoais sensíveis; as hipóteses legais correspondentes estão no art. 11 da LGPD. **PROPOSTA:** documentar controlador/operador, finalidade e base aplicável a assistência, faturamento, pesquisa e treinamento separadamente. Não presumir consentimento como única base, nem transportar automaticamente a finalidade assistencial para treinamento. Inventariar tratamentos, retenções, subprocessadores, transferências e atendimento aos titulares. Elaborar RIPD conforme avaliação de risco e exigências aplicáveis; pseudonimização não equivale a anonimização. [ANPD — perguntas frequentes](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes), [ANPD — dados sensíveis](https://www.gov.br/anpd/pt-br/canais_atendimento/cidadao-titular-de-dados/denuncia-peticao-de-titular-referente-lgpd).

Pesquisa pública recebe perguntas clínicas generalizadas sem identidade ou arquivos reais. APIs externas com dados clínicos dependem de destino autorizado, contrato, finalidade e configuração de retenção/treinamento. Transferências internacionais devem ser avaliadas pelo mecanismo aplicável, sem assumir que criptografia ou escolha da região bastem. [ANPD — Resolução 19/2024](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024).

## 6. Autonomia e promoção de mudanças

| Classe | Ação prevista | Limite |
|---|---|---|
| A0 — leitura | Pesquisa pública, inventário e alertas | Sem PACS, segredos ou modificações em produção |
| A1 — proposta | Candidato de código, corpus, template, ferramenta ou modelo | Branch/área isolada, fontes e justificativa |
| A2 — execução experimental | Testes sintéticos ou dados autorizados; comparação de versões | Quotas, sandbox e ferramentas explicitamente permitidas |
| A3 — impacto operacional/clínico | Implantação, novo processamento clínico ou mudança de template/prompt | Validação, aprovação nominal, rollback e auditoria |
| A4 — responsabilidade clínica | Assinatura, liberação de laudo e conduta | Profissional habilitado no desenho inicial |

A autorização precisa existir fora do prompt, no gateway de ferramentas. Não dar shell irrestrito, acesso ao cofre ou credencial universal aos agentes. Mensagens entre agentes também são entradas não confiáveis. A OWASP identifica permissões, funcionalidades e autonomia excessivas como fatores de risco. [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).

Promover artefatos imutáveis com digest, licença, configuração, testes, avaliação clínica pertinente e plano de reversão. Mudanças de pesos, templates, corpus e prompts podem alterar comportamento mesmo sem mudança do código. Atualização urgente de segurança segue procedimento acelerado documentado, não supressão de todos os testes. O agente que cria não aprova sozinho sua mudança.

## 7. Continuidade, incidentes e gates de entrega

Definir RPO/RTO com a operação e simular indisponibilidade, restauração e reconciliação de pedidos, imagens, resultados e laudos. Preservar cópia recuperável mesmo se a identidade administrativa principal for comprometida. Testes de restauração devem medir recuperação e consistência, não apenas sucesso do job de backup. [CISA — StopRansomware Guide, arquivo de março/2025](https://www.cisa.gov/sites/default/files/2025-03/StopRansomware-Guide%20508.pdf).

O plano de incidentes inclui detecção, contenção, preservação de evidências, avaliação assistencial, recuperação e comunicação. A orientação da ANPD consultada, atualizada em 26/08/2026, informa três dias úteis para comunicação pelo controlador quando aplicável, ressalvada legislação específica; nem todo incidente exige comunicação. Operador informa o controlador sem demora injustificada. O responsável deve verificar enquadramento e exceções no caso concreto; o software acompanha prazos, não decide sozinho a obrigação. [ANPD — comunicação de incidentes](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis).

Gates propostos: **G1** threat model e inventário; **G2** autenticação/isolamento e testes negativos; **G3** pipeline seguro e restauração comprovada; **G4** avaliação independente, privacidade e enquadramento regulatório; **G5** validação clínica e autorização de operação. Permanecem desconhecidos infraestrutura, volume, contratos, responsáveis nominais e finalidade regulatória final. Esta etapa entrega o plano; não declara esses gates cumpridos.
