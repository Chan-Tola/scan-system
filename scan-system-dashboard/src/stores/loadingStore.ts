import { defineStore } from 'pinia'
import { ref } from 'vue'
export const useLoadingStore = defineStore('loading', () => {
  const isLoading = ref(false)
  const loadingMessage = ref('Loading...')

  // Show loading spinner
  const show = (message = 'Loading...') => {
    loadingMessage.value = message
    isLoading.value = true
  }

  // Hide loading spinner
  const hide = () => {
    isLoading.value = false
  }

  return {
    isLoading,
    loadingMessage,
    show,
    hide,
  }
})
