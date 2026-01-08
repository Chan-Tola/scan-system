import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { staffApi } from '../services/staffApi'
import type { StaffMember, StaffCreate, StaffUpdate, Pagination } from '../types'
import { useLoadingStore } from '@/stores/loadingStore'
import { toast } from 'vue-sonner'

export const useStaffStore = defineStore('staff', () => {
  // State
  const staffMembers = ref<StaffMember[]>([])
  const currentStaff = ref<StaffMember | null>(null)
  const pagination = ref<Pagination | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const totalStaff = computed(() => pagination.value?.total || 0)
  const staffCount = computed(() => staffMembers.value.length)

  // Actions
  // Fetch Staff with optional filters (search, office, page)
  async function fetchStaff(params?: {
    search?: string
    office_id?: number
    page?: number
    per_page?: number
  }) {
    isLoading.value = true
    error.value = null
    try {
      const response = await staffApi.getStaff(params)
      staffMembers.value = response.data
      pagination.value = response.pagination
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch staff'
      console.error('Failed to fetch staff:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fetch Staff Member by ID
  async function fetchStaffById(id: number) {
    isLoading.value = true
    error.value = null
    try {
      currentStaff.value = await staffApi.getStaffById(id)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch staff member'
      console.error('Failed to fetch staff member:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }
  // Create Staff
  async function createStaff(staffData: StaffCreate) {
    const loadingStore = useLoadingStore()

    loadingStore.show('Creating staff...')
    error.value = null
    try {
      const newStaff = await staffApi.createStaff(staffData)
      //  Add to begining of list since controller use lastest()
      staffMembers.value.unshift(newStaff)

      // Show success toast
      toast.success(`Staff created: ${newStaff.full_name}`)

      return { success: true, data: newStaff }
    } catch (err: any) {
      // Check if it's a validation error with multiple errors
      if (err.response?.data?.errors) {
        // Get first error message
        const firstError = Object.values(err.response.data.errors)[0]
        error.value = Array.isArray(firstError) ? firstError[0] : firstError
      } else {
        error.value = err.response?.data?.message || 'Failed to create staff'
      }

      // Show error toast
      toast.error(`Failed to create staff: ${error.value}`)

      return { success: false, error: error.value }
    } finally {
      loadingStore.hide()
    }
  }
  // Update staff
  async function updateStaff(id: number, staffData: StaffUpdate) {
    const loadingStore = useLoadingStore()

    loadingStore.show('Updating staff...')
    error.value = null

    try {
      const updatedStaff = await staffApi.updateStaff(id, staffData)

      // Update in local list
      const index = staffMembers.value.findIndex((s) => s.id === id)
      if (index !== -1) {
        staffMembers.value[index] = updatedStaff
      }

      // If updating current user's profile, refresh auth profile
      // This ensures the cached profile in auth store is updated
      const { useAuthStore } = await import('@/features/auth/store/authStore')
      const authStore = useAuthStore()
      if (authStore.user?.profile?.id === id) {
        await authStore.refreshProfile()
      }

      // Show success toast
      toast.success('Staff updated successfully')

      return { success: true, data: updatedStaff }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to update staff'

      // Show error toast
      toast.error(`Failed to update staff: ${error.value}`)

      return { success: false, error: error.value }
    } finally {
      loadingStore.hide()
    }
  }
  // Delete staff
  async function deleteStaff(id: number) {
    const loadingStore = useLoadingStore()

    loadingStore.show('Deleting staff...')
    error.value = null

    try {
      await staffApi.deleteStaff(id)
      staffMembers.value = staffMembers.value.filter((staff) => staff.id !== id)

      if (currentStaff.value?.id === id) {
        currentStaff.value = null
      }

      // Show success toast
      toast.success('Staff deleted successfully')

      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to delete staff'

      // Show error toast
      toast.error(`Failed to delete staff: ${error.value}`)

      return { success: false, error: error.value }
    } finally {
      loadingStore.hide()
    }
  }

  function clearError() {
    error.value = null
  }
  return {
    // State
    staffMembers,
    currentStaff,
    pagination,
    isLoading,
    error,
    // Computed
    totalStaff,
    staffCount,
    // Actions
    fetchStaff,
    fetchStaffById,
    createStaff,
    updateStaff,
    deleteStaff,
    clearError,
  }
})
