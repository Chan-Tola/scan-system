<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { MoreHorizontal, Pencil, Trash2, Building2 } from 'lucide-vue-next'
import type { Office } from '../types'

defineProps<{
  offices: Office[]
}>()

const emit = defineEmits<{
  (e: 'edit', office: Office): void
  (e: 'delete', officeId: number): void
}>()
</script>

<template>
  <div class="rounded-md border bg-white">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead class="w-[250px]">Name</TableHead>
          <TableHead>Public IP</TableHead>
          <TableHead>Shift Hours</TableHead>
          <TableHead>Status</TableHead>
          <TableHead class="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="office in offices" :key="office.id" class="group hover:bg-slate-50">
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <Building2 class="h-4 w-4 text-primary" />
              </div>
              <span class="font-semibold">{{ office.name }}</span>
            </div>
          </TableCell>
          <TableCell
            class="font-mono text-xs text-muted-foreground bg-slate-50 w-fit px-2 py-1 rounded"
          >
            {{ office.public_ip }}
          </TableCell>
          <TableCell>
            <div class="flex items-center gap-1.5 text-sm">
              <span class="font-medium">{{ office.shift_start }}</span>
              <span class="text-muted-foreground">to</span>
              <span class="font-medium">{{ office.shift_end }}</span>
            </div>
          </TableCell>
          <TableCell>
            <span
              class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-emerald-50 text-emerald-700 hover:bg-emerald-50/80"
            >
              Active
            </span>
          </TableCell>
          <TableCell class="text-right">
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <Button
                  variant="ghost"
                  class="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <span class="sr-only">Open menu</span>
                  <MoreHorizontal class="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>Actions</DropdownMenuLabel>
                <DropdownMenuItem @click="emit('edit', office)" class="cursor-pointer">
                  <Pencil class="mr-2 h-4 w-4" />
                  Edit details
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  @click="emit('delete', office.id)"
                  class="text-destructive cursor-pointer hover:bg-destructive/10 focus:bg-destructive/10 focus:text-destructive"
                >
                  <Trash2 class="mr-2 h-4 w-4" />
                  Delete office
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
