import { storeToRefs } from 'pinia'
import { useQRGenerateStore } from '../store/qrGenerateStore'

export function useQrGenerate() {
  const store = useQRGenerateStore()

  // Keep state reactive
  const {
    qrCodes,
    currentQRCode,
    selectedOfficeId,
    isLoading,
    error,
    qrCodesCount,
    activeQRCodes,
    hasQRCodeForSelectedOffice,
    getQRCodeForSelectedOffice,
  } = storeToRefs(store)

  // Generate QR Code for an office
  const handleGenerateQRCode = async (officeId: number) => {
    const result = await store.generateQRCode(officeId)
    if (result.success) {
      return result.qrCode
    }
    return null
  }

  // Regenerate QR Code
  const handleRegenerateQRCode = async (qrCodeId: number) => {
    const result = await store.regenerateQRCode(qrCodeId)
    if (result.success) {
      return result.qrCode
    }
    return null
  }

  // Load QR codes
  const loadQRCodes = async (params?: {
    skip?: number
    limit?: number
    is_active?: boolean
    office_id?: number
  }) => {
    return await store.fetchQRCodes(params)
  }

  // Load QR code by ID
  const loadQRCodeById = async (qrCodeId: number) => {
    const result = await store.fetchQRCodeById(qrCodeId)
    return result.success ? result.qrCode : null
  }

  // Load QR code for an office
  const loadQRCodeForOffice = async (officeId: number) => {
    const result = await store.loadQRCodeForOffice(officeId)
    return result.success ? result.qrCode : null
  }

  // Delete QR Code
  const handleDeleteQRCode = async (qrCodeId: number) => {
    const result = await store.deleteQRCode(qrCodeId)
    return result.success
  }

  // Select office (automatically loads QR code if exists)
  const selectOffice = async (officeId: number | null) => {
    await store.setSelectedOffice(officeId)
  }

  return {
    // State
    qrCodes,
    currentQRCode,
    selectedOfficeId,
    isLoading,
    error,
    qrCodesCount,
    activeQRCodes,
    hasQRCodeForSelectedOffice,
    getQRCodeForSelectedOffice,
    // Actions
    handleGenerateQRCode,
    handleRegenerateQRCode,
    loadQRCodes,
    loadQRCodeById,
    loadQRCodeForOffice,
    handleDeleteQRCode,
    selectOffice,
    clearCurrentQRCode: store.clearCurrentQRCode,
    clearError: store.clearError,
  }
}
