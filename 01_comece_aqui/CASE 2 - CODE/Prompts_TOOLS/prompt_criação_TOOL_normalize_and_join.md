Crie um script Python chamado normalize_and_join.py dentro da pasta tools/.

 Ele lê os 4 arquivos JSON de .claude/data/dadosBrutos/ (leads_raw.json, campaigns.json, interactions.json, pipeline_config.json).
 Normalização: Aplique dois mapas de canonização. O primeiro (CANAL_MAP) converte variações de canal como "LI Ads", "linkedin", "Linkedin Ads" para "LinkedIn Ads", e assim
  por diante para ~8 canais canônicos. O segundo (ETAPA_MAP) converte variações de etapa do funil como "reunião", "call agendada", "demo marcada" para o valor canônico
 "Reunião marcada", cobrindo ~7 etapas. Qualquer valor não mapeado deve ser registrado como inconsistência.

 Índices para join: Construa três índices:
 - campaigns: mapeie campanha_id → metadados da campanha
 - interactions: agrupe por lead_id e calcule: contagem de interações, data da última interação, sentimento dominante (moda), principal objeção (moda) - pipeline: mapeie etapa_funil → ordem, categoria e probabilidade de fechamento

 Join: Para cada lead, normalize os campos de canal e etapa, e enriqueça com os dados dos três índices acima, produzindo um registro com ~40 campos.

 Métricas agregadas: Calcule e salve em aggregated_metrics.json os seguintes grupos:
 - Resumo do funil por etapa (contagem, % do total, valor total, score médio)
 - Taxas de conversão entre etapas consecutivas
 - Volume mensal (12 meses)
 - Análise de deals perdidos/ganhos por canal, segmento, vendedor e objeção
 - Distribuição de score em 4 faixas (0–24, 25–49, 50–74, 75–99)
 - Sentimento por etapa do funil
 - Principais objeções por etapa

 Outputs em .claude/data/processados/:
 - leads_clean.json — leads normalizados e enriquecidos
 - patterns.json — inconsistências encontradas (canais/etapas não mapeados, leads sem responsável, leads sem campanha)
 - aggregated_metrics.json — métricas pré-calculadas para análise LLM
 - analysis_manifest.json — contagem de leads, estatísticas de normalização, status

 Os mapas de normalização devem vir de .claude/agents/analista/config.json.