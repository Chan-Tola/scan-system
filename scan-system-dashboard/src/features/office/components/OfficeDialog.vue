<script setup lang="ts">
import { ref, watch } from 'vue'
import { Plus } from 'lucide-vue-next'
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
import { useOffice } from '@/features/office'

/* =====================
   Props
===================== */
interface Props {
  mode?: 'create' | 'edit'
  officeId?: number
  initialName?: string
  initialIp?: string
  initialShiftStart?: string
  initialShiftEnd?: string
  open?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'create',
  open: false,
})

const emit = defineEmits(['update:open', 'success'])

/* =====================
   Composable
===================== */
const { handleCreateOffice, handleUpdateOffice, isLoading, error, clearError } = useOffice()

/* =====================
   Form State
===================== */
const officeName = ref(props.initialName || '')
const publicIp = ref(props.initialIp || '')
const shiftStart = ref(props.initialShiftStart || '')
const shiftEnd = ref(props.initialShiftEnd || '')
const internalOpen = ref(false)

const formatTimeForInput = (time: string | undefined): string => {
  if (!time) return ''
  // Convert "08:00:00" to "08:00"
  if (time.length === 8) return time.substring(0, 5)
  return time
}

/* =====================
   Sync Props
===================== */
watch(
  () => props.open,
  (val) => (internalOpen.value = val),
)
watch(
  () => props.initialName,
  (val) => (officeName.value = val || ''),
)
watch(
  () => props.initialIp,
  (val) => (publicIp.value = val || ''),
)
watch(
  () => props.initialShiftStart,
  (val) => (shiftStart.value = formatTimeForInput(val) || ''),
)
watch(
  () => props.initialShiftEnd,
  (val) => (shiftEnd.value = formatTimeForInput(val) || ''),
)

/* =====================
   Handlers
===================== */
const handleOpenChange = (open: boolean) => {
  if (props.mode === 'create') internalOpen.value = open
  emit('update:open', open)
  if (!open) clearError()
}

const handleSave = async () => {
  const payload = {
    name: officeName.value.trim(),
    public_ip: publicIp.value.trim() || undefined,
    shift_start: shiftStart.value,
    shift_end: shiftEnd.value,
  }

  const result =
    props.mode === 'edit' && props.officeId
      ? await handleUpdateOffice(props.officeId, payload)
      : await handleCreateOffice(payload)

  if (result) {
    emit('success')
    handleOpenChange(false)
  }
}
</script>

<template>
  <Dialog :open="internalOpen" @update:open="handleOpenChange">
    <!-- Trigger -->
    <DialogTrigger as-child v-if="mode === 'create'">
      <Button class="gap-2">
        <Plus class="w-4 h-4" />
        Create Office
      </Button>
    </DialogTrigger>

    <!-- Content -->
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>
          {{ mode === 'edit' ? 'Edit Office' : 'Create New Office' }}
        </DialogTitle>
        <DialogDescription> Enter the office details below. </DialogDescription>
      </DialogHeader>

      <!-- Form -->
      <div class="grid gap-5 py-4">
        <div v-if="error" class="rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
          {{ error }}
        </div>

        <div class="grid gap-2">
          <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
            >Office Name <span class="text-destructive">*</span></Label
          >
          <Input
            v-model="officeName"
            :disabled="isLoading"
            placeholder="e.g. Headquarters, Branch A"
            class="h-10"
          />
        </div>

        <div class="grid gap-2">
          <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
            >Public IP Address</Label
          >
          <Input
            v-model="publicIp"
            :disabled="isLoading"
            placeholder="e.g. 192.168.1.1"
            class="h-10 font-mono text-sm"
          />
          <p class="text-[10px] text-muted-foreground">Used for validating scan requests.</p>
        </div>

        <!-- SHIFT FIELDS -->
        <div class="grid grid-cols-2 gap-4">
          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Shift Start <span class="text-destructive">*</span></Label
            >
            <Input type="time" v-model="shiftStart" :disabled="isLoading" class="h-10" />
          </div>

          <div class="grid gap-2">
            <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Shift End <span class="text-destructive">*</span></Label
            >
            <Input type="time" v-model="shiftEnd" :disabled="isLoading" class="h-10" />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <DialogFooter>
        <Button
          :disabled="isLoading || !officeName.trim() || !shiftStart || !shiftEnd"
          @click="handleSave"
        >
          {{ isLoading ? 'Saving...' : 'Save Office' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
