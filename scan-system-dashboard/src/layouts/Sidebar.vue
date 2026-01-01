<script setup lang="ts">
import { SidebarProvider, SidebarInset, SidebarTrigger, SidebarRail } from '../components/ui/sidebar'
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
  <SidebarProvider>
    <AppSidebar />
    <SidebarRail />
    <SidebarInset>
      <header
        class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
      >
        <div class="flex items-center gap-2 px-4 ">
          <SidebarTrigger class="-ml-1 lg:hidden" />
          <Separator orientation="vertical" class="mr-2 h-4 lg:hidden" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>Data Fetching</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
      </header>

      <div class="flex flex-1 flex-col gap-4 p-4 pt-0 overflow-auto">
        <slot />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
