<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dashboardApi } from '@/features/dashboard/services/dashboardApi'
import StatCard from '@/features/dashboard/components/StartCard.vue'
import type { DashboardData } from '@/features/dashboard/types'
import MonthlyTrendLineGraph from '@/features/dashboard/components/MonthlyTrendLineGraph.vue'
import MonthlySummaryCards from '@/features/dashboard/components/MonthlySummaryCards.vue'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Loader2, RefreshCw } from 'lucide-vue-next'

const dashboardData = ref<DashboardData | null>(null)
const isLoading = ref(false)
const error = ref('')

const loadDashboard = async () => {
  isLoading.value = true
  error.value = ''

  try {
    dashboardData.value = await dashboardApi.getDashboard()
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Failed to load dashboard'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<template>
  <div class="w-full max-w-full overflow-x-hidden">
    <div
      class="container mx-auto px-3 py-4 sm:px-4 sm:py-6 md:px-6 md:py-8 animate-in fade-in duration-500"
    >
      <!-- Header -->
      <div class="flex items-start justify-between gap-2 sm:gap-3 mb-3 sm:mb-4 md:mb-6">
        <div class="space-y-0.5 min-w-0 flex-1">
          <h1
            class="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold tracking-tight text-foreground truncate"
          >
            Dashboard
          </h1>
          <p class="text-[11px] sm:text-xs md:text-sm lg:text-base text-muted-foreground">
            Overview of attendance statistics
          </p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="space-y-3 sm:space-y-4">
        <Card class="border shadow-sm">
          <CardContent
            class="py-6 sm:py-8 md:py-10 flex items-center justify-center gap-2 sm:gap-3"
          >
            <Loader2 class="h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
            <p class="text-[11px] sm:text-xs md:text-sm text-muted-foreground">
              Loading dashboard…
            </p>
          </CardContent>
        </Card>

        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 sm:gap-3 md:gap-4 lg:gap-6"
        >
          <Card v-for="n in 3" :key="n" class="border shadow-sm">
            <CardContent class="p-3 sm:p-4 md:p-6">
              <div class="h-3 sm:h-4 w-28 sm:w-32 md:w-40 rounded bg-muted" />
              <div
                class="mt-2.5 sm:mt-3 md:mt-4 h-6 sm:h-7 md:h-8 w-14 sm:w-16 md:w-20 rounded bg-muted"
              />
              <div
                class="mt-2 sm:mt-2.5 md:mt-3 h-2.5 sm:h-3 w-20 sm:w-24 md:w-28 rounded bg-muted"
              />
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- Error -->
      <Alert v-else-if="error" variant="destructive" class="border">
        <AlertTitle class="text-xs sm:text-sm font-medium">Couldn't load dashboard</AlertTitle>
        <AlertDescription class="text-[11px] sm:text-xs md:text-sm break-words">
          {{ error }}
        </AlertDescription>
      </Alert>

      <!-- Content -->
      <div v-else-if="dashboardData" class="space-y-3 sm:space-y-4 md:space-y-6 lg:space-y-8">
        <!-- Stats -->
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 sm:gap-3 md:gap-4 lg:gap-6"
        >
          <StatCard
            title="Active Staff Today"
            :value="dashboardData.daily_stats.active_staff"
            type="active"
            class="border shadow-sm"
          />
          <StatCard
            title="Absent Today"
            :value="dashboardData.daily_stats.absent_staff"
            type="absent"
            class="border shadow-sm"
          />
          <StatCard
            title="On Time Today"
            :value="dashboardData.daily_stats.on_time_count"
            type="ontime"
            class="border shadow-sm sm:col-span-2 md:col-span-1"
          />
        </div>

        <!-- Monthly Trend -->
        <Card class="border shadow-sm overflow-hidden">
          <CardHeader class="pb-3 px-3 sm:px-4 md:px-6 pt-4 sm:pt-5 md:pt-6">
            <CardTitle class="text-sm sm:text-base md:text-lg lg:text-xl font-semibold">
              Monthly Attendance Trend
            </CardTitle>
            <CardDescription class="text-xs sm:text-sm md:text-base mt-1">
              Attendance volume by day (last 30 days)
            </CardDescription>
          </CardHeader>

          <!-- Mobile: Show Summary Cards -->
          <div class="block sm:hidden px-3 pb-4">
            <MonthlySummaryCards :data="dashboardData.monthly_trend.data_points" />
          </div>

          <!-- Desktop/Tablet: Show Line Graph -->
          <div class="hidden sm:block">
            <MonthlyTrendLineGraph :data="dashboardData.monthly_trend.data_points" />
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>
