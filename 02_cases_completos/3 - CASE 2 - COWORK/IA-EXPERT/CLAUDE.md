# CLAUDE.md — Raiz do projeto painel-tendencias

> Arquivo de memória de trabalho transversal. Atualizado conforme decisões são tomadas.

## Sobre o projeto
Sistema `painel-tendencias`: agente de domínio único que pesquisa tendências de IA, cruza com lista de temas mantida por Michel, e gera dashboard HTML visual.

**Pasta raiz:** `~/cowork/` (este projeto)
**Fuso horário:** America/Sao_Paulo (UTC−3)
**Domínio ativo:** Inteligência Artificial

## Pessoas
- **Michel Hilgemberg** — dono do projeto. Fundador do IA Sem Frescura (@michelhilg). Opera o sistema e mantém manualmente `tendencias/inputs/temas.md`.

## Terminologia / abreviações
- **CSF** = Claude Sem Frescura (nome anterior; projeto renomeado para IA Sem Frescura)
- **calor** = classificação de relevância de uma tendência: `alto` / `médio` / `baixo`
- **inputs/** = pastas mantidas por humano — NUNCA sobrescrever via automação
- **pesquisar tendências** = comando que dispara a skill `pesquisar-tendencias`

## Regras de operação críticas
1. Arquivos em `tendencias/inputs/` são mantidos por Michel. Nenhum fluxo automático escreve neles.
2. `tendencias/data/` e `tendencias/outputs/` são escritos por máquina.
3. Snapshots datados em `data/` são append-only (um arquivo por dia).
4. `ultima-pesquisa.json` é sobrescrito a cada execução.
5. Dashboard gerado com dados embutidos (sem fetch em runtime) — funciona offline.

## Decisões arquitetônicas (ver PRD-painel-tendencias.md §9 para detalhes)
- Web search nativo (não Firecrawl) pra reduzir risco de auth na demo ao vivo
- Drive (MCP) só pra leitura de `temas.md` — única fonte que faz sentido editar pelo celular
- Skill única `pesquisar-tendencias` com dois gatilhos: manual + cron 07h00

## Log de decisões desta sessão
- 2026-06-02: PRD aprovado. PRD-controle.md = PRD-painel-tendencias.md (Michel confirmou).
- 2026-06-02: Bloco 0 executado — arquivos raiz criados. Drive conectado, pendente habilitar em chat.
