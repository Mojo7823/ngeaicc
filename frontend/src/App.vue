<template>
  <div id="app" class="app-layout">
    <!-- Sidebar -->
    <nav class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <h3 v-if="!sidebarCollapsed">NGEAICC</h3>
        <button @click="toggleSidebar" class="sidebar-toggle">
          <span v-if="sidebarCollapsed">☰</span>
          <span v-else>←</span>
        </button>
      </div>
      
      <div class="sidebar-content">
        <!-- Home -->
        <div class="menu-item">
          <router-link to="/" class="menu-link" exact-active-class="active">
            <span class="menu-icon">🏠</span>
            <span v-if="!sidebarCollapsed" class="menu-text">Home</span>
          </router-link>
        </div>
        
        <!-- Preview -->
        <div class="menu-item">
          <router-link to="/preview" class="menu-link" exact-active-class="active">
            <span class="menu-icon">📄</span>
            <span v-if="!sidebarCollapsed" class="menu-text">Preview</span>
          </router-link>
        </div>
        
        <!-- Test Evaluation -->
        <div class="menu-section">
          <div class="menu-header" @click="toggleSection('testEvaluation')">
            <span class="menu-icon">🧪</span>
            <span v-if="!sidebarCollapsed" class="menu-text">Test Evaluation</span>
            <span v-if="!sidebarCollapsed" class="menu-arrow" :class="{ expanded: expandedSections.testEvaluation }">▼</span>
          </div>
          <div v-if="!sidebarCollapsed && expandedSections.testEvaluation" class="submenu">
            <router-link to="/test-evaluation/test-cases" class="submenu-link">
              <span class="submenu-icon">📋</span>
              <span class="submenu-text">Test Cases</span>
            </router-link>
            <router-link to="/test-evaluation/testing-tools" class="submenu-link">
              <span class="submenu-icon">🛠️</span>
              <span class="submenu-text">Testing Tools</span>
            </router-link>
            <router-link to="/test-evaluation/testing-reports" class="submenu-link">
              <span class="submenu-icon">📊</span>
              <span class="submenu-text">Testing Reports</span>
            </router-link>
            <router-link to="/test-evaluation/test-cves" class="submenu-link">
              <span class="submenu-icon">🔓</span>
              <span class="submenu-text">Test CVEs</span>
            </router-link>
            <router-link to="/test-evaluation/mitre-attack" class="submenu-link">
              <span class="submenu-icon">⚔️</span>
              <span class="submenu-text">MITRE ATT&CK</span>
            </router-link>
          </div>
        </div>
        
        <!-- Documentation -->
        <div class="menu-section">
          <div class="menu-header" @click="toggleSection('documentation')">
            <span class="menu-icon">📚</span>
            <span v-if="!sidebarCollapsed" class="menu-text">Documentation</span>
            <span v-if="!sidebarCollapsed" class="menu-arrow" :class="{ expanded: expandedSections.documentation }">▼</span>
          </div>
          <div v-if="!sidebarCollapsed && expandedSections.documentation" class="submenu">
            <router-link to="/documentation/toe-description" class="submenu-link">
              <span class="submenu-icon">📋</span>
              <span class="submenu-text">TOE Description</span>
            </router-link>
            <router-link to="/documentation/assurance-activities" class="submenu-link">
              <span class="submenu-icon">✅</span>
              <span class="submenu-text">Assurance Activities Identification</span>
            </router-link>
            <router-link to="/documentation/assurance-equivalency" class="submenu-link">
              <span class="submenu-icon">⚖️</span>
              <span class="submenu-text">Assurance Equivalency Justification</span>
            </router-link>
            <router-link to="/documentation/test-bed-description" class="submenu-link">
              <span class="submenu-icon">🧪</span>
              <span class="submenu-text">Test Bed Description</span>
            </router-link>
            <router-link to="/documentation/tss-guidance" class="submenu-link">
              <span class="submenu-icon">📖</span>
              <span class="submenu-text">TSS and Guidance activities</span>
            </router-link>
            <router-link to="/documentation/security-requirements" class="submenu-link">
              <span class="submenu-icon">🔐</span>
              <span class="submenu-text">Security Assurance Requirements</span>
            </router-link>
            <router-link to="/documentation/preview-save" class="submenu-link">
              <span class="submenu-icon">💾</span>
              <span class="submenu-text">Preview and Save Documents</span>
            </router-link>
          </div>
        </div>
        
        <!-- Settings -->
        <div class="menu-section">
          <div class="menu-header" @click="toggleSection('settings')">
            <span class="menu-icon">⚙️</span>
            <span v-if="!sidebarCollapsed" class="menu-text">Settings</span>
            <span v-if="!sidebarCollapsed" class="menu-arrow" :class="{ expanded: expandedSections.settings }">▼</span>
          </div>
          <div v-if="!sidebarCollapsed && expandedSections.settings" class="submenu">
            <router-link to="/settings/database" class="submenu-link">
              <span class="submenu-icon">🗄️</span>
              <span class="submenu-text">Database Settings</span>
            </router-link>
            <router-link to="/settings/api" class="submenu-link">
              <span class="submenu-icon">🔗</span>
              <span class="submenu-text">API</span>
            </router-link>
            <router-link to="/settings/system" class="submenu-link">
              <span class="submenu-icon">💻</span>
              <span class="submenu-text">System</span>
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    
    <!-- Main Content Area -->
    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <!-- Toolbar -->
      <header class="toolbar">
        <div class="toolbar-left">
          <h1>AI Testing Standard Platform</h1>
        </div>
        <div class="toolbar-right">
          <span class="status-indicator" :class="{ online: connectionStatus }">
            {{ connectionStatus ? 'Online' : 'Offline' }}
          </span>
        </div>
      </header>
      
      <!-- Page Content -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiService from './services/api'

const sidebarCollapsed = ref(false)
const connectionStatus = ref(false)
const expandedSections = ref({
  testEvaluation: true,
  documentation: false,
  settings: false
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const toggleSection = (section: string) => {
  if (sidebarCollapsed.value) {
    sidebarCollapsed.value = false
  }
  expandedSections.value[section as keyof typeof expandedSections.value] = !expandedSections.value[section as keyof typeof expandedSections.value]
}

const checkConnection = async () => {
  try {
    await ApiService.getHelloWorld()
    connectionStatus.value = true
  } catch (error) {
    connectionStatus.value = false
  }
}

onMounted(() => {
  checkConnection()
  // Check connection every 30 seconds
  setInterval(checkConnection, 30000)
})
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background-color: #f8f9fa;
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background-color: #2c3e50;
  color: white;
  transition: width 0.3s ease;
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #34495e;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  box-sizing: border-box;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #ecf0f1;
}

.sidebar-toggle {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 5px;
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

.sidebar-toggle:hover {
  background-color: #34495e;
}

.sidebar-content {
  padding: 10px 0;
  overflow-y: auto;
  overflow-x: auto;
  height: calc(100vh - 80px);
}

.menu-item {
  margin-bottom: 5px;
}

.menu-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #ecf0f1;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.menu-link:hover {
  background-color: #34495e;
}

.menu-link.active {
  background-color: #3498db;
}

.menu-section {
  margin-bottom: 5px;
}

.menu-header {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.menu-header:hover {
  background-color: #34495e;
}

.menu-icon {
  width: 20px;
  text-align: center;
  margin-right: 15px;
  font-size: 16px;
}

.menu-text {
  flex: 1;
  white-space: nowrap;
}

.menu-arrow {
  transition: transform 0.3s ease;
  font-size: 12px;
}

.menu-arrow.expanded {
  transform: rotate(180deg);
}

.submenu {
  background-color: #34495e;
}

.submenu-link {
  display: flex;
  align-items: center;
  padding: 10px 20px 10px 50px;
  color: #bdc3c7;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 14px;
}

.submenu-link:hover {
  background-color: #3498db;
  color: white;
}

.submenu-link.router-link-active {
  background-color: #3498db;
  color: white;
}

.submenu-icon {
  width: 16px;
  text-align: center;
  margin-right: 12px;
  font-size: 14px;
}

.submenu-text {
  white-space: nowrap;
  min-width: fit-content;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
}

.toolbar {
  background-color: white;
  border-bottom: 1px solid #ecf0f1;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  height: 60px;
  box-sizing: border-box;
}

.toolbar h1 {
  margin: 0;
  font-size: 1.4em;
  color: #2c3e50;
}

.status-indicator {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background-color: #e74c3c;
  color: white;
  transition: background-color 0.3s ease;
}

.status-indicator.online {
  background-color: #27ae60;
}

.page-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .main-content {
    width: 100%;
  }
  
  .toolbar {
    padding: 15px 20px;
  }
  
  .toolbar h1 {
    font-size: 1.2em;
  }
  
  .page-content {
    padding: 20px;
  }
}
</style>