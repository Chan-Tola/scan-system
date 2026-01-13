<script setup lang="ts">
import { Button } from '@/components/ui/button'

defineProps<{
  pagination: {
    current_page: number
    last_page: number
    total: number
  }
}>()

const emit = defineEmits<{
  (e: 'go-to-page', page: number): void
}>()
</script>

<template>
  <div v-if="pagination.last_page > 1" class="mt-4 flex items-center justify-between">
    <div class="text-sm text-muted-foreground">
      Page {{ pagination.current_page }} of {{ pagination.last_page }}
    </div>
    <div class="flex gap-2">
      <Button
        variant="outline"
        size="sm"
        :disabled="pagination.current_page === 1"
        @click="$emit('go-to-page', pagination.current_page - 1)"
      >
        Previous
      </Button>
      <Button
        variant="outline"
        size="sm"
        :disabled="pagination.current_page === pagination.last_page"
        @click="$emit('go-to-page', pagination.current_page + 1)"
      >
        Next
      </Button>
    </div>
  </div>
</template>

