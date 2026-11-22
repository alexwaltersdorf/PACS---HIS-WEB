# Importação DICOM e visualizador local

**22/11/2026 — primeiro ambiente executável de importação/visualização.** Não implementa ainda RIS, laudos assinados ou IA clínica. Instalação local para desenvolvimento e testes, sem validação diagnóstica.

## Abrir e importar

Com Docker Desktop iniciado, executar na raiz do checkout:

```powershell
.\scripts\start-local-viewer.ps1
```

Abrir `http://127.0.0.1:8042/`. As credenciais ficam em `ACESSO-LOCAL.txt` na pasta de dados, criada pelo script. Na interface, selecionar **Enviar → Selecionar pasta** ou **Selecionar arquivos**. Após concluir o envio, abrir o exame pelo ícone **Visualizar no OHIF**. A lista do viewer também está em `http://127.0.0.1:8042/ohif/`.

Importar os arquivos DICOM do estudo, não capturas de tela ou somente o executável do visualizador distribuído no CD. A compatibilidade de cada modalidade, compressão e tamanho de exame ainda exige teste; o ensaio desta entrega usou CT sintética de três instâncias.

O endereço funciona neste computador. Não encaminhar portas no roteador nem tratar esta configuração como publicação em rede. Os arquivos do usuário são selecionados por ele; nenhum exame real foi usado na validação desta entrega.

## Persistência e reinicialização

Pasta padrão: `D:\PACS-HIS\local`, fora do Git. `archive` contém objetos e índice; `secrets` contém a credencial. O script cria senha aleatória somente se ausente, restringe a pasta ao usuário do Windows e SYSTEM e preserva dados nas execuções seguintes. A pasta deve ser exclusiva. O Docker mantém suas próprias imagens/disco virtual conforme a configuração existente; apenas criar a pasta de dados não migra o Docker.

Para outra pasta local, passar `-DataRoot`. Não apontar para uma pasta com arquivos alheios. A instância tem um único usuário local, sem isolamento multi-instituição ou auditoria clínica completa. A proteção em repouso e a política de backup ainda precisam ser implementadas; persistência após reinício não é backup.

Para parar sem apagar os exames:

```powershell
$env:PACS_LOCAL_ROOT = 'D:/PACS-HIS/local'
docker compose -f infra/local/compose.yaml stop
```

## Componentes e fronteiras

- Orthanc com DICOMweb, Explorer 2, GDCM e OHIF; armazenamento SQLite local neste incremento.
- Nginx publica somente `127.0.0.1:8042`, encaminhando ao Orthanc em rede interna sem porta própria publicada. DICOM TCP está desativado.
- Autenticação Basic obrigatória; segredo montado por arquivo, fora do repositório e sem impressão em logs. HTTP é restrito a loopback; implantação remota exigirá desenho próprio com TLS.
- Proxy não recebe o segredo do servidor. Host/Origin restritos, CSP para conexões do navegador ao próprio serviço, ausência de access log e indicação HTML de não tradução automática dos metadados. Esses controles não são certificação nem garantia contra toda forma de vazamento.
- Configuração explícita carrega somente os quatro plugins necessários. `cap_drop: ALL` e `no-new-privileges`; proxy sem root e filesystem somente leitura. DNS do backend é renovado pelo resolver Docker.

## Versões e fontes verificadas

As imagens estão fixadas por digest em [compose.yaml](../infra/local/compose.yaml). Não há instalação de `latest` na inicialização.

| Componente | Versão selecionada | Fonte e licença consultada |
|---|---|---|
| Pacote Orthanc Team | 26.11.1; core 1.13.1; OHIF plugin 1.8 / viewer 3.12.0 conforme release notes | [Release notes](https://github.com/orthanc-server/orthanc-builder/blob/master/release-notes-docker-images.md), [licenciamento do ecossistema](https://orthanc.uclouvain.be/book/faq/licensing.html) — core GPLv3+, plugins têm licenças próprias, inclusive AGPL |
| OHIF | Distribuição incluída no plugin oficial | [Integração oficial](https://orthanc.uclouvain.be/book/plugins/ohif.html), [MIT do viewer](https://github.com/OHIF/Viewers/blob/master/LICENSE) |
| Nginx | 1.30.7-alpine | [Dockerfile oficial](https://github.com/nginx/docker-nginx/blob/master/stable/alpine-slim/Dockerfile), [licença BSD de duas cláusulas](https://github.com/nginx/nginx/blob/master/LICENSE) |

Binários originais são obtidos das imagens oficiais; este repositório contém configuração e scripts próprios, não cópias dos binários. Fontes consultadas em 22/11/2026. Rever obrigações específicas antes de modificar/distribuir componentes derivados.

## Evidência de execução e limites

Executado: servidor e proxy saudáveis, 401 para acesso anônimo e conta padrão, 403 para Origin externo, rejeição de Host desconhecido e porta publicada somente em loopback. Importação de três instâncias CT geradas sem dados de pacientes; consulta DICOMweb; PNG de preview; integridade SHA-256 do arquivo recuperado antes/depois de reiniciar o serviço. Imagem sintética renderizada no OHIF em Chrome; menu de seleção de pasta/arquivos observado.

O upload foi exercitado pela API local. A automação de seleção de arquivo pelo navegador não foi concluída; não se alega teste completo desse caminho de UI. O formulário está disponível para seleção manual pelo usuário.

[smoke_local_viewer.py](../scripts/smoke_local_viewer.py) gera dados sintéticos exclusivamente na pasta externa. A limpeza verifica identidade do teste e hashes e remove apenas as instâncias registradas, nunca o estudo inteiro nem exames alheios. Sintaxe/configuração e revisão independente foram verificadas; precisão clínica, carga, backup/restore e outras modalidades não foram validados.
