import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { historyApi } from '../services/historyApi'
import type { HistoryRecord, HistoryFilters, HistoryListResponse } from '../types'
import { useLoadingStore } from '@/stores/loadingStore'
import { toast } from 'vue-sonner'

export const useHistoryStore = defineStore('history', () => {
  const historyRecords = ref<HistoryRecord[]>([])
  const isLoading = ref(false)
  const isExporting = ref(false)
  const error = ref<string | null>(null)
  const filters = ref<HistoryFilters>({
    name: undefined,
    status: undefined,
    month: undefined,
    page: 1,
    per_page: 15,
  })
  const pagination = ref({
    current_page: 1,
    total: 0,
    last_page: 1,
    per_page: 15,
  })

  // Computed
  const recordsCount = computed(() => historyRecords.value.length)
  const hasRecords = computed(() => historyRecords.value.length > 0)

  // Fetch history with filters
  async function fetchHistory(customFilters?: HistoryFilters) {
    isLoading.value = true
    error.value = null
    try {
      const filtersToUse = customFilters || filters.value
      const response: HistoryListResponse = await historyApi.getHistory(filtersToUse)
      historyRecords.value = response.data
      pagination.value = response.pagination
      return true
    } catch (err: any) {
      // Handle network errors and blocked requests
      if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
        error.value =
          'Network error: Please check your connection or disable ad blockers that might be blocking the request.'
      } else if (err.code === 'ERR_BLOCKED_BY_CLIENT') {
        error.value =
          'Request blocked: Please disable ad blockers or browser extensions that might be interfering with API requests.'
      } else {
        error.value = err.response?.data?.message || err.message || 'Failed to load attendance history'
      }
      console.error('Failed to fetch history:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Export history
  async function exportHistory(customFilters?: HistoryFilters) {
    const loadingStore = useLoadingStore()
    loadingStore.show('Exporting attendance history...')
    isExporting.value = true
    error.value = null

    try {
      const filtersToUse = customFilters || filters.value
      await historyApi.exportHistory(filtersToUse)
      toast.success('Attendance history exported successfully')
      return { success: true }
    } catch (err: any) {
      // Handle network errors and blocked requests
      if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
        error.value =
          'Network error: Please check your connection or disable ad blockers that might be blocking the request.'
      } else if (err.code === 'ERR_BLOCKED_BY_CLIENT') {
        error.value =
          'Request blocked: Please disable ad blockers or browser extensions that might be interfering with API requests.'
      } else {
        error.value = err.message || 'Failed to export attendance history'
      }
      toast.error(`Failed to export: ${error.value}`)
      console.error('Export error:', err)
      return { success: false, error: error.value }
    } finally {
      isExporting.value = false
      loadingStore.hide()
    }
  }

  // Update filters
  function updateFilters(newFilters: Partial<HistoryFilters>) {
    filters.value = { ...filters.value, ...newFilters }
    if (newFilters.page === undefined) {
      filters.value.page = 1 // Reset to first page when filters change
    }
  }

  // Clear filters
  function clearFilters() {
    filters.value = {
      name: undefined,
      status: undefined,
      month: undefined,
      page: 1,
      per_page: 15,
    }
  }

  // Go to page
  function goToPage(page: number) {
    if (page >= 1 && page <= pagination.value.last_page) {
      filters.value.page = page
    }
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    historyRecords,
    isLoading,
    isExporting,
    error,
    filters,
    pagination,
    // Computed
    recordsCount,
    hasRecords,
    // Actions
    fetchHistory,
    exportHistory,
    updateFilters,
    clearFilters,
    goToPage,
    clearError,
  }
})

