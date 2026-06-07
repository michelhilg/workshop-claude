import { useState, useEffect } from 'react'
import type { AggregatedMetrics, AnalysisManifest } from '../types/crm'

interface DataState {
  metrics: AggregatedMetrics | null
  manifest: AnalysisManifest | null
  loading: boolean
  error: string | null
}

export function useData(): DataState {
  const [state, setState] = useState<DataState>({
    metrics: null,
    manifest: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    Promise.all([
      fetch('/data/aggregated_metrics.json').then((r) => r.json()),
      fetch('/data/analysis_manifest.json').then((r) => r.json()),
    ])
      .then(([metrics, manifest]) => {
        setState({ metrics, manifest, loading: false, error: null })
      })
      .catch((e: Error) => {
        setState((s) => ({ ...s, loading: false, error: e.message }))
      })
  }, [])

  return state
}

export function fmtBRL(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(value)
}

export function fmtNum(value: number): string {
  return new Intl.NumberFormat('pt-BR').format(value)
}

export function fmtPct(value: number): string {
  return value.toFixed(1) + '%'
}
