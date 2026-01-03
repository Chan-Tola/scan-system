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
} from '@/components/ui/dropdown-menu'

import { useAuth } from '@/features/auth'
import { useRouter, useRoute } from 'vue-router'
import {
  User2,
  ChevronUp,
  LayoutDashboard,
  QrCode,
  ScanLine,
  Building2,
  Users,
  LogOut,
  Settings,
  CreditCard,
} from 'lucide-vue-next'
import LogoCompany from '@/assets/images/logo-company.jpg'

// Authentication & Routing
const { user, handleLogout } = useAuth()
const router = useRouter()
const route = useRoute()

// Menu items with their respective icons
const items = [
  {
    title: 'Dashboard',
    url: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    title: 'Generate QR',
    url: '/qr-generate',
    icon: QrCode,
  },
  {
    title: 'Scan QR',
    url: '/scan-qr',
    icon: ScanLine,
  },
  {
    title: 'Office',
    url: '/office',
    icon: Building2,
  },
  {
    title: 'Staff Members',
    url: '/staff',
    icon: Users,
  },
]

// Navigation handler
const handleNavigation = (url: string) => {
  if (url && url !== '#') {
    router.push(url)
  }
}

// Check if the current route matches the menu item
const isActive = (url: string) => route.path === url
</script>

<template>
  <Sidebar collapsible="icon" variant="inset" class="border-r border-slate-200 flex flex-col">
    <SidebarHeader class="shrink-0">
      <div class="flex items-center justify-center px-2 py-6">
        <div
          class="flex h-20 w-20 items-center justify-center rounded-xl bg-white shadow-sm border border-slate-100 overflow-hidden transition-all group-data-[collapsible=icon]:h-8 group-data-[collapsible=icon]:w-8"
        >
          <img :src="LogoCompany" alt="Company Logo" class="h-full w-full object-contain p-1" />
        </div>
      </div>
    </SidebarHeader>

    <SidebarContent class="flex-1 min-h-0 overflow-y-auto">
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="item in items" :key="item.title">
            <SidebarMenuButton
              :tooltip="item.title"
              :is-active="isActive(item.url)"
              @click="handleNavigation(item.url)"
              class="transition-colors hover:bg-slate-100"
            >
              <component :is="item.icon" class="size-4 shrink-0" />
              <span class="font-medium text-sm">{{ item.title }}</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>

    <SidebarFooter class="shrink-0 pb-4 mt-auto border-t border-slate-200 bg-sidebar">
      <SidebarMenu>
        <SidebarMenuItem v-if="user">
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <SidebarMenuButton
                class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
              >
                <div
                  class="flex h-6 w-6 items-center justify-center rounded-full bg-slate-900 text-white shrink-0"
                >
                  <User2 class="size-3" />
                </div>
                <span class="truncate font-semibold">{{ user.username }}</span>
                <ChevronUp class="ml-auto size-4 text-slate-400" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>

            <DropdownMenuContent
              side="top"
              align="start"
              class="w-[--radix-popper-anchor-width] mb-2 p-1"
            >
              <DropdownMenuItem class="flex items-center gap-2 cursor-pointer">
                <Settings class="size-4" />
                <span>Account Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem class="flex items-center gap-2 cursor-pointer">
                <CreditCard class="size-4" />
                <span>Billing</span>
              </DropdownMenuItem>
              <div class="my-1 h-px bg-slate-100" />
              <DropdownMenuItem
                @click="handleLogout"
                class="flex items-center gap-2 cursor-pointer text-rose-600 focus:text-rose-600 focus:bg-rose-50"
              >
                <LogOut class="size-4" />
                <span>Sign out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </Sidebar>
</template>

<style scoped>
/* Ensure the sidebar menu buttons transition smoothly when the sidebar collapses */
span {
  transition: opacity 0.2s ease-in-out;
}

/* Ensure sidebar container uses flex layout and full height */
:deep([data-sidebar="sidebar"]) {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}

/* Ensure content area can scroll independently */
:deep([data-sidebar="content"]) {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: rgb(203 213 225) transparent;
}

:deep([data-sidebar="content"])::-webkit-scrollbar {
  width: 6px;
}

:deep([data-sidebar="content"])::-webkit-scrollbar-track {
  background: transparent;
}

:deep([data-sidebar="content"])::-webkit-scrollbar-thumb {
  background-color: rgb(203 213 225);
  border-radius: 3px;
}

:deep([data-sidebar="content"])::-webkit-scrollbar-thumb:hover {
  background-color: rgb(148 163 184);
}

/* Ensure footer stays fixed at bottom */
:deep([data-sidebar="footer"]) {
  flex-shrink: 0;
  margin-top: auto;
  position: sticky;
  bottom: 0;
  background-color: hsl(var(--sidebar-background));
  z-index: 10;
}

/* Mobile responsive adjustments */
@media (max-width: 1024px) {
  :deep([data-sidebar="sidebar"]) {
    height: 100vh;
    max-height: 100vh;
  }
}

/* Tablet and smaller screens */
@media (max-width: 768px) {
  :deep([data-sidebar="sidebar"]) {
    height: 100vh;
    max-height: 100vh;
  }
  
  :deep([data-sidebar="footer"]) {
    padding-bottom: env(safe-area-inset-bottom, 1rem);
  }
}

/* Small mobile screens */
@media (max-width: 390px) {
  :deep([data-sidebar="sidebar"]) {
    height: 100vh;
    max-height: 100vh;
  }
}
</style>
