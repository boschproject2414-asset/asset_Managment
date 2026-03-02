import { createContext, useContext, useEffect, useState } from 'react'
import api from '../services/api'
import { User } from '../types'

interface AuthState { user: User | null; login: (email: string, password: string) => Promise<void>; logout: () => void }
const AuthContext = createContext<AuthState | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = async (email: string, password: string) => {
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem('token', data.access_token)
    const me = await api.get<User>('/auth/me')
    setUser(me.data)
  }

  const logout = () => { localStorage.removeItem('token'); setUser(null) }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) api.get<User>('/auth/me').then((res) => setUser(res.data)).catch(() => logout())
  }, [])

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
