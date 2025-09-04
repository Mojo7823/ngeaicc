<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiService from './services/api.js'
import AdminDashboard from './components/AdminDashboard.vue'

const currentView = ref('main') // 'main' or 'admin'
const message = ref('')
const response = ref('')
const loading = ref(false)
const helloData = ref(null)
const testCases = ref([])
const devices = ref([])

const newTestCase = ref({
  name: '',
  description: '',
  category: ''
})

const newDevice = ref({
  name: '',
  manufacturer: '',
  model: '',
  description: ''
})

// Fetch hello world on component mount
onMounted(async () => {
  try {
    helloData.value = await ApiService.getHelloWorld()
    await loadTestCases()
    await loadDevices()
  } catch (error) {
    console.error('Failed to fetch initial data:', error)
  }
})

const sendMessage = async () => {
  if (!message.value.trim()) return
  
  loading.value = true
  try {
    const result = await ApiService.sendMessage(message.value)
    response.value = JSON.stringify(result, null, 2)
  } catch (error) {
    response.value = `Error: ${error.message}`
  } finally {
    loading.value = false
  }
}

const loadTestCases = async () => {
  try {
    testCases.value = await ApiService.getTestCases()
  } catch (error) {
    console.error('Failed to load test cases:', error)
  }
}

const loadDevices = async () => {
  try {
    devices.value = await ApiService.getDevices()
  } catch (error) {
    console.error('Failed to load devices:', error)
  }
}

const createTestCase = async () => {
  if (!newTestCase.value.name.trim()) return
  
  try {
    await ApiService.createTestCase(newTestCase.value)
    newTestCase.value = { name: '', description: '', category: '' }
    await loadTestCases()
  } catch (error) {
    console.error('Failed to create test case:', error)
  }
}

const createDevice = async () => {
  if (!newDevice.value.name.trim()) return
  
  try {
    await ApiService.createDevice(newDevice.value)
    newDevice.value = { name: '', manufacturer: '', model: '', description: '' }
    await loadDevices()
  } catch (error) {
    console.error('Failed to create device:', error)
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <div class="header-content">
        <div>
          <h1>AI Testing Standard Platform</h1>
          <p>FastAPI + Vue.js + PostgreSQL (pgvector) Integration Test</p>
        </div>
        <nav class="main-nav">
          <button 
            @click="currentView = 'main'"
            :class="['nav-btn', { active: currentView === 'main' }]"
          >
            🏠 Main
          </button>
          <button 
            @click="currentView = 'admin'"
            :class="['nav-btn', { active: currentView === 'admin' }]"
          >
            🔧 Admin
          </button>
        </nav>
      </div>
    </header>

    <!-- Main Application View -->
    <main v-if="currentView === 'main'">
      <!-- Hello World Section -->
      <section class="hello-section">
        <h2>🚀 Backend Connection Status</h2>
        <div v-if="helloData" class="status-card success">
          <h3>✅ Connected to FastAPI Backend</h3>
          <pre>{{ JSON.stringify(helloData, null, 2) }}</pre>
        </div>
        <div v-else class="status-card error">
          <h3>❌ Backend Connection Failed</h3>
          <p>Make sure FastAPI server is running on http://localhost:8000</p>
        </div>
      </section>

      <!-- Message Echo Section -->
      <section class="echo-section">
        <h2>💬 Message Echo Test</h2>
        <div class="input-group">
          <input 
            v-model="message" 
            type="text" 
            placeholder="Enter a message to send to backend..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage" :disabled="loading || !message.trim()">
            {{ loading ? 'Sending...' : 'Send Message' }}
          </button>
        </div>
        
        <div v-if="response" class="response-card">
          <h4>Response from Backend:</h4>
          <pre>{{ response }}</pre>
        </div>
      </section>

      <!-- Test Cases Section -->
      <section class="data-section">
        <h2>🧪 Test Cases (Database Integration)</h2>
        
        <div class="create-form">
          <h4>Create New Test Case</h4>
          <input v-model="newTestCase.name" placeholder="Test Case Name" />
          <input v-model="newTestCase.description" placeholder="Description" />
          <input v-model="newTestCase.category" placeholder="Category" />
          <button @click="createTestCase" :disabled="!newTestCase.name.trim()">
            Create Test Case
          </button>
        </div>

        <div class="data-list">
          <h4>Existing Test Cases ({{ testCases.length }})</h4>
          <div v-if="testCases.length === 0" class="empty-state">
            No test cases found. Create one above!
          </div>
          <div v-for="testCase in testCases" :key="testCase.id" class="data-item">
            <h5>{{ testCase.name }}</h5>
            <p><strong>Category:</strong> {{ testCase.category || 'N/A' }}</p>
            <p><strong>Description:</strong> {{ testCase.description || 'No description' }}</p>
            <small>Created: {{ new Date(testCase.created_at).toLocaleString() }}</small>
          </div>
        </div>
      </section>

      <!-- Devices Section -->
      <section class="data-section">
        <h2>📱 Devices Under Test</h2>
        
        <div class="create-form">
          <h4>Add New Device</h4>
          <input v-model="newDevice.name" placeholder="Device Name" />
          <input v-model="newDevice.manufacturer" placeholder="Manufacturer" />
          <input v-model="newDevice.model" placeholder="Model" />
          <input v-model="newDevice.description" placeholder="Description" />
          <button @click="createDevice" :disabled="!newDevice.name.trim()">
            Add Device
          </button>
        </div>

        <div class="data-list">
          <h4>Registered Devices ({{ devices.length }})</h4>
          <div v-if="devices.length === 0" class="empty-state">
            No devices found. Add one above!
          </div>
          <div v-for="device in devices" :key="device.id" class="data-item">
            <h5>{{ device.name }}</h5>
            <p><strong>Manufacturer:</strong> {{ device.manufacturer || 'N/A' }}</p>
            <p><strong>Model:</strong> {{ device.model || 'N/A' }}</p>
            <p><strong>Description:</strong> {{ device.description || 'No description' }}</p>
            <small>Created: {{ new Date(device.created_at).toLocaleString() }}</small>
          </div>
        </div>
      </section>
    </main>

    <!-- Admin Dashboard View -->
    <AdminDashboard v-if="currentView === 'admin'" />
  </div>
</template>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

header {
  margin-bottom: 40px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.header-content > div {
  text-align: left;
}

header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5em;
}

header p {
  margin: 0;
  opacity: 0.9;
}

.main-nav {
  display: flex;
  gap: 10px;
}

.nav-btn {
  padding: 10px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

section {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
}

section h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.status-card {
  padding: 20px;
  border-radius: 8px;
  margin: 15px 0;
}

.status-card.success {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.status-card.error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.input-group {
  display: flex;
  gap: 10px;
  margin: 15px 0;
}

.input-group input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.input-group button {
  padding: 12px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.input-group button:hover:not(:disabled) {
  background: #0056b3;
}

.input-group button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.response-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 15px;
  margin: 15px 0;
}

.response-card pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.create-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.create-form h4 {
  margin-top: 0;
  color: #495057;
}

.create-form input {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.create-form button {
  width: 100%;
  padding: 12px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
}

.create-form button:hover:not(:disabled) {
  background: #218838;
}

.create-form button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.data-list h4 {
  color: #495057;
}

.empty-state {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 20px;
}

.data-item {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 15px;
  margin: 10px 0;
}

.data-item h5 {
  margin: 0 0 10px 0;
  color: #343a40;
}

.data-item p {
  margin: 5px 0;
  color: #495057;
}

.data-item small {
  color: #6c757d;
}

pre {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .header-content > div {
    text-align: center;
  }
  
  .main-nav {
    justify-content: center;
  }
  
  .nav-btn {
    flex: 1;
    min-width: 100px;
  }
  
  header h1 {
    font-size: 2em;
  }
}
</style>
