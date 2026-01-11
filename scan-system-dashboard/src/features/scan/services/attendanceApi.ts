import axios from 'axios'
import type {
  QRValidationResponse,
  CheckInResponse,
  PermissionRequest,
  QRValidationRequest,
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
   * Submit permission request
   * Endpoint: POST /api/scan/permission-request
   * Note: Backend endpoint needs to be implemented
   */
  //   submitPermission: async (data: PermissionRequest): Promise<void> => {
  //     // TODO: Implement backend endpoint for permission requests
  //     const response = await axios.post(`${API_BASE}/permission-request`, data, {
  //       withCredentials: true,
  //     })
  //     return response.data
  //   },
}
