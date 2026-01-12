<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarGroupLabel,
  SidebarGroupContent,
  useSidebar,
} from '@/components/ui/sidebar'

import { useRouter, useRoute } from 'vue-router'

import { ChevronRight } from 'lucide-vue-next'

import LogoCompany from '@/assets/images/logo-company.jpg'

// ✅ single source of truth for menu items
import { mainItems, managementItems } from '@/layouts/stores/sidebar.menu'

// Routing + auth
const router = useRouter()
const route = useRoute()

// Sidebar state
const { isMobile, setOpenMobile } = useSidebar()

// Navigate helper - close sidebar on mobile after navigation
const go = (url: string) => {
  if (url && url !== '#') {
    router.push(url)
    // Close sidebar on mobile devices after navigation
    if (isMobile.value) {
      setOpenMobile(false)
    }
  }
}

// Active state (supports nested routes: /setting/account marks /setting active)
const isActive = (url: string) => route.path === url || route.path.startsWith(url + '/')
</script>

<template>
  <Sidebar
    collapsible="icon"
    variant="inset"
    class="border-r bg-sidebar text-sidebar-foreground transition-all duration-300"
  >
    <!-- Header: logo + company name -->
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
          <h2 class="text-sm font-bold tracking-tight text-foreground truncate">Techey</h2>
          <p
            class="text-[10px] font-medium text-muted-foreground truncate uppercase tracking-wider"
          >
            Premium Panel
          </p>
        </div>
      </div>
    </SidebarHeader>

    <!-- Content: menus -->
    <SidebarContent class="flex-1 overflow-y-auto py-4">
      <!-- Main -->
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
                @click="go(item.url)"
                class="group relative px-3 py-2.5 my-0.5 rounded-lg transition-all duration-200 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              >
                <component :is="item.icon" class="size-4 shrink-0" />
                <span class="ml-3 font-medium text-sm truncate">
                  {{ item.title }}
                </span>

                <span
                  v-if="isActive(item.url)"
                  class="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-primary"
                />
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <!-- Management -->
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
                @click="go(item.url)"
                class="group relative px-3 py-2.5 my-0.5 rounded-lg transition-all duration-200 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              >
                <component :is="item.icon" class="size-4 shrink-0" />
                <span class="ml-3 font-medium text-sm truncate">
                  {{ item.title }}
                </span>

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
  </Sidebar>
</template>

<style scoped>
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

:deep([data-sidebar='sidebar']) {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (max-width: 768px) {
  :deep([data-sidebar='sidebar']) {
    position: fixed;
    z-index: 50;
    height: 100vh;
  }
}
</style>
