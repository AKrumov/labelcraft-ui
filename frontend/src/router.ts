import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Projects from './views/Projects.vue'
import Project from './views/Project.vue'
import Dataset from './views/Dataset.vue'
import { useAuthStore } from './stores/auth'

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/login', component: Login },
  { path: '/projects', component: Projects, meta: { requiresAuth: true } },
  { path: '/projects/:id', component: Project, meta: { requiresAuth: true } },
  { path: '/datasets/:id', component: Dataset, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!auth.token && to.path !== '/login') {
    return { path: '/login' }
  }
  if (auth.token && to.path === '/login') {
    return { path: '/' }
  }
})

export default router
