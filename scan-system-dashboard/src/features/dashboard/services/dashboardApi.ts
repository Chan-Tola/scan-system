import axios from 'axios'
import type { DashboardData } from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

export const dashboardApi = {
  // Get complete dashboard data
  getDashboard: async (): Promise<DashboardData> => {
    const response = await api.get<DashboardData>('/api/scan/dashboard')
    return response.data
  },
}
