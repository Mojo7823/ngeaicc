<template>
  <div class="preview-save-page">
    <div class="page-header">
      <h1>Preview and Save Documents</h1>
      <p class="page-subtitle">Generate, preview, and export Common Criteria documentation</p>
      <div class="header-actions">
        <button @click="generateAllDocuments" class="generate-all-button">
          <span class="button-icon">📋</span>
          Generate All Documents
        </button>
      </div>
    </div>

    <div class="documents-container">
      <!-- Document Generation Status -->
      <div class="generation-status">
        <h2>Document Generation Status</h2>
        <div class="status-grid">
          <div
            v-for="doc in documents"
            :key="doc.id"
            class="status-card"
            :class="doc.status"
          >
            <div class="status-icon">
              <span v-if="doc.status === 'completed'">✅</span>
              <span v-else-if="doc.status === 'generating'">⏳</span>
              <span v-else-if="doc.status === 'error'">❌</span>
              <span v-else>⭕</span>
            </div>
            <div class="status-content">
              <h3>{{ doc.title }}</h3>
              <p class="status-text">{{ getStatusText(doc.status) }}</p>
              <div v-if="doc.lastGenerated" class="last-generated">
                Last generated: {{ formatDate(doc.lastGenerated) }}
              </div>
            </div>
            <div class="status-actions">
              <button
                @click="generateDocument(doc)"
                :disabled="doc.status === 'generating'"
                class="generate-button"
              >
                {{ doc.status === 'generating' ? 'Generating...' : 'Generate' }}
              </button>
              <button
                v-if="doc.status === 'completed'"
                @click="previewDocument(doc)"
                class="preview-button"
              >
                📄 Preview
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Document Templates -->
      <div class="templates-section">
        <h2>Document Templates</h2>
        <div class="templates-grid">
          <div
            v-for="template in templates"
            :key="template.id"
            class="template-card"
          >
            <div class="template-header">
              <h3>{{ template.name }}</h3>
              <span class="template-version">v{{ template.version }}</span>
            </div>
            <div class="template-content">
              <p class="template-description">{{ template.description }}</p>
              <div class="template-meta">
                <span class="template-format">Format: {{ template.format }}</span>
                <span class="template-pages">{{ template.estimatedPages }} pages</span>
              </div>
            </div>
            <div class="template-actions">
              <button @click="selectTemplate(template)" class="select-template-button">
                {{ selectedTemplate?.id === template.id ? 'Selected' : 'Select' }}
              </button>
              <button @click="customizeTemplate(template)" class="customize-button">
                ⚙️ Customize
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Options -->
      <div class="export-section">
        <h2>Export Options</h2>
        <div class="export-options">
          <div class="export-formats">
            <h3>Export Formats</h3>
            <div class="format-options">
              <label class="format-option">
                <input type="checkbox" v-model="exportFormats.pdf" />
                <span class="format-icon">📄</span>
                <span class="format-name">PDF</span>
              </label>
              <label class="format-option">
                <input type="checkbox" v-model="exportFormats.docx" />
                <span class="format-icon">📝</span>
                <span class="format-name">Word (DOCX)</span>
              </label>
              <label class="format-option">
                <input type="checkbox" v-model="exportFormats.html" />
                <span class="format-icon">🌐</span>
                <span class="format-name">HTML</span>
              </label>
              <label class="format-option">
                <input type="checkbox" v-model="exportFormats.markdown" />
                <span class="format-icon">📋</span>
                <span class="format-name">Markdown</span>
              </label>
            </div>
          </div>
          
          <div class="export-settings">
            <h3>Export Settings</h3>
            <div class="setting-group">
              <label for="include-appendix" class="setting-label">
                <input id="include-appendix" type="checkbox" v-model="exportSettings.includeAppendix" />
                Include Appendix
              </label>
            </div>
            <div class="setting-group">
              <label for="include-references" class="setting-label">
                <input id="include-references" type="checkbox" v-model="exportSettings.includeReferences" />
                Include References
              </label>
            </div>
            <div class="setting-group">
              <label for="include-test-results" class="setting-label">
                <input id="include-test-results" type="checkbox" v-model="exportSettings.includeTestResults" />
                Include Test Results
              </label>
            </div>
            <div class="setting-group">
              <label for="watermark" class="setting-label">
                <input id="watermark" type="checkbox" v-model="exportSettings.watermark" />
                Add Draft Watermark
              </label>
            </div>
          </div>
        </div>
        
        <div class="export-actions">
          <button
            @click="exportDocuments"
            :disabled="!hasSelectedFormats || isExporting"
            class="export-button"
          >
            {{ isExporting ? 'Exporting...' : 'Export Selected Documents' }}
          </button>
          <button @click="scheduleExport" class="schedule-button">
            📅 Schedule Export
          </button>
        </div>
      </div>

      <!-- Recent Exports -->
      <div class="recent-exports">
        <h2>Recent Exports</h2>
        <div v-if="recentExports.length === 0" class="empty-exports">
          <p>No recent exports found.</p>
        </div>
        <div v-else class="exports-list">
          <div
            v-for="exportItem in recentExports"
            :key="exportItem.id"
            class="export-item"
          >
            <div class="export-info">
              <h4>{{ exportItem.name }}</h4>
              <div class="export-meta">
                <span class="export-format">{{ exportItem.format.toUpperCase() }}</span>
                <span class="export-size">{{ exportItem.size }}</span>
                <span class="export-date">{{ formatDate(exportItem.createdAt) }}</span>
              </div>
            </div>
            <div class="export-actions">
              <button @click="downloadExport(exportItem)" class="download-button">
                💾 Download
              </button>
              <button @click="shareExport(exportItem)" class="share-button">
                🔗 Share
              </button>
              <button @click="deleteExport(exportItem)" class="delete-button">
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Document Preview Modal -->
    <div v-if="previewDoc" class="modal-overlay" @click="closePreview">
      <div class="modal-content preview-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ previewDoc.title }} - Preview</h2>
          <button @click="closePreview" class="modal-close">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="preview-content">
            <div class="document-preview">
              <iframe
                :src="previewDoc.previewUrl"
                class="preview-iframe"
                frameborder="0"
              ></iframe>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="downloadPreview" class="download-preview-button">
            💾 Download
          </button>
          <button @click="closePreview" class="close-button">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'

interface Document {
  id: string
  title: string
  status: 'pending' | 'generating' | 'completed' | 'error'
  lastGenerated?: string
  previewUrl?: string
}

interface Template {
  id: string
  name: string
  version: string
  description: string
  format: string
  estimatedPages: number
}

interface ExportItem {
  id: string
  name: string
  format: string
  size: string
  createdAt: string
}

const selectedTemplate = ref<Template | null>(null)
const previewDoc = ref<Document | null>(null)
const isExporting = ref(false)

const exportFormats = reactive({
  pdf: true,
  docx: false,
  html: false,
  markdown: false
})

const exportSettings = reactive({
  includeAppendix: true,
  includeReferences: true,
  includeTestResults: true,
  watermark: false
})

// Mock data for documents
const documents = ref<Document[]>([
  {
    id: 'toe-description',
    title: 'TOE Description',
    status: 'completed',
    lastGenerated: '2024-01-15T10:30:00Z',
    previewUrl: '/api/preview/toe-description'
  },
  {
    id: 'assurance-activities',
    title: 'Assurance Activities Identification',
    status: 'completed',
    lastGenerated: '2024-01-14T14:20:00Z',
    previewUrl: '/api/preview/assurance-activities'
  },
  {
    id: 'assurance-equivalency',
    title: 'Assurance Equivalency Justification',
    status: 'pending'
  },
  {
    id: 'test-bed-description',
    title: 'Test Bed Description',
    status: 'generating'
  },
  {
    id: 'tss-guidance',
    title: 'TSS and Guidance Activities',
    status: 'error'
  },
  {
    id: 'security-requirements',
    title: 'Security Assurance Requirements',
    status: 'pending'
  }
])

// Mock data for templates
const templates = ref<Template[]>([
  {
    id: 'cc-standard',
    name: 'Common Criteria Standard Template',
    version: '3.1',
    description: 'Standard Common Criteria documentation template following CC v3.1 guidelines',
    format: 'PDF/DOCX',
    estimatedPages: 150
  },
  {
    id: 'cc-compact',
    name: 'Common Criteria Compact Template',
    version: '2.0',
    description: 'Compact version for smaller evaluations with reduced documentation requirements',
    format: 'PDF/DOCX',
    estimatedPages: 75
  },
  {
    id: 'cc-detailed',
    name: 'Common Criteria Detailed Template',
    version: '1.5',
    description: 'Comprehensive template with extended sections and detailed analysis',
    format: 'PDF/DOCX',
    estimatedPages: 300
  }
])

// Mock data for recent exports
const recentExports = ref<ExportItem[]>([
  {
    id: '1',
    name: 'Complete CC Documentation Package',
    format: 'pdf',
    size: '25.4 MB',
    createdAt: '2024-01-15T16:30:00Z'
  },
  {
    id: '2',
    name: 'TOE Description Document',
    format: 'docx',
    size: '2.1 MB',
    createdAt: '2024-01-14T09:15:00Z'
  },
  {
    id: '3',
    name: 'Security Requirements Analysis',
    format: 'html',
    size: '850 KB',
    createdAt: '2024-01-13T14:45:00Z'
  }
])

const hasSelectedFormats = computed(() => {
  return Object.values(exportFormats).some(selected => selected)
})

const generateAllDocuments = async () => {
  for (const doc of documents.value) {
    if (doc.status !== 'generating') {
      generateDocument(doc)
    }
  }
}

const generateDocument = async (doc: Document) => {
  doc.status = 'generating'
  
  // Simulate document generation
  setTimeout(() => {
    doc.status = 'completed'
    doc.lastGenerated = new Date().toISOString()
    doc.previewUrl = `/api/preview/${doc.id}`
  }, 3000)
}

const previewDocument = (doc: Document) => {
  if (doc.status === 'completed') {
    previewDoc.value = doc
  }
}

const closePreview = () => {
  previewDoc.value = null
}

const downloadPreview = () => {
  if (previewDoc.value) {
    alert(`Downloading ${previewDoc.value.title}`)
  }
}

const selectTemplate = (template: Template) => {
  selectedTemplate.value = selectedTemplate.value?.id === template.id ? null : template
}

const customizeTemplate = (template: Template) => {
  alert(`Customizing template: ${template.name}`)
}

const exportDocuments = async () => {
  isExporting.value = true
  
  const selectedFormats = Object.entries(exportFormats)
    .filter(([_, selected]) => selected)
    .map(([format, _]) => format)
  
  // Simulate export process
  setTimeout(() => {
    isExporting.value = false
    
    // Add to recent exports
    const newExport: ExportItem = {
      id: Date.now().toString(),
      name: 'Generated Documentation Package',
      format: selectedFormats[0], // Use first selected format
      size: '15.7 MB',
      createdAt: new Date().toISOString()
    }
    
    recentExports.value.unshift(newExport)
    alert('Documents exported successfully!')
  }, 5000)
}

const scheduleExport = () => {
  alert('Export scheduling feature coming soon!')
}

const downloadExport = (exportItem: ExportItem) => {
  alert(`Downloading ${exportItem.name}`)
}

const shareExport = (exportItem: ExportItem) => {
  alert(`Sharing ${exportItem.name}`)
}

const deleteExport = (exportItem: ExportItem) => {
  if (confirm(`Delete ${exportItem.name}?`)) {
    const index = recentExports.value.findIndex(exp => exp.id === exportItem.id)
    if (index !== -1) {
      recentExports.value.splice(index, 1)
    }
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'completed':
      return 'Ready for export'
    case 'generating':
      return 'Generating document...'
    case 'error':
      return 'Generation failed'
    default:
      return 'Not generated'
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.preview-save-page {
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

.generate-all-button {
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

.generate-all-button:hover {
  background-color: #2980b9;
}

.documents-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.generation-status,
.templates-section,
.export-section,
.recent-exports {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.generation-status h2,
.templates-section h2,
.export-section h2,
.recent-exports h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.status-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  transition: box-shadow 0.15s ease-in-out;
}

.status-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.status-card.completed {
  border-left: 4px solid #10b981;
}

.status-card.generating {
  border-left: 4px solid #f59e0b;
}

.status-card.error {
  border-left: 4px solid #ef4444;
}

.status-card.pending {
  border-left: 4px solid #6b7280;
}

.status-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.status-content {
  flex: 1;
}

.status-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.status-text {
  margin: 0 0 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.last-generated {
  color: #9ca3af;
  font-size: 0.75rem;
}

.status-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-shrink: 0;
}

.generate-button,
.preview-button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  white-space: nowrap;
}

.generate-button:hover {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.generate-button:disabled {
  background-color: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.preview-button:hover {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.template-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: box-shadow 0.15s ease-in-out;
}

.template-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.template-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.template-version {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.template-description {
  margin: 0 0 1rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
}

.template-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.75rem;
  color: #9ca3af;
}

.template-actions {
  display: flex;
  gap: 0.5rem;
}

.select-template-button,
.customize-button {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.select-template-button:hover {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.customize-button:hover {
  background-color: #8b5cf6;
  color: white;
  border-color: #8b5cf6;
}

.export-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.export-formats h3,
.export-settings h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.format-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.format-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  transition: background-color 0.15s ease-in-out;
}

.format-option:hover {
  background-color: #f9fafb;
}

.format-icon {
  font-size: 1.25rem;
}

.format-name {
  font-weight: 500;
  color: #374151;
}

.setting-group {
  margin-bottom: 0.75rem;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  color: #374151;
  font-size: 0.875rem;
}

.export-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-start;
}

.export-button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.export-button:hover:not(:disabled) {
  background-color: #059669;
}

.export-button:disabled {
  background-color: #6b7280;
  cursor: not-allowed;
}

.schedule-button {
  background-color: #8b5cf6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.schedule-button:hover {
  background-color: #7c3aed;
}

.empty-exports {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.exports-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.export-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  transition: box-shadow 0.15s ease-in-out;
}

.export-item:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.export-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.export-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.export-format {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.export-actions {
  display: flex;
  gap: 0.5rem;
}

.download-button,
.share-button,
.delete-button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #374151;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.download-button:hover {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.share-button:hover {
  background-color: #8b5cf6;
  color: white;
  border-color: #8b5cf6;
}

.delete-button:hover {
  background-color: #ef4444;
  color: white;
  border-color: #ef4444;
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

.modal-content.preview-modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 90vw;
  width: 1000px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
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
  flex: 1;
  overflow: hidden;
}

.preview-content {
  height: 100%;
  padding: 1rem;
}

.document-preview {
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: 500px;
  background-color: #f9fafb;
}

.modal-actions {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  flex-shrink: 0;
}

.download-preview-button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}

.download-preview-button:hover {
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

  .status-grid,
  .templates-grid {
    grid-template-columns: 1fr;
  }

  .export-options {
    grid-template-columns: 1fr;
  }

  .export-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .export-actions {
    align-self: stretch;
    justify-content: space-between;
  }

  .modal-content.preview-modal {
    width: 95vw;
    max-height: 95vh;
  }
}
</style>