import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import CandidateCard from '../components/CandidateCard'
import CandidateModal from '../components/CandidateModal'
import FilterPanel from '../components/FilterPanel'
import { Download, ArrowLeft, Users } from 'lucide-react'

const Results = () => {
  const navigate = useNavigate()
  const [candidates, setCandidates] = useState([])
  const [filteredCandidates, setFilteredCandidates] = useState([])
  const [selectedCandidate, setSelectedCandidate] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [filters, setFilters] = useState({
    tier: 'all',
    profileType: 'all'
  })
  const [sortBy, setSortBy] = useState('relevance')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadResults()
  }, [])

  useEffect(() => {
    applyFiltersAndSort()
  }, [candidates, filters, sortBy, searchTerm])

  const loadResults = () => {
    const storedResults = localStorage.getItem('searchResults')
    if (storedResults) {
      try {
        const results = JSON.parse(storedResults)
        setCandidates(results.candidates || results || [])
      } catch (error) {
        console.error('Error parsing stored results:', error)
        navigate('/')
      }
    } else {
      navigate('/')
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
      {filteredCandidates.length === 0 ? (
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
