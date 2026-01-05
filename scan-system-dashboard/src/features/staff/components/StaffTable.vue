<script setup lang="ts">
import { Table, TableBody, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import StaffTableRow from './StaffTableRow.vue'
import type { StaffMember } from '../types'

defineProps<{
  users: StaffMember[]
}>()

const emit = defineEmits<{
  (e: 'edit', user: StaffMember): void
  (e: 'delete', userId: number): void
  (e: 'toggle', user: StaffMember): void
}>()
</script>

<template>
  <div class="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
    <Table>
      <TableHeader class="bg-slate-50/50">
        <TableRow class="hover:bg-transparent border-b border-slate-200">
          <TableHead class="w-12"></TableHead>
          <TableHead class="w-[80px] font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >ID</TableHead
          >
          <TableHead class="font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Staff Member</TableHead
          >
          <TableHead
            class="hidden md:table-cell font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Email</TableHead
          >
          <TableHead
            class="hidden lg:table-cell font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Phone</TableHead
          >
          <TableHead
            class="hidden md:table-cell font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Office</TableHead
          >
          <TableHead
            class="hidden md:table-cell font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Role</TableHead
          >
          <TableHead
            class="hidden xl:table-cell font-bold text-[11px] uppercase tracking-wider text-slate-500"
            >Joined</TableHead
          >
          <TableHead class="w-[50px]"></TableHead>
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
        />

        <TableRow v-if="users.length === 0">
          <TableCell colspan="9" class="h-32 text-center text-slate-500">
            No staff members found matching your criteria.
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
