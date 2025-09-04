<template>
  <div class="ping-tool">
    <h2>🏓 Ping Test Tool</h2>
    <p>Real-time network connectivity testing with live output</p>
    
    <div class="ping-form">
      <h3>Configuration</h3>
      <div class="form-group">
        <label for="ipAddress">IP Address / Hostname:</label>
        <input 
          id="ipAddress"
          v-model="form.ipAddress" 
          type="text" 
          placeholder="e.g., 8.8.8.8 or google.com"
          :disabled="isRunning"
        />
      </div>
      
      <div class="form-group">
        <label for="packetSize">Packet Size (bytes):</label>
        <input 
          id="packetSize"
          v-model.number="form.packetSize" 
          type="number" 
          placeholder="32"
          min="1"
          max="65500"
          :disabled="isRunning"
        />
      </div>
      
      <div class="form-group">
        <label for="additionalCommand">Additional Arguments:</label>
        <input 
          id="additionalCommand"
          v-model="form.additionalCommand" 
          type="text" 
          placeholder="e.g., -c 4 -W 1000"
          :disabled="isRunning"
        />
      </div>
      
      <div class="button-group">
        <button 
          @click="startPing" 
          :disabled="!form.ipAddress || isRunning"
          class="start-btn"
        >
          {{ isRunning ? 'Running...' : 'Start Ping' }}
        </button>
        
        <button 
          @click="stopPing" 
          :disabled="!isRunning"
          class="stop-btn"
        >
          Stop Ping
        </button>
      </div>
    </div>
    
    <div class="terminal-container">
      <h3>Live Output</h3>
      <div ref="terminal" class="terminal">
        <div v-for="(line, index) in output" :key="index" class="terminal-line">
          {{ line }}
        </div>
        <div v-if="isRunning" class="cursor">_</div>
      </div>
      <div class="terminal-controls">
        <button @click="clearOutput" class="clear-btn">Clear Output</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import ApiService from '../services/api'

const form = ref({
  ipAddress: '',
  packetSize: 32,
  additionalCommand: ''
})

const output = ref<string[]>([])
const isRunning = ref(false)
const terminal = ref<HTMLElement>()
const sessionId = ref<string | null>(null)
const websocket = ref<WebSocket | null>(null)

const scrollToBottom = async () => {
  await nextTick()
  if (terminal.value) {
    terminal.value.scrollTop = terminal.value.scrollHeight
  }
}

const addOutput = (line: string) => {
  output.value.push(`[${new Date().toLocaleTimeString()}] ${line}`)
  scrollToBottom()
}

const connectWebSocket = (sessionId: string) => {
  const wsUrl = `ws://localhost:8000/api/v1/ping/ws/${sessionId}`
  websocket.value = new WebSocket(wsUrl)
  
  websocket.value.onopen = () => {
    addOutput('Connected to ping session')
  }
  
  websocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'output') {
      addOutput(data.content)
    } else if (data.type === 'error') {
      addOutput(`ERROR: ${data.content}`)
    } else if (data.type === 'finished') {
      addOutput('Ping completed')
      isRunning.value = false
    }
  }
  
  websocket.value.onclose = () => {
    addOutput('Connection closed')
    isRunning.value = false
  }
  
  websocket.value.onerror = (error) => {
    addOutput(`WebSocket error: ${error}`)
    isRunning.value = false
  }
}

const startPing = async () => {
  if (!form.value.ipAddress) return
  
  try {
    isRunning.value = true
    addOutput(`Starting ping to ${form.value.ipAddress}...`)
    
    const response = await ApiService.startPing(
      form.value.ipAddress,
      form.value.packetSize,
      form.value.additionalCommand
    )
    
    sessionId.value = response.sessionId
    connectWebSocket(response.sessionId)
    
  } catch (error: any) {
    addOutput(`Failed to start ping: ${error.message}`)
    isRunning.value = false
  }
}

const stopPing = async () => {
  if (!sessionId.value) return
  
  try {
    if (websocket.value) {
      websocket.value.close()
    }
    
    await ApiService.stopPing(sessionId.value)
    addOutput('Ping stopped by user')
    isRunning.value = false
    sessionId.value = null
    
  } catch (error: any) {
    addOutput(`Failed to stop ping: ${error.message}`)
  }
}

const clearOutput = () => {
  output.value = []
}
</script>

<style scoped>
.ping-tool {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

p {
  color: #7f8c8d;
  margin-bottom: 30px;
}

.ping-form {
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 30px;
}

.ping-form h3 {
  margin-top: 0;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.form-group input:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 25px;
}

.start-btn, .stop-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-btn {
  background-color: #27ae60;
  color: white;
}

.start-btn:hover:not(:disabled) {
  background-color: #229954;
}

.start-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.stop-btn {
  background-color: #e74c3c;
  color: white;
}

.stop-btn:hover:not(:disabled) {
  background-color: #c0392b;
}

.stop-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.terminal-container {
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  overflow: hidden;
}

.terminal-container h3 {
  margin: 0;
  padding: 15px 20px;
  background-color: #34495e;
  color: white;
  border-bottom: 1px solid #2c3e50;
}

.terminal {
  background-color: #2c3e50;
  color: #ecf0f1;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  height: 400px;
  overflow-y: auto;
  padding: 20px;
  line-height: 1.4;
}

.terminal-line {
  margin-bottom: 2px;
  word-wrap: break-word;
}

.cursor {
  display: inline-block;
  background-color: #ecf0f1;
  width: 8px;
  height: 14px;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.terminal-controls {
  padding: 10px 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #ecf0f1;
}

.clear-btn {
  padding: 6px 12px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.clear-btn:hover {
  background-color: #5a6268;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
  }
  
  .start-btn, .stop-btn {
    width: 100%;
  }
}
</style>