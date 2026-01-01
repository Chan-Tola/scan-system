<script setup lang="ts">
  import { onMounted } from 'vue'
  import OfficeDialog from '@/features/office/components/OfficeDialog.vue'
  import OfficeCard from '@/features/office/components/OfficeCard.vue'
  import { useOffice } from '@/features/office'
  import { Building2 } from 'lucide-vue-next'
  
  const { offices, isLoading, error, loadOffices } = useOffice()
  
  onMounted(async () => {
    await loadOffices()
  })
  
  const refreshData = async () => {
    await loadOffices()
  }
  </script>
  
  <template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold tracking-tight">Offices</h1>
          <p class="text-muted-foreground">Manage your office locations and scanners.</p>
        </div>
        <OfficeDialog mode="create" @success="refreshData" />
      </div>
  
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="text-muted-foreground">Loading offices...</div>
      </div>
  
      <div v-else-if="error" class="rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
        {{ error }}
      </div>
  
      <div v-else-if="offices.length > 0" class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <OfficeCard
          v-for="office in offices"
          :key="office.id"
          :icon="Building2"
          :title="office.name"
          :office-id="office.id"
          :public-ip="office.public_ip"
          @delete="refreshData"
          @updated="refreshData"
        />
      </div>
  
      <div v-else class="flex flex-col items-center justify-center py-12 text-center">
        <Building2 class="mb-4 h-12 w-12 text-muted-foreground" />
        <h3 class="text-lg font-semibold">No offices found</h3>
        <p class="text-sm text-muted-foreground">Get started by creating your first office.</p>
      </div>
    </div>
  </template>