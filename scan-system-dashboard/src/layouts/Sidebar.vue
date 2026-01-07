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
import AppSidebar from './AppSidebar.vue'
import { Search } from 'lucide-vue-next'
import Input from '@/components/ui/input/Input.vue'
import { computed } from 'vue'

// Filtered Data
// const filteredOffices = computed(() => {
//   if (!AppSidebar.) return offices.value
//   const query = searchQuery.value.toLowerCase()
//   return offices.value.filter(
//     (office) =>
//       office.name.toLowerCase().includes(query) || office.public_ip?.toLowerCase().includes(query),
//   )
// })
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
          <div class="flex flex-col sm:flex-row items-center gap-4 flex-1">
            <div class="relative w-full max-w-md">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />

              <Input
                v-model="searchQuery"
                placeholder="Search staff members..."
                class="pl-10 bg-white border-slate-200 focus:ring-primary/20 transition-all shadow-sm"
              />
            </div>

            <div class="flex-1"></div>
          </div>

          <!-- <Breadcrumb class="hidden sm:flex">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink
                  href="#"
                  class="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                >
                  Dashboard
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage class="text-sm font-medium text-foreground">
                  Data Fetching
                </BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb> -->

          <!-- Mobile title with premium typography -->
          <!-- <div class="flex-1 sm:hidden flex justify-center">
            <h1 class="text-sm font-semibold tracking-tight">Dashboard</h1>
          </div> -->
          <!-- Spacer to balance the center title on mobile if needed, or just let it flex -->
          <!-- <div class="w-9 sm:hidden"></div> -->
        </div>

        <!-- Header Actions -->
        <div class="flex items-center gap-2">
          <!-- Add Theme Toggle or Notifications here later -->
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
/* Smooth transitions */
header {
  transition: all 0.2s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  main {
    padding: 1rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  header {
    background-color: hsl(var(--background) / 0.8);
  }
}
</style>
