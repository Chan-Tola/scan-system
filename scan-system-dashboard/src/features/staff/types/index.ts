// Roles (Strictly Admin or Staff)
export type UserRoleName = 'admin' | 'staff'

// (Optional) If you still use roles array somewhere else
export interface Role {
  id: number
  name: UserRoleName
  pivot: { model_id: number; role_id: number }
}

export interface UserAccount {
  id: number
  username: string
  email: string
  roles: Role[]
}

export interface Office {
  id: number
  name: string
}

// ✅ Matches your API response item exactly
export interface StaffMember {
  id: number
  username: string
  full_name: string
  phone: string
  email: string
  password: string
  role: UserRoleName
  office_name: string
  shift: string // e.g. "08:00 - 17:00"

  join_date: string // "YYYY-MM-DD"
  date_of_birth: string | null
  address: string | null
  gender: 'male' | 'female' | null
  profile_image: string | null // API returns URL string or null

  // UI State only
  expanded?: boolean
}

export interface StaffCreate {
  username: string
  email: string
  password?: string
  office_id: number
  full_name: string
  gender: 'male' | 'female'
  phone: string
  address: string
  date_of_birth: string
  join_date: string
  shift_start?: string
  shift_end?: string
  role: UserRoleName
  profile_image?: File | null // upload file
}

export type StaffUpdate = Partial<StaffCreate> & { _method?: 'PUT' }

// ✅ Pagination matches your response (no per_page)
export interface Pagination {
  current_page: number
  total: number
  last_page: number
}

// ✅ List response matches your JSON
export interface StaffListResponse {
  status: 'success' | 'error'
  data: StaffMember[]
  pagination: Pagination
}

// ✅ Single item response (if you have it)
export interface StaffMemberResponse {
  status: 'success' | 'error'
  data: StaffMember
}
