<script setup lang="ts">
import { useLoadingStore } from '@/stores/loadingStore'
import { Loader2 } from 'lucide-vue-next'
const loadingStore = useLoadingStore()
</script>
<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="loadingStore.isLoading"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      >
        <div class="bg-white rounded-lg p-8 shadow-2xl">
          <!-- Spinning loader -->
          <Loader2 class="w-12 h-12 animate-spin text-black mx-auto" />

          <!-- Loading message -->
          <p class="mt-4 text-sm font-medium text-black/70">
            {{ loadingStore.loadingMessage }}
          </p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
