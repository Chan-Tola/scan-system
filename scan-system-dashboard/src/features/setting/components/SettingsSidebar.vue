<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

type NavItem = { label: string; to: { name: string }; desc?: string }

const route = useRoute()

const items: NavItem[] = [
  { label: 'Acount', to: { name: 'setting-account' }, desc: 'Profile & Information' },
  { label: 'Theme', to: { name: '' }, desc: 'Appearance preferences' },
  { label: 'Security', to: { name: '' }, desc: 'Password & sessions' },
]

const isActive = (name: string) => route.name === name
</script>
<template>
  <div class="p-3">
    <div class="p-2 text-sm font-medium text-muted-foreground">Preferences</div>

    <nav class="space-y-1">
      <RouterLink
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        class="block rounded-lg px-3 py-2 transition"
        :class="isActive(item.to.name) ? 'bg-accent text-accent-foreground' : 'hover:bg-muted'"
      >
        <div class="text-sm font-medium">{{ item.label }}</div>
        <div v-if="item.desc" class="text-xs text-muted-foreground">{{ item.desc }}</div>
      </RouterLink>
    </nav>
  </div>
</template>
