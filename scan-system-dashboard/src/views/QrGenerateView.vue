<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
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

// Handle office selection (automatically loads QR code if exists)
const handleOfficeSelect = async (officeId: number) => {
  await selectOffice(officeId)
}

// Handle QR code generation/regeneration
const handleGenerate = async () => {
  if (!selectedOfficeId.value) {
    alert('Please select an office first')
    return
  }

  // If QR code exists, regenerate it; otherwise generate new one
  if (currentQRCode.value && hasQRCodeForSelectedOffice.value) {
    // Regenerate - the store will update currentQRCode with the new token from backend
    await handleRegenerateQRCode(currentQRCode.value.id)
  } else {
    await handleGenerateQRCode(selectedOfficeId.value)
  }
}

// Refresh data
const refreshData = async () => {
  await loadOffices()
  await loadQRCodes({ is_active: true })
  // Reload QR code for selected office if exists
  if (selectedOfficeId.value) {
    await selectOffice(selectedOfficeId.value)
  }
}
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-0 lg:h-full lg:min-h-0">
    <!-- OFFICE DIRECTORY -->
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

    <!-- LIVE PREVIEW -->
    <LivePreview
      :qr-code="currentQRCode"
      :is-loading="qrLoading"
      :error="qrError"
      @refresh="refreshData"
    />
  </div>
  <!-- <div class="bg-slate-50 sm:p-4 md:p-6 overflow-hidden flex flex-col font-sans">
    <div
      class="bg-white border border-slate-200 rounded-3xl shadow-sm flex-1 flex flex-col overflow-hidden"
    >
    </div>
  </div> -->
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:deep(*) {
  font-family: 'Inter', sans-serif;
}

/* Custom Clean Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
