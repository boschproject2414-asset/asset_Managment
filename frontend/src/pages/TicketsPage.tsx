import { useEffect, useState } from 'react'
import api from '../services/api'
import { Ticket } from '../types'

export default function TicketsPage() {
  const [rows, setRows] = useState<Ticket[]>([])
  const fetchRows = () => api.get('/tickets').then((res) => setRows(res.data))
  useEffect(() => { fetchRows() }, [])

  return <div><h2 className="text-3xl font-bold mb-4">Ticket Management</h2><table className="w-full bg-white rounded shadow"><thead><tr className="text-left border-b"><th className="p-2">ID</th><th>Tool</th><th>Department</th><th>Status</th><th>Approval</th></tr></thead><tbody>{rows.map(t => <tr key={t.id} className="border-b"><td className="p-2">{t.id}</td><td>{t.tool_id}</td><td>{t.department}</td><td>{t.status}</td><td>{t.approval_status}</td></tr>)}</tbody></table></div>
}
