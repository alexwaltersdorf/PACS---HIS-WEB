# Interoperabilidade clínica e administrativa — planner PACS/RIS/HIS

**Revisão:** 18/11/2026. **Estado:** especificação pesquisada; interfaces, conformidade e certificações ainda não implementadas ou testadas. **OBSERVADO** identifica documentação consultada; **PROPOSTA** identifica decisão arquitetural. Não há evidência de integrações internas do Eden ou do nReport nesta seção.

## 1. Arquitetura proposta

Criar um **núcleo de interoperabilidade** entre HIS/RIS, PACS, equipamentos, laboratórios, operadoras e serviços de IA. Seus componentes são: adaptadores por parceiro; validação estrutural; resolução de identidade; serviço terminológico; armazenamento protegido do original; barramento de eventos; normalização clínica; auditoria; e APIs de consulta autorizada. Os agentes recebem um contexto clínico versionado e rastreável, não acesso irrestrito aos sistemas de origem.

Usar FHIR como contrato de intercâmbio clínico, sem transformar cada evento interno em recurso FHIR à força. Negociar versão, perfis, operações e cardinalidades por integração. R4 pode ser candidato inicial pela compatibilidade a avaliar, mas não é uma versão obrigatória definida aqui; a documentação R5 consultada não significa que os parceiros a suportem. Produzir `CapabilityStatement`, guia de implementação do projeto e exemplos sintéticos antes de declarar conformidade.

O fluxo RIS é pedido → agendamento → preparação → aquisição → conferência → interpretação → assinatura → distribuição. A worklist do radiologista é diferente da **DICOM Modality Worklist**, consumida pelo equipamento. Associar pedido, procedimento agendado e estudo, preservando números de ordem do solicitante/executor, accession number, domínio emissor e `StudyInstanceUID` como identificadores distintos.

## 2. Matriz de padrões e responsabilidades

| Padrão ou catálogo | OBSERVADO na fonte | Aplicação proposta e limite |
|---|---|---|
| HL7 v2; OBR/OBX | OBR descreve solicitação/cabeçalho do conjunto de observações; OBX transporta observações. **OBR não é terminologia clínica.** [HL7 v2.5.1](https://hl7.eu/HL7v2x/v251/std251/ch07.html) | Adaptadores ADT, ordens e resultados conforme o contrato do parceiro. Não converter somente pelo nome do segmento; preservar versão, repetições e identificadores. Se “OBR” no escopo significar outra coisa, esclarecer antes de implementar. |
| FHIR | `ServiceRequest` representa solicitação; `DiagnosticReport` agrupa resultados e interpretação; `Observation` representa medidas/afirmações. [Pedido](https://hl7.org/fhir/servicerequest.html), [relatório](https://hl7.org/fhir/diagnosticreport.html), [observação](https://hl7.org/fhir/observation.html) | Relacionar Patient, Encounter, ServiceRequest, Appointment/Task, ImagingStudy, Specimen, Observation e DiagnosticReport conforme o caso; anexos com DocumentReference. |
| IHE SWF.b / PIR | SWF.b integra pedido, agenda, aquisição, armazenamento e visualização; incorpora reconciliação de informações de pacientes. [SWF.b](https://wiki.ihe.net/index.php/Scheduled_Workflow.b) | Definir atores e transações suportados pelo RIS/PACS. Incluir urgência sem cadastro definitivo, correção e reconciliação; não alegar “IHE compliant” genericamente. |
| IHE ATNA | Perfil cobre autenticação, auditoria e proteção de comunicação. [ATNA](https://profiles.ihe.net/ITI/TF/Volume1/ch-9.html) | Auditar acesso, exportação, reconciliação, alteração e assinatura; combinar com política de autorização. Implementar um perfil não comprova segurança integral. |
| IHE XDS-I.b | Perfil de compartilhamento de imagens entre organizações integra o framework radiológico. [IHE RAD](https://profiles.ihe.net/RAD/) | Avaliar somente quando houver comunidade de compartilhamento e atores definidos. DICOMweb de um PACS isolado não equivale a XDS-I.b. |
| CID-10 / CID-11 | MS publicou cronograma de implementação da CID-11 previsto para janeiro de 2027. [MS](https://www.gov.br/saude/pt-br/assuntos/noticias/2025/janeiro/11a-revisao-da-classificacao-internacional-de-doencas-sera-implementada-no-brasil-ate-2027/) | Conservar sistema, edição e código originais; preparar coexistência. Cronograma publicado não autoriza afirmar adoção universal em todos os parceiros. |
| SNOMED CT | Uso e distribuição dependem das condições de licença/território. [SNOMED International](https://www.snomed.org/get-snomed) | Codificar conceitos clínicos quando houver licença e edição adequadas; não publicar o conteúdo completo da terminologia no GitHub. |
| LOINC | Identifica exames e observações laboratoriais e clínicas. [LOINC](https://loinc.org/start) | Mapear teste/medida por material, método e contexto; não escolher código apenas por similaridade do nome. |
| UCUM | Padroniza representação eletrônica de unidades. [UCUM](https://ucum.org/ucum) | Preservar unidade recebida, unidade normalizada e transformação; só converter grandezas compatíveis. |
| TISS / TUSS | TISS organiza intercâmbio na saúde suplementar; TUSS integra sua representação de conceitos. [ANS](https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss) | Módulo administrativo separado para autorização, guias, lotes, retorno e glosas. Fixar componentes, schemas e vigências por operadora. FHIR não substitui automaticamente essas obrigações. |
| SIGTAP | Gerencia procedimentos, medicamentos e OPM do SUS. [MS](https://www.gov.br/saude/pt-br/acesso-a-informacao/faq/tematicos-e-outros/onde-encontrar-todos-os-procedimentos) | Importar competências e relacionamentos; preservar histórico. Não presumir equivalência exata com TUSS. |
| CATMAT | Catálogo de descrição/codificação de materiais para compras. [MS](https://www.gov.br/saude/pt-br/composicao/sectics/daf/cbaf/repasse/faq/em-relacao-ao-processo-de) | Relacionar materiais, insumos e suprimentos; não usar como código de diagnóstico ou pedido de exame. |
| ANVISA | Consulta oficial informa situação de produtos sujeitos à vigilância sanitária. [Anvisa](https://www.gov.br/anvisa/pt-br/sistemas/sistema-de-consultas) | Registrar identificador regulatório e situação quando aplicável a dispositivo/insumo; registro não é terminologia nem comprova segurança de toda a plataforma. |
| SBIS / CFM / NGS2 | A página vigente da SBIS disponibiliza listas por categoria, incluindo RIS, e requisitos de documentos assinados associados ao NGS2. [SBIS](https://sbis.org.br/certificacoes/certificacao-software/manuais-e-listas-de-requisitos/) | Criar matriz de requisitos/evidências da categoria aplicável e avaliar regras profissionais pertinentes. “Preparado para avaliação” difere de certificado; NGS2 não é protocolo de interoperabilidade. |

## 3. Terminologias e identidade

**PROPOSTA:** serviço terminológico com `CodeSystem`, `ValueSet` e `ConceptMap`, versões imutáveis, vigência e aprovação humana dos mapeamentos. Salvar código local, sistema/versão, significado e responsável. Mapeamento deve explicitar equivalência, granularidade e uso; não assumir reversibilidade nem converter doença em código de faturamento automaticamente. A especificação de [ConceptMap](https://hl7.org/fhir/conceptmap.html) distingue relações e contexto de utilização.

Adotar índice de pacientes com identificadores qualificados por emissor e organização. Nome/data de nascimento ajudam na revisão, mas não autorizam fusão automática. Divergências, pacientes provisórios e possíveis duplicidades entram em fila; merge e eventual desfazimento precisam de auditoria e propagação controlada. O recurso [Patient](https://hl7.org/fhir/patient.html) admite registros mantidos por organizações distintas; isso exige política de reconciliação, não um identificador global inventado.

## 4. Integração de exames além da radiologia

| Domínio | Dados a entregar ao contexto clínico | Cuidados do adaptador |
|---|---|---|
| Laboratório | Resultado, unidade, referência local, espécime, coleta, liberação, método, status e laudo original | Diferenciar preliminar, final e corrigido; não tratar resultado de espécime distinto como série comparável. |
| ECG / Holter | Laudo, medidas e sinal com derivações, taxa de amostragem, ganho, unidade e tempo | Manter traçado original e sincronização; PDF isolado não substitui waveform quantitativa. |
| Ecocardiografia | Imagens/cine, medidas, método, fase cardíaca e interpretação | Preservar DICOM/SR quando fornecidos; relacionar medidas à aquisição e não apenas ao paciente. |
| EEG | Laudo e sinal, montagem, canais, referência, filtros, eventos e horários | Preservar formato nativo e metadados; conversão só após validação de fidelidade e suporte do dispositivo. |
| Espirometria | Valores, curvas fluxo-volume/volume-tempo, qualidade, condição pré/pós-broncodilatador e equação de referência | Não comparar percentuais previstos sem conhecer referência e contexto; conservar curvas originais. |
| Outros exames | Pedido, execução, documento/sinal/imagens e observações específicas | Conector por contrato real; evitar promessa de suporte universal sem amostras e conformidade. |

O DICOM inclui [Waveform IODs](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.34.html), mas seu suporte depende de equipamento, objeto e consumidor. FHIR organiza observações e relatórios; não elimina a necessidade de armazenar sinais originais grandes em repositório apropriado. PDF/OCR é fallback identificado, com conferência dos dados extraídos; nunca fingir precisão de medição equivalente à fonte digital.

## 5. Contexto para os agentes e critérios de aceitação

O pacote entregue à IA deve conter problema clínico, pedido, hipóteses do solicitante, exames prévios pertinentes, medicamentos/alergias quando relevantes, resultados e cronologia. Cada item carrega origem, autor, status, instante do evento, instante de emissão/ingestão e versão. Diferenciar “não informado”, “negado”, “não avaliado” e “não disponível”. O recurso [Provenance](https://hl7.org/fhir/provenance.html) sustenta a origem e transformação; auditoria registra acesso/ações, com finalidade diferente.

Resultados posteriores ao exame devem estar explicitamente identificados. Para avaliações retrospectivas, aplicar corte temporal para evitar vazamento de informação futura. Documentos conflitantes permanecem visíveis com procedência; uma síntese de IA não apaga a fonte nem resolve silenciosamente discrepâncias.

Antes de ativar cada parceiro: testar identidade equivocada, pedido cancelado, paciente provisório, mensagens repetidas/fora de ordem, resultado corrigido, unidades incompatíveis, indisponibilidade e retomada. Implementar ACK/retry, idempotência e fila de erros no contrato aplicável. Validar recursos, terminologias e relações; testar round-trip com consumidor independente. Publicar matriz de capacidades com estados “planejado”, “implementado”, “testado” e “homologado com parceiro”, sem equipará-los a certificação.

**Decisões pendentes:** parceiros e interfaces disponíveis; versão/perfis FHIR; atores IHE; escopo SUS/suplementar; licenças; categoria de certificação; formatos nativos de sinais; regras de identidade e retenção. Nenhuma dessas lacunas impede protótipos sintéticos; todas limitam alegações de integração concluída.

## Fontes primárias de referência

Consultadas em 18/11/2026, com links diretos nas seções correspondentes: HL7 v2.5.1 capítulo 7; FHIR ServiceRequest, DiagnosticReport, Observation, Patient, ConceptMap e Provenance; IHE SWF.b, RAD Technical Framework e ATNA; DICOM PS3.3 Waveform IODs; SNOMED International; LOINC; UCUM; ANS/TISS; Ministério da Saúde/CID-11, SIGTAP e CATMAT; Anvisa/consultas; SBIS/manuais e listas de requisitos. Revalidar edição, vigência, licença e contrato antes da implementação de cada interface.
