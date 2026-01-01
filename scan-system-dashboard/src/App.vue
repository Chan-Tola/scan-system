<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

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
  <component :is="layout">
    <RouterView />
  </component>
</template>
