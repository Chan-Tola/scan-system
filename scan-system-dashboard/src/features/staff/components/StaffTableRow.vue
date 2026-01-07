<script setup lang="ts">
import { computed } from 'vue'
import { TableRow, TableCell } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { MoreVertical, ChevronDown, Trash2, Pencil, Eye, Clock } from 'lucide-vue-next'
import type { StaffMember } from '../types'

const props = defineProps<{
  user: StaffMember
}>()

const emit = defineEmits<{
  (e: 'edit', user: StaffMember): void
  (e: 'delete', userId: number): void
  (e: 'toggle', user: StaffMember): void
}>()

// Performance: Cache formatting logic using computed
const formattedDate = computed(() => {
  if (!props.user.join_date) return 'N/A'
  return new Date(props.user.join_date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
})

const roleBadgeClass = computed(() => {
  const base = 'font-medium px-2 py-0.5 text-xs'
  return props.user.role === 'admin'
    ? `${base} bg-red-50 text-red-700 ring-1 ring-red-600/10`
    : `${base} bg-blue-50 text-blue-700 ring-1 ring-blue-700/10`
})
</script>

<template>
  <TableRow class="group hover:bg-slate-50/80 transition-colors border-b border-slate-100">
    <TableCell class="w-12 text-center">
      <Button
        variant="ghost"
        size="sm"
        @click="emit('toggle', user)"
        class="h-8 w-8 p-0 text-slate-400 hover:text-slate-600"
      >
        <ChevronDown :class="['h-4 w-4 transition-transform', user.expanded ? 'rotate-180' : '']" />
      </Button>
    </TableCell>

    <TableCell>
      <div class="flex flex-col">
        <span class="font-semibold text-slate-900 text-sm">{{ user.full_name }}</span>
        <span class="text-[11px] text-slate-400 md:hidden capitalize">{{ user.role }}</span>
      </div>
    </TableCell>

    <TableCell class="hidden md:table-cell text-sm text-slate-600">{{ user.email }}</TableCell>
    <TableCell class="hidden lg:table-cell text-sm text-slate-600 font-mono">{{
      user.phone
    }}</TableCell>
    <TableCell class="hidden md:table-cell text-sm font-medium text-slate-700">{{
      user.office_name
    }}</TableCell>

    <TableCell class="hidden md:table-cell">
      <Badge variant="secondary" :class="roleBadgeClass">{{ user.role }}</Badge>
    </TableCell>

    <TableCell class="hidden xl:table-cell text-xs text-slate-500">{{ formattedDate }}</TableCell>

    <TableCell class="text-right">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="ghost" size="sm" class="h-8 w-8 p-0 opacity-0 group-hover:opacity-100">
            <MoreVertical class="h-4 w-4 text-slate-400" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="w-40">
          <DropdownMenuLabel>Actions</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem @click="emit('toggle', user)"
            ><Eye class="mr-2 h-4 w-4" /> Details</DropdownMenuItem
          >
          <DropdownMenuItem @click="emit('edit', user)"
            ><Pencil class="mr-2 h-4 w-4" /> Edit</DropdownMenuItem
          >
          <DropdownMenuSeparator />
          <DropdownMenuItem class="text-destructive" @click="emit('delete', user.id)"
            ><Trash2 class="mr-2 h-4 w-4" /> Delete</DropdownMenuItem
          >
        </DropdownMenuContent>
      </DropdownMenu>
    </TableCell>
  </TableRow>

  <TableRow v-if="user.expanded" class="bg-slate-50/50 shadow-inner">
    <TableCell colspan="8" class="p-6">
      <div class="bg-white p-4 rounded-xl border grid grid-cols-2 gap-4">
        <div>
          <p class="text-[10px] font-bold text-slate-400 uppercase">Shift</p>
          <div class="flex items-center gap-2 text-sm">
            <Clock class="h-4 w-4" /> {{ user.shift }}
          </div>
        </div>
        <div>
          <p class="text-[10px] font-bold text-slate-400 uppercase">Location</p>
          <p class="text-sm">{{ user.office_name }}</p>
        </div>
      </div>
    </TableCell>
  </TableRow>
</template>
