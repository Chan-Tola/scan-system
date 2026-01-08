<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import GlobalLoading from '@/components/global/GlobalLoading.vue'
import { Toaster } from 'vue-sonner'

const route = useRoute()

// Map the layouts
const layouts = {
  AuthLayout,
  MainLayout,
}

// Logic: Use the layout defined in router meta, default to MainLayout if none found
const layout = computed(() => {
  const layoutName = route.meta.layout as keyof typeof layouts
  return layouts[layoutName] || MainLayout
})
</script>

<template>
  <!-- Global Loading (can be outside) -->
  <GlobalLoading />

  <component :is="layout">
    <!-- Toast notifications (inside layout) -->
    <Toaster position="top-right" richColors />

    <!-- Your app content -->
    <RouterView />
  </component>
</template>
