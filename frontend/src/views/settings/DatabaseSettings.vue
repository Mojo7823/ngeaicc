<template>
  <div class="database-settings">
    <div class="page-header">
      <h1>Database Settings</h1>
      <p class="page-subtitle">Manage and monitor your database</p>
      <div class="header-actions">
        <button @click="refreshData" class="refresh-button" :disabled="loading">
          🔄 Refresh
        </button>
      </div>
    </div>

    <!-- Database Health Status -->
    <div class="section-card">
      <h2>Database Health</h2>
      <div v-if="loading" class="loading-state">Loading...</div>
      <div v-else-if="databaseHealth" class="health-grid">
        <div class="health-item">
          <label>Status:</label>
          <span :class="'health-status health-' + databaseHealth.status">
            {{ databaseHealth.status.toUpperCase() }}
          </span>
        </div>
        <div class="health-item">
          <label>Connection:</label>
          <span :class="'health-status health-' + databaseHealth.connection">
            {{ databaseHealth.connection.toUpperCase() }}
          </span>
        </div>
        <div class="health-item">
          <label>pgVector:</label>
          <span :class="'health-status health-' + (databaseHealth.pgvector_enabled ? 'enabled' : 'disabled')">
            {{ databaseHealth.pgvector_enabled ? 'ENABLED' : 'DISABLED' }}
          </span>
        </div>
        <div class="health-item full-width">
          <label>Database Version:</label>
          <span>{{ databaseHealth.database_version || 'Unknown' }}</span>
        </div>
        <div class="health-item full-width">
          <label>Last Check:</label>
          <span>{{ formatDate(databaseHealth.last_check) }}</span>
        </div>
      </div>
    </div>

    <!-- Database Tables -->
    <div class="section-card">
      <h2>Database Tables</h2>
      <div v-if="loading" class="loading-state">Loading...</div>
      <div v-else-if="tables.length > 0" class="tables-grid">
        <div v-for="table in tables" :key="table.name" class="table-card">
          <div class="table-header">
            <h3>{{ table.name }}</h3>
            <span class="table-size">{{ table.size }}</span>
          </div>
          <div class="table-stats">
            <div class="stat-item">
              <label>Scans:</label>
              <span>{{ table.statistics.scans }}</span>
            </div>
            <div class="stat-item">
              <label>Inserts:</label>
              <span>{{ table.statistics.inserts }}</span>
            </div>
            <div class="stat-item">
              <label>Updates:</label>
              <span>{{ table.statistics.updates }}</span>
            </div>
            <div class="stat-item">
              <label>Deletes:</label>
              <span>{{ table.statistics.deletes }}</span>
            </div>
          </div>
          <div class="table-actions">
            <button @click="viewTableData(table.name)" class="view-button">
              👁️ View Data
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Data Viewer -->
    <div v-if="selectedTable" class="section-card">
      <div class="table-viewer-header">
        <h2>{{ selectedTable }} Data</h2>
        <div class="table-viewer-actions">
          <button @click="refreshTableData" class="refresh-button">
            🔄 Refresh
          </button>
          <button @click="closeTableViewer" class="close-button">
            ✕ Close
          </button>
        </div>
      </div>
      
      <div v-if="loadingTableData" class="loading-state">Loading table data...</div>
      <div v-else-if="tableData.length > 0" class="table-data">
        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th v-for="column in tableColumns" :key="column">{{ column }}</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableData" :key="row.id">
                <td v-for="column in tableColumns" :key="column" class="data-cell">
                  <div class="cell-content">
                    {{ formatCellValue(row[column]) }}
                  </div>
                </td>
                <td class="actions-cell">
                  <button 
                    @click="deleteTableRow(row.id)" 
                    class="delete-button"
                    :disabled="deletingItems.has(row.id)"
                  >
                    {{ deletingItems.has(row.id) ? '⏳' : '🗑️' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="empty-table">
        <p>No data found in this table.</p>
      </div>
    </div>

    <!-- SQL Query Executor -->
    <div class="section-card">
      <h2>SQL Query Executor</h2>
      <p class="sql-warning">⚠️ Only SELECT queries are allowed for security reasons.</p>
      
      <div class="sql-input">
        <textarea
          v-model="sqlQuery"
          placeholder="Enter your SQL query here... (SELECT only)"
          class="sql-textarea"
          rows="4"
        ></textarea>
        <button 
          @click="executeSqlQuery" 
          class="execute-button"
          :disabled="executingQuery || !sqlQuery.trim()"
        >
          {{ executingQuery ? 'Executing...' : '▶️ Execute Query' }}
        </button>
      </div>

      <div v-if="sqlResult" class="sql-result">
        <h3>Query Result ({{ sqlResult.count }} rows)</h3>
        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th v-for="column in sqlResult.columns" :key="column">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in sqlResult.rows" :key="index">
                <td v-for="column in sqlResult.columns" :key="column" class="data-cell">
                  <div class="cell-content">
                    {{ formatCellValue(row[column]) }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="sqlError" class="sql-error">
        <h3>Query Error</h3>
        <p>{{ sqlError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminService from '../../services/admin'

interface DatabaseHealth {
  status: string
  connection: string
  pgvector_enabled: boolean
  database_version: string
  last_check: string
}

interface DatabaseTable {
  schema: string
  name: string
  size: string
  statistics: {
    scans: number
    inserts: number
    updates: number
    deletes: number
  }
}

const loading = ref(true)
const databaseHealth = ref<DatabaseHealth | null>(null)
const tables = ref<DatabaseTable[]>([])

// Table viewer
const selectedTable = ref<string | null>(null)
const tableData = ref<any[]>([])
const loadingTableData = ref(false)
const deletingItems = ref(new Set<string>())

// SQL executor
const sqlQuery = ref('')
const sqlResult = ref<any>(null)
const sqlError = ref<string | null>(null)
const executingQuery = ref(false)

const tableColumns = computed(() => {
  if (tableData.value.length === 0) return []
  return Object.keys(tableData.value[0]).filter(key => key !== 'id')
})

onMounted(() => {
  loadDatabaseInfo()
})

const loadDatabaseInfo = async () => {
  loading.value = true
  try {
    const [healthData, tablesData] = await Promise.all([
      AdminService.getDatabaseHealth(),
      AdminService.getDatabaseTables()
    ])
    
    databaseHealth.value = healthData
    tables.value = tablesData
  } catch (error) {
    console.error('Error loading database info:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadDatabaseInfo()
}

const viewTableData = async (tableName: string) => {
  selectedTable.value = tableName
  loadingTableData.value = true
  
  try {
    const data = await AdminService.getTableData(tableName)
    tableData.value = data
  } catch (error) {
    console.error(`Error loading data for table ${tableName}:`, error)
    tableData.value = []
  } finally {
    loadingTableData.value = false
  }
}

const refreshTableData = () => {
  if (selectedTable.value) {
    viewTableData(selectedTable.value)
  }
}

const closeTableViewer = () => {
  selectedTable.value = null
  tableData.value = []
}

const deleteTableRow = async (itemId: string) => {
  if (!selectedTable.value) return
  
  if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
    return
  }
  
  deletingItems.value.add(itemId)
  
  try {
    await AdminService.deleteTableItem(selectedTable.value, itemId)
    
    // Remove from local data
    tableData.value = tableData.value.filter(row => row.id !== itemId)
    
    // Refresh database stats
    loadDatabaseInfo()
  } catch (error) {
    console.error('Error deleting item:', error)
    alert('Error deleting item. Please try again.')
  } finally {
    deletingItems.value.delete(itemId)
  }
}

const executeSqlQuery = async () => {
  if (!sqlQuery.value.trim()) return
  
  executingQuery.value = true
  sqlResult.value = null
  sqlError.value = null
  
  try {
    const result = await AdminService.executeSqlQuery(sqlQuery.value)
    sqlResult.value = result
  } catch (error: any) {
    console.error('SQL query error:', error)
    sqlError.value = error.response?.data?.detail || error.message || 'Unknown error occurred'
  } finally {
    executingQuery.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const formatCellValue = (value: any) => {
  if (value === null || value === undefined) return 'NULL'
  if (typeof value === 'string' && value.length > 100) {
    return value.substring(0, 100) + '...'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}
</script>

<style scoped>
.database-settings {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.refresh-button, .execute-button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.15s ease;
}

.refresh-button:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.execute-button {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.execute-button:hover:not(:disabled) {
  background: #2980b9;
  border-color: #2980b9;
}

.section-card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.health-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.health-item {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.375rem;
  border: 1px solid #e5e7eb;
}

.health-item.full-width {
  grid-column: 1 / -1;
}

.health-item label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
}

.health-status {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.health-status.health-healthy,
.health-status.health-active,
.health-status.health-enabled {
  background: #d1fae5;
  color: #065f46;
}

.health-status.health-error,
.health-status.health-failed,
.health-status.health-disabled {
  background: #fee2e2;
  color: #991b1b;
}

.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.table-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  padding: 1rem;
  background: #f9fafb;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.table-size {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.table-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.stat-item label {
  color: #6b7280;
}

.table-actions {
  text-align: center;
}

.view-button {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.15s ease;
}

.view-button:hover {
  background: #2980b9;
}

.table-viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table-viewer-actions {
  display: flex;
  gap: 0.5rem;
}

.close-button {
  padding: 0.5rem 1rem;
  background: #e5e7eb;
  color: #374151;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.15s ease;
}

.close-button:hover {
  background: #d1d5db;
}

.table-scroll {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.data-table th {
  background: #f9fafb;
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  font-weight: 600;
  color: #374151;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.data-cell {
  max-width: 200px;
}

.cell-content {
  word-break: break-word;
}

.actions-cell {
  text-align: center;
  width: 80px;
}

.delete-button {
  padding: 0.25rem 0.5rem;
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.15s ease;
}

.delete-button:hover:not(:disabled) {
  background: #fecaca;
}

.delete-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty-table {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.sql-warning {
  color: #d97706;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: #fef3c7;
  border-radius: 0.375rem;
  border: 1px solid #fcd34d;
}

.sql-input {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.sql-textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  resize: vertical;
}

.sql-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.sql-result, .sql-error {
  margin-top: 1rem;
}

.sql-result h3, .sql-error h3 {
  margin-bottom: 1rem;
  font-size: 1rem;
  font-weight: 600;
}

.sql-error {
  color: #991b1b;
  background: #fee2e2;
  padding: 1rem;
  border-radius: 0.375rem;
  border: 1px solid #fecaca;
}

/* Responsive design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    margin-top: 1rem;
  }

  .health-grid {
    grid-template-columns: 1fr;
  }

  .tables-grid {
    grid-template-columns: 1fr;
  }

  .sql-input {
    flex-direction: column;
  }

  .table-viewer-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .table-viewer-actions {
    margin-top: 1rem;
  }
}
</style>