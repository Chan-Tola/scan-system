import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { officeApi } from '../services/officeApi'
import type { Office, OfficeCreate, OfficeUpdate } from '../types'

export const useOfficeStore = defineStore('office', () => {
  const offices = ref<Office[]>([])
  const currentOffice = ref<Office | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const officesCount = computed(() => offices.value.length)

  // Fetch all offices
  async function fetchOffices() {
    isLoading.value = true
    error.value = null
    try {
      offices.value = await officeApi.getOffices()
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch offices'
      console.error('Failed to fetch offices:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fetch office by ID
  async function fetchOfficeById(id: number) {
    isLoading.value = true
    error.value = null
    try {
      currentOffice.value = await officeApi.getOfficeById(id)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch office'
      console.error('Failed to fetch office:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Create office
  async function createOffice(officeData: OfficeCreate) {
    isLoading.value = true
    error.value = null
    try {
      const newOffice = await officeApi.createOffice(officeData)
      offices.value.push(newOffice)
      return { success: true, office: newOffice }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to create office'
      console.error('Failed to create office:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Update office
  async function updateOffice(id: number, officeData: OfficeUpdate) {
    isLoading.value = true
    error.value = null
    try {
      const updatedOffice = await officeApi.updateOffice(id, officeData)
      const index = offices.value.findIndex((o) => o.id === id)
      if (index !== -1) {
        offices.value[index] = updatedOffice
      }
      if (currentOffice.value?.id === id) {
        currentOffice.value = updatedOffice
      }
      return { success: true, office: updatedOffice }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to update office'
      console.error('Failed to update office:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Delete office
  async function deleteOffice(id: number) {
    isLoading.value = true
    error.value = null
    try {
      await officeApi.deleteOffice(id)
      offices.value = offices.value.filter((o) => o.id !== id)
      if (currentOffice.value?.id === id) {
        currentOffice.value = null
      }
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to delete office'
      console.error('Failed to delete office:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    offices,
    currentOffice,
    isLoading,
    error,
    // Computed
    officesCount,
    // Actions
    fetchOffices,
    fetchOfficeById,
    createOffice,
    updateOffice,
    deleteOffice,
    clearError,
  }
})
