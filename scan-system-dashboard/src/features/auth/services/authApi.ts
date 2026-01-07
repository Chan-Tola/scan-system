import axios from 'axios'
import type { AuthResponse } from '../types'
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true, // CRUCIAL: This allows cookies to be sent/received
  // headers: {
  //   // This header tells ngrok to skip the warning page
  //   'ngrok-skip-browser-warning': 'true',
  // },
})
export const authApi = {
  // Matches your endpoint: /auth/login
  // login method
  login: async (credentials: any): Promise<AuthResponse> => {
    const response = await api.post('/api/auth/login', credentials)
    return response.data
  },

  // Get current user from session
  me: async (): Promise<AuthResponse> => {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  // logout method
  logout: async (): Promise<void> => {
    await api.post('/api/auth/logout')
  },
}
