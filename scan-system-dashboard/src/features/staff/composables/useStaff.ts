import { storeToRefs } from 'pinia'
import { useStaffStore } from '../store/staffStore'
import type { StaffCreate, StaffUpdate } from '../types'

export function useStaff() {
  const store = useStaffStore()

  // keep state reactive
  const { staffMembers, currentStaff, pagination, isLoading, error, staffCount, totalStaff } =
    storeToRefs(store)

  /**
   * Load staff list with optional filters
   * Useful for search bars and pagination controls
   */
  const loadStaffMembers = async (params?: {
    search?: string
    office_id?: number
    page?: number
    per_page?: number
  }) => {
    await store.fetchStaff(params)
  }

  // Load a single staff member by ID
  const loadStaffMemberById = async (id: number) => {
    await store.fetchStaffById(id)
  }

  // create staff
  const handleCreateStaff = async (staffData: StaffCreate) => {
    const result = await store.createStaff(staffData)
    if (result.success) {
      return result.data
    }
    return null
  }

  // update staff
  const handleUpdateStaff = async (id: number, staffData: StaffUpdate) => {
    const result = await store.updateStaff(id, staffData)
    if (result.success) {
      return result.data
    }
    return null
  }

  // delete staff
  const handleDeleteStaff = async (id: number) => {
    const result = await store.deleteStaff(id)
    return result
  }

  return {
    // state
    staffMembers,
    currentStaff,
    pagination,
    isLoading,
    error,
    staffCount,
    totalStaff,
    // Action
    loadStaffMembers,
    loadStaffMemberById,
    handleCreateStaff,
    handleUpdateStaff,
    handleDeleteStaff,
  }
}
