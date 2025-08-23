import React from 'react'
import { Filter, SortAsc, SortDesc, X } from 'lucide-react'

const FilterPanel = ({ 
  filters, 
  onFilterChange, 
  sortBy, 
  onSortChange, 
  searchTerm, 
  onSearchChange,
  totalResults 
}) => {
  const tierOptions = [
    { value: 'all', label: 'All Tiers' },
    { value: 'A', label: 'Tier A' },
    { value: 'B', label: 'Tier B' },
    { value: 'C', label: 'Tier C' }
  ]

  const profileTypeOptions = [
    { value: 'all', label: 'All Types' },
    { value: 'business', label: 'Business' },
    { value: 'technical', label: 'Technical' }
  ]

  const sortOptions = [
    { value: 'relevance', label: 'Relevance' },
    { value: 'name', label: 'Name' },
    { value: 'tier', label: 'Tier' },
    { value: 'profile_type', label: 'Profile Type' }
  ]

  const clearFilters = () => {
    onFilterChange({
      tier: 'all',
      profileType: 'all'
    })
    onSearchChange('')
  }

  const hasActiveFilters = filters.tier !== 'all' || filters.profileType !== 'all' || searchTerm

  return (
    <div className="card mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Filter className="h-5 w-5 text-gray-500" />
          <h3 className="text-lg font-semibold text-gray-900">Filters & Search</h3>
        </div>
        <div className="text-sm text-gray-600">
          {totalResults} result{totalResults !== 1 ? 's' : ''}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search candidates..."
            className="input-field"
          />
        </div>

        {/* Tier Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tier
          </label>
          <select
            value={filters.tier}
            onChange={(e) => onFilterChange({ ...filters, tier: e.target.value })}
            className="input-field"
          >
            {tierOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Profile Type Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Profile Type
          </label>
          <select
            value={filters.profileType}
            onChange={(e) => onFilterChange({ ...filters, profileType: e.target.value })}
            className="input-field"
          >
            {profileTypeOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Sort */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sort By
          </label>
          <select
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value)}
            className="input-field"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700">Active Filters:</span>
              {filters.tier !== 'all' && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  Tier {filters.tier}
                  <button
                    onClick={() => onFilterChange({ ...filters, tier: 'all' })}
                    className="ml-1 text-primary-600 hover:text-primary-800"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {filters.profileType !== 'all' && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  {filters.profileType}
                  <button
                    onClick={() => onFilterChange({ ...filters, profileType: 'all' })}
                    className="ml-1 text-primary-600 hover:text-primary-800"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {searchTerm && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  "{searchTerm}"
                  <button
                    onClick={() => onSearchChange('')}
                    className="ml-1 text-primary-600 hover:text-primary-800"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
            </div>
            <button
              onClick={clearFilters}
              className="text-sm text-gray-600 hover:text-gray-800 underline"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default FilterPanel
