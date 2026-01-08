<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Separator } from '@/components/ui/separator'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { ref, computed } from 'vue'
import { useAuthStore } from '@/features/auth'
import { useAccountStore } from '../stores/accountStore'
import type { StaffUpdate } from '@/features/staff/types'

const authStore = useAuthStore()
const accountStore = useAccountStore()

const form = ref<StaffUpdate>({
  full_name: authStore.user?.profile?.full_name || '',
  phone: authStore.user?.profile?.phone || '',
  address: authStore.user?.profile?.address || '',
  gender: authStore.user?.profile?.gender || 'male',
  date_of_birth: authStore.user?.profile?.date_of_birth || '',
  shift_start: authStore.user?.profile?.shift_start || '',
  shift_end: authStore.user?.profile?.shift_end || '',
})

// Image Preview
const profileImage = ref<File | null>(null)
const imagePreview = ref<string | null>(authStore.user?.profile?.profile_image || null)

// Handle Image selection
function handleImageChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (file) {
    profileImage.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

// Submit Form
async function handleSubmit() {
  const updateData: StaffUpdate = {
    ...form.value,
  }

  // Add Image if selected
  if (profileImage.value) {
    updateData.profile_image = profileImage.value
  }

  const result = await accountStore.updateProfile(updateData)

  if (result.success) {
    // Reset image file input
    profileImage.value = null
  }
}

const isAdmin = computed(() => authStore.user?.role === 'admin')
</script>

<
<template>
  <div class="min-h-full bg-background p-6 text-foreground">
    <div class="mx-auto max-w-3xl">
      <Card class="shadow-sm">
        <CardHeader class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <CardTitle>Account Settings</CardTitle>
            <CardDescription>Update your profile details and preferences.</CardDescription>
          </div>

          <Button type="submit" form="account-form" class="hidden sm:inline-flex">
            Update Profile
          </Button>
        </CardHeader>

        <CardContent>
          <form id="account-form" class="space-y-6" @submit.prevent="handleSubmit">
            <!-- Profile Image -->
            <div class="space-y-2">
              <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                Profile Image
              </Label>

              <div class="flex items-center gap-4">
                <div class="h-20 w-20 overflow-hidden rounded-full border bg-muted">
                  <img
                    v-if="imagePreview"
                    :src="imagePreview"
                    alt="Profile"
                    class="h-full w-full object-cover"
                  />
                  <div
                    v-else
                    class="grid h-full w-full place-items-center text-xl font-bold text-muted-foreground"
                  >
                    U
                  </div>
                </div>

                <div class="space-y-2">
                  <p class="text-sm text-muted-foreground">JPG/PNG. Click to upload or replace.</p>

                  <!-- shadcn Button as label -->
                  <Button variant="outline" as-child>
                    <label class="cursor-pointer">
                      Choose Image
                      <input
                        type="file"
                        accept="image/*"
                        class="hidden"
                        @change="handleImageChange"
                      />
                    </label>
                  </Button>
                </div>
              </div>
            </div>

            <Separator />

            <!-- Full name + phone -->
            <div class="grid gap-4 sm:grid-cols-2">
              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Full Name
                </Label>
                <Input v-model="form.full_name" required placeholder="Full name" />
              </div>

              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Phone
                </Label>
                <Input v-model="form.phone" type="tel" placeholder="Phone number" />
              </div>
            </div>

            <!-- Address -->
            <div class="space-y-2">
              <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                Address
              </Label>
              <Textarea v-model="form.address" rows="3" placeholder="Address" />
            </div>

            <!-- Gender + DOB -->
            <div class="grid gap-4 sm:grid-cols-2">
              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Gender
                </Label>

                <Select v-model="form.gender">
                  <SelectTrigger>
                    <SelectValue placeholder="Select gender" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Date of Birth
                </Label>
                <Input v-model="form.date_of_birth" type="date" />
              </div>
            </div>

            <!-- Shift -->
            <div class="grid gap-4 sm:grid-cols-2">
              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Shift Start
                </Label>
                <Input v-model="form.shift_start" type="time" />
              </div>

              <div class="space-y-2">
                <Label class="text-xs uppercase tracking-wider text-muted-foreground">
                  Shift End
                </Label>
                <Input v-model="form.shift_end" type="time" />
              </div>
            </div>

            <!-- Admin note -->
            <Alert v-if="isAdmin">
              <AlertTitle>Admin Settings</AlertTitle>
              <AlertDescription>
                To change username, email, or role, use the Staff Management page.
              </AlertDescription>
            </Alert>

            <!-- Mobile submit -->
            <Button type="submit" class="w-full sm:hidden"> Update Profile </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
