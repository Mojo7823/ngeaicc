<template>
  <div class="test-cves-page">
    <div class="page-header">
      <h1>Test CVEs</h1>
      <p class="page-subtitle">Common Vulnerabilities and Exposures database for security testing</p>
      <div class="header-actions">
        <button @click="refreshCVEs" class="refresh-button">
          <span class="button-icon">🔄</span>
          Refresh CVEs
        </button>
      </div>
    </div>

    <div class="cves-container">
      <!-- Search and Filter Section -->
      <div class="search-filter-section">
        <div class="search-group">
          <label for="cve-search" class="search-label">Search CVEs</label>
          <input
            id="cve-search"
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Search by CVE ID, description, or vendor..."
          />
        </div>
        
        <div class="filter-group">
          <label for="severity-filter" class="filter-label">Severity</label>
          <select id="severity-filter" v-model="severityFilter" class="filter-input">
            <option value="">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="year-filter" class="filter-label">Year</label>
          <select id="year-filter" v-model="yearFilter" class="filter-input">
            <option value="">All Years</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
            <option value="2020">2020</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="category-filter" class="filter-label">Category</label>
          <select id="category-filter" v-model="categoryFilter" class="filter-input">
            <option value="">All Categories</option>
            <option value="web">Web Application</option>
            <option value="network">Network</option>
            <option value="system">System</option>
            <option value="mobile">Mobile</option>
            <option value="iot">IoT</option>
          </select>
        </div>
      </div>

      <!-- CVE Statistics -->
      <div class="stats-section">
        <div class="stat-card critical">
          <div class="stat-icon">🔴</div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.critical }}</div>
            <div class="stat-label">Critical</div>
          </div>
        </div>
        
        <div class="stat-card high">
          <div class="stat-icon">🟠</div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.high }}</div>
            <div class="stat-label">High</div>
          </div>
        </div>
        
        <div class="stat-card medium">
          <div class="stat-icon">🟡</div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.medium }}</div>
            <div class="stat-label">Medium</div>
          </div>
        </div>
        
        <div class="stat-card low">
          <div class="stat-icon">🟢</div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.low }}</div>
            <div class="stat-label">Low</div>
          </div>
        </div>
      </div>

      <!-- CVEs List -->
      <div class="cves-list">
        <div v-if="filteredCVEs.length === 0" class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>No CVEs Found</h3>
          <p>No CVEs match your current search and filter criteria.</p>
        </div>
        
        <div v-else class="cves-grid">
          <div
            v-for="cve in paginatedCVEs"
            :key="cve.id"
            class="cve-card"
            :class="cve.severity"
          >
            <div class="card-header">
              <div class="cve-info">
                <h3>{{ cve.id }}</h3>
                <div class="cve-meta">
                  <span class="cve-severity" :class="cve.severity">
                    {{ cve.severity.toUpperCase() }}
                  </span>
                  <span class="cve-score">CVSS: {{ cve.cvss_score }}</span>
                  <span class="cve-date">{{ formatDate(cve.published_date) }}</span>
                </div>
              </div>
              <div class="card-actions">
                <button @click="viewCVE(cve)" class="view-button">👁️</button>
                <button @click="createTestFromCVE(cve)" class="test-button">🧪</button>
                <button @click="favoriteCVE(cve)" class="favorite-button" :class="{ active: cve.is_favorite }">
                  {{ cve.is_favorite ? '❤️' : '🤍' }}
                </button>
              </div>
            </div>
            
            <div class="card-content">
              <p class="cve-description">{{ cve.description }}</p>
              
              <div class="cve-details">
                <div class="detail-item">
                  <span class="detail-label">Vendor:</span>
                  <span class="detail-value">{{ cve.vendor }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Product:</span>
                  <span class="detail-value">{{ cve.product }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Category:</span>
                  <span class="detail-value">{{ cve.category }}</span>
                </div>
              </div>
              
              <div v-if="cve.cwe_ids.length > 0" class="cwe-tags">
                <span class="cwe-label">CWE:</span>
                <div class="cwe-list">
                  <span
                    v-for="cwe in cve.cwe_ids"
                    :key="cwe"
                    class="cwe-tag"
                  >
                    {{ cwe }}
                  </span>
                </div>
              </div>
              
              <div v-if="cve.references.length > 0" class="references">
                <span class="references-label">References:</span>
                <div class="references-list">
                  <a
                    v-for="(ref, index) in cve.references.slice(0, 2)"
                    :key="index"
                    :href="ref.url"
                    target="_blank"
                    class="reference-link"
                  >
                    {{ ref.source }}
                  </a>
                  <span v-if="cve.references.length > 2" class="more-refs">
                    +{{ cve.references.length - 2 }} more
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="pagination-button"
          >
            ← Previous
          </button>
          
          <span class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          
          <button
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="pagination-button"
          >
            Next →
          </button>
        </div>
      </div>
    </div>

    <!-- CVE Detail Modal -->
    <div v-if="selectedCVE" class="modal-overlay" @click="closeModal">
      <div class="modal-content cve-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedCVE.id }}</h2>
          <button @click="closeModal" class="modal-close">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="cve-detail-header">
            <div class="severity-badge" :class="selectedCVE.severity">
              {{ selectedCVE.severity.toUpperCase() }}
            </div>
            <div class="cvss-score">
              CVSS Score: {{ selectedCVE.cvss_score }}
            </div>
            <div class="publish-date">
              Published: {{ formatDate(selectedCVE.published_date) }}
            </div>
          </div>
          
          <div class="cve-description-full">
            <h3>Description</h3>
            <p>{{ selectedCVE.description }}</p>
          </div>
          
          <div class="cve-technical-details">
            <h3>Technical Details</h3>
            <div class="detail-grid">
              <div class="detail-row">
                <span class="label">Vendor:</span>
                <span class="value">{{ selectedCVE.vendor }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Product:</span>
                <span class="value">{{ selectedCVE.product }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Version:</span>
                <span class="value">{{ selectedCVE.version || 'N/A' }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Category:</span>
                <span class="value">{{ selectedCVE.category }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="selectedCVE.cwe_ids.length > 0" class="cwe-section">
            <h3>Common Weakness Enumeration (CWE)</h3>
            <div class="cwe-tags-full">
              <span
                v-for="cwe in selectedCVE.cwe_ids"
                :key="cwe"
                class="cwe-tag-large"
              >
                {{ cwe }}
              </span>
            </div>
          </div>
          
          <div v-if="selectedCVE.references.length > 0" class="references-section">
            <h3>References</h3>
            <div class="references-full">
              <a
                v-for="(ref, index) in selectedCVE.references"
                :key="index"
                :href="ref.url"
                target="_blank"
                class="reference-link-full"
              >
                {{ ref.source }} - {{ ref.url }}
              </a>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="createTestFromCVE(selectedCVE)" class="create-test-button">
            Create Test Case
          </button>
          <button @click="closeModal" class="close-button">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface CVEReference {
  source: string
  url: string
}

interface CVE {
  id: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  cvss_score: number
  published_date: string
  vendor: string
  product: string
  version?: string
  category: string
  cwe_ids: string[]
  references: CVEReference[]
  is_favorite: boolean
}

const searchQuery = ref('')
const severityFilter = ref('')
const yearFilter = ref('')
const categoryFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 12
const selectedCVE = ref<CVE | null>(null)

// Mock CVE data
const cves = ref<CVE[]>([
  {
    id: 'CVE-2024-0001',
    description: 'A critical remote code execution vulnerability in Apache HTTP Server allows attackers to execute arbitrary code via crafted HTTP requests.',
    severity: 'critical',
    cvss_score: 9.8,
    published_date: '2024-01-15T00:00:00Z',
    vendor: 'Apache',
    product: 'HTTP Server',
    version: '2.4.x',
    category: 'web',
    cwe_ids: ['CWE-78', 'CWE-94'],
    references: [
      { source: 'Apache Security Advisory', url: 'https://httpd.apache.org/security/' },
      { source: 'NVD', url: 'https://nvd.nist.gov/vuln/detail/CVE-2024-0001' }
    ],
    is_favorite: false
  },
  {
    id: 'CVE-2024-0002',
    description: 'SQL injection vulnerability in MySQL Workbench allows local users to execute arbitrary SQL commands.',
    severity: 'high',
    cvss_score: 8.4,
    published_date: '2024-01-14T00:00:00Z',
    vendor: 'Oracle',
    product: 'MySQL Workbench',
    category: 'system',
    cwe_ids: ['CWE-89'],
    references: [
      { source: 'Oracle Security Alert', url: 'https://www.oracle.com/security-alerts/' }
    ],
    is_favorite: true
  },
  {
    id: 'CVE-2024-0003',
    description: 'Cross-site scripting (XSS) vulnerability in WordPress core allows remote attackers to inject arbitrary web script.',
    severity: 'medium',
    cvss_score: 6.1,
    published_date: '2024-01-13T00:00:00Z',
    vendor: 'WordPress',
    product: 'WordPress Core',
    category: 'web',
    cwe_ids: ['CWE-79'],
    references: [
      { source: 'WordPress Security Team', url: 'https://wordpress.org/news/category/security/' }
    ],
    is_favorite: false
  },
  {
    id: 'CVE-2024-0004',
    description: 'Information disclosure vulnerability in Android system service allows local users to access sensitive data.',
    severity: 'low',
    cvss_score: 3.3,
    published_date: '2024-01-12T00:00:00Z',
    vendor: 'Google',
    product: 'Android',
    category: 'mobile',
    cwe_ids: ['CWE-200'],
    references: [
      { source: 'Android Security Bulletin', url: 'https://source.android.com/security/bulletin' }
    ],
    is_favorite: false
  },
  {
    id: 'CVE-2023-0001',
    description: 'Buffer overflow in IoT device firmware allows remote code execution through malformed network packets.',
    severity: 'critical',
    cvss_score: 9.0,
    published_date: '2023-12-20T00:00:00Z',
    vendor: 'IoT Vendor',
    product: 'Smart Device Firmware',
    category: 'iot',
    cwe_ids: ['CWE-120', 'CWE-787'],
    references: [
      { source: 'CERT Advisory', url: 'https://www.cert.org/' }
    ],
    is_favorite: false
  }
])

const stats = computed(() => {
  const filtered = filteredCVEs.value
  return {
    critical: filtered.filter(cve => cve.severity === 'critical').length,
    high: filtered.filter(cve => cve.severity === 'high').length,
    medium: filtered.filter(cve => cve.severity === 'medium').length,
    low: filtered.filter(cve => cve.severity === 'low').length
  }
})

const filteredCVEs = computed(() => {
  let filtered = cves.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(cve =>
      cve.id.toLowerCase().includes(query) ||
      cve.description.toLowerCase().includes(query) ||
      cve.vendor.toLowerCase().includes(query) ||
      cve.product.toLowerCase().includes(query)
    )
  }

  if (severityFilter.value) {
    filtered = filtered.filter(cve => cve.severity === severityFilter.value)
  }

  if (yearFilter.value) {
    filtered = filtered.filter(cve => cve.published_date.startsWith(yearFilter.value))
  }

  if (categoryFilter.value) {
    filtered = filtered.filter(cve => cve.category === categoryFilter.value)
  }

  return filtered.sort((a, b) => new Date(b.published_date).getTime() - new Date(a.published_date).getTime())
})

const totalPages = computed(() => Math.ceil(filteredCVEs.value.length / itemsPerPage))

const paginatedCVEs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredCVEs.value.slice(start, end)
})

const refreshCVEs = () => {
  // Simulate refreshing CVE data
  alert('CVE database refreshed!')
}

const viewCVE = (cve: CVE) => {
  selectedCVE.value = cve
}

const closeModal = () => {
  selectedCVE.value = null
}

const createTestFromCVE = (cve: CVE) => {
  // Navigate to test cases with pre-filled CVE data
  alert(`Creating test case for ${cve.id}`)
}

const favoriteCVE = (cve: CVE) => {
  cve.is_favorite = !cve.is_favorite
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}
</script>

<style scoped>
.test-cves-page {
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

.refresh-button {
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

.refresh-button:hover {
  background-color: #2980b9;
}

.cves-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.search-filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1.5rem;
  align-items: end;
}

.search-group,
.filter-group {
  display: flex;
  flex-direction: column;
}

.search-label,
.filter-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.search-input,
.filter-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
}

.search-input:focus,
.filter-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid;
}

.stat-card.critical {
  border-left-color: #dc2626;
}

.stat-card.high {
  border-left-color: #ea580c;
}

.stat-card.medium {
  border-left-color: #d97706;
}

.stat-card.low {
  border-left-color: #059669;
}

.stat-icon {
  font-size: 2rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #374151;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 500;
}

.cves-list {
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

.cves-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.cve-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: box-shadow 0.15s ease-in-out;
  border-left: 4px solid;
}

.cve-card.critical {
  border-left-color: #dc2626;
}

.cve-card.high {
  border-left-color: #ea580c;
}

.cve-card.medium {
  border-left-color: #d97706;
}

.cve-card.low {
  border-left-color: #059669;
}

.cve-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.cve-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  font-family: monospace;
}

.cve-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.75rem;
  flex-wrap: wrap;
}

.cve-severity {
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.cve-severity.critical {
  background-color: #fee2e2;
  color: #991b1b;
}

.cve-severity.high {
  background-color: #fed7aa;
  color: #9a3412;
}

.cve-severity.medium {
  background-color: #fef3c7;
  color: #92400e;
}

.cve-severity.low {
  background-color: #dcfce7;
  color: #166534;
}

.cve-score,
.cve-date {
  background-color: #f3f4f6;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  color: #374151;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.view-button,
.test-button,
.favorite-button {
  background: none;
  border: 1px solid #d1d5db;
  padding: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.15s ease-in-out;
}

.view-button:hover {
  background-color: #3498db;
  border-color: #3498db;
}

.test-button:hover {
  background-color: #10b981;
  border-color: #10b981;
}

.favorite-button.active {
  background-color: #fef2f2;
  border-color: #f87171;
}

.card-content {
  padding: 1.5rem;
}

.cve-description {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  line-height: 1.5;
  font-size: 0.9rem;
}

.cve-details {
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.detail-label {
  font-weight: 500;
  color: #374151;
  min-width: 80px;
}

.detail-value {
  color: #6b7280;
}

.cwe-tags,
.references {
  margin-bottom: 1rem;
}

.cwe-label,
.references-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
  display: block;
  margin-bottom: 0.5rem;
}

.cwe-list,
.references-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cwe-tag {
  background-color: #e0e7ff;
  color: #3730a3;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  font-family: monospace;
}

.reference-link {
  background-color: #f3f4f6;
  color: #374151;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  text-decoration: none;
  transition: background-color 0.15s ease-in-out;
}

.reference-link:hover {
  background-color: #e5e7eb;
}

.more-refs {
  color: #6b7280;
  font-size: 0.75rem;
  font-style: italic;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.pagination-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.pagination-button:disabled {
  background-color: #6b7280;
  cursor: not-allowed;
}

.pagination-info {
  color: #6b7280;
  font-size: 0.9rem;
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

.modal-content.cve-modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 800px;
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
  font-family: monospace;
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

.cve-detail-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.severity-badge {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-badge.critical {
  background-color: #fee2e2;
  color: #991b1b;
}

.severity-badge.high {
  background-color: #fed7aa;
  color: #9a3412;
}

.severity-badge.medium {
  background-color: #fef3c7;
  color: #92400e;
}

.severity-badge.low {
  background-color: #dcfce7;
  color: #166534;
}

.cvss-score,
.publish-date {
  background-color: #f3f4f6;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  color: #374151;
  font-weight: 500;
}

.cve-description-full,
.cve-technical-details,
.cwe-section,
.references-section {
  margin-bottom: 2rem;
}

.cve-description-full h3,
.cve-technical-details h3,
.cwe-section h3,
.references-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.detail-grid {
  display: grid;
  gap: 0.75rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
}

.detail-row .label {
  font-weight: 500;
  color: #374151;
}

.detail-row .value {
  color: #6b7280;
}

.cwe-tags-full {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cwe-tag-large {
  background-color: #e0e7ff;
  color: #3730a3;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-family: monospace;
}

.references-full {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reference-link-full {
  color: #3498db;
  text-decoration: none;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
  transition: background-color 0.15s ease-in-out;
}

.reference-link-full:hover {
  background-color: #e9ecef;
}

.modal-actions {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.create-test-button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.create-test-button:hover {
  background-color: #059669;
}

.close-button {
  background-color: #6b7280;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.close-button:hover {
  background-color: #4b5563;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .search-filter-section {
    grid-template-columns: 1fr;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .cves-grid {
    grid-template-columns: 1fr;
  }

  .cve-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .detail-row {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }

  .cve-detail-header {
    flex-direction: column;
  }
}
</style>