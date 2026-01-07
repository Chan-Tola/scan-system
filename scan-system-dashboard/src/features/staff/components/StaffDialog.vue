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

// --- UI STATE ---
const currentStep = ref(1)
const totalSteps = 2
const internalOpen = ref(false)
const localError = ref('')
const previewImage = ref<string | null>(null)

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

// --- LOGIC ---
watch(
  () => props.open,
  (val) => {
    internalOpen.value = val
    if (val) {
      currentStep.value = 1
      localError.value = ''
    }
  },
)

watch(
  () => props.user,
  (val) => {
    if (val && props.mode === 'edit') {
      const matchingOffice = offices.value.find((o) => o.name === val.office_name)

      form.value = {
        username: val.username,
        email: val.email,
        full_name: val.full_name,
        phone: val.phone,
        role: val.role,
        office_id: matchingOffice ? matchingOffice.id : 0,
        gender: 'male',
        address: '', // This will bind to the new input
        date_of_birth: '',
        join_date: val.join_date,
        profile_image: null, // Reset file on edit start
      }
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
  currentStep.value = 1
}

const handleOpenChange = (open: boolean) => {
  if (props.mode === 'create') internalOpen.value = open
  emit('update:open', open)
}

// Handle file selection with automatic compression
const handleFileChange = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]

  if (file) {
    try {
      console.log('Original file:', {
        name: file.name,
        type: file.type,
        size: file.size,
        isFile: file instanceof File,
      })

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
        console.warn('Compressed result is not a File, using original file')
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
      console.error('Error processing image:', error)
      // Fallback: use original file if compression fails
      if (previewImage.value) {
        URL.revokeObjectURL(previewImage.value)
      }
      previewImage.value = URL.createObjectURL(file)
      form.value.profile_image = file
      console.log('Using original file due to compression error')
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

  console.log(result)
}
</script>

<template>
  <Dialog :open="internalOpen" @update:open="handleOpenChange">
    <DialogTrigger as-child v-if="mode === 'create'">
      <Button class="bg-indigo-600 hover:bg-indigo-700 text-white gap-2 shadow-md">
        <Plus class="w-4 h-4" /> Add Staff Member
      </Button>
    </DialogTrigger>

    <DialogContent class="sm:max-w-[600px] p-0 overflow-hidden border-none shadow-2xl">
      <div class="bg-slate-900 p-6 text-white relative">
        <div class="z-10 relative">
          <DialogTitle class="text-2xl font-bold tracking-tight">
            {{ mode === 'edit' ? 'Update Staff Member' : 'Register New Staff' }}
          </DialogTitle>
          <DialogDescription class="text-slate-400 mt-1">
            Step {{ currentStep }} of {{ totalSteps }}:
            {{ currentStep === 1 ? 'Personal Information' : 'Employment Details' }}
          </DialogDescription>
        </div>

        <div class="flex gap-2 mt-6">
          <div
            v-for="s in totalSteps"
            :key="s"
            :class="[
              'h-1.5 flex-1 rounded-full transition-all duration-500',
              currentStep >= s ? 'bg-indigo-500' : 'bg-slate-700',
            ]"
          ></div>
        </div>
      </div>

      <div class="p-8 bg-white">
        <div
          v-if="error || localError"
          class="mb-6 p-3 rounded-lg bg-red-50 border border-red-100 text-red-600 text-sm flex items-center gap-2"
        >
          <X class="w-4 h-4" /> {{ error || localError }}
        </div>

        <div
          v-if="currentStep === 1"
          class="space-y-6 animate-in slide-in-from-right-4 duration-300"
        >
          <div
            v-if="mode === 'create'"
            class="flex items-center gap-6 p-4 rounded-2xl bg-slate-50 border border-slate-100 group"
          >
            <div
              class="relative w-24 h-24 rounded-full bg-white border-4 border-white shadow-sm overflow-hidden shrink-0 flex items-center justify-center"
            >
              <img v-if="previewImage" :src="previewImage" class="w-full h-full object-cover" />
              <User v-else class="w-10 h-10 text-slate-200" />
              <input
                type="file"
                accept=".jpg,.jpeg,.png"
                @change="handleFileChange"
                class="absolute inset-0 opacity-0 cursor-pointer z-10"
              />
              <div
                class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <Upload class="w-6 h-6 text-white" />
              </div>
            </div>
            <div class="space-y-1">
              <h4 class="text-sm font-bold text-slate-800">Profile Image</h4>
              <p class="text-xs text-slate-500 leading-relaxed">
                JPG, PNG or GIF. Max size 10MB.<br />Click the circle to upload.
              </p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Full Name</Label
              >
              <Input
                v-model="form.full_name"
                placeholder="Enter name"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Username</Label
              >
              <Input
                v-model="form.username"
                placeholder="johndoe"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Email Address</Label
              >
              <Input
                v-model="form.email"
                type="email"
                :disabled="mode === 'edit'"
                placeholder="name@company.com"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
            <div v-if="mode === 'create'" class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Initial Password</Label
              >
              <Input
                v-model="form.password"
                type="password"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
          </div>
        </div>

        <div
          v-if="currentStep === 2"
          class="space-y-6 animate-in slide-in-from-right-4 duration-300"
        >
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label
                class="text-[10px] font-black uppercase text-slate-400 tracking-widest text-indigo-600"
                >Office Location</Label
              >
              <select
                v-model="form.office_id"
                class="flex h-11 w-full rounded-md border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm"
              >
                <option value="0" disabled>Select Office</option>
                <option v-for="office in offices" :key="office.id" :value="office.id">
                  {{ office.name }}
                </option>
              </select>
            </div>
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Role Type</Label
              >
              <select
                v-model="form.role"
                class="flex h-11 w-full rounded-md border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm"
              >
                <option value="staff">Staff Member</option>
                <option value="admin">Administrator</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Phone Number</Label
              >
              <Input
                v-model="form.phone"
                placeholder="+1..."
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Gender</Label
              >
              <div class="flex gap-4 items-center h-11">
                <label class="flex items-center gap-2 text-sm font-medium"
                  ><input
                    type="radio"
                    v-model="form.gender"
                    value="male"
                    class="accent-indigo-600 w-4 h-4"
                  />
                  Male</label
                >
                <label class="flex items-center gap-2 text-sm font-medium"
                  ><input
                    type="radio"
                    v-model="form.gender"
                    value="female"
                    class="accent-indigo-600 w-4 h-4"
                  />
                  Female</label
                >
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Join Date</Label
              >
              <Input
                type="date"
                v-model="form.join_date"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
            <div class="grid gap-2">
              <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
                >Date of Birth</Label
              >
              <Input
                type="date"
                v-model="form.date_of_birth"
                class="h-11 bg-slate-50/50 border-slate-200"
              />
            </div>
          </div>

          <div class="grid gap-2">
            <Label class="text-[10px] font-black uppercase text-slate-400 tracking-widest"
              >Residential Address</Label
            >
            <Input
              v-model="form.address"
              placeholder="Enter full address"
              class="h-11 bg-slate-50/50 border-slate-200"
            />
          </div>
        </div>
      </div>

      <DialogFooter
        class="p-6 bg-slate-50 border-t border-slate-100 flex items-center justify-between sm:justify-between"
      >
        <Button
          v-if="currentStep > 1"
          variant="ghost"
          @click="currentStep--"
          class="text-slate-500 font-bold hover:bg-transparent"
        >
          <ChevronLeft class="w-4 h-4 mr-1" /> Previous
        </Button>
        <div v-else></div>

        <div class="flex gap-3">
          <Button
            variant="outline"
            @click="handleOpenChange(false)"
            class="border-slate-200 font-bold"
            >Cancel</Button
          >

          <Button
            v-if="currentStep < totalSteps"
            @click="currentStep++"
            :disabled="!isStep1Valid"
            class="bg-indigo-600 hover:bg-indigo-700 font-bold min-w-[120px]"
          >
            Continue <ChevronRight class="w-4 h-4 ml-1" />
          </Button>

          <Button
            v-else
            @click="handleSave"
            :disabled="isLoading"
            class="bg-emerald-600 hover:bg-emerald-700 font-bold min-w-[140px] gap-2"
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
