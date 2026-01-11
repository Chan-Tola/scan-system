<script setup lang="ts">
import { ref, watch } from 'vue'
import { QrcodeStream } from 'vue-qrcode-reader'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Camera, XCircle, CheckCircle2 } from 'lucide-vue-next'

interface Props {
  open: boolean
}

interface Emits {
  (e: 'update:open', value: boolean): void
  (e: 'scan-success', qrData: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// State management
const isLoading = ref(true)
const error = ref<string | null>(null)
const scannedData = ref<string | null>(null)
const isSuccess = ref(false)

// Handle QR code detection
const onDetect = async (detectedCodes: any[]) => {
  if (detectedCodes && detectedCodes.length > 0) {
    const qrData = detectedCodes[0].rawValue
    scannedData.value = qrData
    isSuccess.value = true

    // Show success feedback briefly before closing
    setTimeout(() => {
      emit('scan-success', qrData)
      resetState()
    }, 500)
  }
}

// Handle camera initialization
const onInit = async () => {
  isLoading.value = false
  error.value = null
}

// Handle camera errors
const onError = (err: Error) => {
  isLoading.value = false

  if (err.name === 'NotAllowedError') {
    error.value = 'Camera permission denied. Please allow camera access in your browser settings.'
  } else if (err.name === 'NotFoundError') {
    error.value = 'No camera found on this device.'
  } else if (err.name === 'NotReadableError') {
    error.value = 'Camera is already in use by another application.'
  } else if (err.name === 'OverconstrainedError') {
    error.value = 'Camera constraints not supported.'
  } else {
    error.value = `Failed to access camera: ${err.message}`
  }
}

// Reset state when dialog closes
const resetState = () => {
  isLoading.value = true
  error.value = null
  scannedData.value = null
  isSuccess.value = false
}

// Watch for dialog close to reset state
watch(
  () => props.open,
  (newValue) => {
    if (!newValue) {
      resetState()
    }
  },
)

// Close dialog
const closeDialog = () => {
  emit('update:open', false)
}
</script>

<template>
  <Dialog :open="open" @update:open="(value) => emit('update:open', value)">
    <DialogContent class="sm:max-w-sm">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2">
          <Camera class="h-5 w-5" />
          Scan QR Code
        </DialogTitle>
        <DialogDescription> Point your camera at the QR code to check in </DialogDescription>
      </DialogHeader>

      <div class="space-y-4">
        <!-- Camera Preview Area -->
        <div
          class="relative aspect-square w-full overflow-hidden rounded-xl border-2 border-slate-200 bg-slate-950"
        >
          <!-- QR Code Stream Component -->
          <QrcodeStream
            v-if="open && !error"
            @detect="onDetect"
            @camera-on="onInit"
            @error="onError"
            class="h-full w-full"
          >
            <!-- Loading Overlay -->
            <div
              v-if="isLoading"
              class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/80 text-white"
            >
              <Loader2 class="h-12 w-12 animate-spin mb-4" />
              <p class="text-sm font-medium">Initializing camera...</p>
            </div>

            <!-- Success Overlay -->
            <div
              v-if="isSuccess"
              class="absolute inset-0 flex flex-col items-center justify-center bg-green-500/90 text-white"
            >
              <CheckCircle2 class="h-16 w-16 mb-4" />
              <p class="text-lg font-semibold">QR Code Detected!</p>
            </div>

            <!-- Scanning Frame Overlay -->
            <div
              v-if="!isLoading && !isSuccess"
              class="absolute inset-0 flex items-center justify-center pointer-events-none"
            >
              <div class="relative w-64 h-64">
                <!-- Corner borders for scanning frame -->
                <div
                  class="absolute top-0 left-0 w-12 h-12 border-t-4 border-l-4 border-white rounded-tl-lg"
                ></div>
                <div
                  class="absolute top-0 right-0 w-12 h-12 border-t-4 border-r-4 border-white rounded-tr-lg"
                ></div>
                <div
                  class="absolute bottom-0 left-0 w-12 h-12 border-b-4 border-l-4 border-white rounded-bl-lg"
                ></div>
                <div
                  class="absolute bottom-0 right-0 w-12 h-12 border-b-4 border-r-4 border-white rounded-br-lg"
                ></div>
              </div>
            </div>
          </QrcodeStream>

          <!-- Error State -->
          <div
            v-if="error"
            class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950 text-white p-6"
          >
            <XCircle class="h-16 w-16 text-red-400 mb-4" />
            <p class="text-sm text-center text-slate-300">Camera unavailable</p>
          </div>
        </div>

        <!-- Error Alert -->
        <Alert v-if="error" variant="destructive">
          <XCircle class="h-4 w-4" />
          <AlertDescription>
            {{ error }}
          </AlertDescription>
        </Alert>

        <!-- Instructions -->
        <div v-if="!error" class="text-center text-sm text-slate-500">
          <p>Position the QR code within the frame</p>
        </div>

        <!-- Close Button -->
        <div class="flex justify-end">
          <Button variant="outline" @click="closeDialog" class="w-full sm:w-auto"> Cancel </Button>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<style scoped>
/* Ensure camera preview fills container */
:deep(video) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
