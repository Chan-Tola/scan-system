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
  SidebarGroupLabel,
  SidebarGroupContent,
} from '@/components/ui/sidebar'

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
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
  ChevronRight,
  Home,
} from 'lucide-vue-next'
import LogoCompany from '@/assets/images/logo-company.jpg'
import { computed } from 'vue'
import AvatarImage from '@/components/ui/avatar/AvatarImage.vue'
import Avatar from '@/components/ui/avatar/Avatar.vue'

// Authentication & Routing
const { user, handleLogout } = useAuth()
const router = useRouter()
const route = useRoute()

// Menu items with their respective icons
const mainItems = [
  {
    title: 'Dashboard',
    url: '/dashboard',
    icon: Home,
    isActive: true,
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
]

const managementItems = [
  {
    title: 'Office Management',
    url: '/office',
    icon: Building2,
  },
  {
    title: 'Staff Members',
    url: '/staff',
    icon: Users,
  },
]

const settingItems = [
  {
    title: 'Settings',
    url: '/setting',
    icon: Settings,
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

// User initials for avatar
const userInitials = computed(() => {
  if (!user.value?.username) return 'U'
  return user.value.username.charAt(0).toUpperCase()
})
</script>

<template>
  <Sidebar
    collapsible="icon"
    variant="inset"
    class="border-r bg-sidebar text-sidebar-foreground transition-all duration-300"
  >
    <!-- Logo Header -->
    <SidebarHeader class="px-3 py-4 border-b">
      <div class="flex items-center gap-2 px-1">
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 border border-primary/20 shadow-sm overflow-hidden transition-all duration-300 group-data-[collapsible=icon]/sidebar:h-8 group-data-[collapsible=icon]/sidebar:w-8"
        >
          <img
            :src="LogoCompany"
            alt="Company Logo"
            class="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
          />
        </div>
        <div
          class="flex flex-col overflow-hidden transition-all duration-300 group-data-[collapsible=icon]/sidebar:opacity-0 group-data-[collapsible=icon]/sidebar:w-0"
        >
          <h2 class="text-sm font-bold tracking-tight text-foreground truncate">Your Company</h2>
          <p
            class="text-[10px] font-medium text-muted-foreground truncate uppercase tracking-wider"
          >
            Premium Panel
          </p>
        </div>
      </div>
    </SidebarHeader>

    <!-- Navigation Content -->
    <SidebarContent class="flex-1 overflow-y-auto py-4">
      <!-- Main Navigation -->
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarGroupLabel
            class="px-3 text-xs font-semibold uppercase text-muted-foreground tracking-wider"
          >
            Main Menu
          </SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in mainItems" :key="item.title">
              <SidebarMenuButton
                :tooltip="item.title"
                :is-active="isActive(item.url)"
                @click="handleNavigation(item.url)"
                class="group relative px-3 py-2.5 my-0.5 rounded-lg transition-all duration-200 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              >
                <component
                  :is="item.icon"
                  class="size-4 shrink-0 transition-transform group-hover:scale-110"
                />
                <span class="ml-3 font-medium text-sm truncate transition-all duration-200">
                  {{ item.title }}
                </span>
                <ChevronRight
                  class="ml-auto size-3 opacity-0 -translate-x-1 transition-all group-hover:opacity-100 group-hover:translate-x-0"
                />
                <span
                  v-if="isActive(item.url)"
                  class="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-primary"
                />
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <!-- Management Section -->
      <SidebarGroup class="mt-6">
        <SidebarGroupLabel
          class="px-3 text-xs font-semibold uppercase text-muted-foreground tracking-wider"
        >
          Management
        </SidebarGroupLabel>
        <SidebarGroupContent class="mt-2">
          <SidebarMenu>
            <SidebarMenuItem v-for="item in managementItems" :key="item.title">
              <SidebarMenuButton
                :tooltip="item.title"
                :is-active="isActive(item.url)"
                @click="handleNavigation(item.url)"
                class="group relative px-3 py-2.5 my-0.5 rounded-lg transition-all duration-200 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              >
                <component
                  :is="item.icon"
                  class="size-4 shrink-0 transition-transform group-hover:scale-110"
                />
                <span class="ml-3 font-medium text-sm truncate transition-all duration-200">
                  {{ item.title }}
                </span>
                <ChevronRight
                  class="ml-auto size-3 opacity-0 -translate-x-1 transition-all group-hover:opacity-100 group-hover:translate-x-0"
                />
                <span
                  v-if="isActive(item.url)"
                  class="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-primary"
                />
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>

    <!-- User Profile Footer -->
    <SidebarFooter class="p-3 border-t">
      <SidebarMenu>
        <SidebarMenuItem v-if="user">
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <SidebarMenuButton
                class="w-full px-3 py-2.5 rounded-lg hover:bg-sidebar-accent transition-colors duration-200 group"
              >
                <div class="flex items-center w-full">
                  <!-- Avatar -->
                  <div class="relative group">
                    <Avatar
                      class="h-9 w-9 border-2 border-sidebar-accent/50 transition-transform group-hover:scale-105"
                    >
                      <AvatarImage
                        v-if="user?.profile?.profile_image"
                        :src="user.profile.profile_image"
                      />
                      <AvatarFallback
                        class="bg-gradient-to-br from-primary to-primary/70 text-white text-xs font-bold"
                      >
                        {{ userInitials }}
                      </AvatarFallback>
                    </Avatar>

                    <!-- <div
                      class="absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-sidebar bg-emerald-500 shadow-sm"
                      title="Online"
                    /> -->
                  </div>

                  <!-- User Info -->
                  <div
                    class="ml-3 flex-1 overflow-hidden text-left transition-all duration-300 group-data-[collapsible=icon]/sidebar:opacity-0 group-data-[collapsible=icon]/sidebar:w-0"
                  >
                    <p class="text-sm font-semibold truncate">{{ user.username }}</p>
                    <p class="text-xs text-muted-foreground truncate">{{ user.role }}</p>
                  </div>

                  <!-- Chevron -->
                  <ChevronUp
                    class="ml-auto size-4 text-muted-foreground transition-transform duration-200 group-data-[state=open]:rotate-180"
                  />
                </div>
              </SidebarMenuButton>
            </DropdownMenuTrigger>

            <DropdownMenuContent
              side="top"
              align="end"
              class="w-56 p-2 rounded-lg shadow-lg border bg-popover"
            >
              <DropdownMenuLabel class="p-2">
                <div class="flex items-center gap-2">
                  <div class="flex flex-col">
                    <span class="font-semibold">{{ user.username }}</span>
                    <span class="text-xs text-muted-foreground">{{ user.email }}</span>
                  </div>
                </div>
              </DropdownMenuLabel>

              <DropdownMenuSeparator class="my-2" />

              <DropdownMenuItem
                v-for="item in settingItems"
                :key="item.title"
                @click="handleNavigation(item.url)"
                class="flex items-center gap-2 p-2 rounded-md cursor-pointer hover:bg-accent focus:bg-accent"
              >
                <component
                  :is="item.icon"
                  class="size-4 shrink-0 transition-transform group-hover:scale-110"
                />
                <span>{{ item.title }}</span>
              </DropdownMenuItem>

              <DropdownMenuSeparator class="my-2" />

              <DropdownMenuItem
                @click="handleLogout"
                class="flex items-center gap-2 p-2 rounded-md cursor-pointer text-destructive hover:bg-destructive/10 focus:bg-destructive/10 focus:text-destructive"
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
/* Custom scrollbar for sidebar */
:deep([data-sidebar='content']) {
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--muted)) transparent;
}

:deep([data-sidebar='content'])::-webkit-scrollbar {
  width: 4px;
}

:deep([data-sidebar='content'])::-webkit-scrollbar-track {
  background: transparent;
}

:deep([data-sidebar='content'])::-webkit-scrollbar-thumb {
  background-color: hsl(var(--muted));
  border-radius: 20px;
}

/* Sidebar collapse animation */
:deep([data-sidebar='sidebar']) {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  :deep([data-sidebar='sidebar']) {
    position: fixed;
    z-index: 50;
    height: 100vh;
  }
}

/* Smooth hover transitions */
.sidebar-menu-button {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
