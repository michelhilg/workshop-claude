# Content Wiki — Projeto Claude Code

## Objetivo

Transformar documentação interna bagunçada de um creator solo em uma wiki organizada e em materiais de treinamento prontos para consumo.

O projeto lê arquivos brutos de múltiplos formatos na pasta `inputs/`, organiza o conhecimento em documentos temáticos na pasta `wiki/`, sobe esses documentos no NotebookLM e gera artefatos de aprendizado na pasta `outputs/`.

**Resultado esperado:** material que chegou como caos (transcrições, chats, rascunhos, planilhas) sai como wiki estruturada + podcast + quiz + infográfico + mapa mental — sem reescrever nada manualmente.

---

## Ambiente

- O `notebooklm` está instalado localmente em `.venv`. Sempre use `.venv/bin/notebooklm`, nunca o comando global.
- No Windows, o caminho é `.venv\Scripts\notebooklm`.
- Instale novos pacotes Python com `uv pip install`, nunca com `pip` ou `pip3`.
- A variável `PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers` está no `.env` — o Chromium fica na pasta do projeto.

---

## Estrutura do projeto

```
projeto-content-wiki/
├── CLAUDE.md              ← este arquivo (leia sempre antes de agir)
├── skills/
│   ├── organizar-docs.md  ← lê inputs/ e gera wiki/ em arquivos temáticos .txt
│   ├── notebooklm.md      ← conecta ao NotebookLM, cria notebook, sobe docs, usa recursos
│   └── gerar-outputs.md   ← gera infográfico, quiz, mindmap e podcast no NotebookLM
├── inputs/                ← material bruto (não modificar)
├── wiki/                  ← documentação organizada gerada pela skill organizar-docs
└── outputs/               ← artefatos gerados pelo NotebookLM
```

---

## Skills disponíveis

### `organizar-docs`
Lê todos os arquivos em `inputs/`, extrai o conhecimento útil e gera múltiplos arquivos `.txt` temáticos em `wiki/`. Cada arquivo cobre um tema específico do processo do creator.

**Quando usar:** quando os inputs foram atualizados ou quando a wiki ainda não existe.

**Como acionar:**
> "Organize os documentos de inputs e gere a wiki"

---

### `notebooklm`
Conecta ao NotebookLM via skill instalada. Permite listar notebooks existentes, criar um notebook novo, adicionar fontes (arquivos da pasta `wiki/`) e usar os recursos nativos do NotebookLM.

**Quando usar:** depois que a wiki foi gerada, para criar o notebook e subir os documentos como fontes.

**Como acionar:**
> "Crie um notebook chamado [nome] e suba os arquivos da wiki como fontes"
> "Liste meus notebooks do NotebookLM"
> "Adicione o arquivo wiki/processo-gravacao.txt como fonte do notebook"

---

### `gerar-outputs`
Usa o NotebookLM (via skill notebooklm) para gerar quatro formatos de output a partir do notebook alimentado: infográfico, quiz, mapa mental e podcast. Salva os arquivos gerados em `outputs/`.

**Quando usar:** depois que o notebook está criado e as fontes foram adicionadas.

**Como acionar:**
> "Gere todos os outputs do notebook [nome]"
> "Gere só o podcast do notebook [nome]"

---

## Fluxo de trabalho

O projeto segue sempre esta sequência. Nunca pule uma etapa.

```
1. organizar-docs   →   lê inputs/, gera wiki/*.txt
2. notebooklm       →   cria notebook, sobe wiki/*.txt como fontes
3. gerar-outputs    →   gera infográfico + quiz + mindmap + podcast → outputs/
```

---

## Regras de operação

**Sobre os inputs:**
- Nunca modifique ou delete arquivos em `inputs/`. São a fonte original.
- Os inputs podem estar em qualquer formato: `.txt`, `.pptx`, `.xlsx`, `.pdf`. Leia todos.
- Informações contraditórias entre arquivos são normais — use o dado mais recente ou o mais detalhado, e anote a contradição no arquivo wiki gerado.

**Sobre a wiki:**
- Gere sempre em `.txt` — é o formato mais compatível com o NotebookLM.
- Um arquivo por tema. Não misture temas em um único arquivo.
- Nomeie os arquivos em kebab-case descritivo: `processo-gravacao.txt`, `fluxo-aprovacao.txt`.
- O conteúdo deve ser claro, direto e em português. Sem jargão desnecessário.
- Se uma informação estava incompleta no input (ex.: "ferramenta a definir"), anote como pendência no arquivo wiki, não invente.

**Sobre os outputs:**
- Salve cada artefato em `outputs/` com nome descritivo: `infografico.png`, `quiz.json`, `mindmap.json`, `podcast.mp3`.
- Se um formato não estiver disponível no NotebookLM no momento, registre em `outputs/pendencias.txt` e continue com os demais.
- **Idioma:** sempre execute `notebooklm language set pt_BR` antes de gerar qualquer output. Todo conteúdo gerado deve estar em português.
- **Formato do mapa mental:** `mindmap.json` deve sempre seguir o esquema abaixo — é o único formato que `recursos/mindmap.html` aceita:
  ```json
  {
    "name": "Título raiz",
    "children": [
      { "name": "Nó filho", "children": [ { "name": "Nó neto" } ] }
    ]
  }
  ```
  Regras: `"name"` é obrigatório em cada nó; `"children"` é opcional e nunca deve ser array vazio (omita em nós folha). Se o download do NotebookLM retornar formato diferente, converta para este padrão antes de salvar.

**Sobre erros e bloqueios:**
- Se a conexão com o NotebookLM falhar, informe o erro claramente e aguarde instrução. Não tente reconectar em loop.
- Se um arquivo de input não puder ser lido (formato corrompido, etc.), pule e registre em `outputs/pendencias.txt`.
- Sempre confirme antes de criar um notebook novo se já não existe um com o mesmo nome.

---

## Contexto do projeto

**Creator:** Michel — infoprodutor e educator de IA, criando conteúdo sobre produtividade e ferramentas de IA para o Instagram.

**Colaboradores mencionados nos inputs:**
- Carol — editora de vídeo
- Jana — editora de vídeo (nova)
- Rodrigo — responsável pelo calendário editorial
- Gabriel — mentor do Michel

**Canais de foco:** Instagram (prioridade 1). YouTube apenas reaproveitamento.

**Métricas que importam:**
- Taxa de salvos (meta: acima de 3%)
- Compartilhamentos
- Comentários com pergunta
- Crescimento de seguidores (meta 2026: 10k até junho)
