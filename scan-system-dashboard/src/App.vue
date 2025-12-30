<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AuthLayout from './layouts/AuthLayout.vue'
import MainLayout from './layouts/MainLayout.vue'

const route = useRoute()

// Map the layouts
const layouts = {
  AuthLayout,
  MainLayout
}

// Logic: Use the layout defined in router meta, default to MainLayout if none found
const activeLayout = computed(() => {
  const layoutName = route.meta.layout as keyof typeof layouts
  return layouts[layoutName] || MainLayout
})
</script>

<template>
  <component :is="activeLayout">
    <router-view />
  </component>
</template>
