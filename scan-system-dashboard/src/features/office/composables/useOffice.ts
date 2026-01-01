import { storeToRefs } from 'pinia'
import { useOfficeStore } from '../store/officeStore'
import type { OfficeCreate, OfficeUpdate } from '../types'

export function useOffice() {
  const store = useOfficeStore()

  // Keep state reactive
  const { offices, currentOffice, isLoading, error, officesCount } = storeToRefs(store)

  // Load offices on mount or when needed
  const loadOffices = async () => {
    return await store.fetchOffices()
  }

  // Get office by ID
  const loadOffice = async (id: number) => {
    return await store.fetchOfficeById(id)
  }

  // Create office handler
  const handleCreateOffice = async (officeData: OfficeCreate) => {
    const result = await store.createOffice(officeData)
    if (result.success) {
      return result.office
    }
    return null
  }

  // Update office handler
  const handleUpdateOffice = async (id: number, officeData: OfficeUpdate) => {
    const result = await store.updateOffice(id, officeData)
    if (result.success) {
      return result.office
    }
    return null
  }

  // Delete office handler
  const handleDeleteOffice = async (id: number) => {
    const result = await store.deleteOffice(id)
    return result.success
  }

  return {
    // State
    offices,
    currentOffice,
    isLoading,
    error,
    officesCount,
    // Actions
    loadOffices,
    loadOffice,
    handleCreateOffice,
    handleUpdateOffice,
    handleDeleteOffice,
    clearError: store.clearError,
  }
}