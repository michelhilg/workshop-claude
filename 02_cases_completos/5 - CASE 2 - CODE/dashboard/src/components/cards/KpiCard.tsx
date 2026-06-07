interface KpiCardProps {
  title: string
  value: string
  subtitle?: string
  accent?: 'blue' | 'green' | 'red' | 'amber' | 'purple'
}

const accentClass: Record<string, string> = {
  blue: 'border-blue-500',
  green: 'border-green-500',
  red: 'border-red-500',
  amber: 'border-amber-500',
  purple: 'border-purple-500',
}

const subtitleClass: Record<string, string> = {
  blue: 'text-blue-600',
  green: 'text-green-600',
  red: 'text-red-600',
  amber: 'text-amber-600',
  purple: 'text-purple-600',
}

export default function KpiCard({ title, value, subtitle, accent = 'blue' }: KpiCardProps) {
  return (
    <div className={`bg-white rounded-xl p-5 shadow-sm border-l-4 ${accentClass[accent]}`}>
      <p className="text-slate-500 text-xs font-medium uppercase tracking-wide">{title}</p>
      <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
      {subtitle && (
        <p className={`text-xs font-medium mt-1 ${subtitleClass[accent]}`}>{subtitle}</p>
      )}
    </div>
  )
}
