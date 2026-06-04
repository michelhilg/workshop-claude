# Roteiro de Workshop — Do PRD ao Build em Cowork (30 min)

> **Caso usado como exemplo vivo:** `painel-tendencias` — um agente que pesquisa o que está em alta em IA, cruza com a lista de temas do Michel, e monta um dashboard sozinho.
> **Público:** iniciante não-técnico (não precisa saber programar).
> **O que o aluno sai sabendo fazer:** o método replicável para sair de uma ideia solta e chegar a um sistema funcionando dentro do Cowork — sem escrever código.
> **Formato:** roteiro em tópicos por bloco de tempo + passo a passo de replicação no final.

---

## A ideia central do workshop (decore isto)

> **"Você não construiu um sistema digitando comando por comando. Você escreveu um plano em português, deu para o Cowork, e ele construiu para você. O segredo não é a ferramenta — é o método de planejar antes de mandar fazer."**

Tudo no roteiro serve para provar essa frase. O `painel-tendencias` é a prova.

---

## Mapa de tempo (30 min)

| Bloco | Tempo | Minutos | O que acontece |
|---|---|---|---|
| 0 | Abertura | 0–3 | Mostra o resultado pronto antes de explicar nada |
| 1 | A ideia | 3–7 | O problema e a ideia em 1 frase |
| 2 | A camada invisível | 7–13 | Contrato + instruções: por que o agente se comporta |
| 3 | O PRD | 13–20 | O coração do método: planejar antes de construir |
| 4 | A construção em blocos | 20–26 | Como o sistema nasceu, pedaço por pedaço |
| 5 | Como replicar / escalar | 26–29 | O aluno aplica no nicho dele |
| 6 | Encerramento + CTA | 29–30 | Chamada para ação |

> Regra de palco: se atrasar, **corte o Bloco 5** (vira fala rápida) e proteja Blocos 3 e 4 — são o núcleo do método.

---

## BLOCO 0 — Abertura: mostre o resultado primeiro (0–3 min)

**Objetivo:** criar o "uau" antes de qualquer teoria. Ninguém liga para o processo até ver que o resultado vale a pena.

Tópicos para cobrir:

- Abrir o `dashboard-tendencias.html` na tela. Deixar a plateia olhar 5 segundos em silêncio.
- Dizer a frase âncora: *"Esse painel se montou sozinho. Eu não desenhei nenhum card. Eu não pesquisei nenhuma notícia. Eu escrevi um plano e o Cowork fez o resto."*
- Mostrar o `briefing-2026-06-03.md` (o resumo que "chegou" de manhã). *"E todo dia 7h da manhã isso atualiza antes de eu acordar."*
- Prometer o que eles vão aprender: *"Em 30 minutos você vai entender exatamente como sair de uma ideia na cabeça até isso aqui rodando — sem escrever uma linha de código."*

Fala de abertura sugerida (não-técnico):
> "Levanta a mão quem já teve uma ideia de automação e travou porque 'não sei programar'. Guarda essa mão na cabeça. No fim dos 30 minutos você vai ver que o problema nunca foi código — era método."

---

## BLOCO 1 — A ideia e o problema (3–7 min)

**Objetivo:** mostrar que todo projeto começa com um problema chato e uma ideia simples — não com tecnologia.

Tópicos para cobrir:

- **O problema real do Michel:** todo dia preciso saber o que está acontecendo em IA pra criar conteúdo. Isso some o tempo: abrir 10 sites, filtrar o que importa, decidir o que vale postar.
- **A ideia em 1 frase:** *"Um assistente que pesquisa o que está em alta em IA, compara com a MINHA lista de temas, e me entrega um painel pronto — com um comando só."*
- **A regra de ouro do método:** a ideia tem que caber em uma frase. Se você não consegue dizer em uma frase o que o sistema faz, ainda não está pronto pra construir.
- **O que define o escopo:** um nicho só (IA), uma fonte de busca (web), uma entrega (o painel). *"Comecei pequeno de propósito. Dá pra crescer depois."*

Analogia para não-técnico:
> "Pensa num estagiário novo. Antes de pedir qualquer coisa, você precisa explicar três coisas: quem você é, o que você quer, e como gosta que seja feito. Com o Cowork é igual. A diferença é que você explica uma vez, por escrito, e ele nunca esquece."

---

## BLOCO 2 — A camada invisível: contrato + instruções (7–13 min)

**Objetivo:** este é o pulo do gato que ninguém mostra. Antes de pedir qualquer tarefa, você configura *como* o assistente trabalha. É isso que separa um resultado genérico de um resultado que parece feito por você.

Tópicos para cobrir — as **três camadas de configuração** (do geral ao específico):

1. **O contrato geral (instruções globais).** Vale para tudo que o Cowork faz para você.
   - Quem eu sou (Michel, IA Sem Frescura, público brasileiro).
   - Como quero que ele trabalhe: *direto, sem puxar saco, discorda quando eu erro, planeja antes de construir, nunca apaga nada sem avisar.*
   - Frase para a plateia: *"Eu não quero um assistente que concorda com tudo. Eu escrevi no contrato: 'discorde de mim quando eu estiver errado'. Isso muda completamente a qualidade do que volta."*

2. **As instruções do projeto.** Valem só para este projeto (o painel de tendências).
   - O que é o sistema, onde ficam os arquivos, quais as regras específicas (ex: *"nunca sobrescreva a minha lista de temas"*).
   - Frase: *"Aqui eu digo o que é sagrado. Tem uma pasta que é MINHA — o robô lê, mas nunca escreve. Isso está escrito na regra, então ele respeita."*

3. **A voz por pasta (memória de domínio).** Quando ele trabalha dentro de tendências, ele assume um tom específico.
   - Tom direto, foco em "o que isso muda pra quem cria conteúdo de IA", sem hype vazio.
   - Os arquivos de memória: critérios (o que conta como tendência relevante), fontes (onde olhar), glossário (pra ele não se perder nos termos).

Ponto-chave para fixar:
> "Repara: até aqui eu não pedi NENHUMA tarefa. Eu só configurei o comportamento. 80% da qualidade vem dessa camada invisível. A maioria das pessoas pula isso e depois reclama que 'a IA é genérica'."

Analogia:
> "É a diferença entre contratar alguém e dar um manual da empresa, versus jogar a pessoa na mesa e dizer 'se vira'. Mesmo profissional, resultado completamente diferente."

---

## BLOCO 3 — O PRD: o coração do método (13–20 min)

**Objetivo:** mostrar que o documento de planejamento (o PRD) é o que faz tudo funcionar. É o passo que parece chato e que todo mundo quer pular — e é exatamente o que separa quem constrói de quem só conversa com a IA.

Tópicos para cobrir:

- **O que é um PRD, em português:** um documento curto que descreve *o que* você vai construir, *por quê*, e *como*, ANTES de construir. PRD = "documento de requisitos do produto", mas pense nele como **o briefing que você daria pro melhor freelancer do mundo.**
- **Por que escrever isso primeiro:** *"Se o plano está claro no papel, a construção vira execução. Se o plano está confuso na cabeça, a construção vira retrabalho infinito."*
- **As seções que todo PRD precisa ter** (mostrar na tela o `PRD-painel-tendencias.md` rolando):
  - **Problema** — o que está faltando ou quebrado.
  - **Critérios de sucesso** — como vou saber que funcionou.
  - **Escopo** — o que está dentro E, principalmente, o que está FORA.
  - **Restrições** — tempo, custo, o que não pode quebrar.
  - **Plano** — os passos em ordem.
  - **Decisões** — as escolhas que fiz e por quê.
- **O detalhe que ensina mais:** a lista de "o que está FORA". *"Olha aqui: eu escrevi explicitamente o que eu NÃO ia construir — scraping profundo, multi-nicho, publicação automática. Dizer 'não' é o que faz um projeto caber em 3 horas em vez de virar um monstro de 3 meses."*
- **O registro de decisões:** cada escolha tem um porquê escrito. Ex: *"usei busca simples da web em vez de uma ferramenta de scraping — porque numa demo ao vivo, menos login = menos coisa pra dar errado."* Frase: *"Daqui a um mês eu não vou lembrar por que escolhi isso. O PRD lembra por mim."*

Ponto-chave para fixar:
> "O PRD não é burocracia. É a diferença entre dizer 'me faz um painel de tendências' e receber qualquer coisa, versus entregar um plano de 2 páginas e receber exatamente o que você imaginou. A IA é boa executando. Você tem que ser bom planejando."

Como o aluno gera o PRD sem saber escrever um:
> "E o melhor: você não precisa escrever o PRD sozinho. Você conversa com a IA, descreve a ideia, e PEDE pra ela montar o PRD com você. Ela te entrevista, aponta os buracos do seu plano, e cospe o documento. Você revisa e aprova."

---

## BLOCO 4 — A construção em blocos (20–26 min)

**Objetivo:** mostrar que, com o PRD pronto, a construção foi feita em pedaços pequenos e verificáveis — não tudo de uma vez. Isso é o que torna o processo confiável.

Tópicos para cobrir — os **4 blocos da construção** (mostrar como cada um virou parte do sistema):

- **Bloco 0 — Preparar o terreno.** Instalar o necessário, confirmar que as pastas existem, conectar o Google Drive (de onde vem a lista de temas). *"Nada de tarefa ainda. Só garantir que a base existe."*
- **Bloco 1 — A camada de dados.** Criar a estrutura de pastas: a lista de temas (input do humano), a pasta de dados (a máquina escreve), a pasta de saída (o painel). Frase: *"Separei o que é MEU do que é da máquina. Minha lista de temas fica numa pasta que a automação tem proibição de tocar."*
- **Bloco 2 — A habilidade + o painel.** Aqui nasce a `skill pesquisar-tendencias`: ela lê minha lista, pesquisa cada tema na web, classifica por "calor" (alto/médio/baixo), e gera o dashboard. *"Esse é o momento 'uau'. Um comando — 'pesquisar tendências' — e ele faz tudo isso sozinho."*
- **Bloco 3 — O agendamento.** A MESMA lógica, mas disparada por um relógio em vez de um comando. Todo dia de manhã ele roda e deixa o briefing pronto. *"Construí a lógica uma vez. O comando manual e o alarme das 7h chamam a mesma coisa."*

O princípio técnico explicado sem jargão:
> "Por que isso é esperto? Eu não construí a pesquisa duas vezes — uma pro botão e outra pro alarme. Construí UMA vez, e os dois gatilhos apontam pra ela. Menos coisa pra manter, menos coisa pra quebrar."

A regra de segurança que vale ouro:
> "Repara que em todo passo tem uma regra repetida: 'escreve só na pasta de dados, nunca na minha lista'. Quando você dá poder de escrever arquivos pra um robô, a regra mais importante é dizer onde ele NÃO pode mexer. Isso protege seu trabalho."

Demonstração ao vivo (se houver tempo e conexão):
> Rodar o comando `pesquisar tendências` ao vivo e narrar enquanto ele trabalha. **Tenha o Plano B pronto** (ver checklist) caso a internet ou a busca falhem no palco.

---

## BLOCO 5 — Como replicar e escalar (26–29 min)

**Objetivo:** virar a chave de "que legal o projeto do Michel" para "eu consigo fazer isso pro meu negócio hoje".

Tópicos para cobrir:

- **Trocar de nicho é trocar um arquivo.** *"Esse sistema é de IA. Mas se você é de marketing imobiliário, nutrição, jurídico — você só troca a lista de temas. Toda a máquina continua igual."*
- **O método é o produto, não o painel.** Ideia em 1 frase → configurar comportamento → escrever o PRD → construir em blocos → verificar cada bloco. *"Isso funciona pra QUALQUER automação, não só painel de tendências."*
- **Comece pequeno.** Um nicho, uma fonte, uma entrega. Crescer é adicionar pastas seguindo o mesmo padrão — não recomeçar do zero.

Frase de virada:
> "O que você viu hoje não foi um curso de programação. Foi um curso de como pensar antes de pedir. A ferramenta faz o trabalho braçal. Você faz o trabalho de cabeça."

---

## BLOCO 6 — Encerramento + CTA (29–30 min)

Tópicos para cobrir:

- Recapitular o método em 5 palavras: **Ideia → Contrato → PRD → Blocos → Verificar.**
- Reforçar a frase âncora da abertura: *"Não foi a ferramenta. Foi o método."*
- CTA (adaptar ao seu funil): convite pro próximo workshop / mentoria / material complementar.
- Última frase: *"Sua próxima ideia de automação não precisa de um programador. Precisa de um plano. Agora você tem o método pra escrever ele."*

---

# PASSO A PASSO — Como o aluno replica (entregar como guia)

> Use isto como o "leve para casa". É a receita que o aluno segue depois do workshop para construir o próprio sistema, sem código.

### Passo 1 — Escreva sua ideia em uma frase
Complete a frase: *"Eu quero um assistente que [faz o quê] usando [qual fonte] e me entrega [qual resultado]."*
Se não couber em uma frase, simplifique até caber.

### Passo 2 — Configure o comportamento (a camada invisível)
Antes de pedir qualquer tarefa, escreva:
- **Quem você é** e quem é seu público.
- **Como quer que a IA trabalhe** (ex: direta, que discorde quando você erra, que planeje antes de construir, que nunca apague nada sem avisar).
- **As regras do projeto** (ex: "esta pasta é minha, nunca escreva nela").

### Passo 3 — Gere o PRD conversando com a IA
Peça: *"Me entreviste sobre essa ideia e monte um PRD com problema, critérios de sucesso, escopo (dentro e fora), restrições, plano em passos e registro de decisões."*
Responda as perguntas dela. Revise. **Aprove só quando estiver claro.**

### Passo 4 — Defina o que está FORA
Liste explicitamente o que você NÃO vai construir agora. Isso é o que mantém o projeto pequeno e possível.

### Passo 5 — Construa em blocos pequenos
Quebre em 3–4 blocos. Peça para a IA executar **um bloco por vez** e reportar o resultado antes de seguir. Nunca peça tudo de uma vez.

### Passo 6 — Verifique cada bloco antes de avançar
Depois de cada bloco, confira: o resultado existe? Funciona? Só então libere o próximo. *"Pode seguir."*

### Passo 7 — Proteja o que é seu e tenha um Plano B
- Diga onde a automação **não** pode escrever.
- Guarde uma cópia funcional do resultado final, caso algo falhe na hora de mostrar.

### Passo 8 — Para escalar: troque o input, não o sistema
Novo nicho = nova lista de temas. Novo tipo de tarefa = nova pasta seguindo o mesmo padrão. Você nunca recomeça do zero.

---

# Apêndice A — Glossário sem jargão (cola de palco)

Tradução dos termos técnicos para a linguagem da plateia. Use só se alguém perguntar.

- **PRD** → o briefing/plano que você escreve antes de construir.
- **Skill (habilidade)** → uma tarefa que você ensina uma vez e dispara com um comando.
- **Agendamento (cron)** → um alarme que dispara a tarefa sozinho num horário fixo.
- **Dashboard** → o painel visual com o resultado, que abre no navegador.
- **Memória** → arquivos onde a IA guarda o que ela precisa lembrar entre conversas.
- **Input** → o que VOCÊ controla e mantém (sua lista de temas).
- **MCP / conector** → a ponte que liga a IA a outro app (ex: o Google Drive de onde vem a lista).
- **Calor (alto/médio/baixo)** → o nível de importância de cada tendência — um selo, não um número, pra ler na hora.

---

# Apêndice B — Os 5 princípios do método (para repetir no palco)

1. **Planeje antes de construir.** O PRD primeiro, sempre. Plano confuso = retrabalho.
2. **Configure o comportamento antes da tarefa.** 80% da qualidade vem da camada invisível.
3. **Diga 'não' explicitamente.** O escopo "fora" é o que faz o projeto caber.
4. **Construa em blocos e verifique.** Um pedaço por vez, confirmado antes do próximo.
5. **Proteja o que é seu.** Diga onde a automação não pode mexer. Tenha Plano B.

---

# Apêndice C — Checklist de palco e Plano B

**Antes de subir:**
- [ ] `dashboard-tendencias.html` aberto numa aba (resultado pronto pra mostrar no Bloco 0).
- [ ] `briefing-2026-06-03.md` aberto (prova do agendamento).
- [ ] `PRD-painel-tendencias.md` aberto pra rolar no Bloco 3.
- [ ] **Plano B:** uma cópia salva de um dashboard que já funcionou — se a demo ao vivo travar, abra essa e a narrativa não quebra.
- [ ] Internet testada (a busca ao vivo depende dela).

**Se a demo ao vivo falhar:** não conserte no palco. Abra o resultado salvo (Plano B), diga *"esse é o resultado de uma execução real de mais cedo"*, e siga. A plateia veio pelo método, não pelo show técnico.

---

# Apêndice D — Perguntas que a plateia vai fazer (prepare-se)

- **"Preciso saber programar?"** → Não. Você precisa saber planejar e escrever em português claro.
- **"Quanto tempo levou pra construir?"** → O sistema todo cabe em ~3 horas de construção, dividido em blocos de ~1h.
- **"Funciona pro meu nicho?"** → Sim. Você troca a lista de temas; a máquina é a mesma.
- **"E se a IA fizer besteira nos meus arquivos?"** → Por isso a regra de proteger pastas. Você define onde ela pode e não pode escrever, e ela respeita.
- **"Quanto custa?"** → (adaptar — depende do plano do Cowork; foque que o custo de uso é baixo perto do tempo economizado.)
- **"Por que não usei uma ferramenta mais potente de scraping?"** → Decisão consciente: menos logins = menos risco numa demo ao vivo. Está no registro de decisões do PRD.

---

> **Fechamento do roteiro:** o aluno não sai com um sistema pronto. Sai com o método para construir o dele. Esse é o produto do workshop.
