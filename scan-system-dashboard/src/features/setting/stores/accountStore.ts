import { defineStore } from 'pinia'
import { ref } from 'vue'
import { staffApi } from '@/features/staff/services/staffApi'
import type { StaffUpdate } from '@/features/staff/types'
import { useLoadingStore } from '@/stores/loadingStore'
import { toast } from 'vue-sonner'
import { useAuthStore } from '@/features/auth'

export const useAccountStore = defineStore('account', () => {
  const error = ref<string | null>(null)

  async function updateProfile(profileData: StaffUpdate) {
    const authStore = useAuthStore()
    const loadingStore = useLoadingStore()

    // Get profile ID from auth user
    const profileId = authStore.user?.profile?.id
    if (!profileId) {
      toast.error('Profile not found.')
      return { success: false, error: 'Profile not found.' }
    }

    loadingStore.show('Updating Profile...')
    error.value = null

    try {
      // user existing staffApi.updateStaff - it already handle images!
      const updateProfile = await staffApi.updateStaff(profileId, profileData)

      //   Refresh auth profile to update UI everywhere
      await authStore.refreshProfile()

      toast.success('Profile updated successfully')
      return { success: true, data: updateProfile }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to update profile'
      toast.error(`Failed to update profile: ${error.value}`)
      return { success: false, error: error.value }
    } finally {
      loadingStore.hide()
    }
  }
  return {
    error,
    updateProfile,
  }
})
