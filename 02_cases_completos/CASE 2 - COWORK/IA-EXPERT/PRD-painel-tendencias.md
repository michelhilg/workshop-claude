# PRD — Painel de Tendências do Nicho (Claude Cowork)

> **Sistema:** `painel-tendencias`
> **Plataforma de construção:** Claude Cowork (este PRD é produzido no Claude chat e levado pro Cowork)
> **Tempo de construção:** 3 horas (Bloco 0 de setup + 3 blocos de ~1h)
> **Domínio único:** Tendências de nicho — nicho seed: **Inteligência Artificial**
> **Fundação:** plugin Productivity do Cowork
> **Fuso horário:** America/Sao_Paulo (UTC−3)
> **Status:** pronto para construção, zero decisões de design pendentes

---

## 1. Executive summary

`painel-tendencias` é um agente de domínio único no Claude Cowork que, **com um comando** (`pesquisar tendências`), pesquisa o que está em alta no nicho de Inteligência Artificial via web search nativo, cruza os achados com uma **lista de temas mantida por você** (puxada do Google Drive), e gera um **dashboard HTML visual** pronto para olhar. O agente roda fim a fim, sozinho — esse é o momento "uau" da demonstração no workshop.

**Domínio:** tendências de nicho (IA como seed; trocável editando um arquivo de input).

**Padrões de interação expostos:**
- **Habilidade sob demanda** — `pesquisar tendências`: o comando que dispara a pesquisa completa.
- **Painel sempre ativo** — `dashboard-tendencias.html`: o output visual.
- **Briefing agendado** — execução automática toda manhã (07h00) que roda a mesma pesquisa e atualiza o painel antes de você acordar.

**Por que cabe em 3h:** um domínio, uma fonte de busca (web search nativo, sem MCP de scraping), uma integração (Drive, só leitura da lista de temas), um output (dashboard HTML). Sem builder autônomo, sem multi-domínio. O Bloco 0 cuida do setup; os Blocos 1–3 entregam camada de dados → habilidade + painel → agendamento.

**Como escala depois:** novo nicho = editar `tendencias/inputs/temas.md`. Novo domínio (ex.: concorrentes, conteúdo) = nova pasta seguindo o mesmo padrão `{domain}/` + os mesmos três padrões de interação. Nenhuma reestruturação.

---

## 2. Quick start — movendo isso para o Cowork

Este PRD foi produzido no Claude chat. Esta seção é a transferência para o Cowork, onde a construção realmente acontece.

### Entrando no Cowork (eu faço isso)
1. Abrir o Claude Cowork.
2. Criar um projeto apontado para uma pasta local: `~/cowork/`.
3. Carregar este PRD no projeto — soltar o arquivo `PRD-painel-tendencias.md` na pasta do projeto, ou colar seu conteúdo na primeira mensagem do Cowork.

Esta é a primeira vez que o Cowork está envolvido. Nada está configurado ainda.

### Instruções do projeto (colar no campo de custom instructions do Cowork)

```
Você é o construtor e operador do sistema "painel-tendencias", um agente de
tendências de nicho rodando em ~/cowork/. Domínio único: tendências do nicho
de Inteligência Artificial.

Regras de operação:
- A camada de dados é LOCAL, em ~/cowork/. Conectores (Drive) são fontes de
  dados, nunca armazenamento.
- NUNCA sobrescreva nada em qualquer pasta inputs/. Arquivos de inputs/ são
  mantidos por mim (humano). Tarefas de atualização escrevem só em data/ e
  outputs/.
- Construa em blocos. Quando eu disser "Iniciar Bloco N", execute só aquele
  bloco, reporte o que fez + o resultado da verificação de conclusão, e espere
  meu sinal verde antes do próximo.
- Fuso horário: America/Sao_Paulo (UTC−3). Tarefas agendadas rodam às 07h00.
- Planeje antes de agir em passos destrutivos; prefira ações reversíveis;
  documente decisões não óbvias no CLAUDE.md raiz.
```

### Como executar a construção (instruções pro Cowork)
Quando eu disser para começar, **assuma que nada está configurado ainda.**

1. **PRIMEIRO execute o Bloco 0 (Configuração)** da §7: confirme se o plugin Productivity está instalado — se não, me dê os passos exatos e aguarde; faça-me rodar `/start` e confirme que os arquivos raiz do plugin existem; confirme se o conector Google Drive está ativado e me diga pra ativar caso contrário.
2. **Só depois da configuração confirmada**, construa o plano um bloco de cada vez, em ordem (Bloco 1 → 2 → 3).
3. Após cada bloco, **relate o que foi feito e o resultado da verificação de conclusão**, e aguarde meu sinal verde.

### A primeira coisa que digo
> **"Start building — comece pelo Bloco 0."**

---

## 3. Goals and non-goals

### Goals
- Um comando dispara a pesquisa completa de tendências de IA e gera um dashboard HTML, fim a fim, sem intervenção.
- O dashboard cruza o que está em alta na web com a minha lista de temas (Drive), sinalizando quais temas estão "quentes" agora.
- A mesma pesquisa roda automaticamente toda manhã às 07h00, deixando o painel atualizado antes de eu sentar pra trabalhar.
- O sistema é digerível ao vivo em ~12 min de execução narrada (momento "uau" do palco).

### Non-goals (deliberadamente fora desta janela de 3h)
- **Scraping profundo de páginas específicas (Firecrawl/MCP de crawl).** Web search nativo entrega o "uau de autonomia" com uma auth a menos. Fica como trabalho futuro (§10).
- **Multi-domínio (concorrentes, conteúdo, etc.).** Este PRD é um domínio só. A arquitetura comporta mais; não é o escopo de hoje.
- **Builder autônomo** (soltar um briefing e receber um produto finalizado). Fora de 3h.
- **Escrita/publicação de conteúdo a partir das tendências.** O painel informa; não produz post.
- **Histórico de longo prazo / análise de séries temporais.** Guardamos snapshots datados (append-only), mas não construímos análise de tendência-sobre-tendência agora.

---

## 4. Architecture overview

### As três camadas
1. **Pastas locais** (`~/cowork/`) — a fonte da verdade. Arquivos simples: a lista de temas, os dados pesquisados, o dashboard gerado.
2. **Projeto do Cowork** — aponta para `~/cowork/`, carrega o plugin Productivity, lê/escreve os arquivos locais.
3. **Fluxos de trabalho** — a habilidade `pesquisar tendências`, o briefing agendado das 07h00, e o painel HTML.

### Padrões de interação e quais fluxos usam cada um
| Padrão | Fluxo | Quando dispara |
|---|---|---|
| Habilidade (sob demanda) | `pesquisar-tendencias` | Eu digo o comando |
| Briefing (agendado) | `briefing-matinal` | Automático, 07h00 diário |
| Painel (sempre ativo) | `dashboard-tendencias.html` | Atualizado por ambos acima |

> O briefing matinal e a habilidade rodam **a mesma lógica de pesquisa**. A diferença é só o gatilho (cron vs. comando manual). Construímos a lógica uma vez (Bloco 2) e o agendamento a aponta (Bloco 3).

### Arquitetura de memória (três níveis fixos)
- **`CLAUDE.md` raiz** — pessoas, terminologia, abreviações transversais (do plugin).
- **`memory/tendencias/`** — conhecimento profundo do domínio: o que conta como "tendência relevante", fontes preferidas, glossário de IA.
- **`tendencias/CLAUDE.md`** — voz e função ao trabalhar dentro do domínio (tom direto, foco em "o que isso muda pra um creator de IA").

### Principais decisões arquitetônicas e a tensão por trás
| Decisão | Tensão |
|---|---|
| Web search nativo em vez de Firecrawl/MCP | Profundidade de extração ↔ risco de auth ao vivo. Escolhido o risco menor. |
| Drive só pra leitura da lista de temas | Conveniência de editar no celular ↔ uma auth de MCP no palco. A lista é o único dado que faz sentido fora do PC. |
| Snapshots datados append-only em `data/` | Espaço em disco ↔ poder dizer "compare com ontem" depois. Append vence; arquivos são minúsculos. |
| Lógica de pesquisa única, dois gatilhos | Duplicação ↔ manutenção. Uma skill, o cron a chama. |

---

## 5. The data layer

A fundação. Construída sobre os arquivos raiz do plugin Productivity (`/start` cria `CLAUDE.md`, `TASKS.md`, `memory/`, `dashboard.html`) e segue o esqueleto raiz fixo + o padrão por domínio.

### Onde ela vive
Local: arquivos simples em `~/cowork/`, pasta que o projeto do Cowork aponta. **Não** em um conector. O Google Drive é **fonte** (de onde o agente lê a lista de temas), nunca armazenamento. Para backup, `~/cowork/` pode estar dentro de uma pasta sincronizada, mas o Cowork sempre lê/escreve arquivos locais.

### A árvore de pastas
```
~/cowork/                              ← Raiz do projeto Cowork (pasta LOCAL)
├── CLAUDE.md                          ← plugin: memória de trabalho transversal
├── TASKS.md                           ← plugin: lista de tarefas
├── memory/                            ← plugin: memória profunda por domínio
│   ├── people.md                      ← (plugin) pessoas relevantes
│   ├── terminology.md                 ← (plugin) termos/abreviações transversais
│   └── tendencias/                    ← conhecimento profundo do domínio
│       ├── criterios.md               ← o que conta como "tendência relevante"
│       ├── fontes.md                  ← fontes/sites preferidos pra calibrar busca
│       └── glossario-ia.md            ← termos de IA pra o agente não se perder
├── dashboard.html                     ← painel raiz do plugin (índice; linka o de tendências)
├── PRD-painel-tendencias.md           ← este PRD, na raiz pra referência
├── briefs/                            ← saídas do briefing matinal
│   └── archive/                       ← briefings antigos arquivados
└── tendencias/                        ← o domínio
    ├── CLAUDE.md                       ← voz/função ao trabalhar neste domínio
    ├── inputs/                         ← MANTIDO POR MIM — nunca sobrescrever
    │   └── temas.md                    ← minha lista de temas a monitorar (espelho do Drive)
    ├── data/                           ← atualizado por máquina (append-only)
    │   ├── tendencias-AAAA-MM-DD.json  ← snapshot datado da pesquisa do dia
    │   └── ultima-pesquisa.json        ← cópia do snapshot mais recente (sobrescrita)
    └── outputs/                        ← artefatos gerados
        └── dashboard-tendencias.html   ← o painel visual do domínio
```

### Entradas vs. dados
- `tendencias/inputs/temas.md` é **mantido por mim**. A habilidade e o cron **nunca** escrevem nele. Eu edito esse arquivo (ou sua origem no Drive) pra mudar o que é monitorado.
- `tendencias/data/` é **atualizado por máquina**. Snapshots datados são **append-only** (um arquivo novo por dia); `ultima-pesquisa.json` é **sobrescrito** a cada execução.

### Arquivos de memória — o que vai em cada um
- **`memory/people.md`** — (do plugin) vazio/seed; não crítico pra este domínio.
- **`memory/terminology.md`** — abreviações que eu uso (ex.: "CSF = Claude Sem Frescura").
- **`memory/tendencias/criterios.md`** — regra do que entra no painel: "tendência relevante = lançamento, mudança de preço, feature nova, ou debate em alta nos últimos 7 dias que afete quem cria conteúdo ou trabalha com IA. Ignorar fofoca de mercado e rumor não confirmado."
- **`memory/tendencias/fontes.md`** — sites/contas que costumam pautar IA (blogs oficiais de labs, agregadores de notícia de IA). Calibra a busca, não a limita.
- **`memory/tendencias/glossario-ia.md`** — termos pra o agente classificar certo (ex.: "MCP", "agente", "context window", "benchmark").

### Esquema de cada arquivo de dados

**`tendencias/inputs/temas.md`** (mantido por humano — Markdown, espelho da lista do Drive):
```markdown
# Temas que eu monitoro — nicho: Inteligência Artificial

## Modelos e lançamentos
- Novos modelos (Claude, GPT, Gemini, open-source)
- Mudanças de preço / planos de assinatura

## Ferramentas pra creator/empreendedor
- Ferramentas de IA pra conteúdo (texto, imagem, vídeo)
- Automação / agentes / Cowork-like

## Conceitos em alta
- MCP e integrações
- Skills / agentes autônomos
- Economia de tokens / custo de uso
```

**`tendencias/data/tendencias-AAAA-MM-DD.json`** (gerado por máquina — snapshot datado, append-only):
```json
{
  "data": "2026-06-05",
  "nicho": "Inteligência Artificial",
  "gerado_em": "2026-06-05T07:00:12-03:00",
  "itens": [
    {
      "titulo": "Anthropic lança Claude Opus 4.8",
      "categoria": "Modelos e lançamentos",
      "tema_relacionado": "Novos modelos",
      "resumo": "Novo modelo de topo com ganho em raciocínio e código.",
      "por_que_importa": "Eleva o teto do que dá pra fazer no Code; vale citar no workshop.",
      "calor": "alto",
      "fonte_titulo": "Anthropic News",
      "fonte_url": "https://www.anthropic.com/news",
      "publicado_em": "2026-06-04"
    }
  ],
  "temas_sem_movimento": ["Mudanças de preço / planos de assinatura"]
}
```

**`tendencias/data/ultima-pesquisa.json`** — formato idêntico ao snapshot datado; é só a cópia mais recente, sobrescrita a cada run (o dashboard lê este).

### Estratégia de atualização
| Arquivo | O que preenche | Frequência | Sobrescrita vs. append | Dedupe |
|---|---|---|---|---|
| `inputs/temas.md` | Eu (humano), espelhando o Drive | Quando eu quiser | n/a (humano) | n/a |
| `data/tendencias-AAAA-MM-DD.json` | habilidade + cron | 1×/dia (cron) + sob demanda | Append (1 arquivo/dia; sob demanda no mesmo dia sobrescreve o do dia) | Por `fonte_url` dentro do run |
| `data/ultima-pesquisa.json` | habilidade + cron | Toda execução | Sobrescrita | n/a |
| `outputs/dashboard-tendencias.html` | habilidade + cron | Toda execução | Sobrescrita | n/a |
| `briefs/briefing-AAAA-MM-DD.md` | cron matinal | 1×/dia | Append (1/dia) | n/a |

Nomenclatura conforme convenções fixas: pastas `kebab-case`, memória `.md`, dados `.json`, datados `nome-AAAA-MM-DD`.

---

## 6. Component specifications

### 6.1 Habilidade `pesquisar-tendencias` (sob demanda)
- **Propósito:** disparar a pesquisa completa e regenerar o painel com um comando.
- **Lê:** `tendencias/inputs/temas.md`, `memory/tendencias/criterios.md`, `memory/tendencias/fontes.md`, `memory/tendencias/glossario-ia.md`.
- **Escreve:** `tendencias/data/tendencias-AAAA-MM-DD.json`, `tendencias/data/ultima-pesquisa.json`, `tendencias/outputs/dashboard-tendencias.html`.
- **Cronograma:** sob demanda (comando: `pesquisar tendências`).
- **Saída:** JSON do snapshot + dashboard HTML regenerado. Nunca toca `inputs/`.

### 6.2 Briefing matinal `briefing-matinal` (agendado)
- **Propósito:** rodar a mesma pesquisa automaticamente toda manhã e deixar um resumo curto em Markdown + o painel atualizado.
- **Lê:** mesmos arquivos da habilidade.
- **Escreve:** mesmos arquivos da habilidade + `briefs/briefing-AAAA-MM-DD.md` (resumo de 5–8 bullets dos itens "calor: alto").
- **Cronograma:** diário, 07h00 America/Sao_Paulo.
- **Saída:** briefing Markdown + dashboard atualizado, prontos antes das 08h.

### 6.3 Painel `dashboard-tendencias.html` (sempre ativo)
- **Propósito:** visão visual do estado das tendências, cruzando web × minha lista.
- **Lê (em build-time, ao ser gerado):** `tendencias/data/ultima-pesquisa.json`.
- **Escreve:** nada (é artefato final).
- **Estrutura de saída:** HTML standalone, identidade Claude Sem Frescura (creme + verde, coral de acento; fontes Hanken Grotesk + JetBrains Mono via CDN). Seções: cabeçalho com nicho + data/hora da última pesquisa; grid de cards por item (título, categoria, "por que importa", selo de calor alto/médio/baixo, link da fonte); faixa de "temas sem movimento hoje". Lê dados embutidos no HTML no momento da geração (não faz fetch em runtime).

---

## 7. The build plan

3 horas → Bloco 0 (setup) + 3 blocos de ~1h. Tudo executado pelo Cowork, exceto onde marcado.

| Bloco | O que é construído | Quem executa | Saída | Concluído quando… |
|---|---|---|---|---|
| **0 — Setup** | (1) Confirmar plugin Productivity instalado; se não, me guiar (Cowork → Customizar → Plugins → "Productivity"). (2) Me fazer rodar `/start`. (3) Confirmar conector Google Drive ativado; me dizer pra ativar se faltar. | Eu (com Cowork verificando) | `CLAUDE.md`, `TASKS.md`, `memory/`, `dashboard.html` existem; Drive ativo | Os 4 arquivos raiz existem E o Drive responde |
| **1 — Camada de dados** | Criar a árvore `tendencias/` completa; popular `inputs/temas.md` (seed IA acima); escrever os 3 arquivos `memory/tendencias/`; criar `briefs/` + `archive/`. Puxar a lista de temas do Drive uma vez pra confirmar o espelho. | Cowork | Árvore de pastas + seeds preenchidos | Toda a árvore da §5 existe com conteúdo seed; `inputs/temas.md` bate com o Drive |
| **2 — Habilidade + painel** | Criar a skill `pesquisar-tendencias` (prompt em §8): web search por tema → classificar por critérios → escrever JSON datado + `ultima-pesquisa.json` → gerar `dashboard-tendencias.html`. Rodar 1× pra validar fim a fim. | Cowork | Skill instalada + 1 dashboard real gerado | `pesquisar tendências` roda sozinho e produz JSON + HTML válidos |
| **3 — Agendamento + polimento** | Configurar a execução agendada das 07h00 (briefing-matinal chamando a mesma lógica + escrevendo o briefing .md). Testar disparo manual do agendado. Linkar `dashboard-tendencias.html` no `dashboard.html` raiz. Salvar **plano B**: copiar o último dashboard bom pra um arquivo à prova de falha pro palco. | Cowork (agendamento) + Eu (confirmar permissão de execução agendada) | Cron 07h00 ativo + plano B salvo | Disparo manual do job agendado gera briefing + atualiza painel; cópia plano-B existe |

### Ordem de corte (se eu atrasar)
1. **Polimento visual do dashboard** (mantém funcional, corta refino).
2. **Briefing .md** (mantém o cron atualizando o painel, corta o resumo em texto).
3. **Agendamento** (Bloco 3 inteiro) — vira promessa contada, demo roda no manual.

### Nunca cortar
Bloco 0 (setup) + Bloco 1 (camada de dados) + a habilidade `pesquisar-tendencias` com geração do dashboard (núcleo do "uau" do palco).

---

## 8. Setup details and copy-paste prompts

### Criação de pastas (Bloco 1 — Cowork executa)
```
Em ~/cowork/, crie:
  tendencias/CLAUDE.md
  tendencias/inputs/temas.md
  tendencias/data/        (vazio por enquanto)
  tendencias/outputs/     (vazio por enquanto)
  memory/tendencias/criterios.md
  memory/tendencias/fontes.md
  memory/tendencias/glossario-ia.md
  briefs/archive/
Popule inputs/temas.md e os 3 arquivos de memory/tendencias/ com o conteúdo
seed do PRD (§5). CRÍTICO: inputs/temas.md é mantido por humano — depois deste
seed inicial, nenhum fluxo automático pode reescrevê-lo.
```

### Prompt da habilidade `pesquisar-tendencias` (Bloco 2 — copiar pra criação da skill)
```
NOME: pesquisar-tendencias
GATILHO: quando eu disser "pesquisar tendências" (ou variações).

O QUE FAZER:
1. LER tendencias/inputs/temas.md (minha lista de temas). NUNCA escrever neste arquivo.
2. LER memory/tendencias/criterios.md, fontes.md e glossario-ia.md pra calibrar.
3. Para CADA tema da lista, fazer web search nativo focado nos últimos 7 dias
   do nicho de Inteligência Artificial. Priorizar lançamentos, mudanças de
   preço, features novas e debates em alta. Ignorar rumor não confirmado.
4. Classificar cada achado: categoria (do meu tema), por_que_importa (1 frase
   pro meu público de creators/empreendedores de IA), calor (alto/médio/baixo),
   fonte (título + url + data de publicação).
5. Dedupe por fonte_url dentro deste run.
6. ESCREVER tendencias/data/tendencias-AAAA-MM-DD.json (data de hoje, fuso
   America/Sao_Paulo) no esquema do PRD §5. Sobrescrever se já existir hoje.
7. ESCREVER tendencias/data/ultima-pesquisa.json (cópia do snapshot de hoje).
8. GERAR tendencias/outputs/dashboard-tendencias.html: HTML standalone com os
   dados embutidos (sem fetch em runtime), identidade Claude Sem Frescura
   (fundo creme, verde #0E3A2F, coral #E8865A; Hanken Grotesk + JetBrains Mono
   via Google Fonts CDN). Cabeçalho: nicho + data/hora da última pesquisa. Grid
   de cards por item com selo de calor. Faixa final com temas_sem_movimento.
9. Listar em temas_sem_movimento os temas da lista que não tiveram achado.
CRÍTICO: escreve só em data/ e outputs/. Nunca em inputs/.
```

### Prompt do briefing agendado `briefing-matinal` (Bloco 3 — copiar)
```
NOME: briefing-matinal
GATILHO: agendado, diário, 07h00 America/Sao_Paulo.

O QUE FAZER:
1. Executar exatamente a mesma lógica da skill pesquisar-tendencias (passos 1–9).
2. Adicionalmente, ESCREVER briefs/briefing-AAAA-MM-DD.md: um resumo de 5 a 8
   bullets só com os itens de calor "alto", cada bullet = título + por_que_importa.
   Cabeçalho do arquivo: data + "Tendências de IA — briefing matinal".
CRÍTICO: escreve só em data/, outputs/ e briefs/. Nunca em inputs/.
```

---

## 9. Decision log

| # | Decisão | Raciocínio / trade-off |
|---|---|---|
| 1 | Web search nativo, não Firecrawl/MCP | Firecrawl dá extração profunda de páginas; o painel só precisa de manchetes/tendências. Tirar uma auth de MCP reduz o risco da demo ao vivo. Profundidade perdida é marginal pro caso de uso. |
| 2 | Drive (MCP) só pra ler `temas.md` | A lista é o único dado que faz sentido eu editar fora do PC (celular). Mantém uma auth única e justifica a narrativa "ele cruza com a MINHA lista" no palco. |
| 3 | Snapshots datados append-only | Habilita "compare com ontem" no futuro sem rearquitetar. Arquivos JSON são minúsculos; custo de disco irrelevante. |
| 4 | Skill única + cron que a chama | Evita duplicar a lógica de pesquisa em dois lugares. Um ponto de manutenção. |
| 5 | Dashboard com dados embutidos (sem fetch runtime) | HTML standalone abre em qualquer lugar, inclusive offline no palco. Não depende de servidor nem de caminho de arquivo local pra ler JSON. |
| 6 | `inputs/` imutável por automação | Protege a lista mantida por humano de ser apagada por um run. Regra dura repetida em todo prompt. |
| 7 | Agendamento construído (não só prometido) | Você escolheu construir de verdade; vira diferencial real do palco ("isso roda antes de você acordar — e aqui está o briefing de hoje cedo"). |
| 8 | Plano B (cópia do último dashboard bom) | A geração ao vivo ou a auth do Drive podem travar em 30 min. Ter um HTML pronto salva a demo sem quebrar a narrativa. |
| 9 | `por_que_importa` em cada item | O público não decide por manchete crua; decide pelo "o que isso muda pra mim". É a coluna que vende, igual à coluna conclusão das tabelas de benchmark. |
| 10 | Calor (alto/médio/baixo) em vez de score numérico | Iniciante não-técnico lê selo de calor instantaneamente; número pede interpretação. |

---

## 10. Out of scope / future work

**Adiado (não construído nesta janela):**
- **Firecrawl/MCP de scraping** — pra ler fontes específicas a fundo (changelogs, pricing pages, blogs monitorados). Adiciona uma auth; entra quando o valor migrar de "manchetes" pra "leitura de fonte".
- **Segundo domínio** (concorrentes, ideias de conteúdo, monitoramento de menções) — nova pasta `{domain}/` no mesmo padrão + os mesmos três fluxos. Sem reestruturação.
- **Builder autônomo** — soltar um briefing e receber post/carrossel pronto a partir das tendências.
- **Análise temporal** — usar os snapshots datados pra mostrar o que subiu/caiu semana a semana.

**Como escala sem reestruturação:**
Novo nicho = editar `tendencias/inputs/temas.md`. Novo domínio = nova pasta seguindo o padrão `{domain}/` (`CLAUDE.md` + `inputs/` + `data/` + `outputs/`) + sua skill + entrada no cron + seção no dashboard raiz.

**O que forçaria uma rearquitetura:**
Precisar de banco de dados real (volume de dados grande demais pra arquivos simples), ou multi-usuário (vários operadores no mesmo sistema), ou pipelines em tempo real (em vez de batch diário). Nada disso está no horizonte do uso pessoal/demonstração.
