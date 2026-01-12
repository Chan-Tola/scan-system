<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { attendanceApi } from '@/features/scan/services/attendanceApi'
import type { CheckOutResponse } from '@/features/scan/types'
import EarlyLeaveReasonDialog from '@/features/scan/components/EarlyLeaveReasonDialog.vue'
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
import { Clock, LogOut, CheckCircle2, Loader2, AlertCircle } from 'lucide-vue-next'

const router = useRouter()

// State
const isLoading = ref(false)
const isCheckedOut = ref(false)
const errorMessage = ref<string>('')

const showEarlyLeaveDialog = ref(false)
const checkOutResponse = ref<CheckOutResponse | null>(null)

// Computed
const checkOutTime = computed(() => {
  const checkout = checkOutResponse.value?.attendance?.check_out
  if (!checkout) return ''

  const date = new Date(checkout)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  })
})

// Methods
const fetchTodayAttendance = async () => {
  try {
    const response = await attendanceApi.getTodayAttendance()

    // If already checked out, block this page
    if (response?.check_out) {
      toast.error('Already Checked Out', {
        description: 'You have already checked out today',
      })
      router.push('/attendance')
    }
  } catch (error: any) {
    console.error('Failed to fetch attendance:', error)
    errorMessage.value =
      error?.response?.data?.detail || 'Failed to load attendance data. Please try again.'
    toast.error('Error', { description: errorMessage.value })
  }
}

const handleCheckOut = () => {
  // Always collect reason for audit trail
  showEarlyLeaveDialog.value = true
}

const handleEarlyLeaveSubmit = async (reason: string) => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await attendanceApi.checkOut({
      reason_type: 'early_leave',
      reason,
    })

    checkOutResponse.value = response

    toast.success('Check-out Successful!', {
      description: response.is_early_leave
        ? `Early check-out recorded. Work hours: ${response.work_hours} hours`
        : `Check-out successful! Work hours: ${response.work_hours} hours`,
    })

    showEarlyLeaveDialog.value = false
    isCheckedOut.value = true

    window.setTimeout(() => {
      router.push('/dashboard')
    }, 3000)
  } catch (error: any) {
    console.error('Check-out failed:', error)
    errorMessage.value = error?.response?.data?.detail || 'Failed to check out'
    toast.error('Check-out Failed', { description: errorMessage.value })
  } finally {
    isLoading.value = false
  }
}

const handleCancel = () => router.push('/dashboard')

// Lifecycle
onMounted(() => {
  fetchTodayAttendance()
})
</script>

<template>
  <div
    class="container mx-auto min-h-[70svh] lg:min-h-[80svh] grid place-items-center px-4 py-6 md:p-8 animate-in fade-in duration-500"
  >
    <div class="w-full max-w-md">
      <!-- Check-Out Confirmation Card -->
      <Card v-if="!isCheckedOut" class="border-2 scale-95 sm:scale-100">
        <CardHeader class="text-center space-y-3 md:space-y-4 pb-3 md:pb-4">
          <div class="flex justify-center">
            <div
              class="w-12 h-12 md:w-16 md:h-16 bg-primary rounded-full flex items-center justify-center"
            >
              <LogOut class="w-6 h-6 md:w-8 md:h-8 text-primary-foreground" />
            </div>
          </div>

          <div>
            <CardTitle class="text-xl md:text-2xl">Ready to Check Out</CardTitle>
            <CardDescription class="text-sm md:text-base mt-1 md:mt-2">
              Confirm your check-out
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent class="space-y-4 md:space-y-6">
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
            @click="handleCheckOut"
            :disabled="isLoading"
            class="w-full h-10 md:h-11 text-sm md:text-base"
          >
            <LogOut v-if="!isLoading" class="w-4 h-4 md:w-5 md:h-5 mr-2" />
            <Loader2 v-else class="w-4 h-4 md:w-5 md:h-5 mr-2 animate-spin" />
            {{ isLoading ? 'Checking Out...' : 'Check Out Now' }}
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

      <!-- Success State - After Check-Out -->
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
            <CardTitle class="text-2xl md:text-3xl">Check-out Successful</CardTitle>
            <CardDescription class="text-sm md:text-base mt-1 md:mt-2">
              Checked out at {{ checkOutTime }}
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent class="space-y-3 md:space-y-4">
          <div class="flex items-center justify-between p-4 md:p-6 border rounded-lg">
            <div>
              <p
                class="text-[10px] md:text-xs font-medium text-muted-foreground uppercase tracking-wide"
              >
                Total Work Hours
              </p>
              <p class="text-xl md:text-2xl font-bold mt-1">
                {{ checkOutResponse?.work_hours || 0 }} hours
              </p>
            </div>

            <div
              class="w-10 h-10 md:w-12 md:h-12 bg-primary rounded-full flex items-center justify-center"
            >
              <Clock class="w-5 h-5 md:w-6 md:h-6 text-primary-foreground" />
            </div>
          </div>

          <div v-if="checkOutResponse?.is_early_leave" class="flex justify-center pt-1 md:pt-2">
            <Badge variant="default" class="text-xs md:text-sm px-3 py-1 md:px-4 md:py-1.5">
              Early leave recorded
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>

    <EarlyLeaveReasonDialog
      v-model:open="showEarlyLeaveDialog"
      @submit="handleEarlyLeaveSubmit"
      :is-loading="isLoading"
    />
  </div>
</template>
