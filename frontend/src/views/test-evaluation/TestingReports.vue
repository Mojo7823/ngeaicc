<template>
  <div class="testing-reports-page">
    <div class="page-header">
      <h1>Testing Reports</h1>
      <p class="page-subtitle">View and manage testing reports and results</p>
      <div class="header-actions">
        <button @click="generateReport" class="generate-button">
          <span class="button-icon">📄</span>
          Generate Report
        </button>
      </div>
    </div>

    <div class="reports-container">
      <!-- Reports Filter -->
      <div class="filters-section">
        <div class="filter-group">
          <label for="filter-status" class="filter-label">Status</label>
          <select id="filter-status" v-model="filterStatus" class="filter-input">
            <option value="">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-type" class="filter-label">Report Type</label>
          <select id="filter-type" v-model="filterType" class="filter-input">
            <option value="">All Types</option>
            <option value="security">Security Assessment</option>
            <option value="penetration">Penetration Test</option>
            <option value="vulnerability">Vulnerability Scan</option>
            <option value="compliance">Compliance Check</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-date" class="filter-label">Date Range</label>
          <select id="filter-date" v-model="filterDate" class="filter-input">
            <option value="">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
          </select>
        </div>
      </div>

      <!-- Reports List -->
      <div class="reports-list">
        <div v-if="filteredReports.length === 0" class="empty-state">
          <div class="empty-icon">📊</div>
          <h3>No Reports Found</h3>
          <p>No testing reports match your current filters.</p>
        </div>
        
        <div v-else class="reports-grid">
          <div
            v-for="report in filteredReports"
            :key="report.id"
            class="report-card"
            :class="{ 'completed': report.status === 'completed' }"
          >
            <div class="card-header">
              <div class="report-info">
                <h3>{{ report.title }}</h3>
                <div class="report-meta">
                  <span class="report-type">{{ report.type }}</span>
                  <span class="report-date">{{ formatDate(report.created_at) }}</span>
                </div>
              </div>
              <div class="report-status" :class="report.status">
                {{ report.status.charAt(0).toUpperCase() + report.status.slice(1) }}
              </div>
            </div>
            
            <div class="card-content">
              <p class="report-description">{{ report.description }}</p>
              
              <div class="report-stats">
                <div class="stat-item">
                  <span class="stat-label">Tests Run:</span>
                  <span class="stat-value">{{ report.tests_run }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Issues Found:</span>
                  <span class="stat-value issues" :class="getIssuesClass(report.issues_found)">
                    {{ report.issues_found }}
                  </span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Duration:</span>
                  <span class="stat-value">{{ report.duration }}</span>
                </div>
              </div>
              
              <div class="card-actions">
                <button @click="viewReport(report)" class="view-button">
                  👁️ View Report
                </button>
                <button @click="downloadReport(report)" class="download-button">
                  💾 Download
                </button>
                <button @click="shareReport(report)" class="share-button">
                  🔗 Share
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Report Generation Modal -->
    <div v-if="showGenerateModal" class="modal-overlay" @click="closeGenerateModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Generate New Report</h2>
          <button @click="closeGenerateModal" class="modal-close">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label for="report-title" class="form-label">Report Title</label>
            <input
              id="report-title"
              v-model="newReport.title"
              type="text"
              class="form-input"
              placeholder="Enter report title"
            />
          </div>
          
          <div class="form-group">
            <label for="report-type-select" class="form-label">Report Type</label>
            <select id="report-type-select" v-model="newReport.type" class="form-input">
              <option value="security">Security Assessment</option>
              <option value="penetration">Penetration Test</option>
              <option value="vulnerability">Vulnerability Scan</option>
              <option value="compliance">Compliance Check</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="report-description" class="form-label">Description</label>
            <textarea
              id="report-description"
              v-model="newReport.description"
              class="form-input form-textarea"
              placeholder="Enter report description"
            ></textarea>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="closeGenerateModal" class="cancel-button">Cancel</button>
          <button @click="createReport" class="create-button">Generate Report</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'

interface Report {
  id: string
  title: string
  type: string
  description: string
  status: 'completed' | 'pending' | 'failed'
  created_at: string
  tests_run: number
  issues_found: number
  duration: string
}

const filterStatus = ref('')
const filterType = ref('')
const filterDate = ref('')
const showGenerateModal = ref(false)

const newReport = reactive({
  title: '',
  type: 'security',
  description: ''
})

// Mock data for reports
const reports = ref<Report[]>([
  {
    id: '1',
    title: 'Network Security Assessment',
    type: 'security',
    description: 'Comprehensive security assessment of network infrastructure',
    status: 'completed',
    created_at: '2024-01-15T10:30:00Z',
    tests_run: 25,
    issues_found: 3,
    duration: '2h 45m'
  },
  {
    id: '2',
    title: 'Web Application Penetration Test',
    type: 'penetration',
    description: 'Penetration testing of main web application',
    status: 'completed',
    created_at: '2024-01-14T14:20:00Z',
    tests_run: 18,
    issues_found: 7,
    duration: '4h 15m'
  },
  {
    id: '3',
    title: 'Quarterly Vulnerability Scan',
    type: 'vulnerability',
    description: 'Automated vulnerability scanning across all systems',
    status: 'pending',
    created_at: '2024-01-13T09:00:00Z',
    tests_run: 42,
    issues_found: 0,
    duration: 'In Progress'
  },
  {
    id: '4',
    title: 'PCI DSS Compliance Check',
    type: 'compliance',
    description: 'Payment Card Industry compliance verification',
    status: 'failed',
    created_at: '2024-01-12T16:45:00Z',
    tests_run: 15,
    issues_found: 12,
    duration: '1h 30m'
  }
])

const filteredReports = computed(() => {
  let filtered = reports.value

  if (filterStatus.value) {
    filtered = filtered.filter(report => report.status === filterStatus.value)
  }

  if (filterType.value) {
    filtered = filtered.filter(report => report.type === filterType.value)
  }

  if (filterDate.value) {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.created_at)
      
      switch (filterDate.value) {
        case 'today':
          return reportDate >= today
        case 'week':
          const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
          return reportDate >= weekAgo
        case 'month':
          const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
          return reportDate >= monthAgo
        case 'quarter':
          const quarterAgo = new Date(today.getTime() - 90 * 24 * 60 * 60 * 1000)
          return reportDate >= quarterAgo
        default:
          return true
      }
    })
  }

  return filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

const generateReport = () => {
  showGenerateModal.value = true
}

const closeGenerateModal = () => {
  showGenerateModal.value = false
  newReport.title = ''
  newReport.type = 'security'
  newReport.description = ''
}

const createReport = () => {
  const report: Report = {
    id: Date.now().toString(),
    title: newReport.title,
    type: newReport.type,
    description: newReport.description,
    status: 'pending',
    created_at: new Date().toISOString(),
    tests_run: 0,
    issues_found: 0,
    duration: 'Initializing'
  }
  
  reports.value.unshift(report)
  closeGenerateModal()
}

const viewReport = (report: Report) => {
  // Implementation for viewing report details
  alert(`Viewing report: ${report.title}`)
}

const downloadReport = (report: Report) => {
  // Implementation for downloading report
  alert(`Downloading report: ${report.title}`)
}

const shareReport = (report: Report) => {
  // Implementation for sharing report
  alert(`Sharing report: ${report.title}`)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getIssuesClass = (issues: number) => {
  if (issues === 0) return 'success'
  if (issues <= 3) return 'warning'
  return 'danger'
}
</script>

<style scoped>
.testing-reports-page {
  max-width: 1400px;
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

.generate-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.generate-button:hover {
  background-color: #2980b9;
}

.reports-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.filter-input {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
}

.filter-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.reports-list {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #374151;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.report-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: box-shadow 0.15s ease-in-out;
}

.report-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.report-card.completed {
  border-left: 4px solid #10b981;
}

.card-header {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.report-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.report-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.report-type {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.report-status {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.report-status.completed {
  background-color: #dcfce7;
  color: #166534;
}

.report-status.pending {
  background-color: #fef3c7;
  color: #92400e;
}

.report-status.failed {
  background-color: #fee2e2;
  color: #991b1b;
}

.card-content {
  padding: 1.5rem;
}

.report-description {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  line-height: 1.5;
}

.report-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  display: block;
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
}

.stat-value.issues.success {
  color: #059669;
}

.stat-value.issues.warning {
  color: #d97706;
}

.stat-value.issues.danger {
  color: #dc2626;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.view-button,
.download-button,
.share-button {
  flex: 1;
  min-width: 100px;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.view-button:hover {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.download-button:hover {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.share-button:hover {
  background-color: #8b5cf6;
  color: white;
  border-color: #8b5cf6;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
}

.modal-close:hover {
  color: #374151;
}

.modal-body {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
  line-height: 1.5;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.modal-actions {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button {
  background-color: #6b7280;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #4b5563;
}

.create-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.create-button:hover {
  background-color: #2980b9;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filters-section {
    flex-direction: column;
  }

  .reports-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .view-button,
  .download-button,
  .share-button {
    flex: none;
  }
}
</style>