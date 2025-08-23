# Founder Sourcing Agent - Frontend

A professional CRM-style React frontend for the AI-powered founder discovery system.

## Features

✅ **Professional Search Interface**
- Form builder for all criteria types
- Industry/experience/education dropdowns
- Founder signal checkboxes
- Technical signal options
- Search progress indicators

✅ **Results Display System**
- Card layout with A/B/C tier color coding
- Profile type badges (business/technical)
- Summary previews and key highlights
- Contact information display
- Source links and evidence

✅ **Candidate Detail Modals**
- Full profile information
- Complete match justification
- All contact methods
- Export individual candidate

✅ **Filtering and Sorting**
- Filter by tier (A/B/C)
- Filter by profile type
- Sort by relevance/name/date
- Search within results

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons
- **TypeScript** - Type safety (optional)

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend server running on port 8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
frontend/src/
├── components/
│   ├── SearchForm.tsx      # Criteria input form
│   ├── CandidateCard.tsx   # Result display card
│   ├── CandidateModal.tsx  # Detail view modal
│   ├── FilterPanel.tsx     # Results filtering
│   └── Header.jsx          # Navigation header
├── pages/
│   ├── Search.tsx          # Main search page
│   └── Results.jsx         # Results display page
├── services/
│   └── api.js              # Backend communication
├── App.jsx                 # Main app component
├── main.jsx               # React entry point
└── index.css              # Global styles
```

## API Integration

The frontend communicates with the FastAPI backend through the `/api` service:

- `POST /search` - Submit search criteria
- `GET /health` - Check system status
- `POST /export` - Export candidates

## Styling

The app uses Tailwind CSS with custom components:

- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary action buttons
- `.card` - Content containers
- `.input-field` - Form inputs
- `.tier-badge` - Tier indicators

## Development

### Adding New Components

1. Create component in `src/components/`
2. Import and use in pages
3. Add any new styles to `src/index.css`

### API Changes

Update `src/services/api.js` to match backend endpoints.

### Styling Changes

Modify `tailwind.config.js` for theme changes or `src/index.css` for custom components.

## Deployment

The frontend can be deployed to any static hosting service:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Make sure to update the API URL in production environment variables.
