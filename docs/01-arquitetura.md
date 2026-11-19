# Arquitetura funcional e técnica

**Estado:** proposta, 18/11/2026. Arquitetura inicial modular, com workers isolados para processamento; extrair microsserviços quando carga, operação ou fronteira de dados justificarem.

## Componentes e propriedade dos dados

| Componente | Responsabilidade | Dados que governa |
|---|---|---|
| Portal RIS | Pedido, agenda, preparo, presença, prioridade e atribuição | Pedido e episódio de execução |
| Viewer OHIF/Cornerstone3D | Visualização e interação, medidas e referência ao laudo | Estado de apresentação e anotações versionadas |
| PACS Orthanc/DICOMweb | Ingestão e guarda dos objetos médicos | Objetos DICOM, UIDs e referências de integridade |
| Serviço de laudos | Templates, rascunhos, revisão, assinatura e adendos | Versão estruturada e representação assinada |
| Gateway de integração | HL7v2, FHIR, DICOM e adaptadores | Mensagens, acknowledgments, mapeamentos e erros |
| Serviço terminológico | CodeSystem/ValueSet/ConceptMap e validação | Código, sistema, versão, vigência e mapeamento |
| Serviço de contexto | Linha temporal e evidências externas do caso | Snapshot autorizado com proveniência |
| Runtime de agentes | Roteamento de perfis, ferramentas e checkpoints | Execuções, decisões intermediárias e orçamento |
| Workers de imagem | Pré-processamento, inferência e artefatos | Jobs, versão do modelo, SEG/SR e medidas |
| Registro de modelos/evidências | Avaliações e versões | Candidatos, aprovações e artefatos imutáveis |
| Identidade e auditoria | Autenticação, autorização e registros | Usuários, funções, escopo e eventos auditáveis |

OHIF oferece framework web e extensões, e utiliza Cornerstone para renderização; sua documentação consultada também apresenta linha beta. Fixar uma combinação estável compatível, sem atualizar core independentemente do viewer. [OHIF oficial](https://docs.ohif.org/). Orthanc oferece componentes de arquivo e integração, mas não entrega sozinho todo o RIS/HIS, segurança e operação descritos aqui. [Orthanc Book](https://orthanc.uclouvain.be/book/).

## Stack inicial e evolução

- Interface: TypeScript, React/OHIF e extensões do Cornerstone; editor estruturado integrado com o estudo atual.
- Aplicação: backend modular com API tipada; Python para processamento médico; PostgreSQL para domínio, jobs e metadados. Separar contas, schemas e permissões por serviço.
- Arquivo: Orthanc e plugin DICOMweb; armazenamento dimensionado por volume/retencão, com cópias protegidas e testes de restauração.
- Processamento: MONAI/PyTorch e ferramentas DICOM; modelo/runtime escolhidos por tarefa. ONNX Runtime somente após equivalência; Triton quando concorrência e GPU justificarem.
- Agentes: LangGraph como candidato para o grafo de raciocínio controlado; não substitui o motor de regras nem controles de acesso. [Documentação](https://docs.langchain.com/oss/python/langgraph/overview).
- Execução longa: Temporal quando retomadas e múltiplos serviços exigirem workflow durável; proprietário do estado operacional, sem duplicar o grafo de raciocínio. [Documentação](https://docs.temporal.io/).
- Conhecimento: PostgreSQL/pgvector com busca textual, filtros de autorização e versões; corpus técnico separado do clínico e dos dados de pacientes.
- Operação: CI, artefatos imutáveis, registro de modelos, telemetria redigida, infraestrutura declarativa e reversão.

Escolher servidor FHIR e motor de integração após validar perfis e parceiros; não adicionar um produto apenas por popularidade. Base candidata FHIR R4 (4.0.1) para os primeiros contratos, com adaptação por parceiro e ADR. R4 não é apresentado como última versão nem obrigação universal. [FHIR R4](https://hl7.org/fhir/R4/).

## Fluxo RIS e duas listas de trabalho

**Worklist de interpretação do RIS** é uma fila de leitura/atribuição e estados de laudo. **DICOM Modality Worklist** fornece dados de paciente/pedido/agendamento ao equipamento. São superfícies diferentes e precisam manter vínculos, sem confundir status de aquisição com status de interpretação.

Estados de pedido propostos: `requested → scheduled → arrived → acquiring → acquired → quality_checked → ready_for_reading → interpreting → preliminary → final → delivered`. Cancelamento, suspensão, repetição, correção e adendo são transições explícitas e auditáveis. O laudo tem máquina de estados própria; `final` exige assinatura autorizada.

Unicidade por organização e origem para identificadores externos. Não usar nome do paciente como chave. Manter patient identifiers com autoridade emissora, accession com namespace e referências aos estudos. Merge/unmerge e reconciliar exame órfão precisam de revisão e trilha; não deixar uma LLM decidir o vínculo de identidade.

## Contratos e eventos

Objetos de domínio: organização, unidade, paciente, encontro, pedido, procedimento solicitado, agendamento, tarefa de aquisição, estudo/série/instância, laudo/versão, achado, evidência, execução de IA, template/versão, aprovação e evento de auditoria.

Eventos internos versionados: `order.created`, `appointment.changed`, `acquisition.completed`, `study.reconciled`, `study.stable`, `context.snapshot.created`, `analysis.requested`, `analysis.completed`, `report.draft.created`, `report.signed`, `report.amended`, `critical_result.acknowledged`.

Envelope mínimo: `event_id`, `event_type`, `schema_version`, `tenant_id`, `occurred_at`, `correlation_id`, `aggregate_id`, `aggregate_version`, `producer`, `payload_reference`. Não transportar objetos clínicos inteiros em filas sem necessidade. Usar outbox transacional, deduplicação e transições compare-and-set quando aplicável. Retries não garantem efeito externo exatamente uma vez.

Quando imagens chegarem aos poucos, `study.stable` segue regra configurada de completude/estabilidade, não apenas um timeout arbitrário. Chegada tardia cria nova revisão da entrada; resultados anteriores preservam input fingerprint.

## Contexto para IA

Cada `CaseContext` é um snapshot versionado do que era conhecido naquele momento. Inclui pergunta clínica, técnica, sintomas, antecedentes autorizados, terapias relevantes, comparações, resultados laboratoriais e outros exames com datas, unidades, referências e origem. Distinguir `unknown`, `not_asked`, `unavailable`, `conflicting` e `known`.

Resultados de ECG, EEG, espirometria e laboratório não viram imagem radiológica por conversão de formato. Armazenar a representação original, o laudo correspondente e observações normalizadas; registrar se a IA consumiu sinal bruto, texto ou ambos. Um PDF não substitui waveform quantitativo quando este for necessário.

Os agentes recebem o mínimo necessário para a tarefa. Pesquisa pública recebe uma pergunta desidentificada, sem identificadores ou narrativa clínica que permita reidentificação. [Detalhamento de interoperabilidade](03-interoperabilidade.md).

## Invariantes geométricas herdadas da revisão do anexo

Medidas têm origem de calibração, unidade, frame e versão do algoritmo; pan/zoom/rotação da câmera não mudam o valor. Registro de imagens é transformação física explícita, diferente de zoom visual. Spacing de detector e de paciente não são intercambiáveis. HU não é unidade universal. Não fundir RX 2D e MR 3D como simples sobreposição. Separar Tönnis, Sharp e índices pediátricos; definir convenção dos ângulos e validar com especialista.

Não presumir arquitetura interna do Eden ou do nReport. A referência funcional inspira uma implementação independente; ferramentas observadas não demonstram precisão clínica ou direito de copiar código/templates.

## Implantação e requisitos mensuráveis

Ambientes: desenvolvimento sintético → integração → validação restrita → homologação → produção. Dados e identidades segregados; segredos fora do código; egress controlado; gateways DICOM em rede restrita. Produção começa apenas após decisões sobre finalidade, infraestrutura e validação.

Antes do dimensionamento, medir tamanho e número de estudos, concorrência, disponibilidade, latência por etapa, RPO/RTO, banda e GPU. Metas numéricas permanecem abertas; não declarar SLA sem infraestrutura e teste. Falhas devem resultar em mensagens claras e continuidade do fluxo humano, nunca em laudo silenciosamente incompleto.
