import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { useData, fmtNum } from '../hooks/useData'

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">{title}</h2>
      {children}
    </div>
  )
}

export default function Objections() {
  const { metrics, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics)
    return <div className="text-red-500 py-12 text-center">Erro: {error}</div>

  const allObjKeys = new Set([
    ...Object.keys(metrics.lost_analysis.por_objecao),
    ...Object.keys(metrics.won_analysis.por_objecao),
  ])

  const comparisonData = [...allObjKeys]
    .map((obj) => ({
      objecao: obj.length > 22 ? obj.slice(0, 22) + '…' : obj,
      perdidos: metrics.lost_analysis.por_objecao[obj] || 0,
      ganhos: metrics.won_analysis.por_objecao[obj] || 0,
    }))
    .sort((a, b) => b.perdidos - a.perdidos)

  const lostOnlyData = Object.entries(metrics.lost_analysis.por_objecao)
    .sort(([, a], [, b]) => b - a)
    .map(([obj, count]) => ({
      objecao: obj.length > 24 ? obj.slice(0, 24) + '…' : obj,
      count,
    }))

  const canonicalStages = Object.entries(metrics.objecoes_by_stage)
    .filter(([stageName]) => {
      const s = metrics.funnel_summary[stageName]
      return s && s.ordem !== null
    })
    .sort(([a], [b]) => {
      const oa = metrics.funnel_summary[a]?.ordem ?? 99
      const ob = metrics.funnel_summary[b]?.ordem ?? 99
      return oa - ob
    })

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Objeções</h1>
        <p className="text-slate-500 text-sm mt-1">
          Principais bloqueios em deals perdidos e ganhos
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
        <Card title="Top Objeções — Deals Perdidos">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={lostOnlyData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="objecao"
                width={155}
                tick={{ fontSize: 10, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Bar dataKey="count" fill="#ef4444" radius={[0, 4, 4, 0]} name="Deals perdidos" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Objeções: Ganhos vs Perdidos">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="objecao"
                width={155}
                tick={{ fontSize: 10, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" fill="#22c55e" name="Ganhos" radius={[0, 0, 0, 0]} />
              <Bar dataKey="perdidos" fill="#ef4444" name="Perdidos" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {canonicalStages.length > 0 && (
        <Card title="Top 5 Objeções por Etapa do Funil">
          <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {canonicalStages.map(([stageName, objections]) => (
              <div key={stageName} className="rounded-lg border border-slate-100 p-4">
                <p className="font-semibold text-slate-700 text-sm mb-2">{stageName}</p>
                <ol className="space-y-1">
                  {Object.entries(objections)
                    .sort(([, a], [, b]) => b - a)
                    .slice(0, 5)
                    .map(([obj, count], i) => (
                      <li key={obj} className="flex items-start gap-2 text-xs text-slate-600">
                        <span className="text-slate-400 font-mono w-3 shrink-0">{i + 1}.</span>
                        <span className="flex-1 leading-snug">{obj}</span>
                        <span className="font-semibold text-slate-500 shrink-0">{fmtNum(count)}</span>
                      </li>
                    ))}
                </ol>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}
