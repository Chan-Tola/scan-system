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
  <!-- Fixed height container that fits within the layout without scrolling -->
  <div
    class="lg:h-[calc(100vh-8rem)] overflow-hidden bg-white rounded-xl border border-slate-200 shadow-xl ring-1 ring-slate-900/5"
  >
    <!-- Grid layout -->
    <div class="grid grid-cols-1 lg:grid-cols-2 h-full gap-0">
      <!-- OFFICE DIRECTORY -->
      <div class="h-full">
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

      <!-- LIVE PREVIEW -->
      <div class="h-full">
        <LivePreview
          :qr-code="currentQRCode"
          :is-loading="qrLoading"
          :error="qrError"
          @refresh="refreshData"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar styling for the entire app */
:deep(.custom-scrollbar)::-webkit-scrollbar {
  width: 6px;
}
:deep(.custom-scrollbar)::-webkit-scrollbar-track {
  background: #f1f5f9;
}
:deep(.custom-scrollbar)::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
:deep(.custom-scrollbar)::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Mobile: Stack components vertically and allow vertical scrolling */
@media (max-width: 1023px) {
  .grid {
    display: flex;
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }

  .h-full {
    height: auto;
    min-height: 50vh;
  }
}
</style>
