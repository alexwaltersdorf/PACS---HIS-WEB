# Visualizador local executável

Entrada: usuário já possui imagens e solicita acesso para importar o exame. Implementação: Codex. Revisão independente: subagente Codex `revisao_viewer_local`, somente leitura; não representa parecer do Claude Code ou Gemini.

Entregue: Compose com Orthanc/OHIF/DICOMweb e proxy de loopback, credencial gerada externamente, script de início idempotente e ensaio CT sintético. Evidência: autenticação negativa/positiva, Host/Origin, consulta DICOMweb, preview PNG, hash preservado após restart e imagem no OHIF em Chrome. Dados sintéticos removidos do arquivo após teste; fixtures ficam fora do Git. A seleção automática de arquivo pela interface não foi concluída; a importação foi exercitada pela API e o menu manual está disponível.

A revisão encontrou e corrigiu cleanup dependente de assert: agora verifica propriedade/hash explicitamente e exclui só instâncias próprias. Startup foi ajustado para configurações explícitas e hostid montado, preservando cap_drop ALL. Proxy permite publicar loopback mantendo Orthanc em rede interna. Adicionada indicação de não tradução automática após observação de tradução de textos sintéticos no navegador.

Sem exames reais, dados de paciente, credenciais ou inventário privado neste registro. Requisitos e limites em [visualizador local](../../../docs/09-visualizador-local.md). CI documental não é validação clínica; produção, RIS e agentes clínicos continuam pendentes.
