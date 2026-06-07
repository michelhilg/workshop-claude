export interface FunnelStage {
  contagem: number
  percentual_total: number
  valor_total: number
  score_medio: number
  ordem: number | null
  categoria: string | null
  prob_fechamento: number | null
}

export interface ConversionRate {
  de: string
  para: string
  count_de: number
  count_para: number
  taxa_conversao: number | null
}

export interface DealAnalysis {
  total: number
  por_canal: Record<string, number>
  por_segmento: Record<string, number>
  por_vendedor: Record<string, number>
  por_objecao: Record<string, number>
}

export interface AggregatedMetrics {
  _computed_at: string
  total_leads: number
  funnel_summary: Record<string, FunnelStage>
  conversion_rates: Record<string, ConversionRate>
  monthly_volume: Record<string, number>
  lost_analysis: DealAnalysis
  won_analysis: DealAnalysis
  score_distribution: Record<string, number>
  sentiment_by_stage: Record<string, Record<string, number>>
  objecoes_by_stage: Record<string, Record<string, number>>
}

export interface NormalizationStats {
  canal_normalizado: number
  canal_nao_mapeado: number
  etapa_normalizada: number
  etapa_nao_mapeada: number
  pct_canal_ok: number
  pct_etapa_ok: number
}

export interface QualityStats {
  sem_responsavel: number
  sem_campanha: number
  com_inconsistencias: number
  pct_inconsistencias: number
}

export interface AnalysisManifest {
  analysed_at: string
  status: string
  record_counts: {
    leads_total: number
    leads_com_interacoes: number
    leads_sem_interacoes: number
    campaigns_indexadas: number
    interacoes_indexadas: number
    pipeline_etapas: number
  }
  normalization_stats: NormalizationStats
  quality_stats: QualityStats
}
