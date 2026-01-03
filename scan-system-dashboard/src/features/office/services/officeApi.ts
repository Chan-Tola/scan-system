import axios from 'axios'
import type { Office, OfficeCreate, OfficeUpdate } from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  // headers: {
  //   // This header tells ngrok to skip the warning page
  //   'ngrok-skip-browser-warning': 'true',
  // },
})

export const officeApi = {
  // Get all offices
  getOffices: async (): Promise<Office[]> => {
    const response = await api.get<Office[]>('/api/offices')
    return response.data
  },
  getOfficeById: async (id: number): Promise<Office> => {
    const response = await api.get<Office>(`/api/offices/${id}`)
    return response.data
  },
  createOffice: async (officeData: OfficeCreate): Promise<Office> => {
    const response = await api.post<Office>('/api/offices', officeData)
    return response.data
  },
  updateOffice: async (id: number, officeData: OfficeUpdate): Promise<Office> => {
    const response = await api.put<Office>(`/api/offices/${id}`, officeData)
    return response.data
  },
  deleteOffice: async (id: number): Promise<void> => {
    await api.delete(`/api/offices/${id}`)
  },
}
