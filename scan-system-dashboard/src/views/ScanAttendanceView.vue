<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import OfficeCard from '@/features/scan/components/AttendanceCard.vue'
// import PermissionRequestDialog from '@/features/scan/components/PermissionRequestDialog.vue'
import QrScannerDialog from '@/features/scan/components/QrScannerDialog.vue'
import { QrCode, Hand } from 'lucide-vue-next'
import { useAttendance } from '@/features/scan/composables/useAttendance'
import { useAttendanceStore } from '@/features/scan/store/attendanceStore'

const router = useRouter()
const showQrScanner = ref(false)
// const showPermissionDialog = ref(false)

const openQrScanner = () => {
  showQrScanner.value = true
}

// const openPermissionDialog = () => {
//   showPermissionDialog.value = true
// }

const { handleQrScan, isLoading } = useAttendance()
const attendanceStore = useAttendanceStore()

// Pre-fetch public IP when page loads (performance optimization)
// This avoids delay when scanning - IP is ready before user scans
onMounted(() => {
  attendanceStore.preFetchPublicIp().catch((error) => {
    // Non-critical error - will fetch when scanning if this fails
    console.warn('Failed to pre-fetch public IP:', error)
  })
})

// Handle QR scan success with API integration
const handleQrScanSuccess = async (qrData: string) => {
  console.log('QR Code scanned:', qrData)

  // Parse JSON if QR contains JSON object
  let qrToken: string

  try {
    const parsed = JSON.parse(qrData)
    qrToken = parsed.token // Extract just the token
  } catch {
    // If not JSON, use as-is
    qrToken = qrData
  }

  console.log('Extracted token:', qrToken)

  const result = await handleQrScan(qrToken, () => {
    showQrScanner.value = false
  })

  console.log('Validation result:', result)

  // Navigate to check-in confirmation page if validation successful
  if (result.success && result.data?.valid && result.data?.office) {
    // Encode office data as JSON string for URL
    const officeData = encodeURIComponent(JSON.stringify(result.data.office))

    // Navigate to confirmation page
    router.push({
      name: 'check-in-confirm',
      params: {
        qrToken,
        office: officeData,
      },
    })
  }
}
</script>

<template>
  <main class="container mx-auto p-4 md:p-8 animate-in fade-in duration-500">
    <!-- Header -->
    <header class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between mb-8">
      <div class="space-y-1">
        <h1 class="text-3xl font-semibold tracking-tight text-slate-950">Attendance</h1>
        <p class="text-sm text-slate-500">Manage your staff attendance.</p>
      </div>
    </header>

    <!-- Content -->
    <section class="grid gap-4 sm:grid-cols-2">
      <OfficeCard
        title="Scan Attendance"
        description="Open scanner to check-in/out staff."
        :icon="QrCode"
        :disabled="isLoading"
        @click="openQrScanner"
      />

      <OfficeCard
        title="Ask Permission Stop"
        description="Request permission and add a reason."
        :icon="Hand"
        :disabled="isLoading"
      />

      <!-- Dialog components -->
      <QrScannerDialog v-model:open="showQrScanner" @scan-success="handleQrScanSuccess" />

      <!-- <PermissionRequestDialog
        v-model:open="showPermissionDialog"
        @submit="handlePermissionSubmit"
      /> -->
    </section>
  </main>
</template>
