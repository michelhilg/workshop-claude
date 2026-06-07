![Capa](capa.png)

# Workshop Claude — IA Sem Frescura

Materiais do workshop de uso prático do Claude, organizado em três módulos: Chat, Cowork e Code. Cada case explora uma camada diferente de colaboração com IA, do simples ao sistêmico.

---

## Estrutura do Repositório

```
workshop-claude/
├── 01_comece_aqui/          ← ponto de partida: enunciados e materiais para você resolver
├── 02_cases_completos/      ← versão final resolvida de cada case
├── 03_apresentacao/         ← HTML da apresentação usada no workshop
├── 04_diagramas/            ← diagramas de arquitetura de cada case (.excalidraw + .png)
└── 05_bonus/                ← skills de economia de tokens para instalar no Claude Code
```

---

## Os Cases

O workshop cobre três modos de uso do Claude, organizados em cinco cases progressivos.

### Módulo 1 · Chat 

**Case 1 · Do caos à skill: organizando seu dia**  
`01_comece_aqui/1 - CASE 1 - CHAT/`

Uma lista bagunçada de tarefas entra no chat e sai como um quadro visual priorizado, com uma skill para repetir o processo toda manhã e o resultado salvo no Notion.

Todo mundo tem tarefas espalhadas entre e-mail, WhatsApp e bloco de notas. O exercício mostra como organizar isso só com o chat do Claude, sem instalar nada, sem planilha, sem código.

`Projetos` `Contexto` `Artefatos` `Iteração` `Skills` `Conectores`

---

### Módulo 2 · Cowork 

**Case 1 · Auditoria de fornecedores: das NFs ao relatório**  
`01_comece_aqui/2 - CASE 1 - COWORK/`

O Cowork conecta Drive, Gmail e arquivos locais numa única tarefa. Ele coleta notas fiscais, lê contratos, cruza com contexto de emails e entrega uma planilha consolidada e um relatório PDF prontos, sem você alternar entre abas.

O Chat responde. O Cowork executa. Ele lê arquivos, acessa ferramentas e gera entregas na sua máquina. O case mostra como montar um projeto com memória, regras e conectores para que o processo rode de forma repetível.

`Projetos` `CLAUDE.md` `Instruções globais` `Skills` `Conectores` `Tasks paralelas`

---

**Case 2 · Painel de Tendências do Nicho**  
`01_comece_aqui/3 - CASE 2 - COWORK/`

Um agente que, com um comando, pesquisa tendências do seu nicho na web, cruza com uma lista de temas que você mantém e entrega um dashboard HTML pronto, sozinho, fim a fim.

O objetivo é automatizar uma tarefa que costuma ser manual: monitorar o que está em alta no nicho e ter o resultado formatado sem precisar varrer a web na mão.

`Web Search` `Google Drive MCP` `CLAUDE.md` `Dashboard HTML` `Agendamento`

---

### Módulo 3 · Code

**Case 1 · Base de documentos integrada ao NotebookLM**  
`01_comece_aqui/4 - CASE 1 - CODE/`

O Claude Code conecta direto no NotebookLM: organiza seus documentos numa base limpa, sobe como fontes e usa a IA do próprio NotebookLM para gerar infográfico, quiz, mapa mental e podcast. Tudo comandado em português, sem você abrir a ferramenta.

A geração dos artefatos roda no NotebookLM, não no Claude. O case mostra como usar ferramentas externas a partir do Claude Code, deixando cada parte do trabalho na ferramenta certa.

`VSCode` `Skills` `MCP NotebookLM` `Base de documentos` `Artefatos (sem token)`

---

**Case 2 · Vários agentes trabalhando por você**  
`01_comece_aqui/5 - CASE 2 - CODE/`

Você pede uma vez, e vários agentes se dividem o trabalho: um busca os dados das suas ferramentas, um encontra os padrões, um organiza tudo. No fim, vira um dashboard publicado na internet, uma página no ar que você compartilha com quem quiser.

O case explora como dividir um problema entre agentes especializados e orquestrar o resultado final, saindo de dados brutos até um dashboard publicado.

`CLI` `Vários agentes` `MCP (suas ferramentas)` `Dashboard automático` `Publicação na web`

---

## Pasta por Pasta

| Pasta | Conteúdo |
|---|---|
| `01_comece_aqui/` | Enunciados, materiais brutos e prompts iniciais — o que você recebe no workshop para resolver |
| `02_cases_completos/` | Versão final resolvida de cada case, com toda documentação pronta |
| `03_apresentacao/` | `workshop_completo.html` — a apresentação completa do workshop para abrir no navegador |
| `04_diagramas/` | Diagramas de arquitetura em `.excalidraw` (editável) e `.png` para cada case |
| `05_bonus/` | Duas skills de economia de tokens: `caveman.skill` e `compactador-de-contexto.skill` |

---

## Bônus — Skills de Economia de Tokens

A pasta `05_bonus/` traz duas skills para instalar no Claude Code e reduzir o consumo de tokens em operações do dia a dia.

- **`caveman.skill`** — versão adaptada do projeto [caveman](https://github.com/JuliusBrussee/caveman): comprime o output de ferramentas (git, bash, etc.) para uma representação mínima antes de entregar ao modelo, cortando tokens sem perder a informação essencial.

- **`compactador-de-contexto.skill`** — skill para compactar o contexto acumulado em conversas longas, preservando decisões e fatos relevantes e descartando verbosidade redundante.

As skills funcionam tanto no Claude Code quanto no aplicativo do Claude.

**No Claude Code:** copie o arquivo `.skill` para `.claude/skills/` dentro do projeto ou para `~/.claude/skills/` para uso global.

**No aplicativo Claude:** acesse **Customize** no menu lateral, vá em **Skills** e importe o arquivo `.skill` diretamente pela interface.

---

## Links Úteis

- **[Visual Studio Code](https://code.visualstudio.com)** — editor recomendado para usar com o Claude Code; a extensão oficial integra o terminal, o diff e o chat do Claude diretamente no editor.

- **[Effective Context Engineering for AI Agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — artigo técnico da Anthropic sobre como estruturar contexto para agentes de IA, direto aplicável aos CLAUDE.md dos cases do workshop.

- **[RTK — Rust Token Killer](https://github.com/rtk-ai/rtk)** — proxy de CLI que intercepta comandos do Claude Code e filtra o output antes de passar ao modelo, economizando 60–90% dos tokens em operações como `git`, `find` e `ls`.

- **[caveman](https://github.com/JuliusBrussee/caveman)** — skill open-source de compressão de output de ferramentas; base da `caveman.skill` incluída no bônus deste repositório.

---

## Sobre o Workshop

Parte da série **IA Sem Frescura** — educação prática de IA para quem quer usar, não só entender.

[@michelhilg](https://www.instagram.com/michelhilg) no Instagram.
