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
  <div class="bg-slate-50/30 p-6 lg:p-8 flex flex-col h-full overflow-hidden">
    <!-- Removed h-auto on mobile, use responsive height for proper spacing -->
    <div class="flex items-center justify-between mb-6 flex-shrink-0">
      <h2 class="text-xs font-bold uppercase tracking-widest text-slate-400">Live Preview</h2>
      <span v-if="qrCode" class="text-[9px] font-mono text-slate-400">
        Token: {{ qrCode.qr_token.substring(0, 8) }}...
      </span>
    </div>

    <div
      class="bg-white rounded-3xl p-6 lg:p-8 border border-slate-200 shadow-sm flex flex-col h-full overflow-hidden"
    >
      <!-- Responsive height: auto on mobile, full height with constraints on desktop -->
      <!-- Loading State -->
      <div v-if="isLoading" class="flex-1 flex items-center justify-center">
        <div class="text-slate-400 text-sm">Generating QR code...</div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex-1 flex items-center justify-center">
        <div class="text-red-500 text-sm">{{ error }}</div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!qrCode" class="flex-1 flex flex-col items-center justify-center">
        <div class="text-slate-400 text-sm text-center">
          <p class="mb-2">No QR code generated yet</p>
          <p class="text-xs">Select an office and click "Initialize New Code"</p>
        </div>
      </div>

      <!-- QR Code Preview -->
      <template v-else>
        <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex-shrink-0">
          <div class="grid grid-cols-2 gap-y-3 font-mono text-[10px] md:text-[11px]">
            <span class="text-slate-400 uppercase tracking-tighter">Status:</span>
            <span
              :class="[
                'text-right font-bold',
                qrCode.is_active ? 'text-emerald-600' : 'text-red-600',
              ]"
            >
              {{ qrCode.is_active ? 'ACTIVE' : 'INACTIVE' }}
            </span>
            <span class="text-slate-400 uppercase tracking-tighter">Office:</span>
            <span class="text-slate-700 text-right font-bold">
              {{ qrCode.office?.name || 'N/A' }}
            </span>
            <span class="text-slate-400 uppercase tracking-tighter">Office ID:</span>
            <span class="text-slate-700 text-right font-bold">{{ qrCode.office_id }}</span>
            <span class="text-slate-400 uppercase tracking-tighter">Secure Token:</span>
            <span class="text-slate-700 text-right font-mono text-[9px]">
              {{ qrCode.qr_token.substring(0, 12) }}...
            </span>
          </div>
        </div>

        <div class="flex-1 flex justify-center items-center py-6 lg:py-8 min-h-[200px] lg:min-h-0">
          <!-- Adjusted padding and removed lg:min-h-0 override for natural scaling -->
          <div class="relative group h-full flex items-center">
            <div
              class="absolute inset-0 bg-slate-100/50 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity"
            ></div>
            <img
              :src="qrCode.qr_code_image"
              alt="QR Code Preview"
              class="relative max-h-[180px] lg:max-h-full w-auto opacity-90 transition-opacity"
            />
          </div>
        </div>

        <div class="mt-auto pt-4 space-y-4 md:space-y-6 flex-shrink-0">
          <div class="grid grid-cols-2 gap-3">
            <button
              class="flex items-center justify-center py-3 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-[10px] md:text-xs font-bold transition-all"
              @click="handleDownloadImage"
            >
              Download Image
            </button>
            <button
              class="flex items-center justify-center py-3 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-[10px] md:text-xs font-bold transition-all"
              @click="emit('refresh')"
            >
              Refresh
            </button>
          </div>

          <div class="text-center">
            <button
              class="text-[10px] md:text-[11px] font-bold text-slate-400 hover:text-slate-900 transition-colors uppercase tracking-widest"
              @click="handleDownloadImage"
            >
              Download RAW image
            </button>
          </div>

          <div class="pt-4 border-t border-slate-100 text-center">
            <p class="text-[10px] text-slate-400 font-medium">Last Sync: {{ formattedDate }}</p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
