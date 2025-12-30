import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useStorage } from '@vueuse/core'
import { authApi } from '../services/authApi'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', () => {
  // Persistence: saves user to localStorage so they stay logged in on refresh
  const user = useStorage<User | null>('auth_user', null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(credentials: any) {
    isLoading.value = true
    error.value = null
    try {
      const data = await authApi.login(credentials)
      user.value = data.user
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Login failed. Please check your credentials.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function checkAuth() {
    // Check if user has valid session cookie
    isLoading.value = true
    try {
      const data = await authApi.me()
      user.value = data.user
      return true
    } catch (err: any) {
      // Session expired or invalid - clear user
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch (err) {
      // Ignore errors on logout
    } finally {
      user.value = null
    }
  }

  return { user, isAuthenticated, isLoading, error, login, checkAuth, logout }
})
