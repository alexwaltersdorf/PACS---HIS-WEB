# Núcleo clínico assistivo, pesquisa e laudos estruturados

**Revisão: 18/11/2026. Estado: arquitetura proposta, sem agentes clínicos implantados ou validação diagnóstica executada.** Este desenho amplia a base DICOM existente e preserva suas correções de geometria, calibração, unidades e revisão humana.

## Evidência e limite da referência nReport

**OBSERVADO:** o endereço público [nReport](https://app-nreport.ionic.health/) respondeu à consulta, mas não forneceu conteúdo textual legível. Não foram acessadas áreas autenticadas, máscaras, integrações ou regras internas. Portanto, “como nReport” é uma intenção funcional do usuário, não evidência de recursos inspecionados. A implementação proposta será independente, sem copiar textos ou modelos proprietários.

Como referências abertas, a RSNA descreve o RadReport como biblioteca de modelos de laudos. A página indexada do portal informa interrupção de revisão/publicação de novos modelos desde dezembro de 2022: o acervo não deve ser tratado como diretriz continuamente atualizada. A adoção de qualquer modelo exige revisão local, licença e adequação ao protocolo. [RSNA RadReport](https://www.rsna.org/practice-tools/data-tools-and-standards/radreport-reporting-templates), [portal RadReport](https://www.radreport.org/).

**OBSERVADO:** o IHE Radiology Technical Framework, revisão 23.0, de 08/08/2025, inclui a estrutura MRRT no volume 3, seção 6.6. Ela descreve campos e conteúdo codificado para modelos de laudos; não substitui o modelo de dados de toda a aplicação nem define sozinho a integração de dados externos. Não adotar o suplemento de 2018 como se fosse a referência atual. [IHE RAD TF-3](https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_TF_Rev23-0_Vol3_FT_2025-08-08.pdf).

## Organização dos agentes e responsabilidade

**PROPOSTA:** quatro funções assistivas clínicas, com revisão independente de qualidade. São componentes de software, não médicos licenciados. Modelos especializados em imagem ficam separados do LLM que organiza o raciocínio e o texto. Uma persona “neurorradiologista” não confere capacidade diagnóstica ao modelo.

| Função | Entrada delimitada | Entrega e consumidor |
|---|---|---|
| Contexto e triagem | Pedido, indicação, histórico autorizado, exames prévios e questionário | Pacote clínico com fontes, datas, lacunas e sugestões de prioridade para revisão |
| Radiologia por subespecialidade | Imagens elegíveis, contexto e resultados de modelos aprovados | Achados estruturados, evidências, limites e rascunho para radiologista humano |
| Consultoria multidisciplinar | Pergunta clínica específica e extrato mínimo do caso | Parecer assistivo com hipóteses, evidências e discordâncias para discussão |
| Pesquisa científica | Pergunta desidentificada e critérios de busca | Síntese crítica rastreável para radiologia e equipe assistencial |
| Revisão de qualidade clínica | Achados, texto, referências e versões | Inconsistências e pendências para correção; não assinatura automática |

O orquestrador seleciona funções necessárias, estabelece prazo e consolida arquivos/resultados. Não convocar todas as especialidades para todos os exames. A consulta pode ocorrer em paralelo quando as perguntas forem independentes; a versão final depende de resolução explícita de divergências pelo profissional responsável.

### Perfis de radiologia

| Perfil | Recorte de avaliação e dados relevantes |
|---|---|
| Neurorradiologia | Encéfalo, coluna e estruturas relacionadas; sequência, indicação e comparação temporal |
| Musculoesquelético | Ossos, articulações e partes moles; trauma, lateralidade, cirurgia e material implantado |
| Abdome e pelve | Órgãos abdominais/pélvicos; fase de contraste, cirurgia e exames laboratoriais pertinentes |
| Tórax | Pulmões, pleura e mediastino; técnica, história respiratória e comparações |
| Mama | MG e US de mama, com RM quando validada; lateralidade, antecedentes e comparação |
| Cardiovascular | Exames de imagem próprios; sincronização, fase, medidas e correlação cardiológica |
| Cabeça e pescoço | Região anatômica e indicação; correlação otorrinolaringológica quando autorizada |
| Pediatria | Protocolos, faixa etária e população próprias; não extrapolar validação adulta |
| Oncologia | Lesões rastreadas no tempo, tratamento e critérios previamente aprovados |
| Emergência/intervencionista | Apoio a contextos delimitados; alertas com confirmação humana e fluxo institucional |

Esses recortes são escopos de desenvolvimento, não lista de capacidades já disponíveis. Cada combinação de modalidade, tarefa, população e modelo deve ter elegibilidade, métricas e responsável clínico. A evidência de um modelo para CT não autoriza uso em MR, US ou MG.

A consultoria multidisciplinar oferece perfis de cirurgia, ortopedia, neurologia, pneumologia, oncologia, otorrinolaringologia e vascular. Cada parecer registra pergunta, dados usados, hipótese, alternativas e o que não foi avaliado. Não emitir decisões terapêuticas nem prescrição automaticamente. Divergências não são resolvidas por votação de LLMs.

## Contexto e triagem antes do laudo

O pacote deve conter motivo do exame, pergunta clínica, cronologia, intervenções prévias, limitações técnicas e resultados relacionados com data, unidade, método e origem. ECG/eco, EEG, espirometria e laboratório contribuem quando relevantes; “ter todos os exames” não equivale a fornecer tudo a cada agente.

Distinguir informação declarada pelo paciente, registro profissional, resultado laboratorial, texto extraído e inferência de IA. Preservar contradições e validade temporal; não inferir alergia ausente, exame normal ou estabilidade clínica a partir de campos vazios. Questionários de segurança e priorização seguem protocolos aprovados, com encaminhamento humano dos casos urgentes e confirmação de recebimento. A IA não altera silenciosamente fila ou preparo.

## Máscaras estruturadas para US, TC, RM, MG e RX

Um motor de formulários versionados combina dados tipados, narrativa editável e evidências vinculadas ao viewer. A interface oferece campos condicionais, grupos repetíveis, medidas importadas com origem, comparação temporal e atalhos. Não pré-marcar “normal” em um órgão não avaliado; diferenciar `presente`, `ausente_avaliado`, `nao_avaliado`, `indeterminado` e `nao_aplicavel`.

| Modalidade | Extensões específicas da máscara |
|---|---|
| US | Região, técnica, limitações, medidas e Doppler quando aplicável; protocolo obstétrico separado |
| TC | Região, protocolo, contraste/fases, reconstruções e comparação; HU apenas quando sustentado pela calibração |
| RM | Região, sequências, contraste, qualidade e limitações; intensidade não rotulada como HU |
| MG | Lateralidade, incidências/técnica, comparação e classificação apenas conforme protocolo/licença adotados |
| RX | Região, incidência, posicionamento, qualidade e limitações; medidas condicionadas à calibração |

O corpo comum inclui indicação, técnica, comparação, achados, impressão e limitações. Sistemas de classificação especializados devem ter versão, direitos de uso e validação próprios; não inventar tabelas ou pontos de corte. A RSNA oferece RadLex como terminologia de radiologia e referências ao LOINC/RSNA Radiology Playbook; códigos devem vir de serviços de terminologia versionados, com bindings revisados, e não ser inventados pelo LLM. [RSNA RadLex](https://www.rsna.org/practice-tools/data-tools-and-standards/radlex-radiology-lexicon).

Separar três objetos: **definição do template**, **instância preenchida** e **documento assinado**. O template guarda identificador, versão, escopo, autor/revisor, referências, licença, campos, condições, vocabulários e testes. A instância guarda valores, evidências e autoria de cada alteração. O documento assinado conserva a versão final; correções posteriores geram adendo, sem reescrever o histórico.

Exemplo **sintético** de resultado assistivo conforme `agent-result.schema.json`; não é recurso FHIR, objeto DICOM ou laudo clínico:

```json
{
  "schema_version": "0.2.0",
  "agent_id": "radiologia-especializada",
  "task_id": "contract-test",
  "synthetic": true,
  "status": "abstained",
  "findings": [],
  "limitations": ["Imagens não fornecidas; não houve análise de pixels."],
  "disagreements": [],
  "human_review_required": true,
  "signed_by": null
}
```

No runtime, referências de evidência identificam estudo, série, instância/frame e região, protegidos pelo mesmo controle de acesso das imagens. Medidas registram unidade, método, calibração e versão do algoritmo. O TID 1500 é um template DICOM SR de relatórios de medidas, não um substituto universal para o laudo narrativo. Exportação SEG/SR e FHIR exigem mapeamentos testados e perfis negociados. [DICOM PS3.21, TID 1500](https://dicom.nema.org/medical/dicom/current/output/chtml/part21/sect_A.7.2.html).

## Pesquisa científica e curadoria

O pesquisador recebe pergunta desidentificada, estrutura população/tarefa/comparador/desfecho e registra estratégia de busca e data. Prioriza estudo primário pertinente, diretriz da entidade emissora e revisão metodologicamente adequada; registra desenho, amostra, população, equipamento, limitações, conflitos e aplicabilidade. Relevância depende da pergunta: eficácia terapêutica, desempenho diagnóstico e reprodutibilidade não usam a mesma avaliação.

Cada alegação aponta para DOI/PMID/URL verificado e localização da evidência. Resumo não lido não vira revisão de texto integral; preprint, estudo retrospectivo e documento retirado permanecem identificados. Verificar correções/retrações antes de promover conteúdo. Resultados discrepantes devem aparecer na síntese, sem escolher apenas os que confirmam a hipótese.

O agente produz uma resposta à dúvida e uma proposta de atualização do corpus. A publicação clínica passa por curadoria com prazo de revisão e escopo explícito. Busca autônoma não modifica protocolos, máscaras, regras de triagem ou pesos em produção. Nunca transmitir identificadores ou texto clínico livre a buscadores públicos.

## Validação e promoção

Estados propostos: `draft → technical_review → clinical_review → approved → active → retired`; mudanças invalidam aprovações afetadas. Templates antigos continuam associados aos laudos anteriores. Testar campos condicionais, ausência de dado, unidades, lateralidade, contradições e fidelidade entre dados e narrativa, inclusive após edição humana e exportação.

Avaliar agentes por tarefa com casos autorizados, splits por paciente e análise por equipamento/protocolo/população. Medir omissão, fabricação de achados, vinculação incorreta de imagem, interpretação temporal, abstenção e carga de revisão, além da métrica específica da imagem. Testes sintéticos verificam contratos; não substituem avaliação clínica. Uso inicial em modo sombra requer autorização e desenho de estudo. O profissional revisa imagens e evidências, resolve pendências e assina; alertas críticos têm confirmação e escalonamento auditáveis.

**DESCONHECIDO:** modelos clínicos finais, equipe humana responsável, protocolos locais, tolerâncias, dados de validação, licenças de classificações e desempenho. Esses itens são gates do produto futuro, não impedimentos para salvar este planner. Nenhuma capacidade diagnóstica ou conformidade foi certificada nesta etapa.
