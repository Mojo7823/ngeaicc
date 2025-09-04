<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h2>🔧 Admin Dashboard</h2>
      <p class="admin-subtitle">System Overview & Database Monitoring</p>
    </div>

    <!-- Navigation -->
    <div class="admin-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-btn', { active: activeTab === tab.id }]"
      >
        {{ tab.icon }} {{ tab.name }}
      </button>
    </div>

    <!-- Content Area -->
    <div class="admin-content">
      <!-- System Overview Tab -->
      <div v-if="activeTab === 'overview'" class="tab-content">
        <h3>📊 System Overview</h3>
        <div v-if="stats" class="stats-grid">
          <div class="stat-card">
            <h4>💾 Database</h4>
            <p><strong>Size:</strong> {{ stats.system.database_size }}</p>
            <p><strong>Tables:</strong> {{ stats.database.total_tables }}</p>
            <p><strong>Test Cases:</strong> {{ stats.database.test_cases_count }}</p>
            <p><strong>Devices:</strong> {{ stats.database.devices_count }}</p>
          </div>
          <div class="stat-card">
            <h4>🚀 API Status</h4>
            <p><strong>Status:</strong> {{ stats.api.status }}</p>
            <p><strong>Endpoints:</strong> {{ stats.api.endpoints_available }}</p>
            <p><strong>System:</strong> {{ stats.system.status }}</p>
          </div>
          <div class="stat-card">
            <h4>📈 Recent Activity</h4>
            <p><strong>Test Cases (24h):</strong> {{ stats.database.recent_activity.test_cases_last_24h }}</p>
            <p><strong>Last Update:</strong> {{ formatTime(stats.system.timestamp) }}</p>
          </div>
        </div>
        <div v-else class="loading">Loading stats...</div>
      </div>

      <!-- Database Tab -->
      <div v-if="activeTab === 'database'" class="tab-content">
        <h3>🗄️ Database Management</h3>
        
        <!-- Database Health -->
        <div v-if="dbHealth" class="health-section">
          <h4>Database Health</h4>
          <div class="health-status" :class="dbHealth.status">
            <span class="status-icon">{{ dbHealth.status === 'healthy' ? '✅' : '❌' }}</span>
            <span>{{ dbHealth.status.toUpperCase() }}</span>
          </div>
          <p><strong>Connection:</strong> {{ dbHealth.connection }}</p>
          <p><strong>pgvector:</strong> {{ dbHealth.pgvector_enabled ? 'Enabled' : 'Disabled' }}</p>
          <p><strong>Version:</strong> {{ dbHealth.database_version.split(' ').slice(0, 2).join(' ') }}</p>
        </div>

        <!-- Database Tables -->
        <div v-if="dbTables" class="tables-section">
          <h4>Tables Information</h4>
          <div class="table-grid">
            <div v-for="table in dbTables" :key="table.name" class="table-card">
              <h5>📋 {{ table.name }}</h5>
              <p><strong>Size:</strong> {{ table.size }}</p>
              <p><strong>Inserts:</strong> {{ table.statistics.inserts }}</p>
              <p><strong>Updates:</strong> {{ table.statistics.updates }}</p>
              <p><strong>Deletes:</strong> {{ table.statistics.deletes }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- API Tab -->
      <div v-if="activeTab === 'api'" class="tab-content">
        <h3>🔗 API Endpoints</h3>
        <div v-if="apiEndpoints" class="endpoints-section">
          <div v-for="category in endpointCategories" :key="category" class="endpoint-category">
            <h4>{{ getCategoryIcon(category) }} {{ category.toUpperCase() }}</h4>
            <div class="endpoints-list">
              <div 
                v-for="endpoint in getEndpointsByCategory(category)" 
                :key="endpoint.path + endpoint.method"
                class="endpoint-item"
              >
                <span class="method" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</span>
                <span class="path">{{ endpoint.path }}</span>
                <span class="description">{{ endpoint.description }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Info Tab -->
      <div v-if="activeTab === 'system'" class="tab-content">
        <h3>⚙️ System Information</h3>
        <div v-if="systemInfo" class="system-info">
          <div class="info-section">
            <h4>📱 Application</h4>
            <p><strong>Name:</strong> {{ systemInfo.application.name }}</p>
            <p><strong>Version:</strong> {{ systemInfo.application.version }}</p>
            <p><strong>Framework:</strong> {{ systemInfo.application.framework }}</p>
          </div>
          <div class="info-section">
            <h4>🎨 Frontend</h4>
            <p><strong>Framework:</strong> {{ systemInfo.frontend.framework }}</p>
            <p><strong>Build Tool:</strong> {{ systemInfo.frontend.build_tool }}</p>
            <p><strong>Language:</strong> {{ systemInfo.frontend.language }}</p>
          </div>
          <div class="info-section">
            <h4>🐳 Deployment</h4>
            <p><strong>Container:</strong> {{ systemInfo.deployment.containerization }}</p>
            <p><strong>Orchestration:</strong> {{ systemInfo.deployment.orchestration }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Refresh Button -->
    <div class="admin-actions">
      <button @click="refreshData" class="refresh-btn" :disabled="loading">
        {{ loading ? '🔄 Refreshing...' : '🔄 Refresh Data' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminService from '../services/admin'

const activeTab = ref('overview')
const loading = ref(false)
const stats = ref(null)
const dbHealth = ref(null)
const dbTables = ref(null)
const apiEndpoints = ref(null)
const systemInfo = ref(null)

const tabs = [
  { id: 'overview', name: 'Overview', icon: '📊' },
  { id: 'database', name: 'Database', icon: '🗄️' },
  { id: 'api', name: 'API', icon: '🔗' },
  { id: 'system', name: 'System', icon: '⚙️' }
]

const endpointCategories = computed(() => {
  if (!apiEndpoints.value) return []
  return [...new Set(apiEndpoints.value.map(ep => ep.category))]
})

const getEndpointsByCategory = (category: string) => {
  if (!apiEndpoints.value) return []
  return apiEndpoints.value.filter(ep => ep.category === category)
}

const getCategoryIcon = (category: string) => {
  const icons = {
    'system': '⚙️',
    'demo': '🎯',
    'data': '📊',
    'admin': '🔧'
  }
  return icons[category] || '📋'
}

const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleString()
}

const loadData = async () => {
  loading.value = true
  try {
    const [statsData, healthData, tablesData, endpointsData, infoData] = await Promise.all([
      AdminService.getStats(),
      AdminService.getDatabaseHealth(),
      AdminService.getDatabaseTables(),
      AdminService.getApiEndpoints(),
      AdminService.getSystemInfo()
    ])
    
    stats.value = statsData
    dbHealth.value = healthData
    dbTables.value = tablesData
    apiEndpoints.value = endpointsData
    systemInfo.value = infoData
  } catch (error) {
    console.error('Failed to load admin data:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', roboto, oxygen, ubuntu, cantarell, 'Helvetica Neue', sans-serif;
}

.admin-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.admin-header h2 {
  margin: 0 0 10px 0;
  font-size: 2.5em;
}

.admin-subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1em;
}

.admin-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.nav-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-btn:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.nav-btn.active {
  background: #007bff;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.admin-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.tab-content h3 {
  margin: 0 0 25px 0;
  color: #2c3e50;
  font-size: 1.8em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #007bff;
}

.stat-card h4 {
  margin: 0 0 15px 0;
  color: #495057;
}

.stat-card p {
  margin: 8px 0;
  color: #6c757d;
}

.health-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.health-status {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
  font-weight: bold;
  font-size: 1.1em;
}

.health-status.healthy {
  color: #28a745;
}

.health-status.error {
  color: #dc3545;
}

.tables-section h4 {
  margin: 20px 0 15px 0;
  color: #495057;
}

.table-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.table-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.table-card h5 {
  margin: 0 0 10px 0;
  color: #495057;
}

.endpoint-category {
  margin-bottom: 30px;
}

.endpoint-category h4 {
  margin: 0 0 15px 0;
  color: #495057;
  padding-bottom: 8px;
  border-bottom: 2px solid #e9ecef;
}

.endpoints-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.endpoint-item {
  display: grid;
  grid-template-columns: 80px 1fr 2fr;
  gap: 15px;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.method {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  text-align: center;
  font-size: 0.8em;
}

.method.get { background: #d4edda; color: #155724; }
.method.post { background: #d1ecf1; color: #0c5460; }
.method.put { background: #fff3cd; color: #856404; }
.method.delete { background: #f8d7da; color: #721c24; }

.path {
  font-family: 'Courier New', monospace;
  color: #495057;
  font-weight: 500;
}

.description {
  color: #6c757d;
}

.system-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.info-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.info-section h4 {
  margin: 0 0 15px 0;
  color: #495057;
}

.info-section p {
  margin: 8px 0;
  color: #6c757d;
}

.admin-actions {
  text-align: center;
}

.refresh-btn {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  background: #28a745;
  color: white;
  cursor: pointer;
  font-weight: 500;
  font-size: 1em;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: #218838;
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #6c757d;
  font-style: italic;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 10px;
  }
  
  .admin-nav {
    justify-content: center;
  }
  
  .nav-btn {
    flex: 1;
    min-width: 120px;
  }
  
  .endpoint-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .stats-grid,
  .table-grid,
  .system-info {
    grid-template-columns: 1fr;
  }
}
</style>