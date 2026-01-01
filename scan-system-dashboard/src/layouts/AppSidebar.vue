<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../components/ui/dropdown-menu'
import { useAuth } from '@/features/auth'
import { useRouter } from 'vue-router'
import { User2, ChevronUp } from 'lucide-vue-next'

// Authentication
const { user, handleLogout } = useAuth()
const router = useRouter()

// Menu items
const items = [
  { title: 'Dashboard', url: '/dashboard' },
  { title: 'Generate QR', url: '/generate-qr' },
  { title: 'Scan QR', url: '/scan-qr' },
  { title: 'Office', url: '/office' },
  { title: 'Staff Members', url: '/staff' },
]

// Navigation handler
const handleNavigation = (url: string) => {
  if (url && url !== '#') {
    router.push(url)
  }
}
</script>

<template>
  <Sidebar collapsible="icon" variant="inset">
    <SidebarHeader>
      <div class="flex items-center gap-2 px-4 py-2">
        <div
          class="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground"
        >
          logo
        </div>
        <span class="font-semibold">Techey</span>
      </div>
    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="item in items" :key="item.title">
            <SidebarMenuButton 
              :tooltip="item.title"
              @click="handleNavigation(item.url)"
            >
              <span>{{ item.title }}</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>

    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem v-if="user">
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <SidebarMenuButton>
                <User2 class="size-4" />
                <span>{{ user.username }}</span>
                <ChevronUp class="ml-auto size-4" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="top" class="w-[--radix-popper-anchor-width]">
              <DropdownMenuItem>Account</DropdownMenuItem>
              <DropdownMenuItem>Billing</DropdownMenuItem>
              <DropdownMenuItem @click="handleLogout">Sign out</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </Sidebar>
</template>
