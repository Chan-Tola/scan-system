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

const isLoading = ref(true)
const error = ref<string | null>(null)
const scannedData = ref<string | null>(null)
const isSuccess = ref(false)

const onDetect = async (detectedCodes: any[]) => {
  if (detectedCodes?.length) {
    const qrData = detectedCodes[0].rawValue
    scannedData.value = qrData
    isSuccess.value = true

    setTimeout(() => {
      emit('scan-success', qrData)
      resetState()
    }, 500)
  }
}

const onInit = async () => {
  isLoading.value = false
  error.value = null
}

const onError = (err: Error) => {
  isLoading.value = false

  if (err.name === 'NotAllowedError') {
    error.value = 'Camera permission denied. Please allow camera access.'
  } else if (err.name === 'NotFoundError') {
    error.value = 'No camera found on this device.'
  } else if (err.name === 'NotReadableError') {
    error.value = 'Camera is already in use.'
  } else {
    error.value = `Failed to access camera: ${err.message}`
  }
}

const resetState = () => {
  isLoading.value = true
  error.value = null
  scannedData.value = null
  isSuccess.value = false
}

watch(
  () => props.open,
  (v) => !v && resetState(),
)

const closeDialog = () => emit('update:open', false)
</script>

<template>
  <Dialog :open="open" @update:open="(v) => emit('update:open', v)">
    <DialogContent class="w-[92vw] max-w-xs sm:max-w-sm p-4 sm:p-6">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2 text-base sm:text-lg">
          <Camera class="h-4 w-4 sm:h-5 sm:w-5" />
          Scan QR Code
        </DialogTitle>
        <DialogDescription class="text-xs sm:text-sm">
          Point your camera at the QR code to check in
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-3 sm:space-y-4">
        <!-- Camera Preview -->
        <div class="relative aspect-square w-full overflow-hidden rounded-lg border bg-slate-950">
          <QrcodeStream
            v-if="open && !error"
            @detect="onDetect"
            @camera-on="onInit"
            @error="onError"
            class="h-full w-full"
          >
            <!-- Loading -->
            <div
              v-if="isLoading"
              class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/80 text-white"
            >
              <Loader2 class="h-8 w-8 sm:h-10 sm:w-10 animate-spin mb-2" />
              <p class="text-xs sm:text-sm">Initializing camera…</p>
            </div>

            <!-- Success -->
            <div
              v-if="isSuccess"
              class="absolute inset-0 flex flex-col items-center justify-center bg-green-500/90 text-white"
            >
              <CheckCircle2 class="h-10 w-10 sm:h-14 sm:w-14 mb-2" />
              <p class="text-sm sm:text-base font-semibold">QR Code Detected</p>
            </div>

            <!-- Scan Frame -->
            <div
              v-if="!isLoading && !isSuccess"
              class="absolute inset-0 flex items-center justify-center pointer-events-none"
            >
              <div class="relative w-48 h-48 sm:w-56 sm:h-56 md:w-64 md:h-64">
                <div
                  v-for="pos in [
                    'top-0 left-0 border-t border-l',
                    'top-0 right-0 border-t border-r',
                    'bottom-0 left-0 border-b border-l',
                    'bottom-0 right-0 border-b border-r',
                  ]"
                  :key="pos"
                  class="absolute w-8 h-8 sm:w-10 sm:h-10 border-white"
                  :class="pos"
                />
              </div>
            </div>
          </QrcodeStream>

          <!-- Error Overlay -->
          <div
            v-if="error"
            class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950 text-white p-4"
          >
            <XCircle class="h-10 w-10 sm:h-14 sm:w-14 text-red-400 mb-2" />
            <p class="text-xs sm:text-sm text-center text-slate-300">Camera unavailable</p>
          </div>
        </div>

        <!-- Error Alert -->
        <Alert v-if="error" variant="destructive">
          <XCircle class="h-4 w-4" />
          <AlertDescription class="text-xs sm:text-sm">
            {{ error }}
          </AlertDescription>
        </Alert>

        <!-- Instruction -->
        <p v-if="!error" class="text-center text-xs sm:text-sm text-slate-500">
          Position the QR code within the frame
        </p>

        <!-- Close -->
        <Button variant="outline" @click="closeDialog" class="w-full h-9 sm:h-10 text-sm">
          Cancel
        </Button>
      </div>
    </DialogContent>
  </Dialog>
</template>

<style scoped>
:deep(video) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
