import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      sessionStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

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
  },

  // Get search history
  getSearchHistory: async () => {
    try {
      const response = await api.get('/search-history')
      return response.data
    } catch (error) {
      console.error('Get search history error:', error)
      throw error
    }
  },

  // Get specific search result
  getSearchResult: async (searchId) => {
    try {
      const response = await api.get(`/search-history/${searchId}`)
      return response.data
    } catch (error) {
      console.error('Get search result error:', error)
      throw error
    }
  },

  // Delete search result
  deleteSearchResult: async (searchId) => {
    try {
      const response = await api.delete(`/search-history/${searchId}`)
      return response.data
    } catch (error) {
      console.error('Delete search result error:', error)
      throw error
    }
  },

  // Get search statistics
  getSearchStatistics: async () => {
    try {
      const response = await api.get('/search-statistics')
      return response.data
    } catch (error) {
      console.error('Get search statistics error:', error)
      throw error
    }
  }
}

export default api
