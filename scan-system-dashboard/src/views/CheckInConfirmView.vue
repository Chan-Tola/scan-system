<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4"
  >
    <div class="w-full max-w-md">
      <!-- Check-In Confirmation Card -->
      <div v-if="!isCheckedIn" class="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
        <!-- Header -->
        <div class="text-center space-y-2">
          <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
            <svg
              class="w-10 h-10 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">QR Code Validated!</h1>
          <p class="text-gray-600">Ready to check in</p>
        </div>

        <!-- Office Info -->
        <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 space-y-4">
          <div class="flex items-start space-x-3">
            <svg
              class="w-6 h-6 text-blue-600 mt-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              ></path>
            </svg>
            <div class="flex-1">
              <p class="text-sm text-gray-600">Office</p>
              <p class="text-lg font-semibold text-gray-900">{{ officeData?.name || 'Unknown' }}</p>
            </div>
          </div>

          <div class="flex items-start space-x-3">
            <svg
              class="w-6 h-6 text-blue-600 mt-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
            <div class="flex-1">
              <p class="text-sm text-gray-600">Current Time</p>
              <p class="text-lg font-semibold text-gray-900">{{ currentTime }}</p>
            </div>
          </div>
        </div>

        <!-- Check-in Button -->
        <button
          @click="handleCheckIn"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="!isLoading" class="flex items-center justify-center space-x-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
            <span>Check In Now</span>
          </span>
          <span v-else class="flex items-center justify-center space-x-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Checking In...</span>
          </span>
        </button>

        <!-- Cancel Button -->
        <button
          @click="handleCancel"
          :disabled="isLoading"
          class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>

        <!-- Error Message -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <svg class="w-5 h-5 text-red-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              ></path>
            </svg>
            <p class="text-sm text-red-800">{{ errorMessage }}</p>
          </div>
        </div>
      </div>

      <!-- Success State - After Check-In -->
      <div v-else class="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
        <!-- Success Icon -->
        <div class="text-center space-y-4">
          <div
            class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto animate-bounce"
          >
            <svg
              class="w-12 h-12 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-gray-900">Check-in Successful!</h1>
          <p class="text-gray-600">You have been checked in at {{ checkInTime }}</p>

          <!-- Late Status -->
          <div
            v-if="attendanceData?.is_late"
            class="bg-yellow-50 border border-yellow-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-center space-x-2">
              <svg class="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <p class="text-sm font-medium text-yellow-800">
                You are {{ attendanceData?.minutes_late }} minutes late
              </p>
            </div>
          </div>
        </div>

        <!-- Check-Out Button -->
        <button
          @click="handleCheckOut"
          :disabled="isCheckingOut"
          class="w-full bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="!isCheckingOut" class="flex items-center justify-center space-x-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              ></path>
            </svg>
            <span>Check Out</span>
          </span>
          <span v-else class="flex items-center justify-center space-x-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Checking Out...</span>
          </span>
        </button>

        <!-- Back to Dashboard -->
        <button
          @click="handleBackToDashboard"
          class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-xl transition-colors"
        >
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- Early Leave Reason Dialog -->
    <EarlyLeaveReasonDialog
      v-model:open="showEarlyLeaveDialog"
      @submit="handleEarlyLeaveSubmit"
      :is-loading="isCheckingOut"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { attendanceApi } from '@/features/scan/services/attendanceApi'
import { checkInConfirmApi } from '@/features/check-in-confirm/services/checkInConfirmApi'
import type { OfficeInfo } from '@/features/scan/types'
import type { CheckInResponse } from '@/features/scan/types'
import EarlyLeaveReasonDialog from '@/features/check-in-confirm/components/EarlyLeaveReasonDialog.vue'
import { toast } from 'vue-sonner'

const route = useRoute()
const router = useRouter()

// State
const qrToken = ref<string>('')
const officeData = ref<OfficeInfo | null>(null)
const currentTime = ref<string>('')
const isLoading = ref(false)
const isCheckedIn = ref(false)
const isCheckingOut = ref(false)
const errorMessage = ref<string>('')
const attendanceData = ref<CheckInResponse | null>(null)
const showEarlyLeaveDialog = ref(false)
const earlyLeaveReason = ref<string>('')

// Timer
let timeInterval: number | null = null

// Computed
const checkInTime = computed(() => {
  if (!attendanceData.value?.attendance?.check_in) return ''
  return attendanceData.value.attendance.check_in
})

// Methods
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  })
}

const handleCheckIn = async () => {
  if (!qrToken.value) {
    errorMessage.value = 'QR token is missing'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await attendanceApi.checkIn(qrToken.value)

    // Store attendance data
    attendanceData.value = response

    // Success!
    isCheckedIn.value = true

    toast.success('Check-in Successful!', {
      description: response.is_late
        ? `You are ${response.minutes_late} minutes late`
        : 'You are on time',
    })
  } catch (error: any) {
    console.error('Check-in failed:', error)
    errorMessage.value =
      error.response?.data?.detail || error.message || 'Failed to check in. Please try again.'

    toast.error('Check-in Failed', {
      description: errorMessage.value,
    })
  } finally {
    isLoading.value = false
  }
}

const handleCheckOut = async () => {
  // Always show dialog to collect reason for audit trail
  // Backend will determine if it's early leave based on shift_end time
  showEarlyLeaveDialog.value = true
}

const handleEarlyLeaveSubmit = async (reason: string) => {
  isCheckingOut.value = true

  try {
    const response = await checkInConfirmApi.checkOut({
      qr_token: qrToken.value,
      reason_type: 'early_leave',
      reason: reason,
    })

    const successMessage = response.is_early_leave
      ? `Early check-out recorded. Work hours: ${response.work_hours} hours`
      : `Check-out successful! Work hours: ${response.work_hours} hours`

    toast.success('Check-out Successful!', {
      description: successMessage,
    })

    // Close dialog
    showEarlyLeaveDialog.value = false

    // Redirect to dashboard after 2 seconds
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)
  } catch (error: any) {
    console.error('Check-out failed:', error)
    toast.error('Check-out Failed', {
      description: error.response?.data?.detail || 'Failed to check out',
    })
  } finally {
    isCheckingOut.value = false
  }
}

const handleCancel = () => {
  router.push('/attendance')
}

const handleBackToDashboard = () => {
  router.push('/dashboard')
}

// Lifecycle
onMounted(() => {
  // Get QR token and office data from route params
  qrToken.value = route.params.qrToken as string
  const officeParam = route.params.office as string

  if (!qrToken.value) {
    errorMessage.value = 'Invalid QR code data'
    toast.error('Invalid QR Code', {
      description: 'QR token is missing',
    })
    return
  }

  // Parse office data
  try {
    if (officeParam) {
      officeData.value = JSON.parse(decodeURIComponent(officeParam))
    }
  } catch (e) {
    console.error('Failed to parse office data:', e)
  }

  // Start time update
  updateCurrentTime()
  timeInterval = window.setInterval(updateCurrentTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style scoped>
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
</style>
