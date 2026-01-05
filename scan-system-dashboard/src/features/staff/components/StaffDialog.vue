<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { Plus, Upload, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type { StaffMember, StaffCreate, UserRoleName } from '../types'
import { useStaff } from '../composables/useStaff'
import { useOffice } from '@/features/office/composables/useOffice'

interface Props {
  mode?: 'create' | 'edit'
  user?: StaffMember | null
  open?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'create',
  open: false,
})

const emit = defineEmits(['update:open', 'success'])

const { handleCreateStaff, handleUpdateStaff, isLoading, error } = useStaff()
const { offices, loadOffices } = useOffice()

// Form State
const internalOpen = ref(false)
const localError = ref('')
const previewImage = ref<string | null>(null)

// Initialize form matching StaffCreate interface
const form = ref<StaffCreate>({
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  role: 'staff',
  office_id: 0,
  gender: 'male',
  address: '',
  date_of_birth: '',
  join_date: new Date().toISOString().split('T')[0] ?? '',
  profile_image: null,
})

// Load offices
onMounted(() => {
  loadOffices()
})

// Sync with props
watch(
  () => props.open,
  (val) => (internalOpen.value = val),
)

watch(
  () => props.user,
  (val) => {
    if (val && props.mode === 'edit') {
      // Populate form for edit
      form.value = {
        username: val.user.username,
        email: val.user.email,
        full_name: val.full_name,
        phone: val.phone,
        role: val.user.roles[0]?.name || 'staff',
        office_id: val.office.id,
        gender: val.gender,
        address: val.address,
        date_of_birth: val.date_of_birth,
        join_date: val.join_date,
      }
      previewImage.value = val.profile_image || null
    } else {
      resetForm()
    }
  },
  { immediate: true },
)

function resetForm() {
  form.value = {
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
    role: 'staff',
    office_id: 0,
    gender: 'male',
    address: '',
    date_of_birth: '',
    join_date: new Date().toISOString().split('T')[0] ?? '',
    profile_image: null,
  }
  previewImage.value = null
}

const handleOpenChange = (open: boolean) => {
  if (props.mode === 'create') internalOpen.value = open
  emit('update:open', open)
  if (!open) localError.value = ''
}

const handleFileChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    form.value.profile_image = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const removeImage = () => {
  form.value.profile_image = null
  previewImage.value = null
}

const handleSave = async () => {
  localError.value = ''

  // Basic Validation
  if (!form.value.full_name || !form.value.email || !form.value.username) {
    localError.value = 'Please fill in all required fields'
    return
  }

  if (props.mode === 'create') {
    if (!form.value.password) {
      localError.value = 'Password is required'
      return
    }
  }

  // Ensure office_id is a number
  form.value.office_id = Number(form.value.office_id)
  if (form.value.office_id === 0) {
    localError.value = 'Please select an office'
    return
  }

  // Debug: Log form data before submission
  console.log('Form data before submission:', form.value)
  console.log('Profile image:', form.value.profile_image)

  let result
  if (props.mode === 'create') {
    result = await handleCreateStaff(form.value)
  } else {
    // Update logic
    if (props.user?.id) {
      result = await handleUpdateStaff(props.user.id, form.value)
    }
  }

  if (result) {
    emit('success')
    handleOpenChange(false)
  } else {
    // Error is handled in store/composable, but we can set local error if needed
    if (error.value) localError.value = error.value
  }
}
</script>

<template>
  <Dialog :open="internalOpen" @update:open="handleOpenChange">
    <!-- Trigger for Create mode -->
    <DialogTrigger as-child v-if="mode === 'create'">
      <Button class="bg-emerald-600 hover:bg-emerald-700 text-white gap-2 shadow-sm font-semibold">
        <Plus class="w-4 h-4" />
        Create Staff
      </Button>
    </DialogTrigger>

    <DialogContent class="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle class="text-xl font-bold tracking-tight text-slate-900">
          {{ mode === 'edit' ? 'Edit Staff Member' : 'Add New Staff Member' }}
        </DialogTitle>
        <DialogDescription class="text-slate-500">
          {{
            mode === 'edit'
              ? 'Update the details for this staff member.'
              : 'Enter the details for the new staff member.'
          }}
        </DialogDescription>
      </DialogHeader>

      <div class="grid gap-5 py-4">
        <div
          v-if="error || localError"
          class="rounded-lg bg-destructive/10 p-3 text-sm text-destructive font-medium"
        >
          {{ error || localError }}
        </div>

        <!-- Image Upload -->
        <div class="flex flex-col items-center justify-center gap-4 py-2">
          <div class="relative group">
            <div
              class="w-24 h-24 rounded-full bg-slate-100 border-2 border-slate-200 flex items-center justify-center overflow-hidden"
            >
              <img v-if="previewImage" :src="previewImage" class="w-full h-full object-cover" />
              <Upload v-else class="w-8 h-8 text-slate-400" />
            </div>
            <div class="absolute -bottom-1 -right-1" v-if="!previewImage">
              <div class="bg-slate-900 text-white p-1.5 rounded-full shadow-sm">
                <Plus class="w-3 h-3" />
              </div>
            </div>
            <button
              v-if="previewImage"
              @click="removeImage"
              class="absolute -top-1 -right-1 bg-destructive text-white p-1 rounded-full shadow-sm hover:bg-destructive/90 transition-colors"
            >
              <X class="w-3 h-3" />
            </button>
            <input
              type="file"
              accept="image/*"
              @change="handleFileChange"
              class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
          </div>
          <p class="text-xs text-slate-500">Upload profile photo</p>
        </div>

        <!-- Basic Info -->
        <div class="grid grid-cols-2 gap-4">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Full Name <span class="text-destructive">*</span></Label
            >
            <Input v-model="form.full_name" placeholder="fullname" class="h-9" />
          </div>
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Email <span class="text-destructive">*</span></Label
            >
            <Input
              v-model="form.email"
              type="email"
              placeholder="example@gmail.com"
              class="h-9"
              :disabled="mode === 'edit'"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Username <span class="text-destructive">*</span></Label
            >
            <Input v-model="form.username" placeholder="username" class="h-9" />
          </div>
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Phone Number</Label
            >
            <Input v-model="form.phone" placeholder="012 345 678" class="h-9" />
          </div>
        </div>

        <!-- Password Section (Create Only) -->
        <div class="grid grid-cols-2 gap-4" v-if="mode === 'create'">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Password <span class="text-destructive">*</span></Label
            >
            <Input v-model="form.password" type="password" placeholder="" class="h-9" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Gender</Label
            >
            <select
              v-model="form.gender"
              class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Role <span class="text-destructive">*</span></Label
            >
            <select
              v-model="form.role"
              class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
            >
              <option value="staff">Staff</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        </div>

        <div class="grid gap-2">
          <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
            >Address</Label
          >
          <Input v-model="form.address" placeholder="123 Street, City" class="h-9" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Date of Birth</Label
            >
            <Input type="date" v-model="form.date_of_birth" class="h-9" />
          </div>
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Join Date</Label
            >
            <Input type="date" v-model="form.join_date" class="h-9" />
          </div>
        </div>

        <div class="grid gap-2 border-t border-slate-100 pt-2">
          <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
            >Office Location <span class="text-destructive">*</span></Label
          >
          <select
            v-model="form.office_id"
            class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          >
            <option value="0" disabled>Select office</option>
            <option v-for="office in offices" :key="office.id" :value="office.id">
              {{ office.name }}
            </option>
          </select>
          <p class="text-[10px] text-muted-foreground">
            Staff shift time will be inherited from the selected office.
          </p>
        </div>
      </div>
      <DialogFooter class="gap-2 sm:gap-0">
        <Button variant="outline" @click="handleOpenChange(false)">Cancel</Button>
        <Button
          @click="handleSave"
          :disabled="isLoading || !form.full_name || !form.email"
          class="bg-slate-900 text-white hover:bg-slate-800"
        >
          {{ isLoading ? 'Saving...' : mode === 'edit' ? 'Update Staff' : 'Create Staff' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
