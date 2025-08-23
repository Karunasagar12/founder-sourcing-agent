import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import SearchForm from '../components/SearchForm'
import { searchAPI } from '../services/api'
import { AlertCircle, CheckCircle } from 'lucide-react'

const Search = () => {
  const navigate = useNavigate()
  const [healthStatus, setHealthStatus] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    checkHealth()
  }, [])

  const checkHealth = async () => {
    try {
      const status = await searchAPI.health()
      setHealthStatus(status)
    } catch (error) {
      setHealthStatus({ status: 'error', message: 'Backend connection failed' })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSearchComplete = (results) => {
    // Store results in localStorage for the results page
    localStorage.setItem('searchResults', JSON.stringify(results))
    localStorage.setItem('searchTimestamp', new Date().toISOString())
    
    // Navigate to results page
    navigate('/results')
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Checking system status...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Health Status */}
      {healthStatus && (
        <div className="mb-6">
          {healthStatus.status === 'healthy' ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-3">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div>
                <h3 className="text-sm font-medium text-green-800">System Status: Healthy</h3>
                <p className="text-sm text-green-700">
                  All services are operational and ready for search
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <div>
                <h3 className="text-sm font-medium text-red-800">System Status: Warning</h3>
                <p className="text-sm text-red-700">
                  {healthStatus.message || 'Some services may not be available'}
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Search Form */}
      <SearchForm onSearchComplete={handleSearchComplete} />

      {/* Instructions */}
      <div className="mt-8 max-w-4xl mx-auto">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">How to Use</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">1. Define Your Criteria</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Set experience requirements</li>
                <li>• Choose industry focus</li>
                <li>• Select founder signals</li>
                <li>• Pick technical skills</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">2. Review Results</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• View tier-ranked candidates</li>
                <li>• Filter by profile type</li>
                <li>• Access contact information</li>
                <li>• Export individual profiles</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Search
