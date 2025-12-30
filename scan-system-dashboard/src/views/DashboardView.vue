<script setup lang="ts">
import { useAuth } from '@/features/auth/composables/useAuth'
import { Button } from '@/components/ui/button'

const { user, handleLogout } = useAuth()
</script>

<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Dashboard</h1>
      <Button @click="handleLogout" variant="outline">Logout</Button>
    </div>
    
    <div v-if="user" class="bg-card p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Welcome, {{ user.username }}!</h2>
      <p class="text-muted-foreground">Email: {{ user.email }}</p>
      <p class="text-muted-foreground">ID: {{ user.id }}</p>
    </div>
  </div>
</template>

