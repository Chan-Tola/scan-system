import axios from 'axios'
import type { HistoryFilters, HistoryListResponse, StatisticsResponse } from '../types'

// Use relative URLs (empty baseURL) to leverage Vite proxy, or use env var if set
const baseURL = import.meta.env.VITE_API_BASE_URL || ''

const api = axios.create({
  baseURL,
  withCredentials: true,
  responseType: 'json',
  transformResponse: [
    function (data) {
      if (typeof data === 'string') {
        try {
          return JSON.parse(data)
        } catch (e) {
          return data
        }
      }
      return data
    },
  ],
})

// For file downloads (Excel), we need a separate axios instance with blob response type
const fileApi = axios.create({
  baseURL,
  withCredentials: true,
  responseType: 'blob', // Important: Use blob for file downloads
})

export const historyApi = {
  // Get paginated attendance history with filters
  getHistory: async (filters?: HistoryFilters): Promise<HistoryListResponse> => {
    // Clean up filters - remove empty/undefined values to avoid sending empty query params
    const cleanParams: Record<string, any> = {}
    if (filters?.name) cleanParams.name = filters.name
    if (filters?.status) cleanParams.status = filters.status
    if (filters?.month) cleanParams.month = filters.month
    if (filters?.page) cleanParams.page = filters.page
    if (filters?.per_page) cleanParams.per_page = filters.per_page

    const response = await api.get<HistoryListResponse>(`/api/attendance-records`, {
      params: cleanParams,
    })
    return response.data
  },

  // Get monthly statistics
  getStatistics: async (month?: string): Promise<StatisticsResponse> => {
    const response = await api.get<StatisticsResponse>(`/api/attendance-records/statistics`, {
      params: month ? { month } : {},
    })
    return response.data
  },

  // Export attendance history to Excel
  exportHistory: async (filters?: HistoryFilters): Promise<void> => {
    try {
      // Clean up filters - remove empty/undefined values
      const cleanParams: Record<string, any> = {}
      if (filters?.name) cleanParams.name = filters.name
      if (filters?.status) cleanParams.status = filters.status
      if (filters?.month) cleanParams.month = filters.month

      const response = await fileApi.get(`/api/attendance-records/export`, {
        params: cleanParams,
        responseType: 'blob',
      })

      // Extract filename from Content-Disposition header or use default
      const contentDisposition = response.headers['content-disposition']
      let filename = 'attendance_history.xlsx'

      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '')
        }
      }

      // Create blob URL and trigger download
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      })

      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()

      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      console.error('Export failed:', error)
      throw new Error(error.response?.data?.message || 'Failed to export attendance history')
    }
  },
}
