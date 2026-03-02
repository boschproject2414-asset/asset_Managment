export type Role = 'asset_incharge' | 'internal_team' | 'external_department'

export interface User { id: number; full_name: string; email: string; role: Role; department?: string }
export interface Tool { id: number; tool_code: string; tool_name: string; category: string; ownership: string; status: string; calibration_due_date?: string }
export interface Ticket { id: number; tool_id: number; department: string; project?: string; reason: string; approval_status: string; status: string; request_date: string }
export interface Trolley { id: number; trolley_code: string; project: string; department: string; status: string }
