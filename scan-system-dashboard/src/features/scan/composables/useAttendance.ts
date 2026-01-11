import { useAttendanceStore } from '../store/attendanceStore'
import { storeToRefs } from 'pinia'

export function useAttendance() {
  const attendanceStore = useAttendanceStore()

  // Reactive state
  const { currentValidation, hasValidQR, officeName, isLoading, error } =
    storeToRefs(attendanceStore)

  // Actions
  const { validateQR, preFetchPublicIp, clearValidation, clearError } = attendanceStore

  // Helper: Handle QR scan
  const handleQrScan = async (qrToken: string, onSuccess?: () => void) => {
    const result = await validateQR(qrToken)

    if (result.success && onSuccess) {
      onSuccess()
    }

    return result
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
    preFetchPublicIp,
    clearValidation,
    clearError,
    // Helpers
    handleQrScan,
  }
}
