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
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
})

const handleDownloadImage = () => {
  if (!props.qrCode?.qr_code_image) return

  const link = document.createElement('a')
  link.href = props.qrCode.qr_code_image
  link.download = `qr-code-${props.qrCode.office_id}-${props.qrCode.qr_token.substring(0, 8)}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const handleCopyToken = () => {
  if (!props.qrCode?.qr_token) return

  navigator.clipboard
    .writeText(props.qrCode.qr_token)
    .then(() => {
      // You could add a toast notification here
      alert('Token copied to clipboard!')
    })
    .catch((err) => {
      console.error('Failed to copy token:', err)
    })
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden h-full">
    <!-- Header -->
    <div class="px-4 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">QR Code Preview</h2>
          <p class="mt-1 text-sm text-gray-600">Real-time QR code generation and management</p>
        </div>
        <div v-if="qrCode" class="flex items-center gap-3">
          <span class="text-xs font-mono text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg">
            Token: {{ qrCode.qr_token.substring(0, 12) }}...
          </span>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="p-4">
      <!-- Loading state -->
      <div v-if="isLoading" class="py-12">
        <div class="flex flex-col items-center justify-center">
          <div class="relative">
            <div class="w-11 h-11 border-4 border-gray-200 rounded-2xl"></div>
            <div
              class="absolute inset-0 border-4 border-blue-600 border-t-transparent rounded-2xl animate-spin"
            ></div>
          </div>
          <p class="mt-4 text-sm font-medium text-gray-900">Generating QR Code</p>
          <p class="mt-1 text-sm text-gray-600">Please wait a moment...</p>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="py-12">
        <div class="flex flex-col items-center justify-center text-center max-w-md mx-auto">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900 mb-2">Failed to load QR code</h3>
          <p class="text-sm text-gray-600 mb-6">{{ error }}</p>
          <button
            @click="emit('refresh')"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm font-medium rounded-lg transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            Try Again
          </button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="!qrCode" class="py-12">
        <div class="flex flex-col items-center justify-center text-center max-w-md mx-auto">
          <div
            class="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center mb-6"
          >
            <svg
              class="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900 mb-2">No QR Code Generated</h3>
          <p class="text-sm text-gray-600 mb-1">
            Select an office from the directory and click "Initialize New Code"
          </p>
          <p class="text-xs text-gray-500">
            Your QR code will appear here for download and management
          </p>
        </div>
      </div>

      <!-- QR code display -->
      <div v-else class="space-y-6">
        <!-- Office info card -->
        <div class="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-5">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">Office</p>
              <p class="text-sm font-semibold text-gray-900">{{ qrCode.office?.name || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">
                Office ID
              </p>
              <p class="text-sm font-semibold text-gray-900 font-mono">{{ qrCode.office_id }}</p>
            </div>
            <div>
              <p class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">Status</p>
              <div class="flex items-center gap-2">
                <div
                  :class="[
                    'w-2 h-2 rounded-full',
                    qrCode.is_active ? 'bg-emerald-500 animate-pulse' : 'bg-gray-400',
                  ]"
                ></div>
                <span
                  :class="[
                    'text-sm font-semibold',
                    qrCode.is_active ? 'text-emerald-700' : 'text-gray-700',
                  ]"
                >
                  {{ qrCode.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- QR code preview -->
        <div class="flex flex-col items-center">
          <div class="relative group">
            <!-- Glow effect -->
            <div
              :class="[
                'absolute -inset-4 rounded-2xl blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300',
                qrCode.is_active ? 'bg-blue-500/20' : 'bg-gray-500/20',
              ]"
            ></div>

            <!-- QR code container -->
            <div class="relative bg-white p-8 rounded-2xl border border-gray-200 shadow-lg">
              <img
                :src="qrCode.qr_code_image"
                alt="QR Code"
                class="w-32 h-36 object-contain"
                loading="lazy"
              />

              <!-- Active indicator animation -->
              <div
                v-if="qrCode.is_active"
                class="absolute inset-x-4 top-0 h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full animate-scan"
              ></div>
            </div>
          </div>

          <!-- QR code dimensions -->
          <p class="mt-4 text-sm text-gray-500">512 × 512 pixels • PNG format</p>
        </div>

        <!-- Token info -->
        <div class="bg-gray-50 rounded-xl p-5">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div class="flex-1 min-w-0">
              <p class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1">
                Secure Token
              </p>
              <p class="text-sm font-mono text-gray-900 truncate" :title="qrCode.qr_token">
                {{ qrCode.qr_token }}
              </p>
            </div>
            <button
              @click="handleCopyToken"
              class="flex-shrink-0 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm font-medium rounded-lg transition-colors flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
              Copy Token
            </button>
          </div>
        </div>

        <!-- Last updated -->
        <div class="text-center">
          <p class="text-sm text-gray-500">
            Last updated: <span class="font-medium text-gray-700">{{ formattedDate }}</span>
          </p>
        </div>

        <!-- Actions -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <button
            @click="handleDownloadImage"
            class="w-full py-3.5 px-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-semibold text-sm hover:from-blue-700 hover:to-blue-800 transition-all active:scale-[0.98] shadow-sm flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            Download QR Code
          </button>

          <button
            @click="emit('refresh')"
            class="w-full py-3.5 px-4 bg-white border border-gray-300 text-gray-700 rounded-lg font-semibold text-sm hover:bg-gray-50 transition-all active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            Refresh & Update
          </button>
        </div>

        <!-- Additional options -->
        <div class="text-center">
          <button
            @click="handleDownloadImage"
            class="inline-flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
              />
            </svg>
            Download raw image file
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes scan {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(calc(100% + 10px));
    opacity: 0;
  }
}

.animate-scan {
  animation: scan 2s ease-in-out infinite;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .w-64 {
    width: 14rem;
  }

  .h-64 {
    height: 14rem;
  }
}

/* Print styles */
@media print {
  .shadow-lg,
  .shadow-sm {
    box-shadow: none !important;
  }

  .border {
    border: 1px solid #000 !important;
  }
}
</style>
