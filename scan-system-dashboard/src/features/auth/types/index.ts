export interface User {
  id: string
  email: string
  username: string
}
export interface AuthResponse {
  user: User
  message?: string
}
