import axios from 'axios'
import type { QRCodeResponse, GenerateQRCodeResponse, GenerateQRCodeRequest } from '../types/index'
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

export const qrGenerateApi = {
  // Generate a new QR Code for an office
  generateQRCode: async (request: GenerateQRCodeRequest): Promise<GenerateQRCodeResponse> => {
    const reponse = await api.post<GenerateQRCodeResponse>(`/api/generate-code`, request)
    return reponse.data
  },

  // Regenerate QR Code token and image
  regenerateQRCode: async (qrCodeId: number): Promise<GenerateQRCodeResponse> => {
    const response = await api.post<GenerateQRCodeResponse>(
      `/api/generate-code/${qrCodeId}/regenerate`,
    )
    return response.data
  },

  //   Get all QR code with optional filters
  getQRCodes: async (params?: {
    skip?: number
    limit?: number
    is_active?: boolean
    office_id?: number
  }): Promise<QRCodeResponse[]> => {
    const response = await api.get<QRCodeResponse[]>('/api/generate-code', { params })
    return response.data
  },

  // Get QR Code by ID
  getQRCodeById: async (qrCodeId: number): Promise<QRCodeResponse> => {
    const response = await api.get<QRCodeResponse>(`/api/generate-code/${qrCodeId}`)
    return response.data
  },

  // Get QR Code by token
  getQRCodeByToken: async (token: string): Promise<QRCodeResponse> => {
    const response = await api.get<QRCodeResponse>(`/api/generate-code/${token}`)
    return response.data
  },

  // Get QR Code image by id
  getQRCodeImage: async (qrCodeId: number): Promise<{ qr_code_image: string }> => {
    const response = await api.get<{ qr_code_image: string }>(
      `/api/generate-code/${qrCodeId}/image`,
    )
    return response.data
  },

  // Soft delete QR code
  deleteQRCode: async (qrCodeId: number): Promise<void> => {
    await api.delete(`/api/generate-code/${qrCodeId}`)
  },
}
