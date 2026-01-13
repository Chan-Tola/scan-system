<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import type { MonthlyTrendPoint } from '../types'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

const props = defineProps<{
  data: MonthlyTrendPoint[]
}>()

const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    windowWidth.value = window.innerWidth
    window.addEventListener('resize', updateWindowWidth)
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateWindowWidth)
  }
})

const chartData = computed(() => ({
  labels: props.data.map((d) => new Date(d.date).getDate()), // 1-31
  datasets: [
    {
      label: 'On Time',
      data: props.data.map((d) => d.on_time_percentage),
      borderColor: '#60a5fa', // Blue
      backgroundColor: 'rgba(96, 165, 250, 0.1)',
      tension: 0.4,
      fill: true,
      borderWidth: windowWidth.value < 640 ? 3 : 2.5,
      pointRadius: windowWidth.value < 640 ? 4 : 3,
      pointHoverRadius: windowWidth.value < 640 ? 6 : 5,
      pointBackgroundColor: '#60a5fa',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointHoverBorderWidth: 3,
    },
    {
      label: 'Late',
      data: props.data.map((d) => d.late_percentage),
      borderColor: '#f59e0b', // Amber
      backgroundColor: 'rgba(245, 158, 11, 0.1)',
      tension: 0.4,
      fill: true,
      borderWidth: windowWidth.value < 640 ? 3 : 2.5,
      pointRadius: windowWidth.value < 640 ? 4 : 3,
      pointHoverRadius: windowWidth.value < 640 ? 6 : 5,
      pointBackgroundColor: '#f59e0b',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointHoverBorderWidth: 3,
    },
    {
      label: 'Absent',
      data: props.data.map((d) => d.absent_percentage),
      borderColor: '#ef4444', // Red
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4,
      fill: true,
      borderWidth: windowWidth.value < 640 ? 3 : 2.5,
      pointRadius: windowWidth.value < 640 ? 4 : 3,
      pointHoverRadius: windowWidth.value < 640 ? 6 : 5,
      pointBackgroundColor: '#ef4444',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointHoverBorderWidth: 3,
    },
  ],
}))

const chartOptions: any = computed(() => {
  const isMobile = windowWidth.value < 640
  const isTablet = windowWidth.value < 1024

  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          usePointStyle: true,
          pointStyle: 'circle',
          padding: isMobile ? 8 : isTablet ? 10 : 12,
          boxWidth: isMobile ? 8 : 10,
          boxHeight: isMobile ? 8 : 10,
          color: '#64748b', // Slate-500
          font: {
            size: isMobile ? 11 : isTablet ? 12 : 13,
            weight: '500',
            family: 'ui-sans-serif, system-ui',
          },
        },
      },
      title: { display: false },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
        backgroundColor: '#ffffff', // White
        titleColor: '#0f172a', // Slate-900
        bodyColor: '#475569', // Slate-600
        borderColor: '#e2e8f0', // Slate-200
        borderWidth: 1,
        padding: isMobile ? 10 : 12,
        displayColors: true,
        titleFont: {
          size: isMobile ? 12 : 13,
          weight: '600',
        },
        bodyFont: {
          size: isMobile ? 11 : 12,
        },
        callbacks: {
          label: (context: any) =>
            `${context.dataset.label}: ${Number(context.parsed.y).toFixed(1)}%`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value: number) => `${value}%`,
          color: '#64748b', // Slate-500
          font: {
            size: isMobile ? 10 : isTablet ? 11 : 12,
            weight: '500',
          },
          maxTicksLimit: isMobile ? 6 : 8,
          padding: isMobile ? 6 : 8,
        },
        grid: {
          color: '#e2e8f0', // Slate-200
          lineWidth: 1,
        },
        border: {
          color: '#cbd5e1', // Slate-300
          width: 1,
        },
      },
      x: {
        ticks: {
          color: '#64748b', // Slate-500
          font: {
            size: isMobile ? 10 : isTablet ? 11 : 12,
            weight: '500',
          },
          maxTicksLimit: isMobile ? 10 : isTablet ? 15 : 20,
          padding: isMobile ? 4 : 6,
        },
        grid: {
          display: true,
          color: '#f1f5f9', // Slate-100 (very subtle)
          lineWidth: 1,
        },
        border: {
          color: '#475569', // Slate-600
          width: 1,
        },
      },
    },
    interaction: {
      mode: 'nearest' as const,
      axis: 'x' as const,
      intersect: false,
    },
    layout: {
      padding: {
        top: isMobile ? 5 : 10,
        bottom: isMobile ? 5 : 10,
        left: isMobile ? 0 : 5,
        right: isMobile ? 0 : 5,
      },
    },
  }
})
</script>

<template>
  <div
    class="w-full max-w-full overflow-hidden px-3 sm:px-4 md:px-5 py-3 sm:py-4 md:py-5 bg-white rounded-lg border border-slate-200"
  >
    <!-- Mobile: Taller chart for better readability -->
    <div class="w-full h-[320px] sm:h-[340px] md:h-[360px] lg:h-[400px] xl:h-[440px] min-w-0">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
