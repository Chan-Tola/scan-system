<script setup lang="ts">
import { ref, computed } from 'vue'
import { TableRow, TableCell } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { Collapsible, CollapsibleTrigger } from '@/components/ui/collapsible'
import { MoreVertical, ChevronDown, Trash2, Pencil, Eye } from 'lucide-vue-next'
import type { StaffMember } from '../types'

const props = defineProps<{
  user: StaffMember
}>()

const emit = defineEmits<{
  (e: 'edit', user: StaffMember): void
  (e: 'delete', userId: number): void
  (e: 'toggle', user: StaffMember): void
}>()

const isExpanded = computed(() => props.user.expanded)

const getInitials = (fullName: string): string => {
  return fullName
    .split(' ')
    .map((name) => name[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatDate = (dateString: string): string => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const getRoleBadgeClass = (role: string | undefined): string => {
  const baseClasses = 'font-medium px-2 py-0.5 text-xs'
  switch (role?.toLowerCase()) {
    case 'staff':
      return `${baseClasses} bg-blue-50 text-blue-700 ring-1 ring-inset ring-blue-700/10`
    case 'admin':
      return `${baseClasses} bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/10`
    case 'manager':
      return `${baseClasses} bg-purple-50 text-purple-700 ring-1 ring-inset ring-purple-700/10`
    default:
      return `${baseClasses} bg-gray-50 text-gray-700 ring-1 ring-inset ring-gray-600/10`
  }
}
</script>

<template>
  <TableRow class="group hover:bg-slate-50/80 transition-colors border-b border-slate-100">
    <TableCell class="w-12 text-center">
      <Collapsible :open="isExpanded" @open-change="emit('toggle', user)">
        <CollapsibleTrigger as-child>
          <Button variant="ghost" size="sm" class="h-8 w-8 p-0 text-slate-400 hover:text-slate-600">
            <ChevronDown
              :class="['h-4 w-4 transition-transform duration-200', isExpanded ? 'rotate-180' : '']"
            />
          </Button>
        </CollapsibleTrigger>
      </Collapsible>
    </TableCell>

    <TableCell class="font-mono text-xs font-semibold text-slate-500">
      #{{ user.user_id }}
    </TableCell>

    <TableCell>
      <div class="flex items-center gap-3">
        <Avatar class="h-9 w-9 border border-slate-100">
          <AvatarImage :src="user.profile_image || ''" />
          <AvatarFallback class="bg-primary/5 text-primary text-xs font-bold">
            {{ getInitials(user.full_name) }}
          </AvatarFallback>
        </Avatar>
        <div class="flex flex-col">
          <span class="font-semibold text-slate-900 text-sm">{{ user.full_name }}</span>
          <span class="text-[11px] text-slate-400 font-medium md:hidden">{{
            user.user.roles[0]?.name
          }}</span>
        </div>
      </div>
    </TableCell>

    <TableCell class="hidden md:table-cell text-sm text-slate-600">
      {{ user.user.email }}
    </TableCell>

    <TableCell class="hidden lg:table-cell text-sm text-slate-600 font-mono">
      {{ user.phone }}
    </TableCell>

    <TableCell class="hidden md:table-cell text-sm font-medium text-slate-700">
      {{ user.office.name }}
    </TableCell>

    <TableCell class="hidden md:table-cell">
      <Badge variant="secondary" :class="getRoleBadgeClass(user.user.roles[0]?.name)">
        {{ user.user.roles[0]?.name || 'N/A' }}
      </Badge>
    </TableCell>

    <TableCell class="hidden xl:table-cell text-xs text-slate-500">
      {{ formatDate(user.join_date) }}
    </TableCell>

    <TableCell class="text-right">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button
            variant="ghost"
            size="sm"
            class="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <MoreVertical class="h-4 w-4 text-slate-400" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="w-40">
          <DropdownMenuLabel>Actions</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem class="cursor-pointer" @click="emit('toggle', user)">
            <Eye class="mr-2 h-4 w-4" /> View Details
          </DropdownMenuItem>
          <DropdownMenuItem class="cursor-pointer" @click="emit('edit', user)">
            <Pencil class="mr-2 h-4 w-4" /> Edit Profile
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            class="cursor-pointer text-destructive focus:text-destructive"
            @click="emit('delete', user.id)"
          >
            <Trash2 class="mr-2 h-4 w-4" /> Delete Access
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </TableCell>
  </TableRow>

  <!-- Expandable Details Row -->
  <TableRow v-if="isExpanded" class="bg-slate-50/50 border-b border-slate-100 shadow-inner">
    <TableCell colspan="9" class="p-0">
      <div class="p-4 md:p-6">
        <div
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 bg-white p-6 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden"
        >
          <div class="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
            <!-- Decorative -->
            <svg class="w-32 h-32" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
              />
            </svg>
          </div>

          <div class="space-y-1">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
              Contact Address
            </p>
            <p class="text-sm font-medium text-slate-900">{{ user.address }}</p>
          </div>
          <div class="space-y-1">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
              Personal Info
            </p>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <span class="text-xs text-slate-500">Gender</span>
                <p class="text-sm font-medium text-slate-900 capitalize">{{ user.gender }}</p>
              </div>
              <div>
                <span class="text-xs text-slate-500">Date of Birth</span>
                <p class="text-sm font-medium text-slate-900">
                  {{ formatDate(user.date_of_birth) }}
                </p>
              </div>
            </div>
          </div>
          <div class="space-y-1">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
              Shift Schedule
            </p>
            <div
              class="flex items-center gap-2 bg-slate-50 w-fit px-3 py-1.5 rounded-lg border border-slate-100"
            >
              <span class="text-sm font-mono font-medium text-slate-700">{{
                user.shift_start
              }}</span>
              <span class="text-slate-400">-</span>
              <span class="text-sm font-mono font-medium text-slate-700">{{ user.shift_end }}</span>
            </div>
          </div>
          <div
            class="space-y-1 md:col-span-2 lg:col-span-3 pt-2 border-t border-slate-100 flex items-center justify-between"
          >
            <div>
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                System Metadata
              </p>
              <p class="text-xs text-slate-500 mt-0.5">
                Record created on <span class="font-mono">{{ formatDate(user.created_at) }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </TableCell>
  </TableRow>
</template>
