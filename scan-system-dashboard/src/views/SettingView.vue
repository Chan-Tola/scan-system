<script setup lang="ts">
import SettingsSidebar from '@/features/setting/components/SettingsSidebar.vue'
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 py-6">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold">Settings</h1>
      <p class="text-sm text-muted-foreground">Manage your account preferences and sercurity.</p>
    </div>

    <div class="grid gap-6 md:grid-cols-[260px_1fr]">
      <aside class="rounded-xl bg-card border">
        <SettingsSidebar />
      </aside>
      <main class="rounded-xl border bg-card p-4 md:p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
