import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const searchAPI = {
  // Search for founders
  search: async (criteria) => {
    try {
      const response = await api.post('/search', criteria)
      return response.data
    } catch (error) {
      console.error('Search API error:', error)
      throw error
    }
  },

  // Get health status
  health: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      console.error('Health check error:', error)
      throw error
    }
  },

  // Export candidates
  exportCandidates: async (candidates) => {
    try {
      const response = await api.post('/export', { candidates })
      return response.data
    } catch (error) {
      console.error('Export error:', error)
      throw error
    }
  }
}

export default api
