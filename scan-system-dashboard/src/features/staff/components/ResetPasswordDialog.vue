<script setup lang="ts">
// 1. Import necessary components and utilities
import { ref } from 'vue'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { KeyRound, Eye, EyeOff } from 'lucide-vue-next'
import type { StaffMember } from '../types'
import { staffApi } from '../services/staffApi'
import { useLoadingStore } from '@/stores/loadingStore'
import { toast } from 'vue-sonner'
// 2. Define props
interface Props {
  open: boolean
  user: StaffMember | null
}
const props = defineProps<Props>()
// 3. Define emits
const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'success'): void
}>()
// 4. Create reactive state
const newPassword = ref('')
const error = ref('')
const showPassword = ref(false)
// 5. Handle password reset
const handleReset = async () => {
  // Clear previous error
  error.value = ''
  // Validate password
  if (!newPassword.value || newPassword.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }
  // Show loading
  const loadingStore = useLoadingStore()
  loadingStore.show('Resetting password...')
  try {
    // Call API to update password
    await staffApi.updateStaff(props.user!.id, {
      password: newPassword.value,
    })
    // Show success toast
    toast.success(`Password reset for ${props.user!.full_name}`)
    // Emit success event
    emit('success')
    // Close dialog
    closeDialog()
  } catch (err: any) {
    // Show error toast
    toast.error('Failed to reset password')
    error.value = err.message || 'An error occurred'
  } finally {
    // Hide loading
    loadingStore.hide()
  }
}
// 6. Handle dialog close
const closeDialog = () => {
  newPassword.value = ''
  error.value = ''
  showPassword.value = false
  emit('update:open', false)
}
</script>
<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogContent class="sm:max-w-md">
      <!-- Header -->
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2">
          <KeyRound class="h-5 w-5" />
          Reset Password
        </DialogTitle>
      </DialogHeader>
      <!-- Content -->
      <div class="space-y-4 py-4">
        <!-- User info card -->
        <div class="rounded-lg bg-muted p-3">
          <p class="text-sm text-muted-foreground">Reset password for:</p>
          <p class="font-semibold">{{ user?.full_name }}</p>
          <p class="text-sm text-muted-foreground">@{{ user?.username }}</p>
        </div>
        <!-- Password input -->
        <div class="space-y-2">
          <Label for="new-password">New Password</Label>
          <div class="relative">
            <Input
              id="new-password"
              v-model="newPassword"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter new password"
              class="pr-10"
              @keyup.enter="handleReset"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            >
              <Eye v-if="!showPassword" class="h-4 w-4" />
              <EyeOff v-else class="h-4 w-4" />
            </button>
          </div>
          <p class="text-xs text-muted-foreground">Minimum 6 characters</p>

          <!-- Error message -->
          <p v-if="error" class="text-xs text-destructive">{{ error }}</p>
        </div>
      </div>
      <!-- Footer buttons -->
      <div class="flex justify-end gap-2">
        <Button variant="outline" @click="closeDialog">Cancel</Button>
        <Button @click="handleReset">Reset Password</Button>
      </div>
    </DialogContent>
  </Dialog>
</template>
