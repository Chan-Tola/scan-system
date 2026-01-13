import { storeToRefs } from 'pinia'
import { useHistoryStore } from '../store/historyStore'
import type { HistoryFilters } from '../types'
import { useDebounceFn } from '@vueuse/core'

export function useHistory() {
  const store = useHistoryStore()

  // Keep state reactive
  const {
    historyRecords,
    isLoading,
    isExporting,
    error,
    filters,
    pagination,
    recordsCount,
    hasRecords,
  } = storeToRefs(store)

  // Load history
  const loadHistory = async (customFilters?: HistoryFilters) => {
    return await store.fetchHistory(customFilters)
  }

  // Export history
  const handleExport = async (customFilters?: HistoryFilters) => {
    return await store.exportHistory(customFilters)
  }

  // Update filters
  const updateFilters = (newFilters: Partial<HistoryFilters>) => {
    store.updateFilters(newFilters)
  }

  // Clear filters
  const clearFilters = () => {
    store.clearFilters()
  }

  // Go to page
  const goToPage = (page: number) => {
    store.goToPage(page)
    loadHistory()
  }

  // Debounced search
  const performSearch = useDebounceFn((searchValue: string) => {
    updateFilters({ name: searchValue.trim() || undefined, page: 1 })
    loadHistory()
  }, 500)

  // Status badge variant helper
  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'on_time':
      case 'present':
        return 'default'
      case 'late':
        return 'secondary'
      case 'absent':
        return 'destructive'
      default:
        return 'outline'
    }
  }

  // Status label helper
  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'on_time':
        return 'On Time'
      case 'present':
        return 'Present'
      case 'late':
        return 'Late'
      case 'absent':
        return 'Absent'
      default:
        return status
    }
  }

  return {
    // State
    historyRecords,
    isLoading,
    isExporting,
    error,
    filters,
    pagination,
    recordsCount,
    hasRecords,
    // Actions
    loadHistory,
    handleExport,
    updateFilters,
    clearFilters,
    goToPage,
    performSearch,
    // Helpers
    getStatusBadgeVariant,
    getStatusLabel,
    clearError: store.clearError,
  }
}

