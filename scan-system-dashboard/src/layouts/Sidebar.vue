<script setup lang="ts">
import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
  SidebarRail,
} from '../components/ui/sidebar'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '../components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import AppSidebar from './components/AppSidebar.vue'
import { Search } from 'lucide-vue-next'
import Input from '@/components/ui/input/Input.vue'
import UserMenuDropdown from './components/UserMenuDropdown.vue'
import { mainItems, managementItems, settingItems } from '@/layouts/stores/sidebar.menu'

import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// ✅ Search menu items (main + management)
const allSidebarItems = computed(() => [...mainItems, ...managementItems, ...settingItems])

const searchQuery = ref('')

const handleSidebarSearch = () => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return

  // exact match first, then partial match
  const match =
    allSidebarItems.value.find((item) => item.title.toLowerCase() === query) ||
    allSidebarItems.value.find((item) => item.title.toLowerCase().includes(query))

  if (match) {
    router.push(match.url)
    searchQuery.value = ''
  }
}
</script>

<template>
  <SidebarProvider class="relative flex min-h-screen w-full">
    <AppSidebar />
    <SidebarRail />

    <SidebarInset class="flex min-h-screen flex-1 flex-col">
      <!-- Header -->
      <header
        class="sticky top-0 z-40 flex h-16 items-center gap-2 border-b bg-background/80 px-4 shadow-sm backdrop-blur-md supports-[backdrop-filter]:bg-background/60 lg:px-6"
      >
        <div class="flex flex-1 items-center gap-2">
          <SidebarTrigger
            class="-ml-1 h-9 w-9 rounded-md hover:bg-accent hover:text-accent-foreground lg:hidden"
          />

          <Separator orientation="vertical" class="mr-2 h-4" />

          <!-- ✅ Search (in Sidebar.vue header) -->
          <div class="relative w-full max-w-md">
            <Search
              class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground"
            />
            <Input
              v-model="searchQuery"
              placeholder="Search menu..."
              class="pl-9 h-9"
              @keyup.enter="handleSidebarSearch"
            />
          </div>

          <!-- Spacer -->
          <div class="flex-1" />

          <!-- User Menu -->
          <UserMenuDropdown />
        </div>

        <!-- Header Actions -->
        <div class="flex items-center gap-2">
          <!-- actions later -->
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto">
        <div class="mx-auto w-full p-4">
          <slot />
        </div>
      </main>
    </SidebarInset>
  </SidebarProvider>
</template>

<style scoped>
header {
  transition: all 0.2s ease;
}

@media (max-width: 768px) {
  main {
    padding: 1rem;
  }
}

@media (prefers-color-scheme: dark) {
  header {
    background-color: hsl(var(--background) / 0.8);
  }
}
</style>
