import axios from 'axios'
import type { AuthResponse } from '../types'
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true, // CRUCIAL: This allows cookies to be sent/received
})
export const authApi = {
  // Matches your endpoint: /auth/login
  // login method
  login: async (credentials: any): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  // Get current user from session
  me: async (): Promise<AuthResponse> => {
    const response = await api.get('/auth/me')
    return response.data
  },

  // logout method
  logout: async (): Promise<void> => {
    await api.post('/auth/logout')
  },
}
