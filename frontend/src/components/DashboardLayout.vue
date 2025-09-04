<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const sidebarExpanded = ref(true)

// Menu items configuration
const menuItems = [
  { 
    id: 'home', 
    title: 'Home', 
    icon: '🏠', 
    route: '/',
    children: []
  },
  {
    id: 'tools',
    title: 'Tools',
    icon: '🔧',
    route: '/tools',
    children: [
      { id: 'ping-test', title: 'Ping Test', route: '/tools/ping', icon: '📡' }
    ]
  },
  {
    id: 'documentation',
    title: 'Documentation',
    icon: '📚',
    route: '/documentation',
    children: [
      { id: 'toe-description', title: 'TOE Description', route: '/documentation/toe-description', icon: '📋' },
      { id: 'assurance-activities', title: 'Assurance Activities Identification', route: '/documentation/assurance-activities', icon: '✅' },
      { id: 'assurance-equivalency', title: 'Assurance Equivalency Justification', route: '/documentation/assurance-equivalency', icon: '⚖️' },
      { id: 'test-bed', title: 'Test Bed Description', route: '/documentation/test-bed', icon: '🧪' },
      { id: 'tss-guidance', title: 'TSS and Guidance activities', route: '/documentation/tss-guidance', icon: '📖' },
      { id: 'security-requirements', title: 'Security Assurance Requirements', route: '/documentation/security-requirements', icon: '🔒' }
    ]
  },
  {
    id: 'settings',
    title: 'Settings',
    icon: '⚙️',
    route: '/settings',
    children: [
      { id: 'database-settings', title: 'Database Settings', route: '/settings/database', icon: '💾' },
      { id: 'api-settings', title: 'API', route: '/settings/api', icon: '🔌' },
      { id: 'system-settings', title: 'System', route: '/settings/system', icon: '🖥️' }
    ]
  }
]

const expandedItems = ref<string[]>(['tools', 'documentation', 'settings'])

const toggleExpanded = (itemId: string) => {
  if (expandedItems.value.includes(itemId)) {
    expandedItems.value = expandedItems.value.filter(id => id !== itemId)
  } else {
    expandedItems.value.push(itemId)
  }
}

const navigateTo = (route: string) => {
  router.push(route)
}

const toggleSidebar = () => {
  sidebarExpanded.value = !sidebarExpanded.value
}
</script>

<template>
  <div class="dashboard-layout">
    <!-- Top Toolbar -->
    <header class="toolbar">
      <div class="toolbar-left">
        <button @click="toggleSidebar" class="sidebar-toggle">
          {{ sidebarExpanded ? '◀' : '▶' }}
        </button>
        <h1 class="app-title">NGE AI Testing Platform</h1>
      </div>
      <div class="toolbar-right">
        <span class="current-page">{{ route.name || 'Dashboard' }}</span>
        <div class="user-menu">
          <span class="user-avatar">👤</span>
        </div>
      </div>
    </header>

    <div class="dashboard-body">
      <!-- Sidebar -->
      <nav :class="['sidebar', { 'sidebar-collapsed': !sidebarExpanded }]">
        <ul class="menu-list">
          <li v-for="item in menuItems" :key="item.id" class="menu-item">
            <!-- Parent item -->
            <div 
              :class="['menu-item-header', { 'active': route.path === item.route }]"
              @click="item.children.length > 0 ? toggleExpanded(item.id) : navigateTo(item.route)"
            >
              <span class="menu-icon">{{ item.icon }}</span>
              <span v-if="sidebarExpanded" class="menu-title">{{ item.title }}</span>
              <span 
                v-if="sidebarExpanded && item.children.length > 0" 
                :class="['menu-expand-icon', { 'expanded': expandedItems.includes(item.id) }]"
              >
                ▼
              </span>
            </div>

            <!-- Children items (accordion) -->
            <ul 
              v-if="item.children.length > 0 && expandedItems.includes(item.id)" 
              :class="['submenu', { 'submenu-collapsed': !sidebarExpanded }]"
            >
              <li v-for="child in item.children" :key="child.id" class="submenu-item">
                <div 
                  :class="['submenu-item-header', { 'active': route.path === child.route }]"
                  @click="navigateTo(child.route)"
                >
                  <span class="submenu-icon">{{ child.icon }}</span>
                  <span v-if="sidebarExpanded" class="submenu-title">{{ child.title }}</span>
                </div>
              </li>
            </ul>
          </li>
        </ul>
      </nav>

      <!-- Main Content Area -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.sidebar-toggle {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.app-title {
  margin: 0;
  font-size: 1.5em;
  font-weight: 600;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.current-page {
  font-size: 0.9em;
  opacity: 0.9;
}

.user-menu {
  display: flex;
  align-items: center;
}

.user-avatar {
  font-size: 1.5em;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
}

.dashboard-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e1e1e1;
  transition: width 0.3s ease;
  overflow-y: auto;
  box-shadow: 2px 0 4px rgba(0,0,0,0.1);
}

.sidebar-collapsed {
  width: 60px;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  border-bottom: 1px solid #f0f0f0;
}

.menu-item-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  position: relative;
}

.menu-item-header:hover {
  background-color: #f8f9fa;
}

.menu-item-header.active {
  background-color: #e3f2fd;
  border-right: 3px solid #667eea;
}

.menu-icon {
  font-size: 1.2em;
  width: 20px;
  text-align: center;
  margin-right: 12px;
}

.menu-title {
  flex: 1;
  font-weight: 500;
  color: #333;
}

.menu-expand-icon {
  font-size: 0.8em;
  color: #666;
  transition: transform 0.2s ease;
}

.menu-expand-icon.expanded {
  transform: rotate(180deg);
}

.submenu {
  list-style: none;
  padding: 0;
  margin: 0;
  background-color: #f8f9fa;
}

.submenu-collapsed {
  display: none;
}

.submenu-item {
  border-bottom: 1px solid #e9ecef;
}

.submenu-item:last-child {
  border-bottom: none;
}

.submenu-item-header {
  display: flex;
  align-items: center;
  padding: 12px 20px 12px 52px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submenu-item-header:hover {
  background-color: #e9ecef;
}

.submenu-item-header.active {
  background-color: #d1ecf1;
  border-right: 3px solid #17a2b8;
}

.submenu-icon {
  font-size: 1em;
  width: 16px;
  text-align: center;
  margin-right: 10px;
}

.submenu-title {
  font-size: 0.9em;
  color: #495057;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f5f5;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    height: 100%;
    z-index: 999;
    left: 0;
    top: 60px;
  }

  .sidebar-collapsed {
    left: -280px;
  }

  .main-content {
    margin-left: 0;
  }

  .app-title {
    font-size: 1.2em;
  }

  .current-page {
    display: none;
  }
}
</style>