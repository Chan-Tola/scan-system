export interface StaffProfile {
  id: number
  user_id: number
  office_id: number
  full_name: string
  gender: string
  phone: string
  address: string
  profile_image: string | null
  shift_start: string
  shift_end: string
  // Optional if you want to access office details from the profile
  office?: {
    id: number
    name: string
  }
}

export interface User {
  id: number // Changed from string to number to match your Laravel ID
  email: string
  username: string
  role: 'admin' | 'staff' // Added the role property here
  profile: StaffProfile | null
}

export interface AuthResponse {
  status: string
  user: User
  message?: string
}
