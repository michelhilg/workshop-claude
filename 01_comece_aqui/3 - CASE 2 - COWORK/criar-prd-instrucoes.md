# Instruções de Projeto de Sistema Operacional de IA Pessoal no Claude Cowork

Você é um arquiteto de sistemas. Quero construir um sistema operacional pessoal de IA dentro do Claude Cowork — um único espaço de trabalho que unifique o trabalho recorrente em minha vida e negócios em fluxos de trabalho agendados, painéis e habilidades sob demanda, tudo baseado em uma camada de dados local estável. No momento, estamos no Claude chat, não no Cowork. Seu único trabalho nesta conversa é me entrevistar brevemente, projetar a arquitetura comigo e produzir um arquivo de PRD (Documento de Requisitos do Produto) pronto para construção. Eu levarei esse PRD para o Cowork separadamente para fazer a construção real — portanto, o PRD deve ser totalmente autossuficiente e dizer ao Cowork tudo o que ele precisa, porque o Cowork será uma tela em branco quando o ler pela primeira vez.

Este é um entregável padronizado. Existe uma estrutura fixa e um conjunto fixo de convenções (veja Convenções Fixas abaixo) que cada versão deste PRD segue. As únicas coisas que mudam de uma pessoa para outra são quais domínios o sistema cobre e quantas horas a construção leva — e a própria duração da construção determina quantos domínios cabem. Não improvise na estrutura. Seja rigoroso, concreto e estrito.

---

## Fase 0 — Oriente-se (faça isso primeiro)

Antes de me perguntar qualquer coisa:

Revise tudo o que você já sabe sobre mim — a partir da memória e de conversas anteriores (pesquise-as se puder). Meu trabalho, ferramentas, projetos ativos, objetivos, restrições, como trabalho, meu fuso horário.

Não pergunte o que você já pode responder. Preencha previamente todas as respostas que puder inferir.

Em seguida, faça um resumo rápido de "Aqui está o que já sei sobre você" — 5 a 7 tópicos curtos — para que eu possa corrigir qualquer erro.

Se você tiver pouco contexto prévio sobre mim, diga isso — a entrevista apenas será mais longa.

---

## Fase 1 — Proponha, não interrogue

Faça com que isso exija o menor esforço possível da minha parte. Opte por propor em vez de perguntar por padrão. Dê um passo curto de cada vez.

### Passo 1 — Sugira os projetos
Com base no que você sabe sobre mim, proponha de 4 a 6 domínios candidatos que este sistema poderia cobrir, cada um com uma descrição de uma linha sobre o que ele faria por mim e por que se adequa. Apresente-os como uma lista de seleção. Eu escolho os que quero e posso adicionar um. Não pergunte "o que você quer construir" de forma aberta.

### Passo 2 — Confirme o ambiente de construção
Indique seu melhor palpite, em um bloco curto, para: meu nível técnico (no-code / script leve / desenvolvedor) e quais conectores eu tenho (Gmail, Calendar, Drive, Slack, Notion, etc.). Formule como "aqui está o que eu acho — corrija qualquer coisa". Assume-se que a plataforma de construção é o Claude Cowork.

### Passo 3 — Obtenha o tempo de construção e concilie o escopo
Pergunte a única coisa que você não consegue adivinhar — quantas horas para a primeira construção — como uma escolha de um clique (ex: 3 / 5 / 8 horas). Em seguida, aplique imediatamente a regra de Escopo nas Convenções Fixas: diga-me quais dos domínios escolhidos serão totalmente construídos nesse orçamento e quais se tornarão pastas de marcadores de posição (placeholders) para mais tarde. Deixe-me ajustar.

### Passo 4 — Preencha as lacunas reais
Qualquer coisa que ainda seja genuinamente desconhecida (fuso horário, quando as tarefas agendadas são executadas, algo que nunca deve ser automatizado) — proponha um padrão sensato e deixe-me confirmar. Uma pergunta curta de cada vez, apenas se não puder inferir.

Mantenha minha entrada total limitada a poucas escolhas e confirmações. No momento em que tiver o suficiente, siga em frente.

---

## Convenções Fixas — siga-as exatamente, não desvie

Tudo nesta seção é fixo e idêntico em todas as PRDs que este metaprompt produz. As únicas variáveis são os domínios e o tempo de construção. Não redesenhe isso, não invente alternativas, não reinvente o que o plugin Productivity (Produtividade) já fornece.

### Fundação — o plugin Productivity
Toda construção se baseia no plugin Productivity do Cowork. Ele é instalado via Cowork → Customizar → Plugins → "Productivity" (ou "Produtividade"), e inicializado uma vez executando `/start`. O `/start` cria, na raiz do projeto: `CLAUDE.md` (memória de trabalho transversal), `TASKS.md` (lista de tarefas), `memory/` (diretório de memória profunda) e `dashboard.html`. O plugin também fornece `/update` (descoberta de itens de ação) e um fluxo de trabalho de criação de habilidades (create-skill). O PRD deve ser construído sobre estes — nunca crie manualmente um arquivo de memória separado, lista de tarefas ou sistema de configuração.

### Sequência de configuração (Setup)
Bloco 0 de cada construção, antes de qualquer trabalho na camada de dados. Esta é a primeira vez que o Cowork roda; assuma que nada está no lugar. O Cowork verifica e me orienta, em ordem:

1. O projeto do Cowork é criado e apontado para uma pasta local (ex: `~/cowork/`).
2. O plugin Productivity é instalado (Cowork → Customizar → Plugins → "Productivity").
3. O comando `/start` foi executado, de modo que os arquivos raiz do plugin (`CLAUDE.md`, `TASKS.md`, `memory/`, `dashboard.html`) existem.
4. Os conectores que esta construção precisa estão ativados. Somente após a confirmação dos quatro itens é que a camada de dados (Bloco 1) começa. Habilidades personalizadas em `toolbox/` são construídas durante os blocos — elas não são um pré-requisito de configuração.

### Esqueleto da pasta raiz — sempre neste formato:

```
~/cowork/                    ← Raiz do projeto Cowork (pasta LOCAL)
├── CLAUDE.md                ← plugin: memória de trabalho transversal
├── TASKS.md                 ← plugin: lista de tarefas
├── memory/                  ← plugin: memória profunda, organizada por domínio
│   ├── people.md
│   ├── terminology.md
│   └── {domain}/            ← uma subpasta por domínio
├── dashboard.html           ← painel (dashboard) do plugin
├── PRD-{system-name}.md     ← este PRD, colocado na raiz para referência
├── toolbox/                 ← habilidades personalizadas instaláveis (fonte da verdade)
├── briefs/                  ← saídas do briefing matinal + arquivo/
└── {domain}/                ← uma pasta por domínio (padrão abaixo)
```

A única parte variável é quais pastas `{domain}/` existem. (Adicione uma zona de descarte `builds/` de nível superior apenas se o padrão do construtor autônomo estiver no escopo.)

### Padrão de pasta por domínio — cada domínio é idêntico em formato:

```
{domain}/
├── CLAUDE.md     ← voz/função no nível da pasta para este domínio
├── inputs/       ← arquivos mantidos por humanos (nunca sobrescritos automaticamente)
├── data/         ← arquivos derivados atualizados por máquina
└── outputs/      ← artefatos gerados (briefings, painéis, documentos)
```

### Arquitetura de memória — três níveis fixos:
* **`CLAUDE.md` Raiz:** memória de trabalho transversal: pessoas, terminologia, abreviações.
* **`memory/{domain}/`:** conhecimento profundo por domínio.
* **`{domain}/CLAUDE.md`:** função e tom ao trabalhar dentro desse domínio.

### Convenções de nomenclatura
Fixas: pastas em `kebab-case`; arquivos de memória `substantivo.md`; arquivos de dados `substantivo.json`; arquivos com data `nome-AAAA-MM-DD.md`.

### Padrões de interação
O sistema sempre expõe estes: painel (visual sempre ativo), resumo/briefing (brief/digest - envio agendado), habilidade (skill - comando sob demanda) e — somente se o tempo de construção permitir — construtor autônomo (autonomous builder - solte um briefing, obtenha um produto de trabalho finalizado).

---

## Fase 2 — Esboce a arquitetura (obtenha minha aprovação antes do PRD)

Antes de escrever o PRD completo, mostre-me um esboço de arquitetura de uma página, construído estritamente sob as Convenções Fixas: os domínios, a árvore de pastas, os fluxos de trabalho por domínio mapeados para padrões de interação e o plano de construção resumido (configuração do Bloco 0 + os blocos de horas). Deixe-me reagir e ajustar. Em seguida, prossiga.

---

## Fase 3 — Produza o PRD

Escreva um PRD completo e pronto para construção como um arquivo markdown para download. Dois públicos: eu (para ler e aprovar) e o Cowork (to execute). Ele segue as Convenções Fixas exatamente e usa a estrutura de seções abaixo — as mesmas seções, na mesma ordem, todas as vezes.

### Calibração — quanto detalhe
Busque a profundidade de um documento de desenvolvimento de engenharia real: concreto o suficiente para construir a partir dele com zero decisões de design adicionais, não um manual extenso.

* A árvore de pastas é escrita na íntegra, cada pasta com um comentário de uma linha sobre seu propósito.
* Cada arquivo de dados possui seu esquema real como um bloco de código — nomes de campos reais, valores de exemplo realistas. Nunca "esquema a definir (TBD)".
* Cada fluxo de trabalho agendado e habilidade tem um prompt completo e pronto para copiar e colar — específico o suficiente para ser executado como está, nomeando os arquivos exatos que ele lê e escreve.
* O plano de construção e o registro de decisões são tabelas. O registro de decisões tem uma linha para cada escolha não óbvia neste projeto (~8 a 15 linhas; sem histórico de registro de alterações inventado).

O detalhamento vem de ser concreto, não de textos longos. Dimensione o documento para o escopo — uma construção de domínio único de 3 horas é um PRD muito mais curto do que uma construção de três domínios de 8 horas.

---

## Seções obrigatórias do PRD — esta estrutura exata, sempre

### 1. Executive summary (Resumo executivo)
O que o sistema é, os domínios, os padrões de interação, por que ele se ajusta ao tempo de construção declarado e como ele escala posteriormente.

### 2. Quick start (Início rápido) — movendo isso para o Cowork
Este PRD é produzido no Claude chat; esta seção é a transferência para o Cowork, onde a construção realmente acontece. Deve conter:
* **Entrando no Cowork (eu faço isso):** abra o Claude Cowork, crie um projeto apontado para uma pasta local (ex: `~/cowork/`) e carregue este PRD nele — solte o arquivo na pasta do projeto ou cole seu conteúdo na primeira mensagem do Cowork. Esta é a primeira vez que o Cowork está envolvido; nada está configurado ainda.
* **Instruções do projeto (Project instructions):** o texto exato para colar no campo de instruções personalizadas do projeto no Cowork (custom instructions), como um bloco de copiar e colar (especifica os domínios, o local da camada de dados local, a regra de que os dados em `inputs/` nunca são sobrescritos, a regra de execução bloco a bloco "Iniciar Bloco N", o fuso horário).
* **Como executar a construção (How to run the build):** instruções para o Cowork: quando eu disser para começar, assuma que nada está configurado ainda. PRIMEIRO execute o Bloco 0 (Configuração) da seção §7 — verifique se o plugin Productivity está instalado e me guie na instalação caso contrário, faça-me executar `/start`, verifique se os conectores necessários estão ativados e nomeie os que eu devo ativar. Somente após a confirmação da configuração, construa o plano um bloco de cada vez, em ordem; após cada bloco, relate o que foi feito e o resultado da verificação de conclusão, então aguarde meu sinal verde.
* **A primeira coisa que digo (The first thing I say):** a frase literal que digito no Cowork para começar (ex: "Start building — begin with Block 0").

### 3. Goals and non-goals (Objetivos e não-objetivos)
Explícito. Nomeie o que deliberadamente não está nesta janela de construção e o porquê.

### 4. Architecture overview (Visão geral da arquitetura)
As três camadas (pastas locais → projeto do Cowork → fluxos de trabalho); os padrões de interação e quais fluxos usam cada um; a arquitetura de memória em três níveis; principais decisões arquitetônicas e a tensão por trás de cada uma. Tudo de acordo com as Convenções Fixas.

### 5. The data layer (A camada de dados)
A fundação. É construída sobre os arquivos raiz do plugin Productivity e segue exatamente o esqueleto raiz fixo e o padrão por domínio — não invente uma estrutura diferente. Especifique:
* **Onde ela vive:** local. Arquivos simples em uma pasta local que o projeto do Cowork aponta (ex: `~/cowork/`). Não em um conector. Os conectores (Drive, Gmail, Calendar, Notion) são fontes de dados das quais os fluxos de trabalho puxam ou empurram — nunca de armazenamento. (Para fins de backup, a pasta local pode ficar dentro de um diretório sincronizado, mas o Cowork ainda lê/escreve arquivos locais.)
* **A árvore de pastas:** a árvore local completa, instanciando o esqueleto fixo com meus domínios reais; comentário de propósito de uma linha por pasta.
* **Entradas vs. dados:** A pasta `inputs/` é mantida por humanos; `data/` é atualizada por máquinas. Uma tarefa de atualização nunca escreve em `inputs/`.
* **Arquivos de memória:** o que vai em `memory/people.md`, `memory/terminology.md` e em cada arquivo `memory/{domain}/`.
* **Cada arquivo de dados recebe um esquema explícito:** formato JSON/CSV real, nomes de campos reais, valores de exemplo.
* **Estratégia de atualização:** para cada arquivo em `data/`: o que o preenche, com que frequência, sobrescrita vs. apenas anexar (append-only), lógica de desduplicação.
* A nomenclatura segue as convenções fixas (memória `.md`, dados `.json`).

### 6. Component specifications (Especificações de componentes)
Para cada fluxo de trabalho (pipeline de dados, painel, resumo/briefing, habilidade, construtor): propósito, o que lê, o que escreve, cronograma, estrutura de saída. As interfaces leem apenas da camada de dados descrita na seção §5.

### 7. The build plan (O plano de construção)
Limitado no tempo, dimensionado para o meu tempo de construção, executável. Regras:
* Abre com o **Bloco 0 — Configuração**. Esta é a primeira vez que o Cowork roda, então assuma que nada está no lugar. O Cowork verifica e me orienta, em ordem: (1) confirmar se o plugin Productivity está instalado — se não, me dar os passos exatos (Cowork → Customizar → Plugins → "Productivity") e aguardar; (2) fazer-me executar `/start` e confirmar se os arquivos raiz do plugin agora existem; (3) confirmar se os conectores que esta construção precisa estão ativados, nomeando quais devo ativar. O Cowork prossegue para o Bloco 1 somente após a confirmação da configuração. Rápido (~15–30 min), a maioria sendo minhas ações com o Cowork verificando.
* O **Bloco 1 é sempre a camada de dados** — cria a árvore de pastas completa, os arquivos de entrada (com dados iniciais/seed) e os fluxos de trabalho de atualização de dados.
* Em seguida, a primeira interface, depois mais interfaces e, por fim, o polimento — nessa ordem.
* **Colunas da tabela:** Bloco | O que é construído | Quem executa | Saída | Concluído quando… — "Quem executa" é o Cowork ou Eu (qualquer coisa que precise de terminal/CLI/cron/git; se eu for no-code, todas as linhas de construção devem ser do Cowork).
* Os Blocos 1…N têm aproximadamente o tamanho de uma hora; N é igual ao tempo de construção declarado em horas.
* **Ordem de corte:** lista ordenada do que descartar primeiro se eu estiver atrasado.
* **Nunca cortar:** o núcleo mínimo viável (sempre inclui a configuração do Bloco 0, a camada de dados e o briefing matinal).

### 8. Setup details and copy-paste prompts (Detalhes de configuração e prompts para copiar e colar)
O passo exato de criação de pastas e um prompt completo e pronto para copiar e colar para cada fluxo de trabalho e habilidade no plano de construção, cada um nomeando os arquivos da camada de dados que lê e escreve, cada um com uma proteção CRÍTICA: "nunca escrever em `inputs/`", onde relevante.

### 9. Decision log (Registro de decisões)
Uma tabela: cada escolha não óbvia e seu raciocínio / compensação (trade-off).

### 10. Out of scope / future work (Fora do escopo / trabalhos futuros)
O que vem depois (incluindo quaisquer domínios adiados pela Regra de Escopo, como pastas de marcação de posição), como a arquitetura escala sem reestruturação (novo domínio = nova pasta + fluxos de trabalho) e o que forçaria uma rearquitetura.

---

## Princípios — mantenha estes ao longo de todo o processo

* **Proponha, não interrogue:** Personalize a partir da memória; pergunte apenas o que você genuinamente não conseguir inferir. Mantenha minha entrada mínima.
* **Estrutura estrita:** Siga as Convenções Fixas e a estrutura §1–§10 exatamente. As únicas coisas que variam são os domínios e a duração da construção. Não improvise.
* **Concreto em vez de abstrato:** Nomes de pastas reais, esquemas reais, prompts reais. Sem marcadores de posição onde uma resposta específica for possível.
* **Pronto para construção no Cowork:** Eu devo ser capaz de colar o PRD em um projeto do Cowork, dizer a palavra de início e tê-lo construído bloco a bloco. Nenhum passo pode precisar de uma ferramenta que o ambiente não possua, a menos que esteja marcado como meu.
* **A camada de dados é local:** Arquivos simples em uma pasta local; conectores são fontes, nunca armazenamento; a construção nunca cria pastas no Google Drive.
* **Use o plugin Productivity:** Nunca reinvente a memória, tarefas ou configurações que o plugin já fornece.
* **Sinale suposições:** Declare-as para que eu possa corrigi-las.
* **Escala sem reestruturação:** Projete para mais domínios do que eu mencionar hoje.
* **Comece agora com a Fase 0.**
