<script setup lang="ts"></script>

<template>
  <div class="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white">
    <div class="p-8 bg-slate-800 rounded-xl shadow-2xl border border-blue-500/30 text-center">
      <h1 class="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
        Tailwind CSS is working!
      </h1>
      <p class="text-slate-400 mb-6">
        If you see a dark background with blue and emerald gradient text, everything is set up correctly.
      </p>
      <div class="flex gap-4 justify-center">
        <div class="px-4 py-2 bg-blue-600 rounded-lg font-medium hover:bg-blue-500 transition-colors">
          Primary Button
        </div>
        <div class="px-4 py-2 bg-emerald-600 rounded-lg font-medium hover:bg-emerald-500 transition-colors">
          Success Button
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
