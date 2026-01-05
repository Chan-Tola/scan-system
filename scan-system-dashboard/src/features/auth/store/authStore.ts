import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useStorage } from '@vueuse/core'
import { authApi } from '../services/authApi'
import type { User, AuthResponse } from '../types'

export const useAuthStore = defineStore('auth', () => {
  // Persistence: saves user to localStorage so they stay logged in on refresh
  const user = useStorage<User | null>('auth_user', null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  // async function login(credentials: any) {
  //   isLoading.value = true
  //   error.value = null
  //   try {
  //     // Step 1: Authenticate and create session
  //     console.log('🔐 Step 1: Authenticating...')
  //     await authApi.login(credentials)

  //     // Step 2: Fetch complete profile with staff details
  //     console.log('👤 Step 2: Fetching complete profile...')
  //     const data = await authApi.me()
  //     user.value = data.user

  //     // Log the complete profile data for verification
  //     console.log('✅ Login successful! Complete profile data:')
  //     console.log('📧 Email:', data.user.email)
  //     console.log('👤 Username:', data.user.username)
  //     console.log('📋 Full Profile:', data.user.profile)

  //     if (data && data.debug_error) {
  //       console.warn('⚠️ Profile fetch debug info:', data.debug_error)
  //     } else if (data && !data.user.profile) {
  //       console.warn('⚠️ Profile is missing but no debug_error was returned from gateway.')
  //     }

  //     return true
  //   } catch (err: any) {
  //     console.error('❌ Login failed:', err)
  //     error.value =
  //       err.response?.data?.detail ||
  //       err.response?.data?.message ||
  //       'Login failed. Please check your credentials.'
  //     return false
  //   } finally {
  //     isLoading.value = false
  //   }
  // }

  async function login(credentials: any) {
    isLoading.value = true
    error.value = null
    try {
      // 1. Auth Call
      await authApi.login(credentials)

      // 2. Get Profile
      const response = (await authApi.me()) as AuthResponse

      // DEBUGGING: If you still see undefined, check this log:
      console.log('DEBUG: Raw response from API:', response)

      // Assign to reactive state
      user.value = response.user

      console.log('✅ Login successful!')
      console.log('📧 Email:', user.value.email)

      // Use optional chaining to prevent crashes if profile is missing
      console.log('📋 Full Profile:', user.value.profile)

      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function checkAuth() {
    // Check if user has valid session cookie and fetch fresh profile
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

  async function refreshProfile() {
    // Refresh user profile (call after updating staff data)
    try {
      const data = await authApi.me()
      user.value = data.user
      return true
    } catch (err: any) {
      console.error('Failed to refresh profile:', err)
      return false
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

  return { user, isAuthenticated, isLoading, error, login, checkAuth, refreshProfile, logout }
})
