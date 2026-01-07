// Roles (Strictly Admin or Staff as you mentioned)
export type UserRoleName = 'admin' | 'staff'

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

// The Staff Member (Response from Server)
export interface StaffMember {
  id: number
  full_name: string
  phone: string
  email: string
  username: string
  role: UserRoleName
  office_name: string
  shift: string // Format: "08:00 - 17:00"
  join_date: string
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
  profile_image?: File | null // The actual file object for upload
}

export type StaffUpdate = Partial<StaffCreate> & { _method?: 'PUT' }

// Response Wrappers
export interface StaffMemberResponse {
  status: string
  data: StaffMember
}

// Pagination Metadata (Matches your controller response)
export interface Pagination {
  current_page: number
  per_page: number
  total: number
  last_page: number
}

// The Full Response (The shape of your response()->json())
export interface StaffListResponse {
  status: string
  data: StaffMember[]
  pagination: Pagination
}
