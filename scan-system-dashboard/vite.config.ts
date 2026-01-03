import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import basicSsl from '@vitejs/plugin-basic-ssl'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // or '0.0.0.0'
    port: 5173,
    allowedHosts: [
      'localhost',
      '.ngrok-free.dev', // Allows ALL ngrok subdomains
      '.ngrok.io', // For older ngrok URLs
    ],
  },
  resolve: {
    alias: {
      // This maps the @ symbol to your src folder
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
