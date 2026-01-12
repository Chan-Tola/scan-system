<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { attendanceApi } from '@/features/scan/services/attendanceApi'
import type { CheckInResponse } from '@/features/scan/types'
import { toast } from 'vue-sonner'

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { CheckCircle2, Loader2, AlertCircle } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

// State
const qrToken = ref<string>('')
const isLoading = ref(false)
const isCheckedIn = ref(false)
const errorMessage = ref<string>('')

const attendanceData = ref<CheckInResponse | null>(null)

// Computed
const checkInTime = computed(() => {
  const checkIn = attendanceData.value?.attendance?.check_in
  if (!checkIn) return ''

  const date = new Date(checkIn)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  })
})

// Methods
const handleCheckIn = async () => {
  if (!qrToken.value) {
    errorMessage.value = 'QR token is missing'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await attendanceApi.checkIn(qrToken.value)
    attendanceData.value = response
    isCheckedIn.value = true

    toast.success('Check-in Successful!', {
      description: response.is_late
        ? `You are ${response.minutes_late} minutes late`
        : 'You are on time',
    })
  } catch (error: any) {
    console.error('Check-in failed:', error)

    errorMessage.value =
      error?.response?.data?.detail || error?.message || 'Failed to check in. Please try again.'

    toast.error('Check-in Failed', { description: errorMessage.value })
  } finally {
    isLoading.value = false
  }
}

const handleCancel = () => router.push('/attendance')
const handleBackToDashboard = () => router.push('/dashboard')

// Lifecycle
onMounted(() => {
  qrToken.value = route.params.qrToken as string

  if (!qrToken.value) {
    errorMessage.value = 'Invalid QR code data'
    toast.error('Invalid QR Code', { description: 'QR token is missing' })
  }
})
</script>

<template>
  <div
    class="container mx-auto min-h-[70svh] lg:min-h-[80svh] grid place-items-center px-4 py-6 md:p-8 animate-in fade-in duration-500"
  >
    <div class="w-full max-w-md">
      <!-- Check-In Confirmation Card -->
      <Card v-if="!isCheckedIn" class="border-2 scale-95 sm:scale-100">
        <CardHeader class="text-center space-y-3 md:space-y-4 pb-3 md:pb-4">
          <div class="flex justify-center">
            <div
              class="w-12 h-12 md:w-16 md:h-16 bg-primary rounded-full flex items-center justify-center"
            >
              <CheckCircle2 class="w-7 h-7 md:w-8 md:h-8 text-primary-foreground" />
            </div>
          </div>

          <div>
            <CardTitle class="text-xl md:text-2xl">QR Code Validated</CardTitle>
            <CardDescription class="text-sm md:text-base mt-1 md:mt-2">
              Ready to check in
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent class="space-y-4 md:space-y-6">
          <!-- Error Message -->
          <div
            v-if="errorMessage"
            class="flex items-start gap-3 p-3 md:p-4 border border-destructive/50 bg-destructive/10 rounded-lg"
          >
            <AlertCircle class="w-4 h-4 md:w-5 md:h-5 text-destructive flex-shrink-0 mt-0.5" />
            <p class="text-xs md:text-sm text-destructive">{{ errorMessage }}</p>
          </div>
        </CardContent>

        <CardFooter class="flex flex-col gap-2.5 md:gap-3">
          <Button
            @click="handleCheckIn"
            :disabled="isLoading || !qrToken"
            class="w-full h-10 md:h-11 text-sm md:text-base"
          >
            <CheckCircle2 v-if="!isLoading" class="w-4 h-4 md:w-5 md:h-5 mr-2" />
            <Loader2 v-else class="w-4 h-4 md:w-5 md:h-5 mr-2 animate-spin" />
            {{ isLoading ? 'Checking In...' : 'Check In Now' }}
          </Button>

          <Button
            @click="handleCancel"
            :disabled="isLoading"
            variant="outline"
            class="w-full h-9 md:h-10 text-sm"
          >
            Cancel
          </Button>
        </CardFooter>
      </Card>

      <!-- Success State - After Check-In -->
      <Card v-else class="border-2 scale-95 sm:scale-100">
        <CardHeader class="text-center space-y-3 md:space-y-4 pb-3 md:pb-4">
          <div class="flex justify-center">
            <div
              class="w-16 h-16 md:w-20 md:h-20 bg-primary rounded-full flex items-center justify-center"
            >
              <CheckCircle2 class="w-8 h-8 md:w-10 md:h-10 text-primary-foreground" />
            </div>
          </div>

          <div>
            <CardTitle class="text-2xl md:text-3xl">Check-in Successful</CardTitle>
            <CardDescription class="text-sm md:text-base mt-1 md:mt-2">
              Checked in at {{ checkInTime }}
            </CardDescription>
          </div>

          <!-- Late Badge -->
          <div v-if="attendanceData?.is_late" class="flex justify-center pt-2">
            <Badge variant="default" class="text-xs md:text-sm px-3 py-1 md:px-4 md:py-1.5">
              {{ attendanceData?.minutes_late }} minutes late
            </Badge>
          </div>
        </CardHeader>

        <CardContent class="space-y-4">
          <div class="flex items-center justify-between p-4 border rounded-lg">
            <div>
              <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                Status
              </p>
              <p class="text-base md:text-lg font-semibold mt-1">
                {{ attendanceData?.is_late ? 'Late Arrival' : 'On Time' }}
              </p>
            </div>

            <div
              :class="[
                'w-3 h-3 rounded-full',
                attendanceData?.is_late ? 'bg-muted-foreground' : 'bg-primary',
              ]"
            />
          </div>
        </CardContent>

        <CardFooter>
          <Button @click="handleBackToDashboard" class="w-full h-10 md:h-11 text-sm md:text-base">
            Back to Dashboard
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
