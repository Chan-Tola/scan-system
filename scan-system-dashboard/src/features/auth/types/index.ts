export interface StaffProfile {
  id: number
  user_id: number
  office_id: number
  full_name: string
  gender: string
  phone: string
  address: string
  date_of_birth: string
  join_date: string
  shift_start: string
  shift_end: string
  profile_image: string | null
  office?: {
    id: number
    name: string
  }
}

export interface User {
  id: string
  email: string
  username: string
  profile?: StaffProfile | null
}

export interface AuthResponse {
  user: User
  message?: string
  debug_error?: any
}
