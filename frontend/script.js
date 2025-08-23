// Global variables
let currentCandidates = [];
let filteredCandidates = [];
let lastSearchResponse = null;

// API Configuration - Always use localhost for development
const API_BASE_URL = 'http://localhost:8000';

console.log('🚀 Frontend initialized, API URL:', API_BASE_URL);

// DOM Elements
const searchForm = document.getElementById('search-form');
const searchBtn = document.getElementById('search-btn');
const clearBtn = document.getElementById('clear-btn');
const loadingState = document.getElementById('loading-state');
const emptyState = document.getElementById('empty-state');
const candidatesGrid = document.getElementById('candidates-grid');
const searchSummary = document.getElementById('search-summary');
const filterPanel = document.getElementById('filter-panel');
const candidateModal = document.getElementById('candidate-modal');
const modalClose = document.getElementById('modal-close');
const exportBtn = document.getElementById('export-btn');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 DOM loaded, initializing app...');
    initializeApp();
    checkBackendHealth();
});

// Initialize application
function initializeApp() {
    // Set up tab switching
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
        });
    });

    // Set up form handlers
    searchForm.addEventListener('submit', handleSearch);
    clearBtn.addEventListener('click', clearForm);
    exportBtn.addEventListener('click', handleExport);

    // Set up modal
    modalClose.addEventListener('click', closeModal);
    candidateModal.addEventListener('click', (e) => {
        if (e.target === candidateModal) closeModal();
    });

    // Set up filters
    document.getElementById('tier-filter').addEventListener('change', applyFilters);
    document.getElementById('type-filter').addEventListener('change', applyFilters);
    document.getElementById('search-filter').addEventListener('input', applyFilters);

    // Set default values
    document.getElementById('maxResults').value = '10';

    console.log('✅ App initialized successfully');
}

// Check backend health
async function checkBackendHealth() {
    console.log('🔍 Checking backend health at:', `${API_BASE_URL}/health`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            // Add timeout
            signal: AbortSignal.timeout(10000)
        });
        
        console.log('📊 Health check response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend health check successful:', data);
            updateSystemStatus(true, data);
            
            // Test connection endpoint too
            testConnection();
        } else {
            console.error('❌ Health check failed with status:', response.status);
            const errorText = await response.text();
            console.error('❌ Error response:', errorText);
            throw new Error(`Health check failed: ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Backend health check failed:', error);
        console.error('❌ Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        updateSystemStatus(false, { error: error.message });
        
        // Show user-friendly error
        showConnectionError(error.message);
    }
}

// Test connection with simple endpoint
async function testConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/test-connection`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Connection test successful:', data);
        }
    } catch (error) {
        console.log('⚠️ Connection test failed (this is okay):', error.message);
    }
}

// Show connection error to user
function showConnectionError(errorMessage) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 16px;
        border-radius: 8px;
        max-width: 500px;
        z-index: 1000;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    `;
    
    errorDiv.innerHTML = `
        <h4 style="margin: 0 0 8px 0; font-weight: 600;">⚠️ Backend Connection Failed</h4>
        <p style="margin: 0 0 12px 0; font-size: 14px;">Cannot connect to the backend server at ${API_BASE_URL}</p>
        <div style="font-size: 12px; color: #7f1d1d;">
            <strong>Troubleshooting:</strong><br>
            1. Make sure your backend server is running on port 8000<br>
            2. Check if you can access <a href="${API_BASE_URL}/health" target="_blank" style="color: #dc2626;">${API_BASE_URL}/health</a><br>
            3. Look for CORS errors in browser console (F12)
        </div>
        <button onclick="this.parentElement.remove(); checkBackendHealth();" 
                style="margin-top: 12px; padding: 8px 16px; background: #dc2626; color: white; border: none; border-radius: 4px; cursor: pointer;">
            Retry Connection
        </button>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto-remove after 15 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 15000);
}

// Update system status indicator
function updateSystemStatus(online, data = null) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status span');
    
    if (online) {
        statusDot.style.background = '#10b981';
        statusText.textContent = 'System Online';
        
        if (data && data.services) {
            const harvestStatus = data.services.harvest_api === 'configured' ? '✓' : '⚠';
            const geminiStatus = data.services.gemini_api === 'configured' ? '✓' : '⚠';
            statusText.textContent = `System Online ${harvestStatus}LinkedIn ${geminiStatus}AI`;
        }
    } else {
        statusDot.style.background = '#ef4444';
        statusText.textContent = 'System Offline';
    }
}

// Tab switching
function switchTab(tabName) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Show/hide tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    console.log(`📋 Switched to ${tabName} tab`);
}

// Handle search form submission
async function handleSearch(e) {
    e.preventDefault();
    
    console.log('🔍 Starting founder search...');
    
    // Get form data
    const formData = new FormData(searchForm);
    const criteria = {
        industry: formData.get('industry') || null,
        experience_depth: formData.get('experience') ? parseInt(formData.get('experience')) : null,
        founder_signals: formData.getAll('founderSignals'),
        technical_signals: formData.getAll('technicalSignals'),
        max_results: parseInt(formData.get('maxResults')) || 10
    };

    console.log('📋 Search criteria:', criteria);

    // Validate form
    if (criteria.founder_signals.length === 0 && criteria.technical_signals.length === 0) {
        alert('Please select at least one founder signal or technical signal to search for.');
        return;
    }

    try {
        // Update UI state
        setSearchState('loading');
        
        // Call search API
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(criteria)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: `HTTP ${response.status}` }));
            throw new Error(errorData.detail || `Search failed with status ${response.status}`);
        }

        const data = await response.json();
        console.log('✅ Search completed:', data);

        // Store results
        lastSearchResponse = data;
        currentCandidates = data.candidates || [];
        filteredCandidates = [...currentCandidates];

        // Update UI
        displaySearchResults(data);
        switchTab('results');

    } catch (error) {
        console.error('❌ Search error:', error);
        setSearchState('error');
        alert(`Search failed: ${error.message}`);
    }
}

// Set search loading state
function setSearchState(state) {
    const elements = {
        loading: loadingState,
        results: candidatesGrid,
        summary: searchSummary,
        filters: filterPanel,
        empty: emptyState
    };

    // Hide all elements
    Object.values(elements).forEach(el => el.classList.add('hidden'));

    switch (state) {
        case 'loading':
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
            elements.loading.classList.remove('hidden');
            break;

        case 'results':
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i> Start AI Search';
            elements.results.classList.remove('hidden');
            elements.summary.classList.remove('hidden');
            elements.filters.classList.remove('hidden');
            break;

        case 'empty':
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i> Start AI Search';
            elements.empty.classList.remove('hidden');
            break;

        case 'error':
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fas fa-search"></i> Start AI Search';
            break;
    }
}

// Display search results
function displaySearchResults(data) {
    console.log('📊 Displaying results for', data.candidates.length, 'candidates');

    // Update summary stats
    updateSearchSummary(data);

    // Show LinkedIn limitation info if detected
    if (data.linkedin_limitation_info && data.linkedin_limitation_info.detected) {
        showLinkedInLimitationWarning(data.linkedin_limitation_info);
    }

    // Display candidates
    displayCandidates(filteredCandidates);

    // Set appropriate state
    if (filteredCandidates.length > 0) {
        setSearchState('results');
    } else {
        setSearchState('empty');
    }
}

// Show LinkedIn limitation warning
function showLinkedInLimitationWarning(limitationInfo) {
    const warningDiv = document.createElement('div');
    warningDiv.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 16px;
        border-radius: 8px;
        max-width: 400px;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-size: 14px;
    `;
    
    warningDiv.innerHTML = `
        <h4 style="margin: 0 0 8px 0; font-weight: 600;">⚠️ LinkedIn Search Limitation Detected</h4>
        <p style="margin: 0 0 12px 0;">${limitationInfo.description}</p>
        <details style="margin-top: 8px;">
            <summary style="cursor: pointer; font-weight: 500;">Solutions to get more results:</summary>
            <ul style="margin: 8px 0 0 20px; padding: 0;">
                ${limitationInfo.solutions.map(solution => `<li style="margin: 4px 0;">${solution}</li>`).join('')}
            </ul>
        </details>
        <button onclick="this.parentElement.remove();" 
                style="margin-top: 12px; padding: 6px 12px; background: #856404; color: white; border: none; border-radius: 4px; cursor: pointer; float: right;">
            Got it
        </button>
        <div style="clear: both;"></div>
    `;
    
    document.body.appendChild(warningDiv);
    
    // Auto-remove after 30 seconds
    setTimeout(() => {
        if (warningDiv.parentElement) {
            warningDiv.remove();
        }
    }, 30000);
}

// Update search summary
function updateSearchSummary(data) {
    const summary = data.summary || {};
    const tierDist = summary.tier_distribution || { A: 0, B: 0, C: 0 };

    // Update stat numbers
    document.getElementById('total-count').textContent = summary.total_candidates || 0;
    document.getElementById('tier-a-count').textContent = tierDist.A || 0;
    document.getElementById('tier-b-count').textContent = tierDist.B || 0;
    document.getElementById('tier-c-count').textContent = tierDist.C || 0;

    // Update search query text
    const queryText = data.search_query || 'Custom criteria';
    document.getElementById('search-query-text').textContent = queryText;

    console.log('📈 Summary updated:', summary);
}

// Display candidates in grid
function displayCandidates(candidates) {
    candidatesGrid.innerHTML = '';

    if (candidates.length === 0) {
        setSearchState('empty');
        return;
    }

    candidates.forEach((candidate, index) => {
        const card = createCandidateCard(candidate, index);
        candidatesGrid.appendChild(card);
    });

    console.log(`🎯 Displayed ${candidates.length} candidate cards`);
}

// Create candidate card HTML
function createCandidateCard(candidate, index) {
    const card = document.createElement('div');
    card.className = `candidate-card tier-${candidate.tier}`;
    card.onclick = () => showCandidateModal(candidate);

    // Get contact links
    const contacts = candidate.contacts || [];
    const linkedinUrl = contacts.find(c => c.includes('linkedin')) || contacts[0] || '#';
    const hasEmail = contacts.some(c => c.includes('@'));

    // Create confidence score display
    const confidenceScore = candidate.confidence_score || 0.75;
    const confidencePercent = Math.round(confidenceScore * 100);

    // Create data source badge
    const dataSourceBadge = candidate.data_source === 'linkedin_real' 
        ? '<div class="data-source-badge real">📊 Real LinkedIn Data</div>'
        : '<div class="data-source-badge mock">🎭 Mock Data</div>';

    card.innerHTML = `
        <div class="candidate-header">
            <div>
                <div class="candidate-name">${escapeHtml(candidate.name || 'Unknown Candidate')}</div>
                <div class="candidate-role">${escapeHtml(candidate.current_role || 'Role not specified')}</div>
                ${candidate.current_company ? `<div class="candidate-role" style="margin-top: 0.25rem; font-weight: 500;">${escapeHtml(candidate.current_company)}</div>` : ''}
                ${dataSourceBadge}
            </div>
            <div class="candidate-badges">
                <div class="tier-badge tier-${candidate.tier}">Tier ${candidate.tier}</div>
                <div class="profile-badge ${candidate.profile_type}">${candidate.profile_type || 'business'}</div>
            </div>
        </div>
        
        <div class="candidate-summary">
            ${escapeHtml(candidate.summary || 'No summary available')}
        </div>
        
        <div class="candidate-footer">
            <div class="contact-info">
                ${linkedinUrl !== '#' ? `<a href="${linkedinUrl}" target="_blank" class="contact-link" onclick="event.stopPropagation();"><i class="fab fa-linkedin"></i> LinkedIn</a>` : ''}
                ${hasEmail ? `<span class="contact-link"><i class="fas fa-envelope"></i> Email</span>` : ''}
            </div>
            <div class="confidence-score">
                ${confidencePercent}% match
            </div>
        </div>
    `;

    return card;
}

// Show candidate modal with details
function showCandidateModal(candidate) {
    console.log('👤 Showing modal for:', candidate.name);

    // Update modal content
    document.getElementById('modal-candidate-name').textContent = candidate.name || 'Unknown Candidate';
    
    const modalBody = document.querySelector('.modal-body');
    modalBody.innerHTML = `
        <div class="candidate-details">
            <div class="detail-section">
                <h4><i class="fas fa-user"></i> Profile Overview</h4>
                <p><strong>Type:</strong> ${candidate.profile_type || 'Business'} Profile</p>
                <p><strong>Tier:</strong> ${candidate.tier} (${Math.round((candidate.confidence_score || 0.75) * 100)}% confidence)</p>
                ${candidate.current_company ? `<p><strong>Company:</strong> ${escapeHtml(candidate.current_company)}</p>` : ''}
                ${candidate.current_role ? `<p><strong>Role:</strong> ${escapeHtml(candidate.current_role)}</p>` : ''}
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-file-alt"></i> Summary</h4>
                <p>${escapeHtml(candidate.summary || 'No summary available')}</p>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-check-circle"></i> Match Justification</h4>
                <p>${escapeHtml(candidate.match_justification || 'No justification provided')}</p>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-link"></i> Contact & Sources</h4>
                <div style="margin-bottom: 1rem;">
                    <strong>Contact Options:</strong>
                    ${(candidate.contacts || []).map(contact => {
                        if (contact.includes('linkedin')) {
                            return `<br><a href="${contact}" target="_blank" class="contact-link"><i class="fab fa-linkedin"></i> LinkedIn Profile</a>`;
                        } else if (contact.includes('@')) {
                            return `<br><a href="mailto:${contact}" class="contact-link"><i class="fas fa-envelope"></i> ${contact}</a>`;
                        } else if (contact.startsWith('http')) {
                            return `<br><a href="${contact}" target="_blank" class="contact-link"><i class="fas fa-external-link-alt"></i> Profile Link</a>`;
                        }
                        return `<br><span class="contact-link"><i class="fas fa-info-circle"></i> ${contact}</span>`;
                    }).join('')}
                </div>
                <div>
                    <strong>Source Links:</strong>
                    ${(candidate.source_links || []).map(link => 
                        `<br><a href="${link}" target="_blank" class="contact-link"><i class="fas fa-external-link-alt"></i> View Source</a>`
                    ).join('')}
                </div>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-download"></i> Actions</h4>
                <button onclick="exportSingleCandidate('${escapeHtml(candidate.name || 'candidate')}')" class="btn-secondary">
                    <i class="fas fa-download"></i> Export This Candidate
                </button>
            </div>
        </div>
    `;

    // Show modal
    candidateModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Close candidate modal
function closeModal() {
    candidateModal.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Apply filters to candidates
function applyFilters() {
    const tierFilter = document.getElementById('tier-filter').value;
    const typeFilter = document.getElementById('type-filter').value;
    const searchFilter = document.getElementById('search-filter').value.toLowerCase();

    filteredCandidates = currentCandidates.filter(candidate => {
        // Tier filter
        if (tierFilter && candidate.tier !== tierFilter) return false;

        // Type filter
        if (typeFilter && candidate.profile_type !== typeFilter) return false;

        // Search filter
        if (searchFilter) {
            const searchableText = [
                candidate.name || '',
                candidate.summary || '',
                candidate.current_role || '',
                candidate.current_company || '',
                candidate.match_justification || ''
            ].join(' ').toLowerCase();

            if (!searchableText.includes(searchFilter)) return false;
        }

        return true;
    });

    console.log(`🔍 Filters applied: ${filteredCandidates.length}/${currentCandidates.length} candidates shown`);

    // Update display
    displayCandidates(filteredCandidates);

    // Update summary with filtered results
    if (lastSearchResponse) {
        const filteredSummary = calculateFilteredSummary(filteredCandidates);
        updateSearchSummary({ ...lastSearchResponse, summary: filteredSummary });
    }
}

// Calculate summary for filtered results
function calculateFilteredSummary(candidates) {
    const tierDist = { A: 0, B: 0, C: 0 };
    const profileDist = { business: 0, technical: 0 };

    candidates.forEach(candidate => {
        tierDist[candidate.tier] = (tierDist[candidate.tier] || 0) + 1;
        profileDist[candidate.profile_type] = (profileDist[candidate.profile_type] || 0) + 1;
    });

    return {
        total_candidates: candidates.length,
        tier_distribution: tierDist,
        profile_distribution: profileDist,
        top_tier_percentage: candidates.length > 0 ? Math.round((tierDist.A / candidates.length) * 100) : 0
    };
}

// Handle CSV export
async function handleExport() {
    if (!lastSearchResponse || !lastSearchResponse.export_path) {
        alert('No search results to export. Please run a search first.');
        return;
    }

    try {
        console.log('📥 Downloading export file:', lastSearchResponse.export_path);
        
        // Extract just the filename from the path
        const filename = lastSearchResponse.export_path.includes('/') 
            ? lastSearchResponse.export_path.split('/').pop()
            : lastSearchResponse.export_path;
            
        console.log('📁 Requesting download for filename:', filename);
        
        const response = await fetch(`${API_BASE_URL}/download/${filename}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Download error response:', errorText);
            throw new Error(`Download failed: ${response.status} - ${errorText}`);
        }

        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        console.log('✅ Export downloaded successfully');
        showToast('CSV file downloaded successfully!', 'success');

    } catch (error) {
        console.error('❌ Export failed:', error);
        showToast(`Export failed: ${error.message}`, 'error');
    }
}

// Export single candidate (placeholder)
function exportSingleCandidate(candidateName) {
    // For now, just copy to clipboard
    const candidate = currentCandidates.find(c => c.name === candidateName);
    if (candidate) {
        const exportText = `Name: ${candidate.name}\nRole: ${candidate.current_role}\nCompany: ${candidate.current_company}\nSummary: ${candidate.summary}\nTier: ${candidate.tier}\nContacts: ${candidate.contacts.join(', ')}`;
        
        navigator.clipboard.writeText(exportText).then(() => {
            alert('Candidate information copied to clipboard!');
        }).catch(() => {
            alert('Could not copy to clipboard. Please manually copy the information from the modal.');
        });
    }
}

// Clear search form
function clearForm() {
    searchForm.reset();
    document.getElementById('maxResults').value = '10';
    
    // Clear all checkboxes
    searchForm.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });

    console.log('🧹 Form cleared');
}

// Utility function to escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key closes modal
    if (e.key === 'Escape' && !candidateModal.classList.contains('hidden')) {
        closeModal();
    }
    
    // Ctrl/Cmd + Enter submits search form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (document.querySelector('#search-tab').classList.contains('active')) {
            handleSearch(e);
        }
    }
});

// Add some helper functions for better UX
function showToast(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-size: 14px;
        max-width: 300px;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Performance optimization: Debounce search filter
let searchFilterTimeout;
const originalSearchFilter = document.getElementById('search-filter');
if (originalSearchFilter) {
    originalSearchFilter.addEventListener('input', function(e) {
        clearTimeout(searchFilterTimeout);
        searchFilterTimeout = setTimeout(() => {
            applyFilters();
        }, 300);
    });
}

console.log('🚀 Founder Sourcing Agent frontend loaded successfully!');
console.log('🔗 Backend URL:', API_BASE_URL);
console.log('✨ Ready to find amazing founders!');

// Export functions for global access
window.switchTab = switchTab;
window.showCandidateModal = showCandidateModal;
window.closeModal = closeModal;