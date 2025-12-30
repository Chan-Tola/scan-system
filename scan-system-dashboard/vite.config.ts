import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // This maps the @ symbol to your src folder
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
