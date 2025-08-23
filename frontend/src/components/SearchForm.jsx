import React, { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'
import { searchAPI } from '../services/api'

const SearchForm = ({ onSearchComplete }) => {
  const [formData, setFormData] = useState({
    experience_depth: '',
    industry: '',
    founder_signals: [],
    technical_signals: [],
    max_results: 10
  })
  
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // Predefined options
  const industries = [
    'Technology',
    'Healthcare',
    'Finance',
    'Education',
    'E-commerce',
    'SaaS',
    'AI/ML',
    'Biotech',
    'Clean Energy',
    'Other'
  ]

  const founderSignals = [
    'Previous startup experience',
    'Leadership roles',
    'Industry expertise',
    'Network connections',
    'Technical background',
    'Business development',
    'Product management',
    'Sales experience'
  ]

  const technicalSignals = [
    'Software engineering',
    'Data science',
    'Machine learning',
    'Full-stack development',
    'DevOps',
    'Mobile development',
    'Cloud architecture',
    'Cybersecurity'
  ]

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleCheckboxChange = (field, value, checked) => {
    setFormData(prev => ({
      ...prev,
      [field]: checked 
        ? [...prev[field], value]
        : prev[field].filter(item => item !== value)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      // Convert experience_depth to number if provided
      const searchCriteria = {
        ...formData,
        experience_depth: formData.experience_depth ? parseInt(formData.experience_depth) : null
      }

      const result = await searchAPI.search(searchCriteria)
      onSearchComplete(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during search')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Search for Founders
        </h2>
        <p className="text-gray-600">
          Define your search criteria to find the best founder candidates
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Experience Depth */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Years of Experience
          </label>
          <input
            type="number"
            min="0"
            max="50"
            value={formData.experience_depth}
            onChange={(e) => handleInputChange('experience_depth', e.target.value)}
            className="input-field"
            placeholder="e.g., 5"
          />
        </div>

        {/* Industry */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Industry Focus
          </label>
          <select
            value={formData.industry}
            onChange={(e) => handleInputChange('industry', e.target.value)}
            className="input-field"
          >
            <option value="">Select an industry</option>
            {industries.map(industry => (
              <option key={industry} value={industry}>
                {industry}
              </option>
            ))}
          </select>
        </div>

        {/* Max Results */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Maximum Results
          </label>
          <input
            type="number"
            min="1"
            max="50"
            value={formData.max_results}
            onChange={(e) => handleInputChange('max_results', parseInt(e.target.value))}
            className="input-field"
          />
        </div>

        {/* Founder Signals */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Founder Signals
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {founderSignals.map(signal => (
              <label key={signal} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.founder_signals.includes(signal)}
                  onChange={(e) => handleCheckboxChange('founder_signals', signal, e.target.checked)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{signal}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Technical Signals */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Technical Signals
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {technicalSignals.map(signal => (
              <label key={signal} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.technical_signals.includes(signal)}
                  onChange={(e) => handleCheckboxChange('technical_signals', signal, e.target.checked)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{signal}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Searching...</span>
              </>
            ) : (
              <>
                <Search className="h-4 w-4" />
                <span>Search Founders</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

export default SearchForm
