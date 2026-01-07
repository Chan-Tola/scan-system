<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Download, Calendar, Filter } from 'lucide-vue-next'
import StaffTable from '@/features/staff/components/StaffTable.vue'
import StaffDialog from '@/features/staff/components/StaffDialog.vue'
import { useStaff } from '@/features/staff'
import type { StaffMember } from '@/features/staff/'

const { staffMembers, loadStaffMembers, handleDeleteStaff } = useStaff()

const searchQuery = ref('')
const isCreateOpen = ref(false)
const isEditOpen = ref(false)
const selectedUser = ref<StaffMember | null>(null)

onMounted(() => loadStaffMembers())

const handleToggle = (user: StaffMember) => {
  user.expanded = !user.expanded
}

const handleEdit = (user: StaffMember) => {
  selectedUser.value = { ...user } // Clone to avoid direct mutation
  isEditOpen.value = true
}

const handleDelete = async (id: number) => {
  if (confirm('Delete this user?')) await handleDeleteStaff(id)
}
</script>

<template>
  <div class="p-6 space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold">Staff Management</h1>
      <StaffDialog mode="create" v-model:open="isCreateOpen" @success="loadStaffMembers" />
    </div>

    <div class="flex gap-4 p-2 bg-white rounded-xl border shadow-sm">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
        <Input v-model="searchQuery" placeholder="Search..." class="pl-10 border-0" />
      </div>
    </div>

    <StaffTable
      :users="staffMembers"
      @edit="handleEdit"
      @delete="handleDelete"
      @toggle="handleToggle"
    />

    <StaffDialog
      mode="edit"
      :user="selectedUser"
      v-model:open="isEditOpen"
      @success="loadStaffMembers"
    />
  </div>
</template>
