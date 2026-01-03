import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { qrGenerateApi } from '../services/qrGenerateApi'
import type { GenerateQRCodeRequest, GenerateQRCodeResponse, OfficeInfo, QRCodeResponse } from '../types'

export const useQRGenerateStore = defineStore('qrGenerate', () => {
  const qrCodes = ref<QRCodeResponse[]>([])
  const currentQRCode = ref<GenerateQRCodeResponse | null>(null)
  const selectedOfficeId = ref<number | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const qrCodesCount = computed(() => qrCodes.value.length)
  const activeQRCodes = computed(() => qrCodes.value.filter((qr) => qr.is_active))

  // Check if selected office has an existing QR code
  const hasQRCodeForSelectedOffice = computed(() => {
    if (!selectedOfficeId.value) return false
    return qrCodes.value.some((qr) => qr.office_id === selectedOfficeId.value && qr.is_active)
  })

  // Get existing QR code for selected office
  const getQRCodeForSelectedOffice = computed(() => {
    if (!selectedOfficeId.value) return null
    return (
      qrCodes.value.find((qr) => qr.office_id === selectedOfficeId.value && qr.is_active) || null
    )
  })

  // Load existing QR code for an office (with image)
async function loadQRCodeForOffice(officeId: number) {
    isLoading.value = true
    error.value = null
    try {
      // First, fetch QR codes for this office
      const qrCodesList = await qrGenerateApi.getQRCodes({
        office_id: officeId,
        is_active: true,
      })
  
      if (qrCodesList.length === 0) {
        currentQRCode.value = null
        return { success: true, qrCode: null }
      }
  
      // Get the most recent active QR code
      const existingQR = qrCodesList[0]
      
      // Type guard: ensure existingQR exists
      if (!existingQR) {
        currentQRCode.value = null
        return { success: true, qrCode: null }
      }
  
      // Fetch the image for this QR code
      const imageData = await qrGenerateApi.getQRCodeImage(existingQR.id)
  
      // Ensure office info exists, create fallback if null
      const officeInfo: OfficeInfo = existingQR.office || {
        id: officeId,
        name: 'Unknown Office',
        public_ip: '',
      }
  
      // Combine QR code data with image to create GenerateQRCodeResponse
      currentQRCode.value = {
        id: existingQR.id,
        office_id: existingQR.office_id,
        qr_token: existingQR.qr_token,
        is_active: existingQR.is_active,
        qr_code_image: imageData.qr_code_image,
        office: officeInfo,
        created_at: existingQR.created_at,
        updated_at: existingQR.updated_at,
      }
  
      return { success: true, qrCode: currentQRCode.value }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load QR code'
      console.error('Failed to load QR code for office:', err)
      currentQRCode.value = null
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Generate new QR code
  async function generateQRCode(officeId: number) {
    isLoading.value = true
    error.value = null
    try {
      const request: GenerateQRCodeRequest = { office_id: officeId }
      currentQRCode.value = await qrGenerateApi.generateQRCode(request)
      // Refresh list after generation
      await fetchQRCodes({ office_id: officeId })
      return { success: true, qrCode: currentQRCode.value }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to generate QR code'
      console.error('Failed to generate QR code:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Regenerate QR code
  async function regenerateQRCode(qrCodeId: number) {
    isLoading.value = true
    error.value = null
    try {
      // Call the regenerate API - this updates the backend and returns the new QR code
      const regeneratedQR = await qrGenerateApi.regenerateQRCode(qrCodeId)
      
      // Update currentQRCode with the response from backend (this has the new token)
      currentQRCode.value = regeneratedQR
      
      // Refresh the QR codes list for the selected office (without loading state to avoid flickering)
      if (selectedOfficeId.value) {
        // Update the list in the background without setting loading state
        try {
          const updatedList = await qrGenerateApi.getQRCodes({ 
            office_id: selectedOfficeId.value, 
            is_active: true 
          })
          qrCodes.value = updatedList
        } catch (listErr) {
          console.warn('Failed to refresh QR codes list:', listErr)
          // Don't fail the whole operation if list refresh fails
        }
      } else {
        // If no office selected, just refresh all QR codes
        try {
          qrCodes.value = await qrGenerateApi.getQRCodes()
        } catch (listErr) {
          console.warn('Failed to refresh QR codes list:', listErr)
        }
      }

      return { success: true, qrCode: currentQRCode.value }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to regenerate QR code'
      console.error('Failed to regenerate QR code:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Fetch all QR codes
  async function fetchQRCodes(params?: {
    skip?: number
    limit?: number
    is_active?: boolean
    office_id?: number
  }) {
    isLoading.value = true
    error.value = null
    try {
      qrCodes.value = await qrGenerateApi.getQRCodes(params)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch QR codes'
      console.error('Failed to fetch QR codes:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fetch QR code by ID
  async function fetchQRCodeById(qrCodeId: number) {
    isLoading.value = true
    error.value = null
    try {
      const qrCode = await qrGenerateApi.getQRCodeById(qrCodeId)
      // Convert to GenerateQRCodeResponse format if needed
      return { success: true, qrCode }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch QR code'
      console.error('Failed to fetch QR code:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Delete QR code (soft delete)
  async function deleteQRCode(qrCodeId: number) {
    isLoading.value = true
    error.value = null
    try {
      await qrGenerateApi.deleteQRCode(qrCodeId)
      qrCodes.value = qrCodes.value.filter((qr) => qr.id !== qrCodeId)
      if (currentQRCode.value?.id === qrCodeId) {
        currentQRCode.value = null
      }
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete QR code'
      console.error('Failed to delete QR code:', err)
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Set selected office and load its QR code if exists
  async function setSelectedOffice(officeId: number | null) {
    selectedOfficeId.value = officeId
    if (officeId) {
      // Load existing QR code for this office
      await loadQRCodeForOffice(officeId)
    } else {
      currentQRCode.value = null
    }
  }

  // Clear current QR code
  function clearCurrentQRCode() {
    currentQRCode.value = null
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    qrCodes,
    currentQRCode,
    selectedOfficeId,
    isLoading,
    error,
    // Computed
    qrCodesCount,
    activeQRCodes,
    hasQRCodeForSelectedOffice,
    getQRCodeForSelectedOffice,
    // Actions
    generateQRCode,
    regenerateQRCode,
    fetchQRCodes,
    fetchQRCodeById,
    deleteQRCode,
    loadQRCodeForOffice,
    setSelectedOffice,
    clearCurrentQRCode,
    clearError,
  }
})
