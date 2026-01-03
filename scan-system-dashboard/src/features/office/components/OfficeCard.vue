<script setup lang="ts">
import { ref, type Component } from 'vue'
import { MoreVertical, Pencil, Trash2, AlertTriangle } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useOffice } from '@/features/office'
import OfficeDialog from './OfficeDialog.vue'

interface Props {
  icon: Component
  title: string
  officeId: number
  publicIp?: string
  shiftStart?: string
  shiftEnd?: string
}

const props = defineProps<Props>()
const emit = defineEmits(['delete', 'updated'])

const { handleDeleteOffice, isLoading } = useOffice()

const isEditOpen = ref(false)
const isDeleteOpen = ref(false)

const onConfirmDelete = async () => {
  const success = await handleDeleteOffice(props.officeId)
  if (success) {
    emit('delete', props.officeId)
    isDeleteOpen.value = false
  }
}

// Helper function to format time from "08:00:00" to "8:00 AM" or "17:00" to "5:00 PM"
const formatTimeForDisplay = (time: string | undefined): string => {
  if (!time) return ''

  // Split by colon and extract hours and minutes
  const parts = time.split(':')
  if (parts.length < 2 || !parts[0] || !parts[1]) return time

  let hours = parseInt(parts[0], 10)
  const minutes = parts[1]

  if (isNaN(hours)) return time

  // Determine AM/PM
  const period = hours >= 12 ? 'PM' : 'AM'
  
  // Convert to 12-hour format (0 -> 12, 13 -> 1, etc.)
  hours = hours % 12 || 12

  return `${hours}:${minutes} ${period}`
}

// Helper function to format time for input (HH:mm format)
const formatTimeForInput = (time: string | undefined): string => {
  if (!time) return ''
  // Convert "08:00:00" to "08:00"
  if (time.length === 8) return time.substring(0, 5)
  return time
}
</script>

<template>
  <Card class="bg-white hover:shadow-lg transition-shadow">
    <CardHeader class="flex flex-row items-start justify-between border-b pb-4">
      <div class="flex items-start gap-3 flex-1">
        <div
          class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center text-orange-500 flex-shrink-0"
        >
          <component :is="icon" class="w-6 h-6" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-gray-900 text-base">{{ title }}</h3>
        </div>
      </div>

      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="ghost" size="icon" class="h-8 w-8">
            <MoreVertical class="w-4 h-4 text-gray-400" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="w-[160px]">
          <DropdownMenuItem @click="isEditOpen = true" class="cursor-pointer">
            <Pencil class="mr-2 h-4 w-4" /> Edit Office
          </DropdownMenuItem>
          <DropdownMenuItem
            @click="isDeleteOpen = true"
            class="cursor-pointer text-destructive focus:text-destructive"
          >
            <Trash2 class="mr-2 h-4 w-4" /> Delete Office
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </CardHeader>

    <CardContent class="pt-4">
      <p v-if="publicIp" class="text-sm font-medium text-gray-600">
        Public IP Address : {{ publicIp }}
      </p>
      <div v-if="shiftStart || shiftEnd" class="flex items-center gap-4 text-sm text-gray-600">
        <div v-if="shiftStart" class="flex items-center gap-1">
          <span class="font-medium">Shift Start:</span>
          <span>{{ formatTimeForDisplay(shiftStart) }}</span>
        </div>
        <div v-if="shiftEnd" class="flex items-center gap-1">
          <span class="font-medium">Shift End:</span>
          <span>{{ formatTimeForDisplay(shiftEnd) }}</span>
        </div>
      </div>
    </CardContent>

    <OfficeDialog
      mode="edit"
      v-model:open="isEditOpen"
      :office-id="officeId"
      :initial-name="title"
      :initial-ip="publicIp"
      :initial-shift-start="formatTimeForInput(shiftStart)"
      :initial-shift-end="formatTimeForInput(shiftEnd)"
      @success="emit('updated')"
    />

    <Dialog :open="isDeleteOpen" @update:open="isDeleteOpen = $event">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle class="flex items-center gap-2">
            <AlertTriangle class="h-5 w-5 text-destructive" />
            Delete Office
          </DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "<strong>{{ title }}</strong
            >"? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        <div class="py-4 text-sm text-gray-500">
          Deleting this office will remove all associated data from the system.
        </div>

        <DialogFooter class="gap-2 sm:gap-0">
          <Button variant="outline" @click="isDeleteOpen = false" :disabled="isLoading">
            No, Keep it
          </Button>
          <Button variant="destructive" @click="onConfirmDelete" :disabled="isLoading">
            {{ isLoading ? 'Deleting...' : 'Yes, Delete' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </Card>
</template>
