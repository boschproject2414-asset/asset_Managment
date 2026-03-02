import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [email, setEmail] = useState('admin@bosch.local')
  const [password, setPassword] = useState('Admin@123')
  const [error, setError] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try { await login(email, password); nav('/') } catch { setError('Invalid credentials') }
  }

  return <div className="min-h-screen grid place-items-center bg-slate-200"><form onSubmit={onSubmit} className="bg-white p-8 rounded-xl shadow w-[360px] space-y-3"><h1 className="text-2xl font-bold">Bosch Asset Login</h1>{error && <p className="text-red-600">{error}</p>}<input className="w-full border p-2" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Email"/><input className="w-full border p-2" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password"/><button className="w-full bg-blue-700 text-white py-2 rounded">Login</button></form></div>
}
