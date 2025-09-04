import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Hello World endpoint
  async getHelloWorld() {
    try {
      const response = await this.client.get('/hello')
      return response.data
    } catch (error) {
      console.error('Error fetching hello world:', error)
      throw error
    }
  }

  // Echo message endpoint
  async sendMessage(message, userId = null) {
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
  async getTestCases() {
    try {
      const response = await this.client.get('/test-cases')
      return response.data
    } catch (error) {
      console.error('Error fetching test cases:', error)
      throw error
    }
  }

  async createTestCase(testCase) {
    try {
      const response = await this.client.post('/test-cases', testCase)
      return response.data
    } catch (error) {
      console.error('Error creating test case:', error)
      throw error
    }
  }

  // Devices endpoints
  async getDevices() {
    try {
      const response = await this.client.get('/devices')
      return response.data
    } catch (error) {
      console.error('Error fetching devices:', error)
      throw error
    }
  }

  async createDevice(device) {
    try {
      const response = await this.client.post('/devices', device)
      return response.data
    } catch (error) {
      console.error('Error creating device:', error)
      throw error
    }
  }
}

export default new ApiService()
