<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Download, Calendar, Filter } from 'lucide-vue-next'
import StaffTable from '@/features/staff/components/StaffTable.vue'
import StaffDialog from '@/features/staff/components/StaffDialog.vue'
import { useStaff } from '@/features/staff'
import type { StaffMember } from '@/features/staff/types'

// Composable
const { staffMembers, isLoading, loadStaffMembers, handleDeleteStaff } = useStaff()

// State
const searchQuery = ref('')
const isCreateOpen = ref(false)
const isEditOpen = ref(false)
const selectedUser = ref<StaffMember | null>(null)

// Load Data
onMounted(async () => {
  await loadStaffMembers()
})

// Handlers
const handleToggle = (user: StaffMember) => {
  user.expanded = !user.expanded
}

const handleEdit = (user: StaffMember) => {
  selectedUser.value = user
  isEditOpen.value = true
}

const handleDelete = async (userId: number) => {
  if (confirm('Are you sure you want to delete this user?')) {
    await handleDeleteStaff(userId)
  }
}

const handleSuccess = async () => {
  // Refresh list to get latest data
  await loadStaffMembers()
}
</script>

<template>
  <div class="w-full bg-slate-50 animate-in fade-in duration-500">
    <div class="mx-auto space-y-6">
      <!-- Header Section -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-900">Staff Management</h1>
          <p class="text-slate-500 mt-1">Manage employee profiles, roles, and shift schedules.</p>
        </div>
        <div class="flex items-center gap-3">
          <Button variant="outline" class="gap-2 bg-white hidden sm:flex">
            <Download class="h-4 w-4" />
            Export
          </Button>
          <StaffDialog mode="create" v-model:open="isCreateOpen" @success="handleSuccess" />
        </div>
      </div>

      <!-- Toolbar -->
      <div
        class="flex flex-col sm:flex-row gap-4 items-center justify-between bg-white p-2 rounded-xl border border-slate-200 shadow-sm"
      >
        <div class="relative w-full sm:w-96">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <Input
            v-model="searchQuery"
            placeholder="Search by name, email, or ID..."
            class="pl-10 bg-transparent border-0 focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-slate-400"
          />
        </div>
        <div class="flex items-center gap-2 w-full sm:w-auto px-2">
          <Button variant="ghost" size="sm" class="gap-2 text-slate-600">
            <Filter class="h-4 w-4" />
            Filters
          </Button>
          <Button variant="ghost" size="sm" class="gap-2 text-slate-600">
            <Calendar class="h-4 w-4" />
            Date Range
          </Button>
        </div>
      </div>

      <div class="overflow-x-auto pb-4 -mx-6 px-6 lg:mx-0 lg:px-0">
        <div class="min-w-[800px] lg:min-w-full inline-block align-middle">
          <StaffTable
            :users="staffMembers"
            @toggle="handleToggle"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>

      <!-- Edit Dialog -->
      <StaffDialog
        mode="edit"
        :user="selectedUser"
        v-model:open="isEditOpen"
        @success="handleSuccess"
      />
    </div>
  </div>
</template>
