<script setup lang="ts">
import type { Office } from '@/features/office/types'
import { computed } from 'vue'

interface Props {
  offices: Office[]
  selectedOfficeId: number | null
  isLoading: boolean
  searchQuery: string
  hasQrCode?: boolean
}

interface Emits {
  (e: 'select-office', officeId: number): void
  (e: 'generate'): void
  (e: 'update:search-query', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const handleOfficeClick = (officeId: number) => {
  emit('select-office', officeId)
}

const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:search-query', target.value)
}

const handleGenerate = () => {
  emit('generate')
}

const buttonText = computed(() => {
  if (props.isLoading) {
    return props.hasQrCode ? 'Regenerating...' : 'Generating...'
  }
  return props.hasQrCode ? 'Regenerate Code' : 'Initialize New Code'
})

// Get selected office name for better UX
const selectedOfficeName = computed(() => {
  if (!props.selectedOfficeId) return null
  return props.offices.find((office) => office.id === props.selectedOfficeId)?.name || null
})
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
    <!-- Header with stats -->
    <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Office Directory</h2>
          <p class="mt-1 text-sm text-gray-600">
            {{ offices.length }} location{{ offices.length !== 1 ? 's' : '' }} available
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div v-if="selectedOfficeName" class="hidden sm:block">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span class="text-sm text-gray-700 font-medium truncate max-w-[200px]">
                {{ selectedOfficeName }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search bar -->
    <div class="px-6 py-4">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <input
          type="text"
          :value="searchQuery"
          @input="handleSearch"
          placeholder="Search offices by name or ID..."
          class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg bg-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm transition-colors"
          :disabled="isLoading"
        />
      </div>
    </div>

    <!-- Content -->
    <div class="px-6 pb-6">
      <!-- Loading state -->
      <div v-if="isLoading" class="py-12">
        <div class="flex flex-col items-center justify-center">
          <div
            class="w-10 h-10 border-3 border-gray-200 border-t-blue-600 rounded-full animate-spin"
          ></div>
          <p class="mt-3 text-sm text-gray-600">Loading offices...</p>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="offices.length === 0" class="py-12 text-center">
        <div
          class="mx-auto w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4"
        >
          <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
            />
          </svg>
        </div>
        <h3 class="text-sm font-medium text-gray-900 mb-1">No offices found</h3>
        <p class="text-sm text-gray-600 max-w-sm mx-auto">
          {{ searchQuery ? 'Try adjusting your search query' : 'Add offices to get started' }}
        </p>
      </div>

      <!-- Offices list -->
      <div v-else class="space-y-2 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
        <div
          v-for="office in offices"
          :key="office.id"
          :class="[
            'group relative p-4 rounded-lg border transition-all duration-150 cursor-pointer',
            selectedOfficeId === office.id
              ? 'border-blue-500 bg-blue-50 shadow-sm'
              : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50',
          ]"
          @click="handleOfficeClick(office.id)"
        >
          <div class="flex items-start">
            <!-- Selection indicator -->
            <div class="flex-shrink-0 mt-0.5 mr-3">
              <div
                :class="[
                  'w-3 h-3 rounded-full transition-colors',
                  selectedOfficeId === office.id ? 'bg-blue-500' : 'bg-gray-300',
                ]"
              ></div>
            </div>

            <!-- Office info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h3 class="text-sm font-semibold text-gray-900 truncate">{{ office.name }}</h3>
                  <div class="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1">
                    <span class="inline-flex items-center text-xs text-gray-500">
                      <svg
                        class="w-3 h-3 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                        />
                      </svg>
                      Office ID: {{ office.id }}
                    </span>
                    <span class="inline-flex items-center text-xs text-gray-500">
                      <svg
                        class="w-3 h-3 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 1.197a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                        />
                      </svg>
                      {{ office.staff_count || 0 }} staff
                    </span>
                  </div>
                </div>

                <!-- Status badge -->
                <div
                  :class="[
                    'flex-shrink-0 px-2.5 py-1 rounded-full text-xs font-medium',
                    selectedOfficeId === office.id
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-emerald-100 text-emerald-800',
                  ]"
                >
                  Active
                </div>
              </div>

              <!-- Additional info (expandable if needed) -->
              <div v-if="office.description" class="mt-2">
                <p class="text-xs text-gray-600 line-clamp-2">{{ office.description }}</p>
              </div>
            </div>
          </div>

          <!-- Active selection indicator -->
          <div
            v-if="selectedOfficeId === office.id"
            class="absolute -left-2 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-500 rounded-full"
          ></div>
        </div>
      </div>

      <!-- Action button -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <button
          :disabled="!selectedOfficeId || isLoading"
          @click="handleGenerate"
          :class="[
            'w-full py-3.5 px-4 rounded-lg font-semibold text-sm transition-all duration-200',
            'flex items-center justify-center gap-2',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            !selectedOfficeId || isLoading
              ? 'bg-gray-100 text-gray-500'
              : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 active:scale-[0.98] shadow-sm',
          ]"
        >
          <svg
            v-if="hasQrCode"
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          {{ buttonText }}
        </button>

        <!-- Helper text -->
        <p v-if="!selectedOfficeId && !isLoading" class="mt-3 text-center text-sm text-gray-500">
          Select an office above to generate a QR code
        </p>
        <p
          v-else-if="selectedOfficeId && !isLoading"
          class="mt-3 text-center text-xs text-gray-500"
        >
          Ready to {{ hasQrCode ? 'regenerate' : 'generate' }} QR code for selected office
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f9fafb;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .max-h-[500px] {
    max-height: 400px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .custom-scrollbar::-webkit-scrollbar-track {
    background: #374151;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #4b5563;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #6b7280;
  }
}
</style>
