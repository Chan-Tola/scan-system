<script setup lang="ts">
import { computed } from 'vue'
import type { MonthlyTrendPoint } from '../types'

const props = defineProps<{
  data: MonthlyTrendPoint[]
}>()

// Calculate monthly averages
const monthlyStats = computed(() => {
  if (!props.data || props.data.length === 0) {
    return {
      onTimeAvg: 0,
      lateAvg: 0,
      absentAvg: 0,
    }
  }

  const total = props.data.length
  const onTimeSum = props.data.reduce((sum, d) => sum + d.on_time_percentage, 0)
  const lateSum = props.data.reduce((sum, d) => sum + d.late_percentage, 0)
  const absentSum = props.data.reduce((sum, d) => sum + d.absent_percentage, 0)

  return {
    onTimeAvg: Math.round(onTimeSum / total),
    lateAvg: Math.round(lateSum / total),
    absentAvg: Math.round(absentSum / total),
  }
})
</script>

<template>
  <div class="grid grid-cols-1 gap-3">
    <!-- On Time Card -->
    <div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-blue-900">On Time This Month</span>
        <span class="text-2xl font-bold text-blue-600">{{ monthlyStats.onTimeAvg }}%</span>
      </div>
      <div class="w-full bg-blue-200 rounded-full h-2.5">
        <div
          class="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
          :style="{ width: `${monthlyStats.onTimeAvg}%` }"
        ></div>
      </div>
    </div>

    <!-- Late Card -->
    <div class="bg-gradient-to-r from-amber-50 to-amber-100 rounded-lg p-4 border border-amber-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-amber-900">Late This Month</span>
        <span class="text-2xl font-bold text-amber-600">{{ monthlyStats.lateAvg }}%</span>
      </div>
      <div class="w-full bg-amber-200 rounded-full h-2.5">
        <div
          class="bg-amber-600 h-2.5 rounded-full transition-all duration-500"
          :style="{ width: `${monthlyStats.lateAvg}%` }"
        ></div>
      </div>
    </div>

    <!-- Absent Card -->
    <div class="bg-gradient-to-r from-red-50 to-red-100 rounded-lg p-4 border border-red-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-red-900">Absent This Month</span>
        <span class="text-2xl font-bold text-red-600">{{ monthlyStats.absentAvg }}%</span>
      </div>
      <div class="w-full bg-red-200 rounded-full h-2.5">
        <div
          class="bg-red-600 h-2.5 rounded-full transition-all duration-500"
          :style="{ width: `${monthlyStats.absentAvg}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>
