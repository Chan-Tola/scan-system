<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { attendanceApi } from '../services/attendanceApi'
import type { PermissionRequest } from '../types'
import { toast } from 'vue-sonner'
import { Label } from '@/components/ui/label'
import Textarea from '@/components/ui/textarea/Textarea.vue'

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{
  'update:open': [value: boolean]
  success: []
}>()

const isOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value),
})

const isLoading = ref(false)
const errorMessage = ref('')
const reason = ref('')

// today (YYYY-MM-DD)
const todayDate = computed(() => new Date().toISOString().split('T')[0] ?? '')

const resetForm = () => {
  reason.value = ''
  errorMessage.value = ''
}

watch(
  () => props.open,
  (v) => {
    if (!v) resetForm()
  },
)

const handleSubmit = async () => {
  errorMessage.value = ''
  isLoading.value = true

  const payload: PermissionRequest = {
    date: todayDate.value,
    reason_type: 'absent',
    reason: reason.value.trim(),
  }

  try {
    await attendanceApi.submitPermission(payload)

    toast.success('Request Submitted', {
      description: `Absent request submitted for ${todayDate.value}.`,
    })

    emit('success')
    isOpen.value = false
    resetForm()
  } catch (error: any) {
    errorMessage.value =
      error?.response?.data?.detail || 'Failed to submit request. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleCancel = () => {
  resetForm()
  isOpen.value = false
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="w-[92vw] max-w-sm sm:max-w-md p-4 sm:p-6">
      <DialogHeader>
        <DialogTitle class="text-base sm:text-lg"> Request Absent Permission </DialogTitle>

        <DialogDescription class="text-xs sm:text-sm leading-relaxed">
          Today: <span class="font-medium">{{ todayDate }}</span> • Type:
          <span class="font-medium">Absent</span>
        </DialogDescription>
      </DialogHeader>

      <!-- ✅ Use native form -->
      <form @submit.prevent="handleSubmit" class="space-y-3 sm:space-y-4">
        <!-- Reason -->
        <div class="space-y-1.5 sm:space-y-2">
          <Label class="text-xs sm:text-sm font-medium">Reason</Label>
          <Textarea
            v-model="reason"
            :disabled="isLoading"
            :rows="3"
            placeholder="Write your reason..."
            class="resize-none text-sm sm:text-base"
          />
        </div>

        <!-- Error -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-xs sm:text-sm text-red-800">{{ errorMessage }}</p>
        </div>

        <!-- Actions -->
        <DialogFooter class="gap-2">
          <Button
            type="button"
            variant="outline"
            @click="handleCancel"
            :disabled="isLoading"
            class="h-9 text-sm"
          >
            Cancel
          </Button>

          <Button type="submit" :disabled="isLoading || !reason.trim()" class="h-9 text-sm">
            <span v-if="!isLoading">Submit</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Submitting...
            </span>
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
