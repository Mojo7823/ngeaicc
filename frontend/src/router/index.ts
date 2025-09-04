import { createRouter, createWebHistory } from 'vue-router'

// Import page components
import Dashboard from '../views/Dashboard.vue'
import PingTool from '../views/PingTool.vue'
import Preview from '../views/Preview.vue'

// Documentation pages (placeholder pages)
import TOEDescription from '../views/documentation/TOEDescription.vue'
import AssuranceActivities from '../views/documentation/AssuranceActivities.vue'
import AssuranceEquivalency from '../views/documentation/AssuranceEquivalency.vue'
import TestBedDescription from '../views/documentation/TestBedDescription.vue'
import TSSGuidance from '../views/documentation/TSSGuidance.vue'
import SecurityRequirements from '../views/documentation/SecurityRequirements.vue'

// Settings pages (placeholder pages)
import DatabaseSettings from '../views/settings/DatabaseSettings.vue'
import APISettings from '../views/settings/APISettings.vue'
import SystemSettings from '../views/settings/SystemSettings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/tools/ping',
    name: 'PingTool',
    component: PingTool
  },
  {
    path: '/preview',
    name: 'Preview',
    component: Preview
  },
  // Documentation routes
  {
    path: '/documentation/toe-description',
    name: 'TOEDescription',
    component: TOEDescription
  },
  {
    path: '/documentation/assurance-activities',
    name: 'AssuranceActivities',
    component: AssuranceActivities
  },
  {
    path: '/documentation/assurance-equivalency',
    name: 'AssuranceEquivalency',
    component: AssuranceEquivalency
  },
  {
    path: '/documentation/test-bed-description',
    name: 'TestBedDescription',
    component: TestBedDescription
  },
  {
    path: '/documentation/tss-guidance',
    name: 'TSSGuidance',
    component: TSSGuidance
  },
  {
    path: '/documentation/security-requirements',
    name: 'SecurityRequirements',
    component: SecurityRequirements
  },
  // Settings routes
  {
    path: '/settings/database',
    name: 'DatabaseSettings',
    component: DatabaseSettings
  },
  {
    path: '/settings/api',
    name: 'APISettings',
    component: APISettings
  },
  {
    path: '/settings/system',
    name: 'SystemSettings',
    component: SystemSettings
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
