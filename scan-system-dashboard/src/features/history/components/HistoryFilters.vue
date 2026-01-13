<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Filter, Search, Calendar } from 'lucide-vue-next'
import type { HistoryFilters } from '../types'

const props = defineProps<{
  filters: HistoryFilters
  searchInput: string
}>()

const emit = defineEmits<{
  (e: 'update:filters', filters: Partial<HistoryFilters>): void
  (e: 'update:searchInput', value: string): void
  (e: 'search', value: string): void
  (e: 'clear'): void
}>()

// Get current month in YYYY-MM format
const currentMonth = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
})

const handleStatusChange = (value: string) => {
  emit('update:filters', {
    status: value === 'all' ? undefined : (value as HistoryFilters['status']),
    page: 1,
  })
}

const handleMonthChange = (value: string | number) => {
  emit('update:filters', {
    month: value ? String(value) : undefined,
    page: 1,
  })
}

const handleSearchInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:searchInput', target.value)
  emit('search', target.value)
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <Filter class="h-5 w-5" />
        Filters
      </CardTitle>
      <CardDescription>Filter attendance history by name, status, or month</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid gap-4 md:grid-cols-3">
        <!-- Search by Name -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Search by Name</label>
          <div class="relative">
            <Search
              class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              :model-value="searchInput"
              @input="handleSearchInput"
              placeholder="Enter staff name..."
              class="pl-9"
            />
          </div>
        </div>

        <!-- Status Filter -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Status</label>
          <Select
            :model-value="filters.status || 'all'"
            @update:model-value="(value) => handleStatusChange(value as string)"
          >
            <SelectTrigger>
              <SelectValue placeholder="All Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="on_time">On Time</SelectItem>
              <SelectItem value="late">Late</SelectItem>
              <SelectItem value="absent">Absent</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Month Filter -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Month</label>
          <div class="relative">
            <Calendar
              class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              type="month"
              :model-value="filters.month || currentMonth"
              @update:model-value="(value) => handleMonthChange(value as string)"
              class="pl-9"
            />
          </div>
        </div>
      </div>

      <!-- Clear Filters Button -->
      <div class="mt-4">
        <Button variant="outline" size="sm" @click="$emit('clear')"> Clear Filters </Button>
      </div>
    </CardContent>
  </Card>
</template>

