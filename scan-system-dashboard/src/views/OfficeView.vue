<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import OfficeDialog from '@/features/office/components/OfficeDialog.vue'
import OfficeCard from '@/features/office/components/OfficeCard.vue'
import { useOffice } from '@/features/office'
import { Building2, Search, Filter, Plus, AlertTriangle } from 'lucide-vue-next'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import type { Office } from '@/features/office/types'

const { offices, isLoading, error, loadOffices, handleDeleteOffice } = useOffice()

// Local State
const searchQuery = ref('')
const isDeleteOpen = ref(false)
const officeToDelete = ref<number | null>(null)

// For Edit Dialog
const isEditOpen = ref(false)
const editingOffice = ref<Office | null>(null)

onMounted(async () => {
  await loadOffices()
})

const refreshData = async () => {
  await loadOffices()
}

// Filtered Data
const filteredOffices = computed(() => {
  if (!searchQuery.value) return offices.value
  const query = searchQuery.value.toLowerCase()
  return offices.value.filter(
    (office) =>
      office.name.toLowerCase().includes(query) || office.public_ip?.toLowerCase().includes(query),
  )
})

const performDelete = async () => {
  if (officeToDelete.value) {
    const success = await handleDeleteOffice(officeToDelete.value)
    if (success) {
      await refreshData()
      isDeleteOpen.value = false
      officeToDelete.value = null
    }
  }
}
</script>

<template>
  <div class="container mx-auto p-4 md:p-8 animate-in fade-in duration-500">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900">Offices</h1>
        <p class="text-slate-500 mt-1">Manage your office locations and scanner configurations.</p>
      </div>
      <OfficeDialog mode="create" @success="refreshData" />
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row gap-4 mb-6">
      <div class="relative flex-1 max-w-md">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
        <Input v-model="searchQuery" placeholder="Search offices..." class="pl-10 bg-white" />
      </div>
      <!-- Add filters here if needed later -->
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 space-y-4">
      <div
        class="h-8 w-8 border-4 border-primary/20 border-t-primary rounded-full animate-spin"
      ></div>
      <div class="text-muted-foreground animate-pulse">Loading office data...</div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="rounded-lg border border-destructive/50 bg-destructive/5 p-4 text-destructive flex items-center gap-2"
    >
      <AlertTriangle class="h-5 w-5" />
      {{ error }}
    </div>

    <!-- Content -->
    <div v-else-if="filteredOffices.length > 0">
      <!-- Card Grid View (Visible on all screens) -->
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <OfficeCard
          v-for="office in filteredOffices"
          :key="office.id"
          :icon="Building2"
          :title="office.name"
          :office-id="office.id"
          :public-ip="office.public_ip"
          :shift-start="office.shift_start"
          :shift-end="office.shift_end"
          @delete="refreshData"
          @updated="refreshData"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else
      class="flex flex-col items-center justify-center py-16 text-center border-2 border-dashed rounded-xl bg-slate-50/50"
    >
      <div class="bg-white p-4 rounded-full shadow-sm mb-4">
        <Building2 class="h-8 w-8 text-slate-400" />
      </div>
      <h3 class="text-lg font-semibold text-slate-900">No offices found</h3>
      <p class="text-sm text-slate-500 max-w-xs mx-auto mt-1">
        {{
          searchQuery
            ? 'No results for your search.'
            : 'Get started by creating your first office location.'
        }}
      </p>
      <Button v-if="searchQuery" variant="link" @click="searchQuery = ''" class="mt-2">
        Clear search
      </Button>
    </div>

    <!-- Global Delete Dialog -->
    <Dialog :open="isDeleteOpen" @update:open="isDeleteOpen = $event">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Office</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete this office? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" @click="isDeleteOpen = false">Cancel</Button>
          <Button variant="destructive" @click="performDelete">Delete</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Global Edit Dialog -->
    <OfficeDialog
      v-if="editingOffice"
      mode="edit"
      v-model:open="isEditOpen"
      :office-id="editingOffice.id"
      :initial-name="editingOffice.name"
      :initial-ip="editingOffice.public_ip"
      :initial-shift-start="editingOffice.shift_start"
      :initial-shift-end="editingOffice.shift_end"
      @success="refreshData"
    />
  </div>
</template>
