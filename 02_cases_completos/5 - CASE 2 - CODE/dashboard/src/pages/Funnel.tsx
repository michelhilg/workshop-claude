import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
  ResponsiveContainer,
} from 'recharts'
import { useData, fmtBRL, fmtNum, fmtPct } from '../hooks/useData'

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">{title}</h2>
      {children}
    </div>
  )
}

const STAGE_COLORS: Record<string, string> = {
  Topo: '#3b82f6',
  Meio: '#8b5cf6',
  Fundo: '#f59e0b',
  Fechado: '#22c55e',
  Perdido: '#ef4444',
}

export default function Funnel() {
  const { metrics, loading, error } = useData()

  if (loading) return <div className="text-slate-500 py-12 text-center">Carregando dados...</div>
  if (error || !metrics)
    return <div className="text-red-500 py-12 text-center">Erro: {error}</div>

  const canonicalStages = Object.entries(metrics.funnel_summary)
    .filter(([, s]) => s.ordem !== null)
    .sort(([, a], [, b]) => (a.ordem ?? 0) - (b.ordem ?? 0))

  const funnelData = canonicalStages.map(([name, s]) => ({
    name,
    contagem: s.contagem,
    categoria: s.categoria,
    cor: STAGE_COLORS[s.categoria ?? ''] ?? '#94a3b8',
  }))

  const conversionData = Object.entries(metrics.conversion_rates).map(([key, cr]) => ({
    transicao: key.replace(' → ', ' →\n'),
    taxa: cr.taxa_conversao ?? 0,
  }))

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Funil de Vendas</h1>
        <p className="text-slate-500 text-sm mt-1">Etapas canônicas com ordem e probabilidade de fechamento</p>
      </div>

      <div className="mb-6">
        <Card title="Distribuição por Etapa">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={funnelData} layout="vertical" margin={{ left: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                type="category"
                dataKey="name"
                width={130}
                tick={{ fontSize: 12, fill: '#64748b' }}
              />
              <Tooltip
                formatter={(v: number) => [fmtNum(v), 'Leads']}
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Bar dataKey="contagem" radius={[0, 4, 4, 0]}>
                {funnelData.map((entry, idx) => (
                  <Cell key={idx} fill={entry.cor} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
        <Card title="Taxas de Conversão entre Etapas">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={conversionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="transicao" tick={{ fontSize: 10, fill: '#64748b' }} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} unit="%" />
              <Tooltip
                formatter={(v: number) => [fmtPct(v), 'Conversão']}
                contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)' }}
              />
              <Bar dataKey="taxa" fill="#6366f1" radius={[4, 4, 0, 0]} name="Taxa %" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Resumo das Etapas">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="text-left py-2 text-slate-500 font-medium">Etapa</th>
                  <th className="text-right py-2 text-slate-500 font-medium">Leads</th>
                  <th className="text-right py-2 text-slate-500 font-medium">%</th>
                  <th className="text-right py-2 text-slate-500 font-medium">Valor</th>
                  <th className="text-right py-2 text-slate-500 font-medium">Prob.</th>
                </tr>
              </thead>
              <tbody>
                {canonicalStages.map(([name, s]) => (
                  <tr key={name} className="border-b border-slate-50 hover:bg-slate-50">
                    <td className="py-2.5 font-medium text-slate-800">{name}</td>
                    <td className="text-right py-2.5 text-slate-700">{fmtNum(s.contagem)}</td>
                    <td className="text-right py-2.5 text-slate-500">{fmtPct(s.percentual_total)}</td>
                    <td className="text-right py-2.5 text-slate-700">{fmtBRL(s.valor_total)}</td>
                    <td className="text-right py-2.5">
                      <span
                        className={`font-medium ${
                          (s.prob_fechamento ?? 0) >= 75
                            ? 'text-green-600'
                            : (s.prob_fechamento ?? 0) >= 35
                            ? 'text-amber-600'
                            : 'text-red-600'
                        }`}
                      >
                        {s.prob_fechamento !== null ? fmtPct(s.prob_fechamento) : '—'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}
