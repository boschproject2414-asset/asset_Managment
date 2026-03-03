import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AuditPage() {
  const [rows, setRows] = useState<any[]>([])
  useEffect(() => { api.get('/audit').then((res) => setRows(res.data)).catch(() => setRows([])) }, [])
  return <div><h2 className="text-3xl font-bold mb-4">Audit Logs</h2><div className="space-y-2">{rows.map(r => <div className="bg-white p-3 rounded shadow" key={r.id}>{r.action} | tool:{r.tool_id ?? '-'} | ticket:{r.ticket_id ?? '-'}</div>)}</div></div>
}
