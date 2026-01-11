<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import type { Component } from 'vue'

interface Props {
  title: string
  description?: string
  icon?: Component
  disabled?: boolean
}

defineProps<Props>()
defineEmits<{
  (e: 'click'): void
}>()
</script>

<template>
  <Card
    class="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md focus-within:ring-2 focus-within:ring-slate-950/10"
  >
    <!-- subtle hover sheen -->
    <div
      class="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100 bg-gradient-to-b from-slate-50 to-transparent"
    />

    <button
      type="button"
      class="w-full text-left p-6 outline-none"
      :disabled="disabled"
      @click="$emit('click')"
    >
      <div class="flex items-start justify-between gap-4">
        <div class="space-y-1">
          <p class="text-base font-semibold tracking-tight text-slate-950">
            {{ title }}
          </p>
          <p v-if="description" class="text-sm text-slate-500">
            {{ description }}
          </p>
        </div>

        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-950 transition-colors group-hover:border-slate-300"
        >
          <component v-if="icon" :is="icon" class="h-5 w-5" />
        </div>
      </div>

      <div class="mt-5">
        <Button
          class="h-10 rounded-xl bg-slate-950 px-4 text-sm font-medium text-white hover:bg-slate-900 active:bg-slate-950 disabled:opacity-60"
        >
          Open
        </Button>
      </div>
    </button>
  </Card>
</template>
