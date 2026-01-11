import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { attendanceApi } from '../services/attendanceApi'
import type { QRValidationResponse } from '../types'
import { useLoadingStore } from '@/stores/loadingStore'
import { toast } from 'vue-sonner'
import { getPublicIp } from '../utils/getPublicIp'

export const useAttendanceStore = defineStore('attendance', () => {
  // State
  const currentValidation = ref<QRValidationResponse | null>(null)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const publicIpCache = ref<string | null>(null)
  const ipFetchPromise = ref<Promise<string | null> | null>(null)

  // Computed
  const hasValidQR = computed(() => currentValidation.value?.valid === true)
  const officeName = computed(() => currentValidation.value?.office?.name || '')

  // Pre-fetch public IP (call this on page load to avoid delay during scan)
  async function preFetchPublicIp() {
    // If already cached in store, return immediately
    if (publicIpCache.value) {
      return publicIpCache.value
    }
    
    // If already fetching, return the same promise (avoid duplicate requests)
    if (ipFetchPromise.value) {
      return ipFetchPromise.value
    }
    
    // Fetch IP and cache it
    ipFetchPromise.value = getPublicIp()
    const ip = await ipFetchPromise.value
    publicIpCache.value = ip
    ipFetchPromise.value = null // Clear promise after completion
    
    return ip
  }

  // Validate QR code
  async function validateQR(qrToken: string) {
    const loadingStore = useLoadingStore()
    loadingStore.show('Validating QR code...')
    error.value = null

    // Ensure IP is fetched (uses cache if already fetched)
    await preFetchPublicIp()

    try {
      currentValidation.value = await attendanceApi.validateQR(qrToken)

      if (currentValidation.value.valid) {
        toast.success('QR Code Valid', {
          description: `Office: ${currentValidation.value.office?.name}`,
        })
      } else {
        toast.error('Invalid QR Code', {
          description: currentValidation.value.message,
        })
      }

      return {
        success: currentValidation.value.valid,
        data: currentValidation.value,
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to validate QR code'
      toast.error(`Validation Failed: ${error.value}`)
      return {
        success: false,
        error: error.value,
      }
    } finally {
      loadingStore.hide()
    }
  }

  // Clear validation
  function clearValidation() {
    currentValidation.value = null
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    currentValidation,
    isLoading,
    error,
    // Computed
    hasValidQR,
    officeName,
    // Actions
    validateQR,
    preFetchPublicIp, // Pre-fetch IP to avoid delay during scan
    clearValidation,
    clearError,
  }
})
