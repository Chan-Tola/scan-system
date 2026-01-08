import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/styles/index.css'
import 'vue-sonner/style.css' // Import vue-sonner styles
import App from './App.vue'
import router from './router'
import { useAuthStore } from './features/auth/store/authStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Check authentication on app startup
const authStore = useAuthStore()
authStore.checkAuth().then(() => {
  app.mount('#app')
})
