import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { layout: 'AuthLayout', requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { layout: 'MainLayout', requiresAuth: true }
    },
    {
      path: '/office',
      name: 'office',
      component: () => import('@/views/OfficeView.vue'),
      meta: { layout: 'MainLayout', requiresAuth: true }
    }
  ],
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // If route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // If route requires guest (login page) and user is authenticated
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router