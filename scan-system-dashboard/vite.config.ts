import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import basicSsl from '@vitejs/plugin-basic-ssl'

export default defineConfig({
  plugins: [vue(), basicSsl()],
  server: {
    host: true, // Allows access from: Phone, Other laptops on same Wi-Fi network
    https: {}, // Enable HTTPS (needed for cookies/camera/iOS)
    /*
    ❗ Uses a self-signed cert (browser will warn)
    Needed for:
    - Cookies (Secure)
    - Camera / QR scanning
    - iOS Safari (https://192.168.18.120:5173)
    */
    port: 5173,
    allowedHosts: ['localhost', '.ngrok-free.dev', '.ngrok.io'],
    // Add proxy configuration
    proxy: {
      '/api': {
        // Use environment variable for API Gateway URL
        target: process.env.VITE_API_GATEWAY_URL || 'http://localhost:80',
        // Falls back to localhost if not set
        changeOrigin: true,
        /*
          Changes request Host header to backend host
          Prevents CORS issues.        
        */
        secure: false, // Allow self-signed certificates
        ws: true,
        /* Enables WebSocket proxy
        Needed for:
        - Realtime updates
        - Socket connections
        - Some QR / live scan use cases
        */
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
