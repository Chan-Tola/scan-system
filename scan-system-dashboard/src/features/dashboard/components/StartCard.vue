<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  value: number
  type: 'active' | 'absent' | 'ontime'
}>()

const subtitle = computed(() => {
  switch (props.type) {
    case 'active':
      return 'Currently present'
    case 'absent':
      return 'Did not attend'
    case 'ontime':
      return 'Arrived on time'
    default:
      return ''
  }
})
</script>
<template>
  <div class="rounded-xl border bg-background p-3 sm:p-4 md:p-6 shadow-sm transition hover:shadow-md w-full min-w-0">
    <div class="flex items-start justify-between gap-2 sm:gap-3 md:gap-4">
      <!-- Left -->
      <div class="space-y-0.5 sm:space-y-1 min-w-0 flex-1">
        <p class="text-[10px] sm:text-[11px] md:text-xs lg:text-sm text-muted-foreground truncate">
          {{ title }}
        </p>

        <p class="text-lg sm:text-2xl md:text-3xl lg:text-4xl font-semibold tracking-tight text-foreground leading-none">
          {{ value }}
        </p>

        <p class="text-[9px] sm:text-[10px] md:text-xs text-muted-foreground truncate">
          {{ subtitle }}
        </p>
      </div>
    </div>
  </div>
</template>
