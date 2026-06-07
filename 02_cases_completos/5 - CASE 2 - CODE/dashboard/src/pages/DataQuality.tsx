import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import KpiCard from '../components/cards/KpiCard'
import { useData, fmtNum, fmtPct } from '../hooks/useData'

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">{title}</h2>
      {children}
    </div>
  )
}

const SENTIMENT_COLORS: Record<string, string> = {
  positivo: '#22c55e',
  neutro: '#94a3b8',
  misto: '#f59e0b',
  negativo: '#ef4444',
}

export default function DataQuality() {
  const { metrics, manifest, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics || !manifest)
    return <div className="text-red-500 py-12 text-center">Erro: {error}</div>

  const { normalization_stats: ns, quality_stats: qs, record_counts: rc } = manifest

  const scoreData = Object.entries(metrics.score_distribution)
    .filter(([k]) => k !== 'sem_score')
    .map(([range, count]) => ({ range, count }))

  const normPieData = [
    { name: 'Canal OK', value: ns.canal_normalizado, color: '#22c55e' },
    { name: 'Canal não mapeado', value: ns.canal_nao_mapeado, color: '#ef4444' },
  ]
  const stagePieData = [
    { name: 'Etapa OK', value: ns.etapa_normalizada, color: '#22c55e' },
    { name: 'Etapa não mapeada', value: ns.etapa_nao_mapeada, color: '#ef4444' },
  ]

  const canonicalStages = Object.entries(metrics.sentiment_by_stage)
    .filter(([name]) => metrics.funnel_summary[name]?.ordem !== null)
    .sort(([a], [b]) => {
      const oa = metrics.funnel_summary[a]?.ordem ?? 99
      const ob = metrics.funnel_summary[b]?.ordem ?? 99
      return oa - ob
    })

  const sentimentChartData = canonicalStages.map(([name, sentiments]) => ({
    stage: name.length > 12 ? name.slice(0, 12) + '…' : name,
    ...sentiments,
  }))

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Qualidade de Dados</h1>
        <p className="text-slate-500 text-sm mt-1">
          Estatísticas de normalização e integridade do pipeline agêntico
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <KpiCard
          title="Canal Normalizado"
          value={fmtPct(ns.pct_canal_ok)}
          subtitle={`${fmtNum(ns.canal_normalizado)} de ${fmtNum(rc.leads_total)}`}
          accent="green"
        />
        <KpiCard
          title="Etapa Normalizada"
          value={fmtPct(ns.pct_etapa_ok)}
          subtitle={`${fmtNum(ns.etapa_normalizada)} de ${fmtNum(rc.leads_total)}`}
          accent={ns.pct_etapa_ok >= 70 ? 'green' : 'amber'}
        />
        <KpiCard
          title="Com Inconsistências"
          value={fmtPct(qs.pct_inconsistencias)}
          subtitle={`${fmtNum(qs.com_inconsistencias)} leads`}
          accent="red"
        />
        <KpiCard
          title="Com Interações"
          value={fmtPct((rc.leads_com_interacoes / rc.leads_total) * 100)}
          subtitle={`${fmtNum(rc.leads_com_interacoes)} leads`}
          accent="blue"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
        <Card title="Normalização de Canal">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={normPieData} dataKey="value" cx="50%" cy="50%" innerRadius={50} outerRadius={80} label={({ name, value }) => `${name}: ${fmtNum(value)}`} labelLine={false}>
                {normPieData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(v: number) => fmtNum(v)} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-4 mt-2">
            {normPieData.map((d) => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-slate-600">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: d.color }} />
                {d.name}
              </div>
            ))}
          </div>
        </Card>

        <Card title="Normalização de Etapa">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={stagePieData} dataKey="value" cx="50%" cy="50%" innerRadius={50} outerRadius={80} label={({ name, value }) => `${name}: ${fmtNum(value)}`} labelLine={false}>
                {stagePieData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(v: number) => fmtNum(v)} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-4 mt-2">
            {stagePieData.map((d) => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-slate-600">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: d.color }} />
                {d.name}
              </div>
            ))}
          </div>
        </Card>

        <Card title="Distribuição de Score CRM">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={scoreData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="range" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip
                formatter={(v: number) => [fmtNum(v), 'Leads']}
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} name="Leads" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card title="Sentimento por Etapa do Funil">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={sentimentChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="stage" tick={{ fontSize: 11, fill: '#64748b' }} />
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} />
            <Tooltip
              contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
            />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            {Object.entries(SENTIMENT_COLORS).map(([key, color]) => (
              <Bar key={key} dataKey={key} stackId="a" fill={color} name={key} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  )
}
