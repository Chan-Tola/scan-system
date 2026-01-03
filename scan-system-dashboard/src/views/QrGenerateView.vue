<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useQrGenerate } from '@/features/qr-generate'
import { useOffice } from '@/features/office'
import OfficeDirectory from '@/features/qr-generate/components/officeDirectory.vue'
import LivePreview from '@/features/qr-generate/components/livePreview.vue'

const { offices, isLoading: officesLoading, loadOffices } = useOffice()
const {
  currentQRCode,
  selectedOfficeId,
  isLoading: qrLoading,
  error: qrError,
  hasQRCodeForSelectedOffice,
  handleGenerateQRCode,
  handleRegenerateQRCode,
  selectOffice,
  loadQRCodes,
} = useQrGenerate()

const searchQuery = ref('')

// Filter offices based on search
const filteredOffices = computed(() => {
  if (!searchQuery.value) return offices.value
  const query = searchQuery.value.toLowerCase()
  return offices.value.filter(
    (office) => office.name.toLowerCase().includes(query) || office.id.toString().includes(query),
  )
})

// Load offices and QR codes on mount
onMounted(async () => {
  await loadOffices()
  await loadQRCodes({ is_active: true })
})

// Handle office selection
const handleOfficeSelect = async (officeId: number) => {
  await selectOffice(officeId)
}

// Handle QR code generation/regeneration
const handleGenerate = async () => {
  if (!selectedOfficeId.value) {
    alert('Please select an office first')
    return
  }

  if (currentQRCode.value && hasQRCodeForSelectedOffice.value) {
    await handleRegenerateQRCode(currentQRCode.value.id)
  } else {
    await handleGenerateQRCode(selectedOfficeId.value)
  }
}

// Refresh data
const refreshData = async () => {
  await loadOffices()
  await loadQRCodes({ is_active: true })
  if (selectedOfficeId.value) {
    await selectOffice(selectedOfficeId.value)
  }
}
</script>

<template>
  <!-- Remove fixed height and allow natural scrolling -->
  <div class="bg-slate-50">
    <!-- Page container with proper padding -->
    <div class="max-w-screen-2xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <!-- Page header -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">QR Code Generator</h1>
        <p class="mt-2 text-sm text-gray-600">
          Generate and manage QR codes for your office locations
        </p>
      </div>

      <!-- Main content grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        <!-- Office Directory - Takes 5 columns on desktop -->
        <div class="lg:col-span-5 xl:col-span-4">
          <OfficeDirectory
            :offices="filteredOffices"
            :selected-office-id="selectedOfficeId"
            :is-loading="officesLoading || qrLoading"
            :search-query="searchQuery"
            :has-qr-code="hasQRCodeForSelectedOffice"
            @select-office="handleOfficeSelect"
            @generate="handleGenerate"
            @update:search-query="searchQuery = $event"
          />
        </div>

        <!-- Live Preview - Takes 7 columns on desktop -->
        <div class="lg:col-span-7 xl:col-span-8">
          <LivePreview
            :qr-code="currentQRCode"
            :is-loading="qrLoading"
            :error="qrError"
            @refresh="refreshData"
          />
        </div>
      </div>

      <!-- Optional footer information -->
      <!-- <div class="mt-12 pt-8 border-t border-gray-200">
        <div class="text-center text-sm text-gray-500">
          <p>Need help? Contact support at support@example.com</p>
          <p class="mt-1">All QR codes are securely generated and encrypted</p>
        </div>
      </div> -->
    </div>
  </div>
</template>

<style scoped>
/* Smooth scrolling for the entire page */
:root {
  scroll-behavior: smooth;
}

/* Custom scrollbar for the page */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Responsive spacing */
@media (max-width: 1024px) {
  .max-w-screen-2xl {
    max-width: 100%;
  }
}

/* Print styles */
@media print {
  .bg-slate-50 {
    background-color: white !important;
  }

  .border,
  .shadow-sm {
    border: 1px solid #e2e8f0 !important;
    box-shadow: none !important;
  }
}
</style>
