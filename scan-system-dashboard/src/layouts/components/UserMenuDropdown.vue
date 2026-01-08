<script setup lang="ts">
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
// Profile Avatar
import AvatarImage from '@/components/ui/avatar/AvatarImage.vue'
import Avatar from '@/components/ui/avatar/Avatar.vue'

import { useAuth } from '@/features/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const { user, handleLogout } = useAuth()
const router = useRouter()
const go = (path: string) => router.push(path)

const userInitials = computed(() => {
  if (!user.value?.username) return 'U'
  return user.value.username.charAt(0).toUpperCase()
})
</script>
<template>
  <DropdownMenu v-if="user">
    <DropdownMenuTrigger as-child>
      <button class="flex items-center gap-2 bg-card px-3 py-2 transition">
        <div class="hidden sm:flex flex-col items-start leading-tight">
          <span class="text-sm font-semibold">{{ user.username }}</span>
          <span class="text-xs text-muted-foreground">{{ user.role }}</span>
        </div>

        <Avatar class="h-8 w-8">
          <AvatarImage v-if="user?.profile?.profile_image" :src="user.profile.profile_image" />
        </Avatar>
      </button>
    </DropdownMenuTrigger>

    <DropdownMenuContent align="start" class="w-56 p-2">
      <DropdownMenuLabel class="p-2">
        <div class="flex flex-col">
          <span class="font-semibold">{{ user.username }}</span>
          <span class="text-xs text-muted-foreground">{{ user.email }}</span>
        </div>
      </DropdownMenuLabel>

      <DropdownMenuSeparator class="my-2" />

      <DropdownMenuItem
        class="flex items-center gap-2 p-2 rounded-md cursor-pointer"
        @click="go('/setting')"
      >
        <Settings class="h-4 w-4" />
        <span>Settings</span>
      </DropdownMenuItem>

      <DropdownMenuSeparator class="my-2" />

      <DropdownMenuItem
        class="flex items-center gap-2 p-2 rounded-md cursor-pointer text-destructive hover:bg-destructive/10"
        @click="handleLogout"
      >
        <LogOut class="h-4 w-4" />
        <span>Sign out</span>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
