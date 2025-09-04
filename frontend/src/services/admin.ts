import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

class AdminService {
  async getStats() {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/stats`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch admin stats:', error)
      throw error
    }
  }

  async getDatabaseTables() {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/database/tables`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch database tables:', error)
      throw error
    }
  }

  async getDatabaseHealth() {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/database/health`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch database health:', error)
      throw error
    }
  }

  async getTableData(tableName: string) {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/database/data/${tableName}`)
      return response.data
    } catch (error) {
      console.error(`Failed to fetch data for table ${tableName}:`, error)
      throw error
    }
  }

  async deleteTableItem(tableName: string, itemId: string) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/admin/database/data/${tableName}/${itemId}`)
      return response.data
    } catch (error) {
      console.error(`Failed to delete item ${itemId} from table ${tableName}:`, error)
      throw error
    }
  }

  async executeSqlQuery(query: string) {
    try {
      const response = await axios.post(`${API_BASE_URL}/admin/database/execute-sql`, { query })
      return response.data
    } catch (error) {
      console.error('Failed to execute SQL query:', error)
      throw error
    }
  }

  async getApiEndpoints() {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/api/endpoints`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch API endpoints:', error)
      throw error
    }
  }

  async getSystemInfo() {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/system/info`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch system info:', error)
      throw error
    }
  }
}

export default new AdminService()