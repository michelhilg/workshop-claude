# Setup — Content Wiki com Claude Code e NotebookLM

Este guia leva o projeto do zero até funcionando. Execute cada etapa na ordem.

---

## Pré-requisitos

Antes de começar, você precisa ter instalado:

| Ferramenta | Como instalar | Verificar |
|---|---|---|
| Python 3.10+ (recomendado 3.11) | [python.org](https://www.python.org/downloads/) | `python3 --version` |
| `uv` (gerenciador de pacotes) | `pip install uv` ou `brew install uv` | `uv --version` |
| Claude Code CLI | [docs.anthropic.com/claude-code](https://docs.anthropic.com/pt-br/claude-code/getting-started) | `claude --version` |
| Conta Google | — | acesso ao [notebooklm.google.com](https://notebooklm.google.com) |

---

## Instalação

Todos os comandos abaixo devem ser executados **na raiz do projeto** (a pasta onde está este arquivo).

### 1. Criar o ambiente virtual

```bash
uv venv --python 3.11
```

Isso cria a pasta `.venv/` dentro do projeto. Todos os pacotes ficam aqui — nada é instalado globalmente no seu computador.

### 2. Instalar o notebooklm

```bash
uv pip install "notebooklm-py[browser]"
```

O sufixo `[browser]` instala o Playwright junto, que é o que permite ao notebooklm abrir o navegador para autenticação.

### 3. Baixar o navegador Chromium

```bash
.venv/bin/playwright install chromium
```

O Chromium será salvo na pasta `.playwright-browsers/` dentro do projeto (não no sistema).

> **Windows:** use `.venv\Scripts\playwright install chromium`

### 4. Criar o arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers
```

Isso garante que o Playwright encontre o Chromium na pasta local do projeto, não no sistema.

### 5. Autenticar no NotebookLM

```bash
.venv/bin/notebooklm login
```

Um navegador vai abrir. Faça login com sua conta Google e feche a janela quando concluir. Suas credenciais ficam salvas localmente — você não precisa repetir esse passo a cada uso.

> **Windows:** use `.venv\Scripts\notebooklm login`

---

## Estrutura do projeto

```
projeto/
├── CLAUDE.md              ← instruções para o Claude Code (leia se quiser entender as regras)
├── SETUP.md               ← este arquivo
├── .env                   ← variável PLAYWRIGHT_BROWSERS_PATH (você acabou de criar)
├── .venv/                 ← ambiente Python local (criado no passo 1)
├── .playwright-browsers/  ← Chromium local (criado no passo 3)
│
├── inputs/                ← seus arquivos brutos (não modifique)
│   ├── *.txt              ← transcrições, anotações, chats
│   ├── *.pptx             ← apresentações
│   └── *.xlsx             ← planilhas
│
├── wiki/                  ← documentos organizados (gerados pelo Claude)
│   └── *.txt              ← um arquivo por tema
│
├── outputs/               ← artefatos finais (gerados pelo Claude via NotebookLM)
│   ├── infografico.png
│   ├── quiz.json
│   ├── mindmap.json
│   ├── podcast.mp3
│   └── pendencias.txt     ← itens que não puderam ser gerados
│
├── recursos/
│   └── mindmap.html       ← visualizador do mapa mental (abra no navegador)
│
└── .claude/
    └── skills/            ← as três skills que orquestram o fluxo
        ├── organizar-docs/
        ├── notebooklm/
        └── gerar-outputs/
```

---

## Como usar

Com o setup pronto, abra o projeto no Claude Code e execute o fluxo em três etapas. **Nunca pule uma etapa.**

### Etapa 1 — Organizar os inputs

Coloque seus arquivos brutos em `inputs/` e diga ao Claude:

> "Organize os documentos de inputs e gere a wiki"

O Claude vai ler todos os arquivos e gerar documentos temáticos em `wiki/`.

### Etapa 2 — Criar o notebook no NotebookLM

> "Crie um notebook chamado [nome do seu projeto] e suba os arquivos da wiki como fontes"

O Claude vai criar o notebook e adicionar todos os `.txt` da `wiki/` como fontes.

### Etapa 3 — Gerar os outputs

> "Gere todos os outputs do notebook [nome do seu projeto]"

O Claude vai gerar infográfico, quiz, mapa mental e podcast, salvando tudo em `outputs/`.

---

## Verificar o mapa mental

Após a geração, abra `recursos/mindmap.html` no navegador. Ele carrega automaticamente o arquivo `outputs/mindmap.json`.

---

## Problemas comuns

**`notebooklm: command not found`**
Você está chamando o comando global. Use sempre o caminho completo: `.venv/bin/notebooklm`.

**`Error: browserType.launch: Executable doesn't exist`**
O Chromium não foi instalado. Execute novamente o passo 3: `.venv/bin/playwright install chromium`.

**`Authentication required` ou sessão expirada**
Execute `.venv/bin/notebooklm login` novamente. Sessões expiram após alguns dias.

**`Python version X.X not supported`**
O notebooklm requer Python 3.10 ou superior. Verifique com `python3 --version` e reinstale se necessário.

**`uv: command not found`**
Instale o uv primeiro: `pip install uv` (ou `brew install uv` no Mac).

**Windows: os caminhos com `.venv/bin/` não funcionam**
No Windows, o caminho correto é `.venv\Scripts\notebooklm` (barra invertida, `Scripts` em vez de `bin`).
