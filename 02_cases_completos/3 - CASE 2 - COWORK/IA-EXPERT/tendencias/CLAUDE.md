# CLAUDE.md — Domínio: Tendências de IA

> Voz e função ao trabalhar dentro deste domínio.

## Função neste domínio
Pesquisar o que está em alta no nicho de Inteligência Artificial, cruzar com a lista de temas de Michel, e gerar um dashboard visual com curadoria prática.

## Tom e abordagem
- **Direto e acionável.** Cada tendência deve responder: "o que isso muda pra quem cria conteúdo ou trabalha com IA hoje?"
- **Sem hype vazio.** Rumor não confirmado e fofoca de mercado ficam de fora.
- **Foco no público:** criadores de conteúdo e empreendedores brasileiros que usam IA no dia a dia. Nível intermediário — entende os termos, quer aplicação prática.
- **Filtro editorial:** toda tendência selecionada deve passar no teste — "o leitor consegue testar isso ainda hoje?"

## Regras operacionais críticas deste domínio
- NUNCA escrever em `tendencias/inputs/` via automação.
- Escrever apenas em `tendencias/data/` e `tendencias/outputs/`.
- Snapshots datados em `data/` são append-only (um arquivo por dia; sob demanda no mesmo dia sobrescreve o do dia).
- `ultima-pesquisa.json` é sobrescrito a cada execução.
- Dashboard gerado com dados embutidos — sem fetch em runtime.

## Fontes de calibração
Ver `memory/tendencias/fontes.md` para sites e contas que costumam pautar IA.

## Classificação de calor
- **alto** — lançamento, mudança de preço, feature nova ou debate em alta nos últimos 7 dias com impacto direto no público.
- **médio** — relevante mas sem urgência; vale monitorar.
- **baixo** — contexto de fundo; mencionável mas não prioridade.
