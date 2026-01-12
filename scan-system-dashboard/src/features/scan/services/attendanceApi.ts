import axios from 'axios'
import type {
  QRValidationResponse,
  CheckInResponse,
  PermissionRequest,
  QRValidationRequest,
  CheckOutRequest,
  CheckOutResponse,
  TodayAttendanceResponse,
} from '../types/index'
import { getPublicIp } from '../utils/getPublicIp'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

// const API_BASE = '/'

export const attendanceApi = {
  /**
   * Validate QR code before check-in
   * Endpoint: POST /api/scan/validate-qr
   */
  validateQR: async (qrToken: string): Promise<QRValidationResponse> => {
    // Get user's public IP from client side (works even when accessing through local network)
    const clientIp = await getPublicIp()

    const requestData: QRValidationRequest = {
      qr_token: qrToken,
      client_ip: clientIp || undefined, // Include client IP if available
    }

    const response = await api.post<QRValidationResponse>('/api/scan/validate-qr', requestData)
    return response.data
  },

  /**
   * Check in using QR code
   * Endpoint: POST /api/scan/check-in
   */
  checkIn: async (qrToken: string): Promise<CheckInResponse> => {
    // Get user's public IP from client side (works even when accessing through local network)
    const clientIp = await getPublicIp()

    const requestData = {
      qr_token: qrToken,
      client_ip: clientIp || undefined, // Include client IP if available
    }

    const response = await api.post<CheckInResponse>(`/api/scan/check-in`, requestData)
    return response.data
  },

  /**
   * Check out from office
   * Endpoint: POST /api/scan/check-out
   */
  checkOut: async (data: CheckOutRequest): Promise<CheckOutResponse> => {
    const response = await api.post<CheckOutResponse>('/api/scan/check-out', data)
    return response.data
  },

  /**
   * Get today's attendance for current user
   * Endpoint: GET /api/scan/today-attendance
   */
  getTodayAttendance: async (): Promise<TodayAttendanceResponse> => {
    const response = await api.get<TodayAttendanceResponse>('/api/scan/today-attendance')
    return response.data
  },

  /**
   * Submit permission request for absence
   * Endpoint: POST /api/scan/permission-request
   * No IP validation - can be submitted from anywhere
   */
  submitPermission: async (data: PermissionRequest): Promise<PermissionRequest> => {
    const response = await api.post<PermissionRequest>('/api/scan/permission-request', data)
    return response.data
  },
}
