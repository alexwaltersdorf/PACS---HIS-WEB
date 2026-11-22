# Infraestrutura para começar o desenvolvimento

**Data:** 22/11/2026. **Estado: proposta do Codex**, para orientar a implementação. Não há contratação, implantação, ensaio de carga ou aprovação de produção nesta atualização.

## Recomendação

Desenvolver primeiro no computador local e usar uma VPS Linux para homologação compartilhada quando o primeiro fluxo estiver executável. Manter aplicação e configuração portáveis por contêineres. Não é necessário contratar servidor para começar a escrever e testar o software.

VPS é o servidor virtual que hospeda serviços. VPN é um canal de acesso privado; pode complementar a VPS, mas não é um substituto de hospedagem.

| Ambiente | Uso inicial | Condição para avançar |
|---|---|---|
| Local | Desenvolvimento, testes e estudos DICOM sintéticos | Engine de contêineres operacional, espaço de disco, volumes persistentes e aplicação acessível apenas localmente |
| VPS de homologação | Demonstração e testes por equipe remota | Autenticação, TLS, portas restritas, backups externos e restauração demonstrada; dados sintéticos |
| Produção | Operação correspondente ao uso pretendido | Dimensionamento, finalidade, responsáveis, contratos, isolamento, recuperação e validações aplicáveis definidos e demonstrados |

A inspeção local encontrou Docker instalado, mas o engine Linux não respondeu. Portanto, o ambiente ainda não está pronto para executar os contêineres. Preparar armazenamento para imagens de contêiner, disco virtual, volumes DICOM e banco antes de baixar dependências volumosas. Diretório do código e diretório de dados podem ser diferentes. Criar uma pasta para DICOM não move automaticamente o disco virtual do Docker. O inventário específico da máquina fica fora deste documento público.

## Candidato de VPS para homologação

**INFERIDO / PROPOSTA:** Hostinger KVM 4, com 4 vCPU, 16 GB RAM e 200 GB NVMe, é um ponto de partida para medir uma instalação pequena com viewer, API, banco e PACS, sem inferência pesada. A configuração é anunciada pelo fornecedor; a suficiência para este software ainda não foi medida. Preferir região brasileira para avaliar latência junto ao piloto, se disponível no provisionamento. [Planos oficiais](https://www.hostinger.com/br/servidor-vps), [região Brasil](https://www.hostinger.com/vps/servers/brazil).

Reavaliar antes da compra: preço total e renovação, prazo contratado, região, armazenamento, transferência, limites operacionais e custo de backups. Não dimensionar produção pela etiqueta do plano. A oferta consultada publica preços promocionais equivalentes mensais vinculados a contratação por prazo; esses valores não são orçamento aprovado do projeto.

A documentação descreve créditos de CPU e limitação após consumo sustentado. Testar ingestão, descompressão e concorrência com carga longa representativa; um teste curto não demonstra capacidade sustentada. O texto consultado apresenta números divergentes em alguns trechos, portanto confirmar os limites efetivos com o fornecedor antes de assumir um orçamento de CPU. [Política de créditos](https://www.hostinger.com/support/how-cpu-credits-work-on-hostinger-vps/).

**IA de imagem:** planejar workers separados, dimensionados pela tarefa e VRAM necessária. O fornecedor distingue VPS baseada em CPU de instâncias GPU, com cobrança e persistência diferentes. A documentação da GPU informa armazenamento efêmero sem backup: não usar esse disco como arquivo primário PACS. Não é necessário contratar GPU para a primeira etapa. [VPS e GPU](https://www.hostinger.com/support/how-to-choose-between-a-hostinger-vps-and-gpu-instance/).

## Primeira implementação proposta

1. Preparar execução local e armazenamento; fixar versões/licenças e registrar compatibilidade antes da instalação.
2. Subir Orthanc com DICOMweb, PostgreSQL, API modular e viewer OHIF com conjunto Cornerstone compatível. Configurar volumes e acesso local; não expor banco, administração PACS ou porta DICOM na internet.
3. Implementar pedido mínimo e identificadores com autoridade emissora. Construir a worklist de interpretação, mantendo sua distinção de DICOM Modality Worklist.
4. Carregar apenas estudos sintéticos; abrir o estudo no viewer e reabri-lo após reinício sem perder dados. Executar o [experimento de reconciliação](../planning/experimentos-reconciliacao.md) com conflitos, duplicação e chegada fora de ordem.
5. Integrar editor de rascunhos com uma base de template versionada e vínculo ao estudo. Assinatura final, IA clínica e integrações externas permanecem incrementos próprios.
6. Reproduzir a instalação em homologação e medir carga antes de ajustar a VPS. GitHub armazena código, configuração sem segredos e evidências sintéticas; não serve como arquivo de exames.

## Armazenamento e operação

Dimensionar a partir de exames/dia × tamanho médio por exame × dias retidos, acrescentando crescimento, índices, derivados e margem operacional. Backups e réplicas são capacidades adicionais. Medir também tamanhos extremos, concorrência e banda; a média isolada pode esconder séries volumosas.

Exemplo hipotético: 100 exames/dia × 0,5 GB × 30 dias = 1.500 GB de dados originais, antes dos demais itens. Não é uma estimativa do piloto. Demonstra por que 200 GB podem servir a uma demonstração sintética, mas não definem a capacidade do PACS real.

Backup semanal anunciado pelo provedor não estabelece o RPO do produto. Definir frequência, retenção, cópia independente, criptografia, consistência entre banco/arquivo e teste de restauração. Uma VPS única tem ponto único de falha; região brasileira, VPN ou certificado TLS não comprovam conformidade ou alta disponibilidade por si sós.

## Evidência e pendências

- **OBSERVADO:** capacidades e políticas nas páginas oficiais acima, consultadas em 22/11/2026; cliente Docker local presente, engine indisponível na consulta.
- **INFERIDO:** desenvolvimento local evita contratação prematura e permite preparar implantação reproduzível; VPS facilita testes remotos sem depender do computador de desenvolvimento ligado.
- **PROPOSTA:** local primeiro, VPS KVM 4 como candidato de homologação, GPU separada quando a tarefa justificar.
- **DESCONHECIDO:** parceiro piloto, volume, concorrência, tamanho/retencão de exames, RPO/RTO, orçamento e desempenho real. Claude Code e Gemini ainda não revisaram esta proposta específica.

Esta atualização registra a escolha candidata e o primeiro incremento. Nenhum serviço do produto foi instalado ou iniciado por esta alteração documental.
