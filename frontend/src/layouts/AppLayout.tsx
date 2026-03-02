import { Link, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const nav = [
  ['Dashboard', '/'],
  ['Tools', '/tools'],
  ['Trolleys', '/trolleys'],
  ['Tickets', '/tickets'],
  ['Audit', '/audit'],
]

export default function AppLayout() {
  const { user, logout } = useAuth()
  return (
    <div className="min-h-screen flex">
      <aside className="w-56 bg-slate-900 text-white p-4">
        <h1 className="text-xl font-bold text-red-500">BOSCH</h1>
        <p className="text-xs text-slate-300 mb-4">Asset Management</p>
        <nav className="space-y-2">{nav.map(([label, href]) => <Link key={href} className="block rounded px-3 py-2 hover:bg-slate-800" to={href}>{label}</Link>)}</nav>
      </aside>
      <main className="flex-1 p-6">
        <div className="mb-4 flex justify-between"><p>{user?.full_name} ({user?.role})</p><button className="text-red-600" onClick={logout}>Logout</button></div>
        <Outlet />
      </main>
    </div>
  )
}
