import { useEffect, useState } from 'react'
import api from '../services/api'
import { Trolley } from '../types'

export default function TrolleyPage() {
  const [rows, setRows] = useState<Trolley[]>([])
  useEffect(() => { api.get('/trolley').then((res) => setRows(res.data)) }, [])

  return <div><h2 className="text-3xl font-bold mb-4">Trolley Management</h2><div className="grid grid-cols-1 md:grid-cols-3 gap-4">{rows.map(t => <div key={t.id} className="bg-white rounded-xl shadow p-4"><p className="text-xl font-bold">{t.trolley_code}</p><p>{t.project}</p><p>{t.department}</p><span className={`px-3 py-1 rounded text-white ${t.status === 'active' ? 'bg-green-600':'bg-slate-500'}`}>{t.status}</span></div>)}</div></div>
}
