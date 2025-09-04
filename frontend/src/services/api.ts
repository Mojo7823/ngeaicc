import axios, { type AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export interface TestCase {
  id: string
  name: string
  description: string
  category: string
  created_at: string
}

export interface Device {
  id: string
  name: string
  manufacturer: string
  model: string
  description: string
  created_at: string
}

export interface HelloResponse {
  message: string
  timestamp: string
}

export interface EchoResponse {
  message: string
  user_id: string | null
  received_at: string
}

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Hello World endpoint
  async getHelloWorld(): Promise<HelloResponse> {
    try {
      const response = await this.client.get('/hello')
      return response.data
    } catch (error) {
      console.error('Error fetching hello world:', error)
      throw error
    }
  }

  // Echo message endpoint
  async sendMessage(message: string, userId: string | null = null): Promise<EchoResponse> {
    try {
      const response = await this.client.post('/echo', {
        message,
        user_id: userId
      })
      return response.data
    } catch (error) {
      console.error('Error sending message:', error)
      throw error
    }
  }

  // Test Cases endpoints
  async getTestCases(): Promise<TestCase[]> {
    try {
      const response = await this.client.get('/test-cases')
      return response.data
    } catch (error) {
      console.error('Error fetching test cases:', error)
      throw error
    }
  }

  async createTestCase(testCase: Omit<TestCase, 'id' | 'created_at'>): Promise<TestCase> {
    try {
      const response = await this.client.post('/test-cases', testCase)
      return response.data
    } catch (error) {
      console.error('Error creating test case:', error)
      throw error
    }
  }

  // Devices endpoints
  async getDevices(): Promise<Device[]> {
    try {
      const response = await this.client.get('/devices')
      return response.data
    } catch (error) {
      console.error('Error fetching devices:', error)
      throw error
    }
  }

  async createDevice(device: Omit<Device, 'id' | 'created_at'>): Promise<Device> {
    try {
      const response = await this.client.post('/devices', device)
      return response.data
    } catch (error) {
      console.error('Error creating device:', error)
      throw error
    }
  }

  // Ping tool endpoints
  async startPing(ipAddress: string, packetSize?: number, additionalCommand?: string): Promise<{ session_id: string }> {
    try {
      const response = await this.client.post('/tools/ping/start', {
        ip_address: ipAddress,
        packet_size: packetSize || 64,
        additional_command: additionalCommand || ''
      })
      return response.data
    } catch (error) {
      console.error('Error starting ping:', error)
      throw error
    }
  }

  async stopPing(sessionId: string): Promise<{ status: string }> {
    try {
      const response = await this.client.post('/tools/ping/stop', {
        session_id: sessionId
      })
      return response.data
    } catch (error) {
      console.error('Error stopping ping:', error)
      throw error
    }
  }
}

export default new ApiService()