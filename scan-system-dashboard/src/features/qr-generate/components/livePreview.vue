<script setup lang="ts">
import { computed } from 'vue'
import type { GenerateQRCodeResponse } from '../types'

interface Props {
  qrCode: GenerateQRCodeResponse | null
  isLoading: boolean
  error: string | null
}

interface Emits {
  (e: 'refresh'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formattedDate = computed(() => {
  if (!props.qrCode?.updated_at) return 'Never'
  return new Date(props.qrCode.updated_at).toLocaleDateString('en-US', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
})

const handleDownloadImage = () => {
  if (!props.qrCode?.qr_code_image) return

  // Convert base64 to blob and download
  const base64Data = props.qrCode.qr_code_image.replace('data:image/png;base64,', '')
  const byteCharacters = atob(base64Data)
  const byteNumbers = new Array(byteCharacters.length)
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i)
  }
  const byteArray = new Uint8Array(byteNumbers)
  const blob = new Blob([byteArray], { type: 'image/png' })

  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `qr-code-${props.qrCode.qr_token}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="h-full bg-slate-50/30 p-6 lg:p-8 flex flex-col lg:overflow-hidden relative">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6 flex-shrink-0">
      <h2 class="text-xs font-bold uppercase tracking-widest text-slate-400">Live Preview</h2>
      <span
        v-if="qrCode"
        class="text-[10px] font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded"
      >
        TOKEN: {{ qrCode.qr_token.substring(0, 8) }}...
      </span>
    </div>

    <!-- Main content - Scrollable on mobile only -->
    <div
      class="bg-white rounded-3xl p-6 lg:p-8 border border-slate-200 shadow-sm flex flex-col flex-1 lg:min-h-0 overflow-y-auto lg:overflow-hidden relative z-10"
    >
      <!-- Loading State -->
      <div v-if="isLoading" class="flex-1 flex items-center justify-center">
        <div class="flex flex-col items-center gap-3">
          <div
            class="h-8 w-8 border-2 border-slate-200 border-t-slate-800 rounded-full animate-spin"
          ></div>
          <div class="text-slate-400 text-sm font-medium">Generating secure code...</div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex-1 flex items-center justify-center">
        <div class="text-red-500 text-sm bg-red-50 px-4 py-3 rounded-xl border border-red-100">
          {{ error }}
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!qrCode" class="flex-1 flex flex-col items-center justify-center text-center">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
          <svg class="h-8 w-8 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"
            />
          </svg>
        </div>
        <div class="text-slate-400 text-sm">
          <p class="mb-1 font-medium text-slate-600">No QR code displayed</p>
          <p class="text-xs">Select a location to view its unique code</p>
        </div>
      </div>

      <!-- QR Code Preview - Full content that can scroll on mobile -->
      <div v-else class="flex flex-col h-full">
        <!-- Info panel -->
        <div class="flex-shrink-0 p-4 bg-slate-50 rounded-2xl border border-slate-100 mb-6 lg:mb-8">
          <div class="grid grid-cols-2 gap-y-3 font-mono text-[10px] md:text-[11px]">
            <span class="text-slate-400 uppercase tracking-tighter flex items-center">STATUS</span>
            <span
              :class="[
                'text-right font-bold flex items-center justify-end gap-1.5',
                qrCode.is_active ? 'text-emerald-600' : 'text-red-600',
              ]"
            >
              <span
                class="block w-1.5 h-1.5 rounded-full"
                :class="qrCode.is_active ? 'bg-emerald-500' : 'bg-red-500'"
              ></span>
              {{ qrCode.is_active ? 'ACTIVE' : 'INACTIVE' }}
            </span>
            <span class="text-slate-400 uppercase tracking-tighter">OFFICE ID</span>
            <span class="text-slate-700 text-right font-bold">{{ qrCode.office_id }}</span>
          </div>
        </div>

        <!-- QR Code Image - Responsive sizing -->
        <div class="flex-1 flex justify-center items-center min-h-0 py-4">
          <div class="relative group">
            <!-- Glow effect -->
            <div
              class="absolute inset-0 bg-blue-500/10 rounded-3xl blur-2xl transform group-hover:bg-blue-500/20 transition-all duration-500"
            ></div>
            <div
              class="relative bg-white p-4 rounded-2xl shadow-sm border border-slate-100 group-hover:shadow-md transition-shadow"
            >
              <img
                :src="qrCode.qr_code_image"
                alt="QR Code Preview"
                class="relative w-48 h-48 md:w-56 md:h-56 lg:w-64 lg:h-64 object-contain"
                loading="lazy"
              />
            </div>
          </div>
        </div>

        <!-- Actions - Fixed at bottom on desktop -->
        <div class="mt-auto pt-6 flex-shrink-0 space-y-4">
          <div class="grid grid-cols-2 gap-3">
            <button
              class="flex items-center justify-center py-3.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 hover:border-slate-300 text-slate-700 rounded-xl text-[10px] md:text-xs font-bold transition-all active:scale-[0.98] shadow-sm"
              @click="handleDownloadImage"
            >
              Download PNG
            </button>
            <button
              class="flex items-center justify-center py-3.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 hover:border-slate-300 text-slate-700 rounded-xl text-[10px] md:text-xs font-bold transition-all active:scale-[0.98] shadow-sm group"
              @click="emit('refresh')"
            >
              <span class="group-hover:rotate-180 transition-transform duration-500 mr-2">↻</span>
              Refresh
            </button>
          </div>

          <div class="pt-4 border-t border-slate-100 text-center">
            <p class="text-[10px] text-slate-400 font-medium tracking-wide">
              LAST SYNC • {{ formattedDate }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base height constraints */
.h-full {
  height: 100%;
}

.flex-1 {
  flex: 1 1 0%;
}

/* Desktop: fixed height, no scroll */
@media (min-width: 1024px) {
  .lg\:min-h-0 {
    min-height: 0;
  }

  .lg\:overflow-hidden {
    overflow: hidden;
  }
}

/* Mobile: allow scrolling */
@media (max-width: 1023px) {
  .flex-1 {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  }
}

/* Custom scrollbar for mobile */
@media (max-width: 1023px) {
  .flex-1::-webkit-scrollbar {
    width: 4px;
  }

  .flex-1::-webkit-scrollbar-track {
    background: #f8fafc;
  }

  .flex-1::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 2px;
  }
}

/* QR code responsive sizing */
img {
  max-width: 100%;
  height: auto;
}

/* Ensure proper spacing on very small screens */
@media (max-width: 640px) {
  .p-6 {
    padding: 1rem;
  }

  .rounded-3xl {
    border-radius: 1.5rem;
  }
}

/* Tablet adjustments */
@media (min-width: 768px) and (max-width: 1023px) {
  img {
    width: 280px !important;
    height: 280px !important;
  }
}
</style>
