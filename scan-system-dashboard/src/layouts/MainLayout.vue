<script setup lang="ts">
import Sidebar from './Sidebar.vue'
</script>

<template>
  <div class="bg-background text-foreground antialiased">
    <Sidebar>
      <slot />
    </Sidebar>
  </div>
</template>
