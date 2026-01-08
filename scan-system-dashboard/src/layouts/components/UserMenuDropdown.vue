<script setup lang="ts">
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import Avatar from '@/components/ui/avatar/Avatar.vue'
import AvatarImage from '@/components/ui/avatar/AvatarImage.vue'
import AvatarFallback from '@/components/ui/avatar/AvatarFallback.vue'

import { Settings, LogOut, ChevronDown } from 'lucide-vue-next'
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
      <button class="inline-flex items-center gap-3 bg-white px-3 py-2 text-black shadow-sm">
        <div class="hidden sm:flex flex-col items-end leading-tight">
          <span class="text-sm font-semibold tracking-tight">{{ user.profile?.full_name }}</span>
          <span class="text-xs text-black/60 capitalize">{{ user.role }}</span>
        </div>

        <Avatar class="h-8 w-8 border border-black/10">
          <AvatarImage v-if="user?.profile?.profile_image" :src="user.profile.profile_image" />
          <AvatarFallback class="bg-black/[0.04] text-[11px] font-bold text-black/60">
            {{ userInitials }}
          </AvatarFallback>
        </Avatar>

        <ChevronDown class="h-4 w-4 text-black/60" />
      </button>
    </DropdownMenuTrigger>

    <DropdownMenuContent
      align="center"
      class="w-56 rounded-2xl border border-black/10 bg-white p-2 shadow-xl"
    >
      <DropdownMenuLabel class="p-2">
        <div class="flex flex-col gap-0.5">
          <span class="text-sm font-semibold">{{ user.username }}</span>
          <span class="text-xs text-black/60">{{ user.email }}</span>
        </div>
      </DropdownMenuLabel>

      <DropdownMenuSeparator class="my-2 bg-black/10" />

      <DropdownMenuItem
        class="flex cursor-pointer items-center gap-2 rounded-xl p-2 text-black outline-none focus:bg-black/[0.04]"
        @click="go('/setting')"
      >
        <Settings class="h-4 w-4 text-black/70" />
        <span class="text-sm font-medium">Settings</span>
      </DropdownMenuItem>

      <DropdownMenuSeparator class="my-2 bg-black/10" />

      <DropdownMenuItem
        class="flex cursor-pointer items-center gap-2 rounded-xl p-2 text-black outline-none focus:bg-black/[0.04]"
        @click="handleLogout"
      >
        <LogOut class="h-4 w-4 text-black/70" />
        <span class="text-sm font-medium">Sign out</span>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
