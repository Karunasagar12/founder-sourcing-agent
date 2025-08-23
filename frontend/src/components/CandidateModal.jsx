import React from 'react'
import { X, ExternalLink, Mail, Phone, MapPin, Briefcase, User, Download } from 'lucide-react'
import clsx from 'clsx'

const CandidateModal = ({ candidate, isOpen, onClose, onExport }) => {
  if (!isOpen || !candidate) return null

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

  const handleExport = () => {
    if (onExport) {
      onExport(candidate)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <User className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">{candidate.name}</h2>
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
          <div className="flex items-center space-x-2">
            <button
              onClick={handleExport}
              className="btn-secondary flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Export</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Summary */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Summary</h3>
            <p className="text-gray-700 leading-relaxed">{candidate.summary}</p>
          </div>

          {/* Match Justification */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Match Justification</h3>
            <p className="text-gray-700 leading-relaxed">{candidate.match_justification}</p>
          </div>

          {/* Profile Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Profile Type */}
            <div>
              <h3 className="text-sm font-medium text-gray-900 mb-2">Profile Type</h3>
              <div className="flex items-center space-x-2">
                <Briefcase className="h-4 w-4 text-gray-500" />
                <span className="text-gray-700 capitalize">{candidate.profile_type}</span>
              </div>
            </div>

            {/* Data Source */}
            {candidate.data_source && (
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-2">Data Source</h3>
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-gray-500" />
                  <span className="text-gray-700">{candidate.data_source}</span>
                </div>
              </div>
            )}
          </div>

          {/* Contact Information */}
          {candidate.contacts && candidate.contacts.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Contact Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {candidate.contacts.map((contact, index) => (
                  <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                    {contact.includes('@') ? (
                      <Mail className="h-5 w-5 text-gray-500" />
                    ) : (
                      <Phone className="h-5 w-5 text-gray-500" />
                    )}
                    <span className="text-gray-700">{contact}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Source Links */}
          {candidate.source_links && candidate.source_links.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Source Links</h3>
              <div className="space-y-2">
                {candidate.source_links.map((link, index) => (
                  <a
                    key={index}
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 p-2 rounded-lg hover:bg-primary-50"
                  >
                    <ExternalLink className="h-4 w-4" />
                    <span className="truncate">{link}</span>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Additional Data */}
          {candidate.additional_data && Object.keys(candidate.additional_data).length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Additional Information</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {JSON.stringify(candidate.additional_data, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="btn-primary"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default CandidateModal
