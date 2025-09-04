import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '../components/DashboardLayout.vue'
import HomePage from '../views/HomePage.vue'
import PingTool from '../views/PingTool.vue'
import MaintenancePage from '../views/MaintenancePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      children: [
        {
          path: '',
          name: 'Home',
          component: HomePage
        },
        {
          path: 'tools',
          name: 'Tools',
          component: MaintenancePage
        },
        {
          path: 'tools/ping',
          name: 'Ping Test',
          component: PingTool
        },
        {
          path: 'documentation',
          name: 'Documentation',
          component: MaintenancePage
        },
        {
          path: 'documentation/toe-description',
          name: 'TOE Description',
          component: MaintenancePage
        },
        {
          path: 'documentation/assurance-activities',
          name: 'Assurance Activities',
          component: MaintenancePage
        },
        {
          path: 'documentation/assurance-equivalency',
          name: 'Assurance Equivalency',
          component: MaintenancePage
        },
        {
          path: 'documentation/test-bed',
          name: 'Test Bed Description',
          component: MaintenancePage
        },
        {
          path: 'documentation/tss-guidance',
          name: 'TSS and Guidance',
          component: MaintenancePage
        },
        {
          path: 'documentation/security-requirements',
          name: 'Security Requirements',
          component: MaintenancePage
        },
        {
          path: 'settings',
          name: 'Settings',
          component: MaintenancePage
        },
        {
          path: 'settings/database',
          name: 'Database Settings',
          component: MaintenancePage
        },
        {
          path: 'settings/api',
          name: 'API Settings',
          component: MaintenancePage
        },
        {
          path: 'settings/system',
          name: 'System Settings',
          component: MaintenancePage
        }
      ]
    }
  ],
})

export default router
