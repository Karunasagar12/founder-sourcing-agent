import React from 'react'
import { ExternalLink, Mail, Phone, MapPin, Briefcase, User } from 'lucide-react'
import clsx from 'clsx'

const CandidateCard = ({ candidate, onViewDetails }) => {
  const getTierColor = (tier) => {
    switch (tier) {
      case 'A':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'B':
        return 'bg-amber-100 text-amber-800 border-amber-200'
      case 'C':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getProfileTypeColor = (type) => {
    return type === 'business' 
      ? 'bg-blue-100 text-blue-800 border-blue-200'
      : 'bg-purple-100 text-purple-800 border-purple-200'
  }

  const truncateText = (text, maxLength = 150) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  return (
    <div className="card hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
            <User className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{candidate.name}</h3>
            <div className="flex items-center space-x-2 mt-1">
              <span className={clsx(
                'tier-badge border',
                getTierColor(candidate.tier)
              )}>
                Tier {candidate.tier}
              </span>
              <span className={clsx(
                'tier-badge border capitalize',
                getProfileTypeColor(candidate.profile_type)
              )}>
                {candidate.profile_type}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-700 text-sm leading-relaxed">
          {truncateText(candidate.summary)}
        </p>
      </div>

      {/* Key Highlights */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Key Highlights</h4>
        <div className="flex items-center space-x-4 text-sm text-gray-600">
          <div className="flex items-center space-x-1">
            <Briefcase className="h-4 w-4" />
            <span>{candidate.profile_type === 'business' ? 'Business Focus' : 'Technical Focus'}</span>
          </div>
          {candidate.data_source && (
            <div className="flex items-center space-x-1">
              <MapPin className="h-4 w-4" />
              <span>{candidate.data_source}</span>
            </div>
          )}
        </div>
      </div>

      {/* Contact Information */}
      {candidate.contacts && candidate.contacts.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Contact</h4>
          <div className="flex flex-wrap gap-2">
            {candidate.contacts.slice(0, 3).map((contact, index) => (
              <div key={index} className="flex items-center space-x-1 text-sm text-gray-600">
                {contact.includes('@') ? (
                  <Mail className="h-3 w-3" />
                ) : (
                  <Phone className="h-3 w-3" />
                )}
                <span className="truncate max-w-32">{contact}</span>
              </div>
            ))}
            {candidate.contacts.length > 3 && (
              <span className="text-xs text-gray-500">
                +{candidate.contacts.length - 3} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Source Links */}
      {candidate.source_links && candidate.source_links.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Sources</h4>
          <div className="flex flex-wrap gap-2">
            {candidate.source_links.slice(0, 2).map((link, index) => (
              <a
                key={index}
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-1 text-xs text-primary-600 hover:text-primary-700"
              >
                <ExternalLink className="h-3 w-3" />
                <span>Source {index + 1}</span>
              </a>
            ))}
            {candidate.source_links.length > 2 && (
              <span className="text-xs text-gray-500">
                +{candidate.source_links.length - 2} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-end">
        <button
          onClick={() => onViewDetails(candidate)}
          className="btn-secondary text-sm"
        >
          View Details
        </button>
      </div>
    </div>
  )
}

export default CandidateCard
