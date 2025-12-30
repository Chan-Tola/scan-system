import { storeToRefs } from 'pinia'
import { useAuthStore } from '../store/authStore'
import { useRouter } from 'vue-router'

export function useAuth() {
  const store = useAuthStore()
  const router = useRouter()

  // Keep state reactive
  const { user, isAuthenticated, isLoading, error } = storeToRefs(store)

  const handleLogin = async (credentials: any) => {
    const success = await store.login(credentials)
    if (success) {
      router.push('/dashboard')
    }
  }

  const handleLogout = async () => {
    await store.logout()
    router.push('/login')
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    handleLogin,
    handleLogout,
  }
}
