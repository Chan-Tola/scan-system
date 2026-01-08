<script setup lang="ts">
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
  TableCell,
} from '@/components/ui/table'
import StaffTableRow from './StaffTableRow.vue'
import type { StaffMember } from '../types'

defineProps<{ users: StaffMember[] }>()
const emit = defineEmits(['edit', 'delete', 'toggle', 'reset-password'])
</script>

<template>
  <div class="rounded-xl border bg-white shadow-sm overflow-hidden">
    <Table>
      <TableHeader class="bg-slate-50/50">
        <TableRow>
          <TableHead class="w-12"></TableHead>
          <TableHead>Staff Member</TableHead>
          <TableHead class="hidden md:table-cell">Email</TableHead>
          <TableHead class="hidden lg:table-cell">Phone</TableHead>
          <TableHead class="hidden md:table-cell">Office</TableHead>
          <TableHead class="hidden md:table-cell">Role</TableHead>
          <TableHead class="hidden xl:table-cell">Joined</TableHead>
          <TableHead class="hidden xl:table-cell text-end">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <StaffTableRow
          v-for="user in users"
          :key="user.id"
          :user="user"
          @edit="emit('edit', $event)"
          @delete="emit('delete', $event)"
          @toggle="emit('toggle', $event)"
          @reset-password="emit('reset-password', $event)"
        />
        <TableRow v-if="users.length === 0">
          <TableCell colspan="8" class="h-32 text-center text-slate-500">No staff found.</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
