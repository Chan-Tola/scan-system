<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>Early Leave Reason</DialogTitle>
        <DialogDescription>
          You are leaving before the shift end time. Please provide a reason for your early
          departure.
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4 py-4">
        <div class="space-y-2">
          <Label for="reason">Reason for Early Leave</Label>
          <Textarea
            id="reason"
            v-model="reason"
            placeholder="Please explain why you need to leave early..."
            rows="4"
            :disabled="isLoading"
            class="resize-none"
          />
          <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>
      </div>

      <DialogFooter class="gap-2">
        <Button type="button" variant="outline" @click="handleCancel" :disabled="isLoading">
          Cancel
        </Button>
        <Button type="button" @click="handleSubmit" :disabled="isLoading || !reason.trim()">
          <span v-if="!isLoading">Submit & Check Out</span>
          <span v-else class="flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
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
            Submitting...
          </span>
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'

interface Props {
  open: boolean
  isLoading?: boolean
}

interface Emits {
  (e: 'update:open', value: boolean): void
  (e: 'submit', reason: string): void
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
})

const emit = defineEmits<Emits>()

// Local state
const isOpen = ref(props.open)
const reason = ref('')
const errorMessage = ref('')

// Watch for prop changes
watch(
  () => props.open,
  (newValue) => {
    isOpen.value = newValue
    if (newValue) {
      // Reset form when dialog opens
      reason.value = ''
      errorMessage.value = ''
    }
  },
)

// Watch for local changes
watch(isOpen, (newValue) => {
  emit('update:open', newValue)
})

// Methods
const handleSubmit = () => {
  errorMessage.value = ''

  if (!reason.value.trim()) {
    errorMessage.value = 'Please provide a reason for early leave'
    return
  }

  if (reason.value.trim().length < 10) {
    errorMessage.value = 'Please provide a more detailed reason (at least 10 characters)'
    return
  }

  emit('submit', reason.value.trim())
}

const handleCancel = () => {
  isOpen.value = false
}
</script>
