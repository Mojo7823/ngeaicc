<template>
  <div class="test-cases-page">
    <div class="page-header">
      <h1>Test Cases</h1>
      <p class="page-subtitle">Manage and configure test cases for evaluation</p>
      <div class="header-actions">
        <button @click="addTestCase" class="add-button">
          <span class="button-icon">➕</span>
          Add Test Case
        </button>
      </div>
    </div>

    <div class="test-cases-container">
      <!-- Test Case Form -->
      <div v-if="showForm" class="test-case-form-container">
        <form @submit.prevent="saveTestCase" class="test-case-form">
          <div class="form-header">
            <h2>{{ editingTestCase ? 'Edit Test Case' : 'New Test Case' }}</h2>
            <button type="button" @click="cancelForm" class="close-button">✕</button>
          </div>
          
          <div class="form-content">
            <div class="form-group">
              <label for="test_name" class="form-label">Test Name</label>
              <input
                id="test_name"
                v-model="testCaseForm.test_name"
                type="text"
                class="form-input"
                placeholder="Enter test name"
                required
              />
            </div>

            <div class="form-group">
              <label for="description" class="form-label">Description</label>
              <textarea
                id="description"
                v-model="testCaseForm.description"
                class="form-input form-textarea"
                placeholder="Enter detailed test description"
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label for="cve_cwe_code" class="form-label">CVE/CWE Code</label>
              <input
                id="cve_cwe_code"
                v-model="testCaseForm.cve_cwe_code"
                type="text"
                class="form-input"
                placeholder="e.g., CVE-2023-1234 or CWE-79"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Tools Used</label>
              <div class="tools-selector">
                <select v-model="selectedTool" @change="addTool" class="form-input">
                  <option value="">Select a tool to add</option>
                  <option v-for="tool in availableTools" :key="tool.id" :value="tool">
                    {{ tool.name }}
                  </option>
                </select>
                <div v-if="testCaseForm.tools_used.length > 0" class="selected-tools">
                  <div
                    v-for="tool in testCaseForm.tools_used"
                    :key="tool.id"
                    class="tool-tag"
                  >
                    <span>{{ tool.name }}</span>
                    <button type="button" @click="removeTool(tool.id)" class="remove-tool">×</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Test Plan</label>
              <div class="test-plan-selector">
                <select v-model="selectedTestPlan" @change="addTestPlan" class="form-input">
                  <option value="">Select a test plan to add</option>
                  <option v-for="plan in testingToolsPlans" :key="plan.id" :value="plan">
                    {{ plan.name }}
                  </option>
                </select>
                <div v-if="testCaseForm.test_plans.length > 0" class="selected-plans">
                  <div
                    v-for="plan in testCaseForm.test_plans"
                    :key="plan.id"
                    class="plan-tag"
                  >
                    <span>{{ plan.name }}</span>
                    <button type="button" @click="removeTestPlan(plan.id)" class="remove-plan">×</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="cancelForm" class="cancel-button">Cancel</button>
            <button type="submit" class="save-button">
              {{ editingTestCase ? 'Update' : 'Create' }} Test Case
            </button>
          </div>
        </form>
      </div>

      <!-- Test Cases List -->
      <div class="test-cases-list">
        <div v-if="testCases.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>No Test Cases Yet</h3>
          <p>Start by creating your first test case to begin evaluation.</p>
        </div>
        
        <div v-else class="test-cases-grid">
          <div
            v-for="testCase in testCases"
            :key="testCase.id"
            class="test-case-card"
          >
            <div class="card-header">
              <h3>{{ testCase.test_name }}</h3>
              <div class="card-actions">
                <button @click="editTestCase(testCase)" class="edit-button">✏️</button>
                <button @click="deleteTestCase(testCase.id)" class="delete-button">🗑️</button>
              </div>
            </div>
            
            <div class="card-content">
              <p class="description">{{ testCase.description }}</p>
              
              <div v-if="testCase.cve_cwe_code" class="cve-code">
                <span class="label">CVE/CWE:</span>
                <span class="value">{{ testCase.cve_cwe_code }}</span>
              </div>
              
              <div v-if="testCase.tools_used.length > 0" class="tools-list">
                <span class="label">Tools:</span>
                <div class="tools-tags">
                  <span
                    v-for="tool in testCase.tools_used"
                    :key="tool.id"
                    class="tool-tag-small"
                  >
                    {{ tool.name }}
                  </span>
                </div>
              </div>
              
              <div v-if="testCase.test_plans.length > 0" class="plans-list">
                <span class="label">Test Plans:</span>
                <div class="plans-tags">
                  <span
                    v-for="plan in testCase.test_plans"
                    :key="plan.id"
                    class="plan-tag-small"
                  >
                    {{ plan.name }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'

interface Tool {
  id: string
  name: string
  description?: string
}

interface TestPlan {
  id: string
  name: string
  description?: string
}

interface TestCase {
  id: string
  test_name: string
  description: string
  cve_cwe_code: string
  tools_used: Tool[]
  test_plans: TestPlan[]
}

interface TestCaseForm {
  test_name: string
  description: string
  cve_cwe_code: string
  tools_used: Tool[]
  test_plans: TestPlan[]
}

const showForm = ref(false)
const editingTestCase = ref<TestCase | null>(null)
const selectedTool = ref<Tool | string>('')
const selectedTestPlan = ref<TestPlan | string>('')

const testCaseForm = reactive<TestCaseForm>({
  test_name: '',
  description: '',
  cve_cwe_code: '',
  tools_used: [],
  test_plans: []
})

const testCases = ref<TestCase[]>([])

// Mock data for available tools
const availableTools = ref<Tool[]>([
  { id: '1', name: 'Nmap', description: 'Network exploration tool' },
  { id: '2', name: 'Ping', description: 'Network connectivity test' },
  { id: '3', name: 'Wireshark', description: 'Network protocol analyzer' },
  { id: '4', name: 'Metasploit', description: 'Penetration testing framework' },
  { id: '5', name: 'Burp Suite', description: 'Web application security testing' }
])

// Mock data for testing tools plans
const testingToolsPlans = ref<TestPlan[]>([
  { id: '1', name: 'Network Discovery', description: 'Basic network scanning' },
  { id: '2', name: 'Port Scanning', description: 'Comprehensive port analysis' },
  { id: '3', name: 'Vulnerability Assessment', description: 'Security vulnerability testing' },
  { id: '4', name: 'Web Application Testing', description: 'Web app security evaluation' },
  { id: '5', name: 'Penetration Testing', description: 'Full security penetration test' }
])

const addTestCase = () => {
  resetForm()
  showForm.value = true
}

const editTestCase = (testCase: TestCase) => {
  editingTestCase.value = testCase
  testCaseForm.test_name = testCase.test_name
  testCaseForm.description = testCase.description
  testCaseForm.cve_cwe_code = testCase.cve_cwe_code
  testCaseForm.tools_used = [...testCase.tools_used]
  testCaseForm.test_plans = [...testCase.test_plans]
  showForm.value = true
}

const cancelForm = () => {
  showForm.value = false
  editingTestCase.value = null
  resetForm()
}

const resetForm = () => {
  testCaseForm.test_name = ''
  testCaseForm.description = ''
  testCaseForm.cve_cwe_code = ''
  testCaseForm.tools_used = []
  testCaseForm.test_plans = []
  selectedTool.value = ''
  selectedTestPlan.value = ''
}

const addTool = () => {
  if (selectedTool.value && typeof selectedTool.value === 'object') {
    const tool = selectedTool.value as Tool
    if (!testCaseForm.tools_used.find(t => t.id === tool.id)) {
      testCaseForm.tools_used.push(tool)
    }
    selectedTool.value = ''
  }
}

const removeTool = (toolId: string) => {
  testCaseForm.tools_used = testCaseForm.tools_used.filter(tool => tool.id !== toolId)
}

const addTestPlan = () => {
  if (selectedTestPlan.value && typeof selectedTestPlan.value === 'object') {
    const plan = selectedTestPlan.value as TestPlan
    if (!testCaseForm.test_plans.find(p => p.id === plan.id)) {
      testCaseForm.test_plans.push(plan)
    }
    selectedTestPlan.value = ''
  }
}

const removeTestPlan = (planId: string) => {
  testCaseForm.test_plans = testCaseForm.test_plans.filter(plan => plan.id !== planId)
}

const saveTestCase = () => {
  const newTestCase: TestCase = {
    id: editingTestCase.value?.id || Date.now().toString(),
    test_name: testCaseForm.test_name,
    description: testCaseForm.description,
    cve_cwe_code: testCaseForm.cve_cwe_code,
    tools_used: [...testCaseForm.tools_used],
    test_plans: [...testCaseForm.test_plans]
  }

  if (editingTestCase.value) {
    const index = testCases.value.findIndex(tc => tc.id === editingTestCase.value!.id)
    if (index !== -1) {
      testCases.value[index] = newTestCase
    }
  } else {
    testCases.value.push(newTestCase)
  }

  cancelForm()
}

const deleteTestCase = (id: string) => {
  if (confirm('Are you sure you want to delete this test case?')) {
    testCases.value = testCases.value.filter(tc => tc.id !== id)
  }
}

onMounted(() => {
  // Load test cases from API
  // For now, we'll use mock data
})
</script>

<style scoped>
.test-cases-page {
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

.add-button {
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

.add-button:hover {
  background-color: #2980b9;
}

.test-cases-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.test-case-form-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid #3498db;
}

.test-case-form {
  padding: 0;
}

.form-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.form-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
}

.close-button:hover {
  color: #374151;
}

.form-content {
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 14px;
  line-height: 1.5;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
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

.tools-selector,
.test-plan-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.selected-tools,
.selected-plans {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tool-tag,
.plan-tag {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.remove-tool,
.remove-plan {
  background: none;
  border: none;
  color: #1976d2;
  cursor: pointer;
  font-weight: bold;
  padding: 0;
  margin-left: 0.25rem;
}

.remove-tool:hover,
.remove-plan:hover {
  color: #d32f2f;
}

.form-actions {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background-color: #f8f9fa;
}

.cancel-button {
  background-color: #6b7280;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #4b5563;
}

.save-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.save-button:hover {
  background-color: #2980b9;
}

.test-cases-list {
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

.test-cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.test-case-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: box-shadow 0.15s ease-in-out;
}

.test-case-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button,
.delete-button {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.15s ease-in-out;
}

.edit-button:hover,
.delete-button:hover {
  transform: scale(1.1);
}

.card-content {
  padding: 1.5rem;
}

.description {
  margin: 0 0 1rem 0;
  color: #6b7280;
  line-height: 1.5;
}

.cve-code,
.tools-list,
.plans-list {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.value {
  color: #6b7280;
  font-family: monospace;
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.tools-tags,
.plans-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tool-tag-small,
.plan-tag-small {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .form-content {
    grid-template-columns: 1fr;
    padding: 1.5rem;
  }

  .test-cases-grid {
    grid-template-columns: 1fr;
  }
}
</style>