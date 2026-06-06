import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/main',
    component: () => import('../views/MainView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: () => import('../views/AdminView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/worldcup',
    component: () => import('../views/WorldCupView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) return next('/login')
  if (to.meta.requiresAdmin && !auth.isAdmin) return next('/main')
  if (to.meta.guest && auth.token) return next('/main')
  next()
})

export default router
