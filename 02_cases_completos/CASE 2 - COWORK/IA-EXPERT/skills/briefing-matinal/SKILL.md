# Skill: briefing-matinal

**Gatilho:** agendado, diário, 04h00 America/Sao_Paulo (teste; produção: 07h00).

## O que fazer

1. **LER** `tendencias/inputs/temas.md` — lista de temas. NUNCA escrever neste arquivo.
2. **LER** `memory/tendencias/criterios.md`, `memory/tendencias/fontes.md` e `memory/tendencias/glossario-ia.md` para calibrar a busca.
3. Para **CADA tema** da lista, fazer web search nativo focado nos últimos 7 dias no nicho de Inteligência Artificial. Priorizar lançamentos, mudanças de preço, features novas e debates em alta. Ignorar rumor não confirmado.
4. **Classificar** cada achado com: categoria, resumo, por_que_importa, calor (alto/médio/baixo), fonte_titulo, fonte_url, publicado_em.
5. **Dedupe** por `fonte_url` dentro deste run.
6. **ESCREVER** `tendencias/data/tendencias-AAAA-MM-DD.json` (data de hoje, fuso America/Sao_Paulo). Sobrescrever se já existir arquivo do dia.
7. **ESCREVER** `tendencias/data/ultima-pesquisa.json` — cópia idêntica do snapshot de hoje.
8. **GERAR** `tendencias/outputs/dashboard-tendencias.html` — HTML standalone com dados embutidos (sem fetch em runtime). Identidade IA Sem Frescura: fundo creme `#F5F0E8`, verde `#0E3A2F`, coral `#E8865A`; fontes Hanken Grotesk + JetBrains Mono via Google Fonts CDN. Cabeçalho: nicho + data/hora da última pesquisa. Grid de cards por item com selo de calor. Faixa final com temas_sem_movimento.
9. **ESCREVER** `briefs/briefing-AAAA-MM-DD.md` — resumo de 5 a 8 bullets apenas com itens de `calor: alto`. Formato:
   ```
   # Tendências de IA — briefing matinal · AAAA-MM-DD
   - **[Título]** — [por_que_importa] ([fonte_titulo])
   ```
10. Listar em `temas_sem_movimento` os temas sem achado neste run.

## ⚠️ Regras críticas
- Escreve SOMENTE em `tendencias/data/`, `tendencias/outputs/` e `briefs/`.
- NUNCA escrever em `tendencias/inputs/`.
