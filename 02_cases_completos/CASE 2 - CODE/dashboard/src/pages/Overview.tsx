import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import KpiCard from '../components/cards/KpiCard'
import { useData, fmtBRL, fmtNum, fmtPct } from '../hooks/useData'

function PageHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
      {subtitle && <p className="text-slate-500 text-sm mt-1">{subtitle}</p>}
    </div>
  )
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">{title}</h2>
      {children}
    </div>
  )
}

export default function Overview() {
  const { metrics, manifest, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics)
    return (
      <div className="text-red-500 py-12 text-center">
        Erro ao carregar dados: {error}.<br />
        <span className="text-sm text-slate-500">Execute <code>bash scripts/sync-data.sh</code> e reinicie o servidor.</span>
      </div>
    )

  const totalValor = Object.values(metrics.funnel_summary).reduce(
    (acc, s) => acc + s.valor_total,
    0,
  )
  const ticketMedio =
    metrics.won_analysis.total > 0
      ? metrics.funnel_summary['Fechado Ganho']?.valor_total / metrics.won_analysis.total ||
        metrics.funnel_summary['Ganho']?.valor_total / metrics.won_analysis.total ||
        0
      : 0

  const pipelineAtivo =
    metrics.total_leads - metrics.won_analysis.total - metrics.lost_analysis.total

  const monthlyData = Object.entries(metrics.monthly_volume)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([month, count]) => ({ month: month.replace('20', '').replace('-', '/'), count }))

  const allChannels = new Set([
    ...Object.keys(metrics.won_analysis.por_canal),
    ...Object.keys(metrics.lost_analysis.por_canal),
  ])
  const channelData = [...allChannels]
    .map((canal) => ({
      canal: canal.length > 12 ? canal.slice(0, 12) + '…' : canal,
      ganhos: metrics.won_analysis.por_canal[canal] || 0,
      perdidos: metrics.lost_analysis.por_canal[canal] || 0,
    }))
    .sort((a, b) => b.ganhos + b.perdidos - (a.ganhos + a.perdidos))
    .slice(0, 10)

  const lastAnalysis = manifest?.analysed_at
    ? new Date(manifest.analysed_at).toLocaleString('pt-BR')
    : '—'

  return (
    <div>
      <PageHeader
        title="Overview"
        subtitle={`Última análise: ${lastAnalysis}`}
      />

      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <KpiCard title="Total de Leads" value={fmtNum(metrics.total_leads)} accent="blue" />
        <KpiCard
          title="Leads Ganhos"
          value={fmtNum(metrics.won_analysis.total)}
          subtitle={fmtPct((metrics.won_analysis.total / metrics.total_leads) * 100)}
          accent="green"
        />
        <KpiCard
          title="Leads Perdidos"
          value={fmtNum(metrics.lost_analysis.total)}
          subtitle={fmtPct((metrics.lost_analysis.total / metrics.total_leads) * 100)}
          accent="red"
        />
        <KpiCard
          title="Pipeline Ativo"
          value={fmtNum(pipelineAtivo)}
          subtitle={fmtPct((pipelineAtivo / metrics.total_leads) * 100)}
          accent="amber"
        />
        <KpiCard
          title="Valor Total Est."
          value={fmtBRL(totalValor)}
          subtitle="todas as etapas"
          accent="purple"
        />
        <KpiCard
          title="Ticket Médio"
          value={ticketMedio > 0 ? fmtBRL(ticketMedio) : '—'}
          subtitle="leads ganhos"
          accent="blue"
        />
      </div>

      <div className="mb-6">
        <Card title="Volume Mensal de Leads">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#64748b' }} />
              <YAxis tick={{ fontSize: 12, fill: '#64748b' }} />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Line
                type="monotone"
                dataKey="count"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 3, fill: '#3b82f6' }}
                name="Leads"
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <Card title="Ganhos vs Perdidos por Canal">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={channelData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="canal"
                width={110}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" fill="#22c55e" name="Ganhos" radius={[0, 3, 3, 0]} />
              <Bar dataKey="perdidos" fill="#ef4444" name="Perdidos" radius={[0, 3, 3, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Ganhos vs Perdidos por Segmento">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart
              data={Object.keys(metrics.won_analysis.por_segmento)
                .slice(0, 10)
                .map((seg) => ({
                  seg: seg.length > 14 ? seg.slice(0, 14) + '…' : seg,
                  ganhos: metrics.won_analysis.por_segmento[seg] || 0,
                  perdidos: metrics.lost_analysis.por_segmento[seg] || 0,
                }))}
              layout="vertical"
              margin={{ left: 8 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="seg"
                width={110}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" fill="#22c55e" name="Ganhos" radius={[0, 3, 3, 0]} />
              <Bar dataKey="perdidos" fill="#ef4444" name="Perdidos" radius={[0, 3, 3, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  )
}
