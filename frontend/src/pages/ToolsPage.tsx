import { useEffect, useState } from 'react'
import api from '../services/api'
import { Tool } from '../types'

export default function ToolsPage() {
  const [tools, setTools] = useState<Tool[]>([])
  const [search, setSearch] = useState('')
  const fetchTools = () => api.get('/tools', { params: { search } }).then((res) => setTools(res.data))
  useEffect(() => { fetchTools() }, [])

  return <div><h2 className="text-3xl font-bold mb-4">Tool Management</h2><div className="flex gap-2 mb-3"><input className="border p-2" placeholder="Search by tool code or name" value={search} onChange={(e)=>setSearch(e.target.value)} /><button className="bg-blue-700 text-white px-3" onClick={fetchTools}>Search</button></div><table className="w-full bg-white rounded shadow"><thead><tr className="text-left border-b"><th className="p-2">Tool Code</th><th>Name</th><th>Category</th><th>Ownership</th><th>Status</th></tr></thead><tbody>{tools.map(t => <tr key={t.id} className="border-b"><td className="p-2">{t.tool_code}</td><td>{t.tool_name}</td><td>{t.category}</td><td>{t.ownership}</td><td>{t.status}</td></tr>)}</tbody></table></div>
}
