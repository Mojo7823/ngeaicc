<template>
  <div class="testing-tools-page">
    <div class="page-header">
      <h1>Testing Tools</h1>
      <p class="page-subtitle">Network testing and security assessment tools</p>
    </div>

    <div class="tools-container">
      <!-- Ping Test Tool -->
      <div class="tool-card">
        <div class="tool-header">
          <div class="tool-info">
            <h2>🏓 Ping Test</h2>
            <p>Test network connectivity and response times</p>
          </div>
          <div class="tool-status" :class="{ active: pingActive }">
            {{ pingActive ? 'Running' : 'Ready' }}
          </div>
        </div>
        
        <div class="tool-content">
          <div class="tool-form">
            <div class="form-group">
              <label for="ping-target" class="form-label">Target Host/IP</label>
              <input
                id="ping-target"
                v-model="pingTarget"
                type="text"
                class="form-input"
                placeholder="e.g., google.com or 8.8.8.8"
                :disabled="pingActive"
              />
            </div>
            
            <div class="form-group">
              <label for="ping-count" class="form-label">Ping Count</label>
              <input
                id="ping-count"
                v-model="pingCount"
                type="number"
                class="form-input"
                min="1"
                max="10"
                :disabled="pingActive"
              />
            </div>
            
            <div class="tool-actions">
              <button
                @click="startPing"
                :disabled="!pingTarget || pingActive"
                class="start-button"
              >
                {{ pingActive ? 'Running...' : 'Start Ping' }}
              </button>
              <button
                v-if="pingActive"
                @click="stopPing"
                class="stop-button"
              >
                Stop
              </button>
              <button
                @click="clearPingOutput"
                class="clear-button"
              >
                Clear
              </button>
            </div>
          </div>
          
          <div class="terminal-output">
            <div class="terminal-header">
              <span>Terminal Output</span>
              <span class="terminal-status" :class="{ connected: pingActive }">
                {{ pingActive ? '🟢 Connected' : '🔴 Disconnected' }}
              </span>
            </div>
            <div ref="pingTerminal" class="terminal-content">
              <div v-for="(line, index) in pingOutput" :key="index" class="terminal-line">
                {{ line }}
              </div>
              <div v-if="pingActive" class="cursor">_</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Nmap Tool -->
      <div class="tool-card">
        <div class="tool-header">
          <div class="tool-info">
            <h2>🗺️ Nmap Scanner</h2>
            <p>Network exploration and security auditing</p>
          </div>
          <div class="tool-status" :class="{ active: nmapActive }">
            {{ nmapActive ? 'Running' : 'Ready' }}
          </div>
        </div>
        
        <div class="tool-content">
          <div class="tool-form">
            <div class="form-group">
              <label for="nmap-target" class="form-label">Target Host/Network</label>
              <input
                id="nmap-target"
                v-model="nmapTarget"
                type="text"
                class="form-input"
                placeholder="e.g., 192.168.1.1 or 192.168.1.0/24"
                :disabled="nmapActive"
              />
            </div>
            
            <div class="form-group">
              <label for="nmap-scan-type" class="form-label">Scan Type</label>
              <select
                id="nmap-scan-type"
                v-model="nmapScanType"
                class="form-input"
                :disabled="nmapActive"
              >
                <option value="-sn">Ping Scan (-sn)</option>
                <option value="-sS">TCP SYN Scan (-sS)</option>
                <option value="-sT">TCP Connect Scan (-sT)</option>
                <option value="-sU">UDP Scan (-sU)</option>
                <option value="-sV">Version Detection (-sV)</option>
                <option value="-O">OS Detection (-O)</option>
                <option value="-A">Aggressive Scan (-A)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="nmap-ports" class="form-label">Ports (optional)</label>
              <input
                id="nmap-ports"
                v-model="nmapPorts"
                type="text"
                class="form-input"
                placeholder="e.g., 22,80,443 or 1-1000"
                :disabled="nmapActive"
              />
            </div>
            
            <div class="tool-actions">
              <button
                @click="startNmap"
                :disabled="!nmapTarget || nmapActive"
                class="start-button"
              >
                {{ nmapActive ? 'Scanning...' : 'Start Scan' }}
              </button>
              <button
                v-if="nmapActive"
                @click="stopNmap"
                class="stop-button"
              >
                Stop
              </button>
              <button
                @click="clearNmapOutput"
                class="clear-button"
              >
                Clear
              </button>
            </div>
          </div>
          
          <div class="terminal-output">
            <div class="terminal-header">
              <span>Nmap Output</span>
              <span class="terminal-status" :class="{ connected: nmapActive }">
                {{ nmapActive ? '🟢 Scanning' : '🔴 Idle' }}
              </span>
            </div>
            <div ref="nmapTerminal" class="terminal-content">
              <div v-for="(line, index) in nmapOutput" :key="index" class="terminal-line">
                {{ line }}
              </div>
              <div v-if="nmapActive" class="cursor">_</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

// Ping Test State
const pingTarget = ref('8.8.8.8')
const pingCount = ref(4)
const pingActive = ref(false)
const pingOutput = ref<string[]>([])
const pingTerminal = ref<HTMLElement>()

// Nmap State
const nmapTarget = ref('')
const nmapScanType = ref('-sn')
const nmapPorts = ref('')
const nmapActive = ref(false)
const nmapOutput = ref<string[]>([])
const nmapTerminal = ref<HTMLElement>()

// WebSocket connections (we'll simulate for now)
let pingWebSocket: WebSocket | null = null
let nmapWebSocket: WebSocket | null = null

const startPing = async () => {
  if (!pingTarget.value) return
  
  pingActive.value = true
  pingOutput.value.push(`Starting ping to ${pingTarget.value}...`)
  
  // Simulate ping output
  simulatePing()
}

const stopPing = () => {
  pingActive.value = false
  if (pingWebSocket) {
    pingWebSocket.close()
    pingWebSocket = null
  }
  pingOutput.value.push('Ping stopped by user')
}

const clearPingOutput = () => {
  pingOutput.value = []
}

const simulatePing = () => {
  let count = 0
  const maxCount = pingCount.value
  
  const interval = setInterval(() => {
    if (!pingActive.value || count >= maxCount) {
      clearInterval(interval)
      pingActive.value = false
      if (count >= maxCount) {
        pingOutput.value.push(`--- ${pingTarget.value} ping statistics ---`)
        pingOutput.value.push(`${maxCount} packets transmitted, ${maxCount} received, 0% packet loss`)
      }
      return
    }
    
    count++
    const time = (Math.random() * 50 + 10).toFixed(1)
    const ttl = Math.floor(Math.random() * 10) + 54
    pingOutput.value.push(`64 bytes from ${pingTarget.value}: icmp_seq=${count} ttl=${ttl} time=${time} ms`)
    
    // Auto-scroll to bottom
    nextTick(() => {
      if (pingTerminal.value) {
        pingTerminal.value.scrollTop = pingTerminal.value.scrollHeight
      }
    })
  }, 1000)
}

const startNmap = async () => {
  if (!nmapTarget.value) return
  
  nmapActive.value = true
  nmapOutput.value.push(`Starting Nmap scan on ${nmapTarget.value}...`)
  
  // Build nmap command
  let command = `nmap ${nmapScanType.value}`
  if (nmapPorts.value) {
    command += ` -p ${nmapPorts.value}`
  }
  command += ` ${nmapTarget.value}`
  
  nmapOutput.value.push(`Command: ${command}`)
  nmapOutput.value.push('')
  
  // Simulate nmap output
  simulateNmap()
}

const stopNmap = () => {
  nmapActive.value = false
  if (nmapWebSocket) {
    nmapWebSocket.close()
    nmapWebSocket = null
  }
  nmapOutput.value.push('Nmap scan stopped by user')
}

const clearNmapOutput = () => {
  nmapOutput.value = []
}

const simulateNmap = () => {
  const steps = [
    'Starting Nmap 7.80 ( https://nmap.org )',
    'Nmap scan report for ' + nmapTarget.value,
    'Host is up (0.001s latency).',
    ''
  ]
  
  let stepIndex = 0
  
  const interval = setInterval(() => {
    if (!nmapActive.value || stepIndex >= steps.length) {
      clearInterval(interval)
      
      if (stepIndex >= steps.length) {
        // Add sample port results based on scan type
        if (nmapScanType.value === '-sn') {
          nmapOutput.value.push('Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds')
        } else {
          nmapOutput.value.push('PORT     STATE SERVICE')
          nmapOutput.value.push('22/tcp   open  ssh')
          nmapOutput.value.push('80/tcp   open  http')
          nmapOutput.value.push('443/tcp  open  https')
          nmapOutput.value.push('')
          nmapOutput.value.push('Nmap done: 1 IP address (1 host up) scanned in 2.5 seconds')
        }
      }
      
      nmapActive.value = false
      return
    }
    
    nmapOutput.value.push(steps[stepIndex])
    stepIndex++
    
    // Auto-scroll to bottom
    nextTick(() => {
      if (nmapTerminal.value) {
        nmapTerminal.value.scrollTop = nmapTerminal.value.scrollHeight
      }
    })
  }, 800)
}
</script>

<style scoped>
.testing-tools-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
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

.tools-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 2rem;
}

.tool-card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.tool-header {
  padding: 1.5rem 2rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tool-info h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.tool-info p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.tool-status {
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  background-color: #e5e7eb;
  color: #6b7280;
}

.tool-status.active {
  background-color: #dcfce7;
  color: #166534;
}

.tool-content {
  padding: 2rem;
}

.tool-form {
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: end;
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

.form-input:disabled {
  background-color: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.tool-actions {
  display: flex;
  gap: 0.75rem;
  grid-column: 1 / -1;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.start-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.start-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.start-button:disabled {
  background-color: #6b7280;
  cursor: not-allowed;
}

.stop-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.stop-button:hover {
  background-color: #c82333;
}

.clear-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.clear-button:hover {
  background-color: #5a6268;
}

.terminal-output {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  overflow: hidden;
  background-color: #1e1e1e;
}

.terminal-header {
  padding: 0.75rem 1rem;
  background-color: #2d2d2d;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.terminal-status {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  background-color: #4b5563;
}

.terminal-status.connected {
  background-color: #059669;
}

.terminal-content {
  height: 300px;
  overflow-y: auto;
  padding: 1rem;
  color: #00ff00;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  background-color: #1e1e1e;
}

.terminal-line {
  margin-bottom: 0.25rem;
  white-space: pre-wrap;
  word-break: break-all;
}

.cursor {
  display: inline-block;
  background-color: #00ff00;
  width: 8px;
  height: 14px;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Custom scrollbar for terminal */
.terminal-content::-webkit-scrollbar {
  width: 8px;
}

.terminal-content::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.terminal-content::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 4px;
}

.terminal-content::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

@media (max-width: 768px) {
  .tools-container {
    grid-template-columns: 1fr;
  }
  
  .tool-form {
    grid-template-columns: 1fr;
  }
  
  .tool-actions {
    justify-content: center;
  }
  
  .tool-content {
    padding: 1.5rem;
  }
}
</style>