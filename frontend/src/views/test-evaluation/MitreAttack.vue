<template>
  <div class="mitre-attack-page">
    <div class="page-header">
      <h1>MITRE ATT&CK Framework</h1>
      <p class="page-subtitle">Adversarial Tactics, Techniques & Common Knowledge</p>
      <div class="header-actions">
        <button @click="refreshFramework" class="refresh-button">
          <span class="button-icon">🔄</span>
          Refresh Framework
        </button>
      </div>
    </div>

    <div class="attack-container">
      <!-- Framework Overview -->
      <div class="overview-section">
        <div class="overview-stats">
          <div class="stat-item">
            <div class="stat-number">{{ framework.tactics.length }}</div>
            <div class="stat-label">Tactics</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ totalTechniques }}</div>
            <div class="stat-label">Techniques</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ totalSubTechniques }}</div>
            <div class="stat-label">Sub-techniques</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ testCoverage }}%</div>
            <div class="stat-label">Test Coverage</div>
          </div>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="filter-section">
        <div class="filter-group">
          <label for="platform-filter" class="filter-label">Platform</label>
          <select id="platform-filter" v-model="platformFilter" class="filter-input">
            <option value="">All Platforms</option>
            <option value="windows">Windows</option>
            <option value="linux">Linux</option>
            <option value="macos">macOS</option>
            <option value="network">Network</option>
            <option value="cloud">Cloud</option>
            <option value="mobile">Mobile</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="data-source-filter" class="filter-label">Data Source</label>
          <select id="data-source-filter" v-model="dataSourceFilter" class="filter-input">
            <option value="">All Data Sources</option>
            <option value="process">Process Monitoring</option>
            <option value="network">Network Traffic</option>
            <option value="file">File Monitoring</option>
            <option value="registry">Registry</option>
            <option value="api">API Monitoring</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="search-techniques" class="filter-label">Search</label>
          <input
            id="search-techniques"
            v-model="searchQuery"
            type="text"
            class="filter-input"
            placeholder="Search techniques..."
          />
        </div>
      </div>

      <!-- MITRE ATT&CK Matrix -->
      <div class="attack-matrix">
        <h2>ATT&CK Matrix</h2>
        <div class="matrix-container">
          <div class="tactics-header">
            <div
              v-for="tactic in framework.tactics"
              :key="tactic.id"
              class="tactic-column"
              @click="selectTactic(tactic)"
              :class="{ active: selectedTactic?.id === tactic.id }"
            >
              <div class="tactic-name">{{ tactic.name }}</div>
              <div class="tactic-id">{{ tactic.id }}</div>
              <div class="technique-count">{{ getTechniqueCount(tactic.id) }} techniques</div>
            </div>
          </div>
          
          <div v-if="selectedTactic" class="techniques-list">
            <h3>{{ selectedTactic.name }} Techniques</h3>
            <div class="techniques-grid">
              <div
                v-for="technique in getFilteredTechniques(selectedTactic.id)"
                :key="technique.id"
                class="technique-card"
                @click="selectTechnique(technique)"
                :class="{ 
                  'has-test': technique.has_test,
                  'selected': selectedTechnique?.id === technique.id
                }"
              >
                <div class="technique-header">
                  <div class="technique-name">{{ technique.name }}</div>
                  <div class="technique-id">{{ technique.id }}</div>
                </div>
                
                <div class="technique-meta">
                  <div class="platforms">
                    <span
                      v-for="platform in technique.platforms.slice(0, 2)"
                      :key="platform"
                      class="platform-tag"
                    >
                      {{ platform }}
                    </span>
                    <span v-if="technique.platforms.length > 2" class="more-platforms">
                      +{{ technique.platforms.length - 2 }}
                    </span>
                  </div>
                  
                  <div class="test-status">
                    <span v-if="technique.has_test" class="has-test-badge">✅ Tested</span>
                    <span v-else class="no-test-badge">❌ No Test</span>
                  </div>
                </div>
                
                <div v-if="technique.sub_techniques.length > 0" class="sub-techniques-count">
                  {{ technique.sub_techniques.length }} sub-techniques
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Technique Detail Panel -->
      <div v-if="selectedTechnique" class="technique-detail">
        <div class="detail-header">
          <h2>{{ selectedTechnique.name }}</h2>
          <div class="detail-actions">
            <button @click="createTestForTechnique" class="create-test-button">
              🧪 Create Test
            </button>
            <button @click="closeDetail" class="close-detail-button">✕</button>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="technique-info">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">{{ selectedTechnique.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Tactic:</span>
                <span class="info-value">{{ getTacticName(selectedTechnique.tactic_id) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Platforms:</span>
                <div class="platforms-list">
                  <span
                    v-for="platform in selectedTechnique.platforms"
                    :key="platform"
                    class="platform-tag-large"
                  >
                    {{ platform }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="technique-description">
            <h3>Description</h3>
            <p>{{ selectedTechnique.description }}</p>
          </div>
          
          <div v-if="selectedTechnique.data_sources.length > 0" class="data-sources">
            <h3>Data Sources</h3>
            <div class="data-sources-list">
              <span
                v-for="source in selectedTechnique.data_sources"
                :key="source"
                class="data-source-tag"
              >
                {{ source }}
              </span>
            </div>
          </div>
          
          <div v-if="selectedTechnique.mitigations.length > 0" class="mitigations">
            <h3>Mitigations</h3>
            <div class="mitigations-list">
              <div
                v-for="mitigation in selectedTechnique.mitigations"
                :key="mitigation.id"
                class="mitigation-item"
              >
                <span class="mitigation-id">{{ mitigation.id }}</span>
                <span class="mitigation-name">{{ mitigation.name }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="selectedTechnique.sub_techniques.length > 0" class="sub-techniques">
            <h3>Sub-techniques</h3>
            <div class="sub-techniques-list">
              <div
                v-for="subTech in selectedTechnique.sub_techniques"
                :key="subTech.id"
                class="sub-technique-item"
                :class="{ 'has-test': subTech.has_test }"
              >
                <div class="sub-technique-header">
                  <span class="sub-technique-id">{{ subTech.id }}</span>
                  <span class="sub-technique-name">{{ subTech.name }}</span>
                  <span v-if="subTech.has_test" class="test-indicator">✅</span>
                </div>
                <p class="sub-technique-description">{{ subTech.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Mitigation {
  id: string
  name: string
}

interface SubTechnique {
  id: string
  name: string
  description: string
  has_test: boolean
}

interface Technique {
  id: string
  name: string
  description: string
  tactic_id: string
  platforms: string[]
  data_sources: string[]
  mitigations: Mitigation[]
  sub_techniques: SubTechnique[]
  has_test: boolean
}

interface Tactic {
  id: string
  name: string
  description: string
}

interface AttackFramework {
  tactics: Tactic[]
  techniques: Technique[]
}

const platformFilter = ref('')
const dataSourceFilter = ref('')
const searchQuery = ref('')
const selectedTactic = ref<Tactic | null>(null)
const selectedTechnique = ref<Technique | null>(null)

// Mock MITRE ATT&CK data
const framework = ref<AttackFramework>({
  tactics: [
    {
      id: 'TA0001',
      name: 'Initial Access',
      description: 'The adversary is trying to get into your network.'
    },
    {
      id: 'TA0002',
      name: 'Execution',
      description: 'The adversary is trying to run malicious code.'
    },
    {
      id: 'TA0003',
      name: 'Persistence',
      description: 'The adversary is trying to maintain their foothold.'
    },
    {
      id: 'TA0004',
      name: 'Privilege Escalation',
      description: 'The adversary is trying to gain higher-level permissions.'
    },
    {
      id: 'TA0005',
      name: 'Defense Evasion',
      description: 'The adversary is trying to avoid being detected.'
    },
    {
      id: 'TA0006',
      name: 'Credential Access',
      description: 'The adversary is trying to steal account names and passwords.'
    },
    {
      id: 'TA0007',
      name: 'Discovery',
      description: 'The adversary is trying to figure out your environment.'
    },
    {
      id: 'TA0008',
      name: 'Lateral Movement',
      description: 'The adversary is trying to move through your environment.'
    },
    {
      id: 'TA0009',
      name: 'Collection',
      description: 'The adversary is trying to gather data of interest.'
    },
    {
      id: 'TA0010',
      name: 'Exfiltration',
      description: 'The adversary is trying to steal data.'
    },
    {
      id: 'TA0011',
      name: 'Command and Control',
      description: 'The adversary is trying to communicate with compromised systems.'
    }
  ],
  techniques: [
    {
      id: 'T1566',
      name: 'Phishing',
      description: 'Adversaries may send phishing messages to gain access to victim systems.',
      tactic_id: 'TA0001',
      platforms: ['Windows', 'macOS', 'Linux'],
      data_sources: ['Email Gateway', 'Network Traffic'],
      mitigations: [
        { id: 'M1017', name: 'User Training' },
        { id: 'M1021', name: 'Restrict Web-Based Content' }
      ],
      sub_techniques: [
        {
          id: 'T1566.001',
          name: 'Spearphishing Attachment',
          description: 'Adversaries may send spearphishing emails with a malicious attachment.',
          has_test: true
        },
        {
          id: 'T1566.002',
          name: 'Spearphishing Link',
          description: 'Adversaries may send spearphishing emails with a malicious link.',
          has_test: false
        }
      ],
      has_test: true
    },
    {
      id: 'T1059',
      name: 'Command and Scripting Interpreter',
      description: 'Adversaries may abuse command and script interpreters to execute commands.',
      tactic_id: 'TA0002',
      platforms: ['Windows', 'Linux', 'macOS'],
      data_sources: ['Process', 'Command'],
      mitigations: [
        { id: 'M1038', name: 'Execution Prevention' },
        { id: 'M1042', name: 'Disable or Remove Feature or Program' }
      ],
      sub_techniques: [
        {
          id: 'T1059.001',
          name: 'PowerShell',
          description: 'Adversaries may abuse PowerShell commands and scripts.',
          has_test: true
        },
        {
          id: 'T1059.003',
          name: 'Windows Command Shell',
          description: 'Adversaries may abuse the Windows command shell.',
          has_test: true
        }
      ],
      has_test: true
    },
    {
      id: 'T1547',
      name: 'Boot or Logon Autostart Execution',
      description: 'Adversaries may configure system settings to automatically execute a program.',
      tactic_id: 'TA0003',
      platforms: ['Windows', 'macOS', 'Linux'],
      data_sources: ['Registry', 'File', 'Process'],
      mitigations: [
        { id: 'M1024', name: 'Restrict Registry Permissions' },
        { id: 'M1018', name: 'User Account Management' }
      ],
      sub_techniques: [],
      has_test: false
    },
    {
      id: 'T1055',
      name: 'Process Injection',
      description: 'Adversaries may inject code into processes in order to evade process-based defenses.',
      tactic_id: 'TA0004',
      platforms: ['Windows', 'macOS', 'Linux'],
      data_sources: ['Process', 'API'],
      mitigations: [
        { id: 'M1040', name: 'Behavior Prevention on Endpoint' }
      ],
      sub_techniques: [
        {
          id: 'T1055.001',
          name: 'Dynamic-link Library Injection',
          description: 'Adversaries may inject dynamic-link libraries (DLLs) into processes.',
          has_test: true
        }
      ],
      has_test: true
    }
  ]
})

const totalTechniques = computed(() => framework.value.techniques.length)
const totalSubTechniques = computed(() => 
  framework.value.techniques.reduce((total, tech) => total + tech.sub_techniques.length, 0)
)
const testCoverage = computed(() => {
  const testedTechniques = framework.value.techniques.filter(tech => tech.has_test).length
  return Math.round((testedTechniques / totalTechniques.value) * 100)
})

const getTechniqueCount = (tacticId: string) => {
  return framework.value.techniques.filter(tech => tech.tactic_id === tacticId).length
}

const getFilteredTechniques = (tacticId: string) => {
  let techniques = framework.value.techniques.filter(tech => tech.tactic_id === tacticId)

  if (platformFilter.value) {
    techniques = techniques.filter(tech => 
      tech.platforms.some(platform => 
        platform.toLowerCase().includes(platformFilter.value.toLowerCase())
      )
    )
  }

  if (dataSourceFilter.value) {
    techniques = techniques.filter(tech => 
      tech.data_sources.some(source => 
        source.toLowerCase().includes(dataSourceFilter.value.toLowerCase())
      )
    )
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    techniques = techniques.filter(tech => 
      tech.name.toLowerCase().includes(query) ||
      tech.id.toLowerCase().includes(query) ||
      tech.description.toLowerCase().includes(query)
    )
  }

  return techniques
}

const getTacticName = (tacticId: string) => {
  const tactic = framework.value.tactics.find(t => t.id === tacticId)
  return tactic ? tactic.name : tacticId
}

const selectTactic = (tactic: Tactic) => {
  selectedTactic.value = selectedTactic.value?.id === tactic.id ? null : tactic
  selectedTechnique.value = null
}

const selectTechnique = (technique: Technique) => {
  selectedTechnique.value = technique
}

const closeDetail = () => {
  selectedTechnique.value = null
}

const createTestForTechnique = () => {
  if (selectedTechnique.value) {
    alert(`Creating test case for ${selectedTechnique.value.id}: ${selectedTechnique.value.name}`)
  }
}

const refreshFramework = () => {
  alert('MITRE ATT&CK Framework refreshed!')
}
</script>

<style scoped>
.mitre-attack-page {
  max-width: 1600px;
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

.attack-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.overview-section {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.05em;
}

.filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.filter-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
}

.filter-input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.attack-matrix {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.attack-matrix h2 {
  margin: 0;
  padding: 1.5rem 2rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.matrix-container {
  padding: 1.5rem;
}

.tactics-header {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.tactic-column {
  background-color: #dc2626;
  color: white;
  padding: 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  text-align: center;
}

.tactic-column:hover {
  background-color: #b91c1c;
  transform: translateY(-2px);
}

.tactic-column.active {
  background-color: #991b1b;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tactic-name {
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.tactic-id {
  font-family: monospace;
  font-size: 0.75rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.technique-count {
  font-size: 0.75rem;
  opacity: 0.9;
}

.techniques-list {
  margin-top: 2rem;
}

.techniques-list h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.techniques-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.technique-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  background: white;
}

.technique-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-color: #dc2626;
}

.technique-card.selected {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.technique-card.has-test {
  border-left: 4px solid #10b981;
}

.technique-header {
  margin-bottom: 0.75rem;
}

.technique-name {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.technique-id {
  font-family: monospace;
  font-size: 0.75rem;
  color: #6b7280;
}

.technique-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.platforms {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.platform-tag {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.625rem;
  font-weight: 500;
}

.more-platforms {
  color: #6b7280;
  font-size: 0.625rem;
}

.test-status {
  display: flex;
  align-items: center;
}

.has-test-badge {
  background-color: #dcfce7;
  color: #166534;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.625rem;
  font-weight: 500;
}

.no-test-badge {
  background-color: #fee2e2;
  color: #991b1b;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.625rem;
  font-weight: 500;
}

.sub-techniques-count {
  color: #6b7280;
  font-size: 0.75rem;
  font-style: italic;
}

.technique-detail {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  padding: 1.5rem 2rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.detail-actions {
  display: flex;
  gap: 1rem;
}

.create-test-button {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
}

.create-test-button:hover {
  background-color: #059669;
}

.close-detail-button {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
}

.close-detail-button:hover {
  color: #374151;
}

.detail-content {
  padding: 2rem;
}

.technique-info {
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
  align-items: center;
}

.info-label {
  font-weight: 500;
  color: #374151;
}

.info-value {
  color: #6b7280;
}

.platforms-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.platform-tag-large {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.technique-description,
.data-sources,
.mitigations,
.sub-techniques {
  margin-bottom: 2rem;
}

.technique-description h3,
.data-sources h3,
.mitigations h3,
.sub-techniques h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.technique-description p {
  color: #6b7280;
  line-height: 1.6;
}

.data-sources-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.data-source-tag {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.mitigations-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mitigation-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.mitigation-id {
  font-family: monospace;
  font-weight: 500;
  color: #374151;
  min-width: 80px;
}

.mitigation-name {
  color: #6b7280;
}

.sub-techniques-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sub-technique-item {
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  padding: 1rem;
}

.sub-technique-item.has-test {
  border-left: 4px solid #10b981;
}

.sub-technique-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.sub-technique-id {
  font-family: monospace;
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.sub-technique-name {
  font-weight: 500;
  color: #374151;
  flex: 1;
}

.test-indicator {
  color: #10b981;
  font-size: 1rem;
}

.sub-technique-description {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .overview-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-section {
    grid-template-columns: 1fr;
  }

  .tactics-header {
    grid-template-columns: repeat(2, 1fr);
  }

  .techniques-grid {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .info-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }
}
</style>