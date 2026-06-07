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
import { useData, fmtNum, fmtPct } from '../hooks/useData'

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">{title}</h2>
      {children}
    </div>
  )
}

export default function SalesReps() {
  const { metrics, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics)
    return <div className="text-red-500 py-12 text-center">Erro: {error}</div>

  const allReps = new Set([
    ...Object.keys(metrics.won_analysis.por_vendedor),
    ...Object.keys(metrics.lost_analysis.por_vendedor),
  ])

  const repData = [...allReps]
    .map((rep) => {
      const ganhos = metrics.won_analysis.por_vendedor[rep] || 0
      const perdidos = metrics.lost_analysis.por_vendedor[rep] || 0
      const total = ganhos + perdidos
      const winRate = total > 0 ? (ganhos / total) * 100 : 0
      return { rep, ganhos, perdidos, total, winRate }
    })
    .sort((a, b) => b.ganhos - a.ganhos)

  const chartData = repData.map((d) => ({
    nome: d.rep.split(' ')[0],
    ganhos: d.ganhos,
    perdidos: d.perdidos,
  }))

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Vendedores</h1>
        <p className="text-slate-500 text-sm mt-1">
          Performance individual — {repData.length} vendedores ativos
        </p>
      </div>

      <div className="mb-6">
        <Card title="Comparativo de Performance">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="nome" tick={{ fontSize: 12, fill: '#64748b' }} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="ganhos" fill="#22c55e" name="Ganhos" radius={[4, 4, 0, 0]} />
              <Bar dataKey="perdidos" fill="#ef4444" name="Perdidos" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {repData.map((rep) => (
          <div key={rep.rep} className="bg-white rounded-xl shadow-sm p-5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm">
                {rep.rep.charAt(0)}
              </div>
              <div>
                <p className="font-semibold text-slate-800 text-sm leading-tight">{rep.rep.split(' ')[0]}</p>
                <p className="text-slate-400 text-xs">{rep.rep.split(' ').slice(1).join(' ')}</p>
              </div>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Ganhos</span>
                <span className="font-semibold text-green-600">{fmtNum(rep.ganhos)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Perdidos</span>
                <span className="font-semibold text-red-500">{fmtNum(rep.perdidos)}</span>
              </div>
              <div className="flex justify-between text-sm pt-1 border-t border-slate-100">
                <span className="text-slate-500">Win Rate</span>
                <span
                  className={`font-bold ${
                    rep.winRate >= 50
                      ? 'text-green-600'
                      : rep.winRate >= 35
                      ? 'text-amber-600'
                      : 'text-red-600'
                  }`}
                >
                  {fmtPct(rep.winRate)}
                </span>
              </div>
            </div>
            <div className="mt-3 h-1.5 rounded-full bg-slate-100 overflow-hidden">
              <div
                className="h-full rounded-full bg-green-500"
                style={{ width: `${Math.min(rep.winRate, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <Card title="Tabela Detalhada">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left py-2 text-slate-500 font-medium">#</th>
                <th className="text-left py-2 text-slate-500 font-medium">Vendedor</th>
                <th className="text-right py-2 text-slate-500 font-medium">Ganhos</th>
                <th className="text-right py-2 text-slate-500 font-medium">Perdidos</th>
                <th className="text-right py-2 text-slate-500 font-medium">Total</th>
                <th className="text-right py-2 text-slate-500 font-medium">Win Rate</th>
              </tr>
            </thead>
            <tbody>
              {repData.map((rep, idx) => (
                <tr key={rep.rep} className="border-b border-slate-50 hover:bg-slate-50">
                  <td className="py-2.5 text-slate-400">{idx + 1}</td>
                  <td className="py-2.5 font-medium text-slate-800">{rep.rep}</td>
                  <td className="text-right py-2.5 text-green-600 font-medium">{fmtNum(rep.ganhos)}</td>
                  <td className="text-right py-2.5 text-red-500">{fmtNum(rep.perdidos)}</td>
                  <td className="text-right py-2.5 text-slate-600">{fmtNum(rep.total)}</td>
                  <td className="text-right py-2.5">
                    <span
                      className={`font-semibold ${
                        rep.winRate >= 50
                          ? 'text-green-600'
                          : rep.winRate >= 35
                          ? 'text-amber-600'
                          : 'text-red-600'
                      }`}
                    >
                      {fmtPct(rep.winRate)}
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
