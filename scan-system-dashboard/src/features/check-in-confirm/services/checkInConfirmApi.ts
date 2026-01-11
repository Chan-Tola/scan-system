import axios from 'axios'
import type { CheckOutRequest, CheckOutResponse, TodayAttendanceResponse } from '../types'
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})
export const checkInConfirmApi = {
  // Check out from office
  checkOut: async (data: CheckOutRequest): Promise<CheckOutResponse> => {
    const response = await api.post<CheckOutResponse>('/api/scan/check-out', data)
    return response.data
  },
  // Get today's attendance for current user
  getTodayAttendance: async (): Promise<TodayAttendanceResponse> => {
    const response = await api.get<TodayAttendanceResponse>('/api/scan/today-attendance')
    return response.data
  },
}
