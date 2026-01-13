<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Download, Loader2, AlertTriangle } from 'lucide-vue-next'
import { useHistory } from '@/features/history'
import HistoryTable from '@/features/history/components/HistoryTable.vue'
import HistoryFilters from '@/features/history/components/HistoryFilters.vue'
import HistoryPagination from '@/features/history/components/HistoryPagination.vue'

// --- COMPOSABLES ---
const {
  historyRecords,
  isLoading,
  isExporting,
  error,
  filters,
  pagination,
  loadHistory,
  handleExport,
  updateFilters,
  clearFilters,
  goToPage,
  performSearch,
  getStatusBadgeVariant,
  getStatusLabel,
} = useHistory()

// --- STATE ---
const searchInput = ref('')

// --- LIFECYCLE ---
onMounted(async () => {
  await loadHistory()
})

// Watch filters and reload when they change
watch(
  () => filters.value,
  () => {
    loadHistory()
  },
  { deep: true }
)

// --- FUNCTIONS ---
const handleSearch = (value: string) => {
  performSearch(value)
}

const handleClearFilters = () => {
  searchInput.value = ''
  clearFilters()
  loadHistory()
}

const handleExportClick = async () => {
  await handleExport()
}

const handleGoToPage = (page: number) => {
  goToPage(page)
}

const refreshData = async () => {
  await loadHistory()
}
</script>

<template>
  <div class="container mx-auto p-4 md:p-8 animate-in fade-in duration-500">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900">Attendance History</h1>
        <p class="text-slate-500 mt-1">View and export attendance records</p>
      </div>
      <Button
        @click="handleExportClick"
        :disabled="isExporting || isLoading"
        class="gap-2"
      >
        <Download v-if="!isExporting" class="h-4 w-4" />
        <Loader2 v-else class="h-4 w-4 animate-spin" />
        {{ isExporting ? 'Exporting...' : 'Export Excel' }}
      </Button>
    </div>

    <!-- Filters Card -->
    <HistoryFilters
      v-model:filters="filters"
      v-model:search-input="searchInput"
      @search="handleSearch"
      @clear="handleClearFilters"
      class="mb-6"
    />

    <!-- Error State -->
    <div
      v-if="error"
      class="rounded-lg border border-destructive/50 bg-destructive/5 p-4 text-destructive flex items-center gap-2 mb-6"
    >
      <AlertTriangle class="h-5 w-5" />
      {{ error }}
    </div>

    <!-- History Table -->
    <Card>
      <CardHeader>
        <CardTitle>Records</CardTitle>
        <CardDescription>
          Showing {{ historyRecords.length }} of {{ pagination.total }} records
        </CardDescription>
      </CardHeader>
      <CardContent>
        <HistoryTable
          :records="historyRecords"
          :is-loading="isLoading"
          :get-status-badge-variant="getStatusBadgeVariant"
          :get-status-label="getStatusLabel"
        />

        <!-- Pagination -->
        <HistoryPagination :pagination="pagination" @go-to-page="handleGoToPage" />
      </CardContent>
    </Card>
  </div>
</template>
