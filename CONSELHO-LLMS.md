# Conselho de construção — Codex, Claude Code e Gemini

**Diretriz do fundador:** as três ferramentas devem colaborar na construção da empresa e do produto, compartilhar conhecimento e discutir criticamente o melhor caminho. A ambição é criar uma startup de grande escala; valuation de unicórnio é uma aspiração, não resultado ou promessa demonstrados.

Este conselho cuida de produto, engenharia, pesquisa e estratégia. Ele é diferente dos agentes clínicos embarcados descritos no planner. As três ferramentas podem usar modelos distintos e versões mutáveis; registre ferramenta, versão/modelo quando conhecido, tarefa, evidências e resultado. Não confundir assinatura de produto com acesso a API ou capacidade clínica validada.

## Fonte compartilhada e entrada de cada ferramenta

| Participante | Arquivo de entrada | Responsabilidade inicial, ajustável por tarefa |
|---|---|---|
| ChatGPT / Codex | [AGENTS.md](AGENTS.md) | Implementação, integração, testes e consolidação rastreável |
| Anthropic / Claude Code | [CLAUDE.md](CLAUDE.md) | Revisão de arquitetura, alternativas e crítica de riscos |
| Google / Gemini | [GEMINI.md](GEMINI.md) | Pesquisa, comparação de alternativas e crítica de produto/custo |

Essa distribuição é uma convenção do projeto, não afirmação de superioridade de um fornecedor. As funções devem rodar entre participantes. Em mudança significativa, quem implementa não é o único revisor.

Ao iniciar, ler este documento, [PLANNER.md](PLANNER.md), [contexto](docs/contexto-projeto.md), a [discussão compartilhada](collaboration/README.md) e o estado do Git. Atualizar o checkout sem descartar alterações alheias. Referenciar o commit examinado; se a base mudar materialmente, reavaliar a conclusão.

## Como conversar e decidir

1. **Proposta:** autor formula problema, alternativas, evidência, benefício esperado, custo/risco e experimento. Cria mensagem endereçada às outras duas ferramentas.
2. **Crítica independente:** cada participante responde com concordâncias, objeções, lacunas e teste discriminante. Não escrever uma resposta em nome de ferramenta não consultada.
3. **Réplica:** o proponente responde às objeções, ajusta a proposta e identifica o que mudou.
4. **Síntese:** uma ferramenta reúne os três pareceres e preserva divergências. Ausência de resposta fica pendente; silêncio não é concordância.
5. **Decisão:** registrar opção, motivo, evidências, responsável e reversão no ADR/PR. Impasse com impacto clínico, segurança, orçamento ou estratégia vai ao responsável humano. Consenso de LLM não é validação clínica ou comercial.
6. **Execução:** atribuir proprietário de arquivos, implementar em branch, testar, revisar e publicar dentro da autorização existente. Mudança de produção continua sujeita aos gates aplicáveis.

Limite padrão: duas rodadas de crítica/réplica e síntese. A discussão precisa produzir experimento, decisão ou pendência concreta, não conversa ilimitada. Para uma alteração pequena e reversível, a coordenação pode solicitar apenas a revisão necessária e registrar por que as outras não participaram.

## Memória e concorrência

Mensagens ficam em `collaboration/messages/` como registros imutáveis por convenção, um arquivo por mensagem. Cada arquivo possui ID, assunto, autor declarado, destinatários, referência à mensagem anterior, commit-base e origem. Correções usam nova mensagem; nunca reescrever a opinião de outro participante. O utilitário [council.py](scripts/council.py) valida e acrescenta mensagens, consulta a caixa de entrada e monta contexto para revisão.

GitHub é o meio de compartilhamento assíncrono. As sessões precisam executar para ler e responder. Este commit não mantém três LLMs ligadas permanentemente nem instala um serviço que se comunica sozinho. A automação futura usa adaptadores autenticados, fila, orçamento, timeout, idempotência e autorização por ferramenta; nenhuma chave fica no repositório.

Cada participante pode propor alterações na documentação canônica por commit/PR. Um responsável integra mudanças conflitantes; nenhum participante faz force-push, resolve conflitos apagando trabalho alheio ou altera permissões por conta própria. Git registra histórico, mas `author` no JSON não autentica a identidade do modelo. Proveniência de respostas retransmitidas é declarada e deve ser verificada pelo executor; autenticação forte será parte dos adaptadores.

## Critérios para o êxito do projeto

Priorizar problema real de uma instituição piloto, redução mensurável de retrabalho/tempo, qualidade e segurança, integração viável e adoção recorrente. Antes de ampliar a plataforma, testar a jornada completa e uma tarefa de IA delimitada. Medir tempo até valor, falhas de integração, carga de revisão, custo por exame/execução e uso recorrente; estabelecer metas com dados de base, sem inventar números.

Hipóteses comerciais — segmento inicial, disposição a pagar, diferenciação, distribuição e economia por cliente — devem ser pesquisadas e testadas. A discussão das três ferramentas deve contestar expansão prematura e promessas não verificadas. Questões regulatórias, direitos de dados, assinatura e decisões clínicas permanecem com responsáveis habilitados.

## Referências de configuração

Codex documenta leitura de `AGENTS.md`; Claude Code documenta `CLAUDE.md` e importações; Gemini CLI documenta `GEMINI.md` e importações. Os arquivos deste projeto usam essas entradas para apontar à mesma governança. Em outras interfaces web/IDE, confirmar o mecanismo de contexto disponível. [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/).
