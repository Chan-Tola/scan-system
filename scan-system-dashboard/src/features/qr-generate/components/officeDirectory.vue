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
    class="p-6 lg:p-8 border-b lg:border-b-0 lg:border-e border-slate-100 flex flex-col h-full overflow-hidden"
  >
    <!-- Removed fixed max-height and used responsive layout for natural scrolling only when needed -->
    <div class="flex items-center justify-between mb-6 flex-shrink-0">
      <h2 class="text-xs font-bold uppercase tracking-widest text-slate-400">Office Directory</h2>
      <span class="text-[10px] font-bold bg-slate-100 px-2 py-0.5 rounded text-slate-500">
        {{ offices.length }} Locations
      </span>
    </div>

    <div class="relative mb-6 flex-shrink-0">
      <input
        type="text"
        :value="searchQuery"
        @input="handleSearch"
        placeholder="Find a location..."
        class="w-full pl-4 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-slate-900/5 transition-all placeholder:text-slate-400 text-sm"
      />
    </div>

    <div v-if="isLoading" class="flex-1 flex items-center justify-center text-slate-400 text-sm">
      Loading offices...
    </div>

    <div v-else class="space-y-2 flex-1 overflow-y-auto pr-2 mb-6 custom-scrollbar">
      <!-- Removed max-height constraints, let flex handle sizing on desktop, natural scroll on mobile -->
      <div
        v-for="office in offices"
        :key="office.id"
        :class="[
          'w-full p-4 rounded-xl flex items-center justify-between cursor-pointer border transition-all duration-300',
          selectedOfficeId === office.id
            ? 'bg-slate-900 border-slate-900 text-white shadow-lg'
            : 'bg-white border-slate-100 text-slate-700 hover:border-slate-300',
        ]"
        @click="handleOfficeClick(office.id)"
      >
        <div class="flex flex-col gap-0.5">
          <span class="font-bold text-sm tracking-tight">{{ office.name }}</span>
        </div>
        <div
          :class="[
            'px-2.5 py-0.5 rounded-full text-[9px] font-bold border uppercase tracking-wider',
            selectedOfficeId === office.id
              ? 'bg-white/10 border-white/20 text-white'
              : 'bg-green-100 text-green-600 border-green-200',
          ]"
        >
          Active
        </div>
      </div>

      <div v-if="offices.length === 0" class="text-center py-8 text-slate-400 text-sm">
        No offices found
      </div>
    </div>

    <button
      :disabled="!selectedOfficeId || isLoading"
      @click="handleGenerate"
      class="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold py-4 rounded-2xl flex-shrink-0 transition-all active:scale-[0.98] shadow-lg shadow-slate-200"
    >
      <span>{{ buttonText }}</span>
    </button>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
