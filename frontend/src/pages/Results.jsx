import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import CandidateCard from '../components/CandidateCard'
import CandidateModal from '../components/CandidateModal'
import FilterPanel from '../components/FilterPanel'
import { Download, ArrowLeft, Users, History, Clock } from 'lucide-react'
import { searchAPI } from '../services/api'

const Results = () => {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [candidates, setCandidates] = useState([])
  const [filteredCandidates, setFilteredCandidates] = useState([])
  const [selectedCandidate, setSelectedCandidate] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [searchHistory, setSearchHistory] = useState([])
  const [currentSearchId, setCurrentSearchId] = useState(null)
  const [filters, setFilters] = useState({
    tier: 'all',
    profileType: 'all'
  })
  const [sortBy, setSortBy] = useState('relevance')
  const [searchTerm, setSearchTerm] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadResults()
  }, [])

  useEffect(() => {
    applyFiltersAndSort()
  }, [candidates, filters, sortBy, searchTerm])

  const loadResults = async () => {
    setIsLoading(true)
    
    // Load current search results from localStorage
    const storedResults = localStorage.getItem('searchResults')
    if (storedResults) {
      try {
        const results = JSON.parse(storedResults)
        const currentCandidates = results.candidates || results || []
        setCandidates(currentCandidates)
        setCurrentSearchId(results.search_result_id || null)
      } catch (error) {
        console.error('Error parsing stored results:', error)
      }
    }

    // Load search history from database if authenticated
    if (isAuthenticated) {
      try {
        const historyResponse = await searchAPI.getSearchHistory()
        if (historyResponse.success) {
          setSearchHistory(historyResponse.history || [])
        }
      } catch (error) {
        console.error('Error loading search history:', error)
      }
    }

    setIsLoading(false)
  }

  const loadSearchFromHistory = async (searchId) => {
    try {
      const response = await searchAPI.getSearchResult(searchId)
      if (response.success) {
        setCandidates(response.search_result.candidates || [])
        setCurrentSearchId(searchId)
        
        // Update localStorage with the loaded search
        localStorage.setItem('searchResults', JSON.stringify(response.search_result))
        localStorage.setItem('searchTimestamp', response.search_result.created_at)
      }
    } catch (error) {
      console.error('Error loading search from history:', error)
    }
  }

  const applyFiltersAndSort = () => {
    let filtered = [...candidates]

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(candidate =>
        candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        candidate.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
        candidate.match_justification.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Apply tier filter
    if (filters.tier !== 'all') {
      filtered = filtered.filter(candidate => candidate.tier === filters.tier)
    }

    // Apply profile type filter
    if (filters.profileType !== 'all') {
      filtered = filtered.filter(candidate => candidate.profile_type === filters.profileType)
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name)
        case 'tier':
          const tierOrder = { 'A': 1, 'B': 2, 'C': 3 }
          return tierOrder[a.tier] - tierOrder[b.tier]
        case 'profile_type':
          return a.profile_type.localeCompare(b.profile_type)
        case 'relevance':
        default:
          // Keep original order (already sorted by relevance from backend)
          return 0
      }
    })

    setFilteredCandidates(filtered)
  }

  const handleViewDetails = (candidate) => {
    setSelectedCandidate(candidate)
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setSelectedCandidate(null)
  }

  const handleExport = (candidate) => {
    // Create CSV content for single candidate
    const csvContent = [
      ['Name', 'Profile Type', 'Tier', 'Summary', 'Match Justification', 'Contacts', 'Source Links'],
      [
        candidate.name,
        candidate.profile_type,
        candidate.tier,
        `"${candidate.summary.replace(/"/g, '""')}"`,
        `"${candidate.match_justification.replace(/"/g, '""')}"`,
        `"${candidate.contacts?.join('; ') || ''}"`,
        `"${candidate.source_links?.join('; ') || ''}"`
      ]
    ].map(row => row.join(',')).join('\n')

    // Download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `candidate_${candidate.name.replace(/\s+/g, '_')}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  const handleExportAll = () => {
    // Create CSV content for all filtered candidates
    const csvContent = [
      ['Name', 'Profile Type', 'Tier', 'Summary', 'Match Justification', 'Contacts', 'Source Links'],
      ...filteredCandidates.map(candidate => [
        candidate.name,
        candidate.profile_type,
        candidate.tier,
        `"${candidate.summary.replace(/"/g, '""')}"`,
        `"${candidate.match_justification.replace(/"/g, '""')}"`,
        `"${candidate.contacts?.join('; ') || ''}"`,
        `"${candidate.source_links?.join('; ') || ''}"`
      ])
    ].map(row => row.join(',')).join('\n')

    // Download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `founder_candidates_${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  const getSearchTimestamp = () => {
    const timestamp = localStorage.getItem('searchTimestamp')
    if (timestamp) {
      return new Date(timestamp).toLocaleString()
    }
    return 'Unknown'
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/')}
            className="btn-secondary flex items-center space-x-2"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>New Search</span>
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Search Results</h1>
            <p className="text-sm text-gray-600">
              Search performed at {getSearchTimestamp()}
            </p>
          </div>
        </div>
        <button
          onClick={handleExportAll}
          className="btn-primary flex items-center space-x-2"
        >
          <Download className="h-4 w-4" />
          <span>Export All</span>
        </button>
      </div>

      {/* Search History Section */}
      {isAuthenticated && searchHistory.length > 0 && (
        <div className="mb-6">
          <div className="card">
            <div className="flex items-center space-x-2 mb-4">
              <History className="h-5 w-5 text-primary-600" />
              <h3 className="text-lg font-semibold text-gray-900">Search History</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchHistory.slice(0, 6).map((search) => (
                <div
                  key={search.id}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    currentSearchId === search.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
                  }`}
                  onClick={() => loadSearchFromHistory(search.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 truncate">
                        {search.search_query || 'Search'}
                      </h4>
                      <p className="text-sm text-gray-600">
                        {search.industry && `${search.industry} • `}
                        {search.total_candidates} candidates
                      </p>
                      <div className="flex items-center space-x-1 mt-2">
                        <Clock className="h-3 w-3 text-gray-400" />
                        <span className="text-xs text-gray-500">
                          {new Date(search.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      {search.tier_distribution && (
                        <div className="flex space-x-1">
                          {Object.entries(search.tier_distribution).map(([tier, count]) => (
                            <span
                              key={tier}
                              className={`px-2 py-1 text-xs rounded-full ${
                                tier === 'A' ? 'bg-green-100 text-green-800' :
                                tier === 'B' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {tier}: {count}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filter Panel */}
      <FilterPanel
        filters={filters}
        onFilterChange={setFilters}
        sortBy={sortBy}
        onSortChange={setSortBy}
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        totalResults={filteredCandidates.length}
      />

      {/* Results */}
      {isLoading ? (
        <div className="text-center py-12">
          <p>Loading search results...</p>
        </div>
      ) : filteredCandidates.length === 0 ? (
        <div className="text-center py-12">
          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No candidates found</h3>
          <p className="text-gray-600">
            Try adjusting your filters or search terms to find more results.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredCandidates.map((candidate, index) => (
            <CandidateCard
              key={`${candidate.name}-${index}`}
              candidate={candidate}
              onViewDetails={handleViewDetails}
            />
          ))}
        </div>
      )}

      {/* Candidate Modal */}
      <CandidateModal
        candidate={selectedCandidate}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onExport={handleExport}
      />
    </div>
  )
}

export default Results
