import { useEffect, useState } from 'react'
import api from '../services/api'

export default function DashboardPage() {
  const [summary, setSummary] = useState<any>({})
  useEffect(() => { api.get('/dashboard/summary').then((res) => setSummary(res.data)) }, [])
  const cards = [
    ['Total Tools', summary.total_tools, 'bg-blue-800'],
    ['Available', summary.available, 'bg-green-700'],
    ['Issued', summary.issued, 'bg-red-600'],
    ['Calibration Due', summary.calibration_due, 'bg-orange-500'],
    ['Pending Tickets', summary.pending_tickets, 'bg-indigo-700'],
  ]
  return <div><h2 className="text-3xl font-bold mb-4">Dashboard</h2><div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">{cards.map(([t,v,c]) => <div key={t as string} className={`${c} text-white rounded p-4`}><p>{t}</p><p className="text-2xl font-bold">{v as string}</p></div>)}</div></div>
}
