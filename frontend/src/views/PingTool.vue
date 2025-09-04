<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import ApiService from '../services/api'

// Form data
const ipAddress = ref('8.8.8.8')
const packetSize = ref(64)
const additionalCommand = ref('')

// State
const isRunning = ref(false)
const sessionId = ref<string | null>(null)
const output = ref<string[]>([])
const isLoading = ref(false)

// WebSocket for real-time output (we'll simulate this for now)
let simulationInterval: number | null = null

const startPing = async () => {
  if (!ipAddress.value.trim()) {
    alert('Please enter an IP address')
    return
  }

  isLoading.value = true
  
  try {
    // Start the ping process
    const response = await ApiService.startPing(
      ipAddress.value,
      packetSize.value,
      additionalCommand.value
    )
    
    sessionId.value = response.session_id
    isRunning.value = true
    output.value = []
    
    // Add initial message
    output.value.push(`Starting ping to ${ipAddress.value}...`)
    output.value.push(`Packet size: ${packetSize.value} bytes`)
    if (additionalCommand.value) {
      output.value.push(`Additional command: ${additionalCommand.value}`)
    }
    output.value.push('---')
    
    // Simulate real-time ping output
    startSimulation()
    
  } catch (error: unknown) {
    console.error('Error starting ping:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    output.value.push(`Error: ${errorMessage}`)
  } finally {
    isLoading.value = false
  }
}

const stopPing = async () => {
  if (!sessionId.value) return
  
  isLoading.value = true
  
  try {
    await ApiService.stopPing(sessionId.value)
    
    if (simulationInterval) {
      clearInterval(simulationInterval)
      simulationInterval = null
    }
    
    isRunning.value = false
    output.value.push('---')
    output.value.push('Ping stopped by user')
    
  } catch (error: unknown) {
    console.error('Error stopping ping:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    output.value.push(`Error stopping ping: ${errorMessage}`)
  } finally {
    isLoading.value = false
  }
}

const startSimulation = () => {
  let packetNumber = 1
  
  simulationInterval = window.setInterval(() => {
    if (!isRunning.value) return
    
    // Simulate ping responses
    const time = (Math.random() * 50 + 10).toFixed(1)
    const ttl = Math.floor(Math.random() * 10) + 50
    
    if (Math.random() > 0.1) { // 90% success rate
      output.value.push(
        `64 bytes from ${ipAddress.value}: icmp_seq=${packetNumber} ttl=${ttl} time=${time} ms`
      )
    } else {
      output.value.push(`Request timeout for icmp_seq ${packetNumber}`)
    }
    
    packetNumber++
    
    // Auto-scroll to bottom
    scrollToBottom()
  }, 1000)
}

const scrollToBottom = () => {
  setTimeout(() => {
    const terminal = document.querySelector('.terminal-output')
    if (terminal) {
      terminal.scrollTop = terminal.scrollHeight
    }
  }, 10)
}

const clearOutput = () => {
  output.value = []
}

// Cleanup on component unmount
onUnmounted(() => {
  if (simulationInterval) {
    clearInterval(simulationInterval)
  }
  if (isRunning.value && sessionId.value) {
    stopPing()
  }
})
</script>

<template>
  <div class="ping-tool">
    <div class="tool-header">
      <h1>🏓 Ping Test Tool</h1>
      <p>Test network connectivity and latency to any host</p>
    </div>

    <div class="tool-content">
      <div class="controls-section">
        <h2>Configuration</h2>
        
        <div class="form-group">
          <label for="ip-address">IP Address / Hostname</label>
          <input
            id="ip-address"
            v-model="ipAddress"
            type="text"
            placeholder="e.g., 8.8.8.8 or google.com"
            :disabled="isRunning"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="packet-size">Packet Size (bytes)</label>
          <input
            id="packet-size"
            v-model.number="packetSize"
            type="number"
            min="32"
            max="65507"
            :disabled="isRunning"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="additional-command">Additional Command Parameters</label>
          <input
            id="additional-command"
            v-model="additionalCommand"
            type="text"
            placeholder="e.g., -c 10 (for 10 pings)"
            :disabled="isRunning"
            class="form-control"
          />
          <small class="form-help">Optional: Add additional ping command parameters</small>
        </div>

        <div class="button-group">
          <button
            @click="startPing"
            :disabled="isRunning || isLoading"
            class="btn btn-start"
          >
            {{ isLoading && !isRunning ? 'Starting...' : 'Start Ping' }}
          </button>
          
          <button
            @click="stopPing"
            :disabled="!isRunning || isLoading"
            class="btn btn-stop"
          >
            {{ isLoading && isRunning ? 'Stopping...' : 'Stop Ping' }}
          </button>
          
          <button
            @click="clearOutput"
            :disabled="isRunning"
            class="btn btn-clear"
          >
            Clear Output
          </button>
        </div>

        <div v-if="isRunning" class="status-indicator">
          <div class="status-dot"></div>
          <span>Ping is running...</span>
        </div>
      </div>

      <div class="output-section">
        <div class="output-header">
          <h2>Live Terminal Output</h2>
          <div class="terminal-controls">
            <span class="terminal-control red"></span>
            <span class="terminal-control yellow"></span>
            <span class="terminal-control green"></span>
          </div>
        </div>
        
        <div class="terminal-container">
          <div class="terminal-output" ref="terminalOutput">
            <div v-if="output.length === 0" class="terminal-placeholder">
              Ready to start ping test. Configure settings above and click "Start Ping".
            </div>
            <div
              v-for="(line, index) in output"
              :key="index"
              class="terminal-line"
            >
              {{ line }}
            </div>
            <div v-if="isRunning" class="terminal-cursor">|</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ping-tool {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.tool-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.tool-header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5em;
  font-weight: 700;
}

.tool-header p {
  margin: 0;
  font-size: 1.1em;
  opacity: 0.9;
}

.tool-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
}

.controls-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.controls-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.5em;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
}

.form-control:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.form-help {
  display: block;
  margin-top: 5px;
  color: #6c757d;
  font-size: 0.85em;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 100px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-start {
  background: #28a745;
  color: white;
}

.btn-start:hover:not(:disabled) {
  background: #218838;
  transform: translateY(-2px);
}

.btn-stop {
  background: #dc3545;
  color: white;
}

.btn-stop:hover:not(:disabled) {
  background: #c82333;
  transform: translateY(-2px);
}

.btn-clear {
  background: #6c757d;
  color: white;
}

.btn-clear:hover:not(:disabled) {
  background: #5a6268;
  transform: translateY(-2px);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
  color: #155724;
}

.status-dot {
  width: 10px;
  height: 10px;
  background: #28a745;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.output-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.output-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.3em;
}

.terminal-controls {
  display: flex;
  gap: 8px;
}

.terminal-control {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.terminal-control.red {
  background: #ff5f56;
}

.terminal-control.yellow {
  background: #ffbd2e;
}

.terminal-control.green {
  background: #27ca3f;
}

.terminal-container {
  height: 500px;
  overflow: hidden;
}

.terminal-output {
  height: 100%;
  padding: 20px;
  background: #1a1a1a;
  color: #00ff00;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.4;
  overflow-y: auto;
}

.terminal-placeholder {
  color: #666;
  font-style: italic;
}

.terminal-line {
  margin-bottom: 2px;
  word-break: break-all;
}

.terminal-cursor {
  display: inline-block;
  animation: blink 1s infinite;
  color: #00ff00;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Responsive */
@media (max-width: 768px) {
  .tool-content {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .btn {
    flex: none;
  }
  
  .tool-header h1 {
    font-size: 2em;
  }
  
  .terminal-container {
    height: 300px;
  }
}
</style>