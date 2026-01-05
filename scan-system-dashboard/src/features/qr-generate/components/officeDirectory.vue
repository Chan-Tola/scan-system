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

// Button text based on whether QR code exists
const buttonText = computed(() => {
  if (props.isLoading) {
    return props.hasQrCode ? 'Regenerating...' : 'Generating...'
  }
  return props.hasQrCode ? 'Regenerate Code' : 'Initialize New Code'
})
</script>

<template>
  <div
    class="h-full p-6 lg:p-8 border-b lg:border-b-0 lg:border-r border-slate-100 flex flex-col bg-slate-50/50"
  >
    <!-- Header -->
    <div class="flex items-center justify-between mb-6 flex-shrink-0">
      <h2 class="text-xs font-bold uppercase tracking-widest text-slate-400">Office Directory</h2>
      <span
        class="text-[10px] font-bold bg-white border border-slate-200 px-2.5 py-1 rounded-md text-slate-500 shadow-sm"
      >
        {{ offices.length }} Locations
      </span>
    </div>

    <!-- Search -->
    <div class="relative mb-6 flex-shrink-0 group">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg
          class="h-4 w-4 text-slate-400 group-focus-within:text-slate-600 transition-colors"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
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
        placeholder="Find a location..."
        class="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-300 transition-all placeholder:text-slate-400 text-sm shadow-sm"
      />
    </div>

    <!-- Scrollable Offices List - Fixed height that allows scrolling -->
    <div class="flex-1 min-h-0 mb-6">
      <!-- Loading State -->
      <div v-if="isLoading" class="h-full flex items-center justify-center text-slate-400 text-sm">
        <div class="flex flex-col items-center gap-2">
          <div
            class="h-5 w-5 border-2 border-slate-200 border-t-slate-800 rounded-full animate-spin"
          ></div>
          <span>Loading offices...</span>
        </div>
      </div>

      <!-- Offices List with Scroll -->
      <div v-else class="h-full overflow-y-auto pr-2 custom-scrollbar">
        <div class="space-y-2.5 pb-4">
          <!-- Extra padding at bottom -->
          <div
            v-for="office in offices"
            :key="office.id"
            :class="[
              'w-full p-4 rounded-xl flex items-center justify-between cursor-pointer border transition-all duration-200 group',
              selectedOfficeId === office.id
                ? 'bg-slate-900 border-slate-900 text-white shadow-md scale-[1.02] z-10'
                : 'bg-white border-slate-100 text-slate-600 hover:border-slate-300 hover:shadow-sm hover:translate-x-1',
            ]"
            @click="handleOfficeClick(office.id)"
          >
            <div class="flex flex-col gap-0.5">
              <span
                class="font-bold text-sm tracking-tight group-hover:text-slate-900 transition-colors"
                :class="selectedOfficeId === office.id ? 'text-white group-hover:text-white' : ''"
                >{{ office.name }}</span
              >
            </div>
            <div
              :class="[
                'px-2 py-0.5 rounded-md text-[10px] font-bold border uppercase tracking-wider',
                selectedOfficeId === office.id
                  ? 'bg-white/10 border-white/20 text-white'
                  : 'bg-emerald-50 text-emerald-600 border-emerald-100',
              ]"
            >
              Active
            </div>
          </div>

          <div v-if="offices.length === 0" class="text-center py-8 text-slate-400 text-sm">
            No offices found
          </div>
        </div>
      </div>
    </div>

    <!-- Action Button - Always visible at bottom -->
    <div class="pt-4 mt-auto border-t border-slate-200 flex-shrink-0">
      <button
        :disabled="!selectedOfficeId || isLoading"
        @click="handleGenerate"
        class="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold py-4 rounded-2xl transition-all active:scale-[0.98] shadow-lg shadow-slate-200"
      >
        <span>{{ buttonText }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.flex-1 {
  flex: 1 1 0%;
  min-height: 0; /* Crucial for scrolling to work */
}

/* Custom scrollbar for the offices list */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Ensure button stays at bottom */
.mt-auto {
  margin-top: auto;
}

/* Mobile responsiveness */
@media (max-width: 1024px) {
  .border-r {
    border-right: none !important;
  }

  .lg\:p-8 {
    padding: 1.5rem !important;
  }
}

/* Small screens: Limit max height for better scrolling */
@media (max-height: 700px) {
  .flex-1 {
    max-height: 50vh;
  }
}
</style>
