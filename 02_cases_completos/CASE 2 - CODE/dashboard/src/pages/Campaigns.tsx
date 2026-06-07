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

export default function Campaigns() {
  const { metrics, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics)
    return <div className="text-red-500 py-12 text-center">Erro: {error}</div>

  const allChannels = new Set([
    ...Object.keys(metrics.won_analysis.por_canal),
    ...Object.keys(metrics.lost_analysis.por_canal),
  ])
  const channelData = [...allChannels]
    .map((canal) => ({
      canal: canal.length > 14 ? canal.slice(0, 14) + '…' : canal,
      ganhos: metrics.won_analysis.por_canal[canal] || 0,
      perdidos: metrics.lost_analysis.por_canal[canal] || 0,
      total:
        (metrics.won_analysis.por_canal[canal] || 0) +
        (metrics.lost_analysis.por_canal[canal] || 0),
    }))
    .sort((a, b) => b.total - a.total)

  const allSegments = new Set([
    ...Object.keys(metrics.won_analysis.por_segmento),
    ...Object.keys(metrics.lost_analysis.por_segmento),
  ])
  const segmentData = [...allSegments]
    .map((seg) => ({
      seg: seg.length > 16 ? seg.slice(0, 16) + '…' : seg,
      ganhos: metrics.won_analysis.por_segmento[seg] || 0,
      perdidos: metrics.lost_analysis.por_segmento[seg] || 0,
      total:
        (metrics.won_analysis.por_segmento[seg] || 0) +
        (metrics.lost_analysis.por_segmento[seg] || 0),
    }))
    .sort((a, b) => b.total - a.total)

  const winRateByChannel = channelData
    .filter((d) => d.total > 0)
    .map((d) => ({
      canal: d.canal,
      winRate: Math.round((d.ganhos / d.total) * 100),
      total: d.total,
    }))
    .sort((a, b) => b.winRate - a.winRate)

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Campanhas</h1>
        <p className="text-slate-500 text-sm mt-1">
          Performance por canal e segmento — {fmtNum(metrics.won_analysis.total)} ganhos ·{' '}
          {fmtNum(metrics.lost_analysis.total)} perdidos
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
        <Card title="Ganhos vs Perdidos por Canal">
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={channelData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="canal"
                width={115}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" stackId="a" fill="#22c55e" name="Ganhos" />
              <Bar dataKey="perdidos" stackId="a" fill="#ef4444" name="Perdidos" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Ganhos vs Perdidos por Segmento">
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={segmentData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="seg"
                width={115}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" stackId="a" fill="#22c55e" name="Ganhos" />
              <Bar dataKey="perdidos" stackId="a" fill="#ef4444" name="Perdidos" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card title="Win Rate por Canal">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left py-2 text-slate-500 font-medium">Canal</th>
                <th className="text-right py-2 text-slate-500 font-medium">Ganhos</th>
                <th className="text-right py-2 text-slate-500 font-medium">Perdidos</th>
                <th className="text-right py-2 text-slate-500 font-medium">Total</th>
                <th className="text-right py-2 text-slate-500 font-medium">Win Rate</th>
              </tr>
            </thead>
            <tbody>
              {winRateByChannel.map((row) => (
                <tr key={row.canal} className="border-b border-slate-50 hover:bg-slate-50">
                  <td className="py-2.5 font-medium text-slate-800">{row.canal}</td>
                  <td className="text-right py-2.5 text-green-600 font-medium">
                    {fmtNum(
                      metrics.won_analysis.por_canal[
                        Object.keys(metrics.won_analysis.por_canal).find(
                          (k) => k.slice(0, 14) + (k.length > 14 ? '…' : '') === row.canal,
                        ) ?? ''
                      ] ?? 0,
                    )}
                  </td>
                  <td className="text-right py-2.5 text-red-500">
                    {fmtNum(
                      metrics.lost_analysis.por_canal[
                        Object.keys(metrics.lost_analysis.por_canal).find(
                          (k) => k.slice(0, 14) + (k.length > 14 ? '…' : '') === row.canal,
                        ) ?? ''
                      ] ?? 0,
                    )}
                  </td>
                  <td className="text-right py-2.5 text-slate-600">{fmtNum(row.total)}</td>
                  <td className="text-right py-2.5">
                    <span
                      className={`font-semibold ${
                        row.winRate >= 30
                          ? 'text-green-600'
                          : row.winRate >= 15
                          ? 'text-amber-600'
                          : 'text-red-600'
                      }`}
                    >
                      {row.winRate}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
