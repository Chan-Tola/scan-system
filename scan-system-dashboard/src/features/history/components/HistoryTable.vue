<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  TableEmpty,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import type { HistoryRecord } from '../types'
import { formatTime } from '@/lib/time';


defineProps<{
  records: HistoryRecord[]
  isLoading: boolean
  getStatusBadgeVariant: (status: string) => string
  getStatusLabel: (status: string) => string
}>()

</script>

<template>
  <div v-if="isLoading" class="flex items-center justify-center py-12">
    <div class="h-8 w-8 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
  </div>

  <div v-else-if="records.length === 0" class="py-12">
    <TableEmpty message="No attendance records found" />
  </div>

  <div v-else class="rounded-md border">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Staff Name</TableHead>
          <TableHead>Office</TableHead>
          <TableHead>Date</TableHead>
          <TableHead>Check In</TableHead>
          <TableHead>Check Out</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Minutes Late</TableHead>
          <TableHead>Work Hours</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="record in records" :key="record.id">
          <TableCell class="font-medium">
            {{ record.staff_name }}
          </TableCell>
          <TableCell>{{ record.office_name }}</TableCell>
          <TableCell>{{ record.log_date }}</TableCell>
          <TableCell>{{ formatTime(record.check_in) }}</TableCell>
          <TableCell>{{ formatTime(record.check_out) }}</TableCell>
          <TableCell>
            <Badge>
              {{ getStatusLabel(record.status) }}
            </Badge>
          </TableCell>
          <TableCell>{{ record.minutes_late }}</TableCell>
          <TableCell>
            {{ record.work_hours ? `${record.work_hours.toFixed(2)}h` : '-' }}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

