<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import {
  Plus,
  Upload,
  X,
  ChevronRight,
  ChevronLeft,
  User,
  Briefcase,
  CheckCircle2,
  Loader2,
} from 'lucide-vue-next'
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
import type { StaffMember, StaffCreate } from '../types'
import { useStaff } from '../composables/useStaff'
import { useOffice } from '@/features/office/composables/useOffice'
import { compressImage } from '../utils/imageCompression'
import { useAuthStore } from '@/features/auth/store/authStore'

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
const authStore = useAuthStore()

// --- UI STATE ---
const currentStep = ref(1)
const totalSteps = 2
const internalOpen = ref(false)
const localError = ref('')
const previewImage = ref<string | null>(null)

const currentUser = computed(() => authStore.user)
const isAdmin = computed(() => currentUser.value?.role === 'admin')
const isEditingSelf = computed(() => {
  if (props.mode === 'create') return false
  return currentUser.value?.id === props.user?.id
})

// --- FORM STATE ---
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

onMounted(() => loadOffices())

// --- WATCHERS & DIALOG LOGIC ---

// Watch dialog open/close state
watch(
  () => props.open,
  (val) => {
    internalOpen.value = val

    // When dialog opens
    if (val) {
      currentStep.value = 1
      localError.value = ''

      // IMPORTANT: Reset form when opening in create mode
      if (props.mode === 'create') {
        resetForm()
      }
    }

    // When dialog closes, clean up
    if (!val) {
      // Clean up preview image URL to prevent memory leaks
      if (previewImage.value && !previewImage.value.startsWith('http')) {
        URL.revokeObjectURL(previewImage.value)
      }

      // Reset form after a short delay (allows close animation to complete)
      setTimeout(() => {
        if (props.mode === 'create') {
          resetForm()
        }
      }, 200)
    }
  },
)

// Watch for user prop changes (for edit mode)
watch(
  () => props.user,
  (val) => {
    // EDIT MODE: Load user data into form
    if (val && props.mode === 'edit') {
      const matchingOffice = offices.value.find((o) => o.name === val.office_name)

      form.value = {
        username: val.username,
        email: val.email,
        full_name: val.full_name,
        phone: val.phone,
        role: val.role,
        office_id: matchingOffice ? matchingOffice.id : 0,
        gender: val.gender || 'male',
        address: val.address || '',
        date_of_birth: val.date_of_birth || '',
        join_date: val.join_date,
        profile_image: null,
      }

      // Clear preview image when switching users
      if (previewImage.value && !previewImage.value.startsWith('http')) {
        URL.revokeObjectURL(previewImage.value)
      }
      previewImage.value = null
    }
    // CREATE MODE: Reset form when user prop becomes null
    else if (props.mode === 'create') {
      resetForm()
    }
  },
  { immediate: true },
)

// Reset form to initial empty state
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

  // Clean up preview image
  if (previewImage.value && !previewImage.value.startsWith('http')) {
    URL.revokeObjectURL(previewImage.value)
  }
  previewImage.value = null
  currentStep.value = 1
  localError.value = ''
}

// Handle dialog open/close state changes
const handleOpenChange = (open: boolean) => {
  // Update internal state for create mode
  if (props.mode === 'create') {
    internalOpen.value = open
  }

  // Emit to parent component
  emit('update:open', open)
}

// Handle file selection with automatic compression
const handleFileChange = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]

  if (file) {
    try {
      // Compress image before setting it in the form
      // This significantly reduces upload time and file size
      const compressedFile = await compressImage(file, {
        maxWidth: 800,
        maxHeight: 800,
        maxSizeMB: 1, // Target 1MB or less
        quality: 0.8, // 80% quality (good balance)
      })

      // Validate that we have a valid File object
      if (!(compressedFile instanceof File)) {
        form.value.profile_image = file
        previewImage.value = URL.createObjectURL(file)
        return
      }

      // Clean up old preview URL to prevent memory leaks
      if (previewImage.value) {
        URL.revokeObjectURL(previewImage.value)
      }

      // Create preview URL from compressed file
      previewImage.value = URL.createObjectURL(compressedFile)

      // Set compressed file in form for upload
      form.value.profile_image = compressedFile

      console.log('File ready for upload:', {
        name: compressedFile.name,
        type: compressedFile.type,
        size: compressedFile.size,
        isFile: compressedFile instanceof File,
        originalSize: (file.size / (1024 * 1024)).toFixed(2) + 'MB',
        compressedSize: (compressedFile.size / (1024 * 1024)).toFixed(2) + 'MB',
      })
    } catch (error) {
      // Fallback: use original file if compression fails
      if (previewImage.value) {
        URL.revokeObjectURL(previewImage.value)
      }
      previewImage.value = URL.createObjectURL(file)
      form.value.profile_image = file
    }
  } else {
    // Clear the file if no file selected
    form.value.profile_image = null
    if (previewImage.value) {
      URL.revokeObjectURL(previewImage.value)
      previewImage.value = null
    }
  }
}

const clearProfileImage = () => {
  form.value.profile_image = null
  if (previewImage.value && !previewImage.value.startsWith('http')) {
    URL.revokeObjectURL(previewImage.value)
  }
  previewImage.value = null
}

const isStep1Valid = computed(() => {
  const f = form.value
  // In Edit mode, we only strictly need full_name and email (email is disabled anyway)
  if (props.mode === 'edit') {
    return !!f.full_name && !!f.email
  }
  // In Create mode, we require the account credentials
  return !!f.full_name && !!f.email && !!f.username && !!f.password
})

const handleSave = async () => {
  localError.value = ''

  // Final validation
  if (Number(form.value.office_id) === 0) {
    localError.value = 'Please select an office location.'
    return
  }

  const result =
    props.mode === 'create'
      ? await handleCreateStaff(form.value)
      : await handleUpdateStaff(props.user!.id, form.value)

  if (result) {
    emit('success')
    handleOpenChange(false)
  }
}
</script>

<template>
  <Dialog :open="internalOpen" @update:open="handleOpenChange">
    <DialogTrigger as-child v-if="mode === 'create' && isAdmin">
      <Button class="gap-2 bg-black text-white hover:bg-black/90">
        <Plus class="w-4 h-4" /> Create Staff
      </Button>
    </DialogTrigger>

    <DialogContent class="sm:max-w-[600px] p-0 overflow-hidden border border-black/10 shadow-2xl">
      <!-- Header -->
      <div class="p-6 text-black relative">
        <div class="z-10 relative">
          <DialogTitle class="text-2xl font-semibold tracking-tight">
            {{ mode === 'edit' ? 'Update Staff Member' : 'Register New Staff' }}
          </DialogTitle>
          <DialogDescription class="text-black/60 mt-1">
            Step {{ currentStep }} of {{ totalSteps }}:
            {{ currentStep === 1 ? 'Personal Information' : 'Employment Details' }}
          </DialogDescription>
        </div>
      </div>

      <!-- Body -->
      <div class="p-8 bg-white">
        <div
          v-if="error || localError"
          class="mb-6 p-3 rounded-lg bg-black text-white text-sm flex items-center gap-2"
        >
          <X class="w-4 h-4" /> {{ error || localError }}
        </div>

        <div
          v-if="currentStep === 1"
          class="space-y-6 animate-in slide-in-from-right-4 duration-300"
        >
          <!-- Profile Image -->
          <div
            v-if="mode === 'create'"
            class="flex items-center gap-5 rounded-2xl border border-black/10 bg-white p-4"
          >
            <div class="relative group shrink-0">
              <div
                class="relative h-24 w-24 overflow-hidden rounded-full border border-black/10 bg-white"
              >
                <img v-if="previewImage" :src="previewImage" class="h-full w-full object-cover" />
                <User v-else class="h-full w-full p-6 text-black/20" />

                <input
                  type="file"
                  accept=".jpg,.jpeg,.png"
                  @change="handleFileChange"
                  class="absolute inset-0 z-10 cursor-pointer opacity-0"
                />

                <div
                  class="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 transition group-hover:opacity-100"
                >
                  <Upload class="h-6 w-6 text-white" />
                </div>
              </div>

              <button
                v-if="previewImage"
                type="button"
                @click.stop="clearProfileImage"
                class="absolute -right-2 -top-2 z-20 rounded-full bg-black p-1.5 text-white shadow hover:bg-black/80"
                aria-label="Remove image"
                title="Remove image"
              >
                <X class="h-4 w-4" />
              </button>
            </div>

            <div class="space-y-1">
              <h4 class="text-sm font-semibold text-black">Profile Image</h4>
              <p class="text-xs text-black/50 leading-relaxed">
                JPG or PNG. Click to upload or replace.
              </p>
            </div>
          </div>

          <!-- Step 1 fields -->
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Full Name
              </Label>
              <Input
                v-model="form.full_name"
                placeholder="Enter name"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>

            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Username
              </Label>
              <Input
                v-model="form.username"
                placeholder="username"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Email Address
              </Label>
              <Input
                v-model="form.email"
                type="email"
                placeholder="name@company.com"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>

            <div v-if="mode === 'create'" class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Initial Password
              </Label>
              <Input
                v-model="form.password"
                type="password"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div
          v-if="currentStep === 2"
          class="space-y-6 animate-in slide-in-from-right-4 duration-300"
        >
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Office Location
              </Label>
              <select
                v-model="form.office_id"
                class="flex h-11 w-full rounded-md border border-black/15 bg-white px-3 py-2 text-sm focus:outline-none focus:border-black"
              >
                <option value="0" disabled>Select Office</option>
                <option v-for="office in offices" :key="office.id" :value="office.id">
                  {{ office.name }}
                </option>
              </select>
            </div>

            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Role Type
              </Label>
              <select
                v-model="form.role"
                class="flex h-11 w-full rounded-md border border-black/15 bg-white px-3 py-2 text-sm focus:outline-none focus:border-black"
              >
                <option value="staff">Staff Member</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Phone Number
              </Label>
              <Input
                v-model="form.phone"
                placeholder="+855..."
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>

            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Gender
              </Label>
              <div class="flex gap-4 items-center h-11">
                <label class="flex items-center gap-2 text-sm font-medium text-black">
                  <input
                    type="radio"
                    v-model="form.gender"
                    value="male"
                    class="accent-black w-4 h-4"
                  />
                  Male
                </label>
                <label class="flex items-center gap-2 text-sm font-medium text-black">
                  <input
                    type="radio"
                    v-model="form.gender"
                    value="female"
                    class="accent-black w-4 h-4"
                  />
                  Female
                </label>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Join Date
              </Label>
              <Input
                type="date"
                v-model="form.join_date"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>

            <div class="grid gap-2">
              <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
                Date of Birth
              </Label>
              <Input
                type="date"
                v-model="form.date_of_birth"
                class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
              />
            </div>
          </div>

          <div class="grid gap-2">
            <Label class="text-[10px] font-semibold uppercase text-black/50 tracking-wider">
              Residential Address
            </Label>
            <Input
              v-model="form.address"
              placeholder="Enter full address"
              class="h-11 bg-white border-black/15 focus-visible:ring-0 focus-visible:border-black"
            />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <DialogFooter
        class="p-6 bg-white border-t border-black/10 flex items-center justify-between sm:justify-between"
      >
        <Button
          v-if="currentStep > 1"
          variant="ghost"
          @click="currentStep--"
          class="text-black/70 font-semibold hover:bg-transparent"
        >
          <ChevronLeft class="w-4 h-4 mr-1" /> Previous
        </Button>
        <div v-else></div>

        <div class="flex gap-3">
          <Button
            variant="outline"
            @click="handleOpenChange(false)"
            class="border-black/15 text-black font-semibold hover:bg-black/5"
          >
            Cancel
          </Button>

          <Button
            v-if="currentStep < totalSteps"
            @click="currentStep++"
            :disabled="!isStep1Valid"
            class="bg-black text-white hover:bg-black/90 font-semibold min-w-[120px]"
          >
            Continue <ChevronRight class="w-4 h-4 ml-1" />
          </Button>

          <Button
            v-else
            @click="handleSave"
            :disabled="isLoading"
            class="bg-black text-white hover:bg-black/90 font-semibold min-w-[140px] gap-2"
          >
            <template v-if="isLoading">
              <Loader2 class="w-4 h-4 animate-spin" /> Saving...
            </template>
            <template v-else>
              <CheckCircle2 class="w-4 h-4" />
              {{ mode === 'edit' ? 'Update Info' : 'Complete Setup' }}
            </template>
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
