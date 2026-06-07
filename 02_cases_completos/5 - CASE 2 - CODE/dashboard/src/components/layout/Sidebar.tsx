import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Filter,
  Megaphone,
  Users,
  MessageSquare,
  ShieldCheck,
} from 'lucide-react'

const nav = [
  { to: '/', label: 'Overview', icon: LayoutDashboard, end: true },
  { to: '/funnel', label: 'Funil de Vendas', icon: Filter, end: false },
  { to: '/campaigns', label: 'Campanhas', icon: Megaphone, end: false },
  { to: '/reps', label: 'Vendedores', icon: Users, end: false },
  { to: '/objections', label: 'Objeções', icon: MessageSquare, end: false },
  { to: '/quality', label: 'Qualidade de Dados', icon: ShieldCheck, end: false },
]

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 w-60 bg-slate-900 flex flex-col">
      <div className="px-6 py-5 border-b border-slate-700">
        <span className="text-white font-bold text-lg tracking-tight">AdGrowth</span>
        <p className="text-slate-400 text-xs mt-0.5">CRM Dashboard</p>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {nav.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-4 border-t border-slate-700">
        <p className="text-slate-500 text-xs">Sistema Agêntico v1</p>
      </div>
    </aside>
  )
}
