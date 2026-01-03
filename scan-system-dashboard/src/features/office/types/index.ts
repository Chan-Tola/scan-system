export interface Office {
  id: number
  name: string
  public_ip: string
  shift_start: string // ISO date string from backend
  shift_end: string // ISO date string from backend
}

export interface OfficeResponse {
  status: string
  data: Office | Office[]
  message?: string
}

export interface OfficeCreate {
  name: string
  public_ip?: string
  shift_start: string // ISO date string from backend
  shift_end: string // ISO date string from backend
}

export interface OfficeUpdate {
  name?: string
  public_ip?: string
  shift_start: string // ISO date string from backend
  shift_end: string // ISO date string from backend
}
