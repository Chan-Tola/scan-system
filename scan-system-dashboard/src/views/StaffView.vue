<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Loader2, X, AlertTriangle } from 'lucide-vue-next'
import { useDebounceFn } from '@vueuse/core'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import StaffTable from '@/features/staff/components/StaffTable.vue'
import StaffDialog from '@/features/staff/components/StaffDialog.vue'
import ResetPasswordDialog from '@/features/staff/components/ResetPasswordDialog.vue'
import { useStaff } from '@/features/staff'
import type { StaffMember } from '@/features/staff/'

// --- COMPOSABLES ---
const { staffMembers, loadStaffMembers, handleDeleteStaff } = useStaff()

// --- STATE ---
const searchQuery = ref('') // Search input value
const isSearching = ref(false) // Loading state for search
const isCreateOpen = ref(false) // Controls create dialog visibility
const isEditOpen = ref(false) // Controls edit dialog visibility
const isDeleteOpen = ref(false) // Controls delete confirmation dialog
const selectedUser = ref<StaffMember | null>(null) // User being edited
const userToDelete = ref<number | null>(null) // ID of user to delete
const isResetPasswordOpen = ref(false)
const userToResetPassword = ref<StaffMember | null>(null)

// --- LIFECYCLE ---
// Load staff members when component mounts
onMounted(() => loadStaffMembers())

// Debounced search function (waits 500ms after typing stops)
const performSearch = useDebounceFn(async () => {
  isSearching.value = true
  try {
    await loadStaffMembers({ search: searchQuery.value.trim() })
  } finally {
    isSearching.value = false
  }
}, 500)

// watch search query and trigger debounced search
watch(searchQuery, (newValue) => {
  const trimmed = newValue.trim()

  if (trimmed.length >= 2) {
    // Search if 2 or more characters
    performSearch()
  } else if (trimmed.length === 0) {
    // If search is cleared, load all staff
    loadStaffMembers()
  }
})

const clearSearch = () => {
  searchQuery.value = ''
}
// --- EVENT HANDLERS ---

// Toggle row expansion in table
const handleToggle = (user: StaffMember) => {
  user.expanded = !user.expanded
}

// Open edit dialog with selected user
const handleEdit = (user: StaffMember) => {
  selectedUser.value = { ...user } // Clone to avoid direct mutation
  isEditOpen.value = true
}

// Open delete confirmation dialog
const handleDelete = (id: number) => {
  userToDelete.value = id
  isDeleteOpen.value = true
}

const handleResetPassword = (user: StaffMember) => {
  userToResetPassword.value = user
  isResetPasswordOpen.value = true
}

// Perform the actual delete after confirmation
const performDelete = async () => {
  if (userToDelete.value) {
    const success = await handleDeleteStaff(userToDelete.value)
    if (success) {
      await loadStaffMembers()
      isDeleteOpen.value = false
      userToDelete.value = null
    }
  }
}

// Reload staff list after successful create/edit
const handleSuccess = () => {
  loadStaffMembers()
  // Reset selected user when dialog closes
  selectedUser.value = null
}
</script>

<template>
  <div class="container mx-auto p-4 md:p-8 animate-in fade-in duration-500">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900">Staff Management</h1>
        <p class="text-slate-500 mt-1">Manage your staff members.</p>
      </div>
      <!-- Create Staff Button (opens dialog) -->
      <StaffDialog mode="create" v-model:open="isCreateOpen" @success="handleSuccess" />
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row gap-4 mb-6">
      <div class="relative flex-1 max-w-md">
        <!-- Search icon (left side) -->
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
        <!-- Loading spinner (right side, shows when searching) -->
        <Loader2
          v-if="isSearching"
          class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 animate-spin"
        />
        <!-- Clear button (right side, shows when search has value) -->
        <button
          v-else-if="searchQuery.trim()"
          @click="clearSearch"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
          title="Clear search"
        >
          <X class="h-4 w-4" />
        </button>
        <!-- Search input -->
        <Input v-model="searchQuery" placeholder="Search staff members..." class="pl-10 bg-white" />
      </div>
    </div>
    <!-- Content -->
    <!-- Staff Table -->
    <StaffTable
      :users="staffMembers"
      @edit="handleEdit"
      @delete="handleDelete"
      @toggle="handleToggle"
      @reset-password="handleResetPassword"
    />

    <!-- Edit Dialog (hidden until user clicks edit) -->
    <StaffDialog
      mode="edit"
      :user="selectedUser"
      v-model:open="isEditOpen"
      @success="handleSuccess"
    />

    <!-- Reset Password Dialog -->
    <ResetPasswordDialog
      v-model:open="isResetPasswordOpen"
      :user="userToResetPassword"
      @success="loadStaffMembers()"
    />

    <!-- Delete Confirmation Dialog -->
    <Dialog :open="isDeleteOpen" @update:open="isDeleteOpen = $event">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Staff Member</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete this staff member? This action cannot be undone and will
            also delete their user account.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" @click="isDeleteOpen = false">Cancel</Button>
          <Button variant="destructive" @click="performDelete">Delete</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
