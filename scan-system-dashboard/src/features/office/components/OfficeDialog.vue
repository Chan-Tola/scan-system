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
  
  interface Props {
    mode?: 'create' | 'edit'
    officeId?: number
    initialName?: string
    initialIp?: string
    open?: boolean 
  }
  
  const props = withDefaults(defineProps<Props>(), {
    mode: 'create',
    open: false
  })
  
  const emit = defineEmits(['update:open', 'success'])
  const { handleCreateOffice, handleUpdateOffice, isLoading, error, clearError } = useOffice()
  
  const officeName = ref(props.initialName || '')
  const publicIp = ref(props.initialIp || '')
  const internalOpen = ref(false)
  
  watch(() => props.open, (newVal) => { internalOpen.value = newVal })
  watch(() => props.initialName, (newVal) => { officeName.value = newVal || '' })
  watch(() => props.initialIp, (newVal) => { publicIp.value = newVal || '' })
  
  const handleOpenChange = (open: boolean) => {
    if (props.mode === 'create') internalOpen.value = open
    emit('update:open', open)
    if (!open) clearError()
  }
  
  const handleSave = async () => {
    const payload = {
      name: officeName.value.trim(),
      public_ip: publicIp.value.trim() || undefined,
    }
  
    const result = props.mode === 'edit' && props.officeId
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
      <DialogTrigger as-child v-if="mode === 'create'">
        <Button class="gap-2"><Plus class="w-4 h-4" /> Create Office</Button>
      </DialogTrigger>
  
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{{ mode === 'edit' ? 'Edit Office' : 'Create New Office' }}</DialogTitle>
          <DialogDescription>Enter the office details below.</DialogDescription>
        </DialogHeader>
        <div class="grid gap-4 py-4">
          <div v-if="error" class="text-sm text-destructive">{{ error }}</div>
          <div class="grid gap-2">
            <Label>Office Name *</Label>
            <Input v-model="officeName" :disabled="isLoading" />
          </div>
          <div class="grid gap-2">
            <Label>Public IP Address</Label>
            <Input v-model="publicIp" :disabled="isLoading" />
          </div>
        </div>
        <DialogFooter>
          <Button :disabled="isLoading || !officeName.trim()" @click="handleSave">
            {{ isLoading ? 'Saving...' : 'Save Office' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </template>