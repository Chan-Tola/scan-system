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
</script>

<template>
  <SidebarProvider class="relative flex min-h-screen w-full">
    <AppSidebar />
    <SidebarRail />

    <SidebarInset class="flex min-h-screen flex-1 flex-col">
      <!-- Header -->
      <header
        class="sticky top-0 z-40 flex h-14 items-center gap-2 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4 lg:px-6"
      >
        <div class="flex flex-1 items-center gap-2">
          <SidebarTrigger
            class="-ml-1 size-9 rounded-md hover:bg-accent lg:hidden"
            variant="ghost"
          />
          <Separator orientation="vertical" class="mr-2 h-4 lg:hidden" />

          <Breadcrumb class="hidden sm:flex">
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
                <BreadcrumbPage class="text-sm font-medium"> Data Fetching </BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>

          <!-- Mobile title -->
          <div class="sm:hidden">
            <h1 class="text-base font-semibold">Dashboard</h1>
          </div>
        </div>

        <!-- Optional: Add header actions here -->
        <div class="flex items-center gap-2">
          <!-- Place for notifications, search, etc. -->
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto">
        <div class="mx-auto w-full max-w-7xl p-4 md:p-6">
          <slot />
        </div>
      </main>

      <!-- Footer -->
      <footer class="border-t py-3 px-6 text-center text-xs text-muted-foreground">
        <div class="flex flex-col items-center justify-between gap-2 md:flex-row">
          <span>© {{ new Date().getFullYear() }} Your Company. All rights reserved.</span>
          <div class="flex items-center gap-4">
            <a href="#" class="hover:text-foreground transition-colors">Privacy Policy</a>
            <a href="#" class="hover:text-foreground transition-colors">Terms of Service</a>
            <a href="#" class="hover:text-foreground transition-colors">Help</a>
          </div>
        </div>
      </footer>
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
