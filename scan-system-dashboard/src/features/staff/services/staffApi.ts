import axios from 'axios'
import type {
  StaffListResponse,
  StaffMember,
  StaffCreate,
  StaffUpdate,
  StaffMemberResponse,
} from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  // Ensure axios handles response encoding correctly
  responseType: 'json',
  // Transform response to handle encoding
  transformResponse: [
    function (data) {
      // If data is a string, try to parse it as JSON
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

const toFormData = (data: any) => {
  const formData = new FormData()
  Object.keys(data).forEach((key) => {
    const value = data[key]

    // CRITICAL: Skip null/undefined values entirely
    // Don't append them to FormData as they cause validation errors
    if (value === null || value === undefined) {
      return // Skip this field completely
    }

    if (value instanceof File) {
      // Validate file before appending
      if (value.size > 0 && value.type) {
        // Third parameter ensures the backend sees the correct extension
        formData.append(key, value, value.name)
        console.log(`FormData: Added file ${key}:`, {
          name: value.name,
          type: value.type,
          size: value.size,
        })
      } else {
        console.warn(`FormData: Skipping invalid file ${key}:`, value)
      }
    } else {
      formData.append(key, String(value))
    }
  })

  // Debug: Log all FormData entries (except files)
  console.log(
    'FormData entries:',
    Array.from(formData.entries()).map(([k, v]) => [
      k,
      v instanceof File ? `[File: ${v.name}, ${v.size} bytes]` : v,
    ]),
  )

  return formData
}

export const staffApi = {
  //  Get List
  getStaff: async (params?: {
    search?: string
    office_id?: number
    page?: number
    per_page?: number
  }): Promise<StaffListResponse> => {
    const response = await api.get<StaffListResponse>(`/api/staff`, { params })
    return response.data
  },

  // Get Single Staff Member by ID
  getStaffById: async (id: number): Promise<StaffMember> => {
    const response = await api.get<StaffMemberResponse>(`/api/staff/${id}`)
    return response.data.data
  },
  //   Create Staff (Handles Image)
  createStaff: async (staffData: StaffCreate): Promise<StaffMember> => {
    const formData = toFormData(staffData)
    // For multipart/form-data, remove Content-Type header to let browser set it with boundary
    const response = await api.post<StaffMemberResponse>(`/api/staff`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data.data
  },
  // Update Staff (Handle Image + Laravel PUT quirk)
  updateStaff: async (id: number, staffData: StaffUpdate): Promise<StaffMember> => {
    const formData = toFormData(staffData)
    // Laravel needs _method: 'PUT' in POST request for multipart/form-data
    formData.append('_method', 'PUT')

    const response = await api.post<StaffMemberResponse>(`/api/staff/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data.data
  },
  deleteStaff: async (id: number): Promise<void> => {
    await api.delete(`/api/staff/${id}`)
  },
}
