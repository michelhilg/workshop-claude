Crie um script Python chamado format_output.py dentro da pasta tools/.

 Ele lê leads_clean.json, patterns.json e insights.json de .claude/data/processed/ e gera 9 arquivos JSON em .claude/data/output/, cada um preparado para ser consumido
 diretamente pelo dashboard React.

 Os 9 arquivos e o que cada função deve gerar:

 1. pipeline_view.json — leads agrupados por etapa do funil. Para cada etapa: nome, ordem, categoria, probabilidade de fechamento, contagem de leads, valor total, score
 médio, e lista enxuta de leads (id, nome, empresa, valor, score, canal, responsável).
2. channel_performance.json — canais ordenados por volume. Para cada canal: contagem, valor total, valor médio, score médio, distribuição de etapas.
 3. seller_performance.json — por responsavel_id: contagem, valor total, score médio, distribuição de etapas.
 4. campaign_performance.json — por campanha_id: metadados da campanha + contagem, valor total, valor médio, contagem de ganhos/perdidos, win rate, ROI (valor gerado /
 investimento), distribuição de etapas.
 5. alerts.json — alertas operacionais:
   - Leads sem responsável atribuído   

   - Leads em etapas avançadas sem interação há mais de 14 dias
  - Leads parados em "Qualificado" há mais de 10 dias
  - Gargalo de funil: queda >20% de "Reunião marcada" para "Proposta enviada"
 6. data_quality_report.json — canais e etapas não mapeados, mapeamentos inconsistentes aplicados, leads sem campanha, leads sem responsável.
 7. leads_table.json — todos os leads com ~30 campos completos para a tabela do dashboard.
 8. dashboard_summary.json — visão consolidada: total de leads, valor total, score médio, leads sem dono; top 5 canais e vendedores; conversões por etapa; receita em
 risco; top 5 alertas críticos; top 3 recomendações.
 9. recommendations.json — recomendações do insights.json separadas por prioridade (alta/média). Gere também um output_manifest.json com lista dos arquivos e timestamp de geração.

▎ Parâmetros como moeda (BRL), casas decimais, thresholds de alertas devem vir de .claude/agents/padronizador/config.json.