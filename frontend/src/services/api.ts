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

export interface TOEDescription {
  id: string
  toe_name: string
  toe_vendor: string
  evaluation_date: string
  laboratory_address: string
  laboratory_name: string
  toe_version: string
  common_criteria_version: string
  vendor_address: string
  evaluation_personnel: string
  protection_profile_module: string
  toe_description: string
  created_at: string
  updated_at?: string
}

export interface HelloWorldResponse {
  message: string
  status: string
  version: string
}

export interface EchoResponse {
  message: string
  echo: string
  timestamp: string
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
  async getHelloWorld(): Promise<HelloWorldResponse> {
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

  async createTestCase(testCase: Partial<TestCase>): Promise<TestCase> {
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

  async createDevice(device: Partial<Device>): Promise<Device> {
    try {
      const response = await this.client.post('/devices', device)
      return response.data
    } catch (error) {
      console.error('Error creating device:', error)
      throw error
    }
  }

  // TOE Description endpoints
  async getTOEDescription(): Promise<TOEDescription | null> {
    try {
      const response = await this.client.get('/toe-description')
      return response.data
    } catch (error) {
      console.error('Error fetching TOE description:', error)
      return null
    }
  }

  async createTOEDescription(toeDescription: Partial<TOEDescription>): Promise<TOEDescription> {
    try {
      const response = await this.client.post('/toe-description', toeDescription)
      return response.data
    } catch (error) {
      console.error('Error creating TOE description:', error)
      throw error
    }
  }

  async updateTOEDescription(id: string, toeDescription: Partial<TOEDescription>): Promise<TOEDescription> {
    try {
      const response = await this.client.put(`/toe-description/${id}`, toeDescription)
      return response.data
    } catch (error) {
      console.error('Error updating TOE description:', error)
      throw error
    }
  }

  async getTOEDescriptionById(id: string): Promise<TOEDescription> {
    try {
      const response = await this.client.get(`/toe-description/${id}`)
      return response.data
    } catch (error) {
      console.error('Error fetching TOE description by ID:', error)
      throw error
    }
  }

  // Ping tool endpoint
  async startPing(target: string, packetSize?: number, additionalArgs?: string): Promise<{ sessionId: string }> {
    try {
      const response = await this.client.post('/ping/start', {
        target,
        packet_size: packetSize,
        additional_args: additionalArgs
      })
      return response.data
    } catch (error) {
      console.error('Error starting ping:', error)
      throw error
    }
  }

  async stopPing(sessionId: string): Promise<void> {
    try {
      await this.client.post('/ping/stop', { session_id: sessionId })
    } catch (error) {
      console.error('Error stopping ping:', error)
      throw error
    }
  }
}

export default new ApiService()