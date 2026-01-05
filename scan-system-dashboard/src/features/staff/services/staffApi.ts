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
  // headers: {
  //   // This header tells ngrok to skip the warning page
  //   'ngrok-skip-browser-warning': 'true',
  // },
})

const toFormData = (data: any) => {
  const formData = new FormData()
  Object.keys(data).forEach((key) => {
    // Check if the valu is a File (like the profile_image) or a standard value
    if (data[key] !== null && data[key] !== undefined) {
      formData.append(key, data[key])
    }
  })
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
    const response = await api.post<StaffMemberResponse>(`/api/staff`, formData)
    return response.data.data
  },
  // Update Staff (Handle Image + Laravel PUT quirk)
  updateStaff: async (id: number, staffData: StaffUpdate): Promise<StaffMember> => {
    const formData = toFormData(staffData)
    // Laravel needs _method: 'PUT' in POST request for multipart/form-data
    formData.append('_method', 'PUT')

    const response = await api.post<StaffMemberResponse>(`/api/staff/${id}`, formData)
    return response.data.data
  },
  deleteStaff: async (id: number): Promise<void> => {
    await api.delete(`/api/staff/${id}`)
  },
}
