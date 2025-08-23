# Founder Sourcing Agent

An AI-powered founder discovery system with a professional CRM-style web interface.

## 🚀 Features

### Backend (FastAPI + Python)
- **AI-Powered Analysis**: Uses Gemini AI to analyze and rank founder candidates
- **Data Harvesting**: Integrates with Harvest API for candidate discovery
- **Smart Ranking**: Tier-based (A/B/C) candidate ranking system
- **Export Capabilities**: CSV export functionality
- **RESTful API**: Clean FastAPI endpoints with CORS support

### Frontend (React + TypeScript)
- **Professional Search Interface**: Form builder for all criteria types
- **Results Display**: Card layout with tier-based visual ranking
- **Candidate Details**: Modal views with full profile information
- **Filtering & Sorting**: Advanced filtering by tier, profile type, and search
- **Export Functionality**: Individual and bulk candidate export
- **Responsive Design**: Modern UI with Tailwind CSS

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Google Gemini AI** - AI analysis and ranking
- **Harvest API** - Candidate data source
- **Python 3.8+** - Core runtime

### Frontend
- **React 18** - Modern React with hooks
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
HARVEST_API_KEY=your_harvest_api_key
GEMINI_API_KEY=your_gemini_api_key
```

4. **Start the backend server:**
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Quick setup (Windows):**
```bash
setup.bat
```

**Or Quick setup (Mac/Linux):**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Manual setup:**
```bash
npm install
cp env.example .env
```

4. **Start the development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

### 1. Search for Founders
- Navigate to the search page
- Fill out the search criteria form:
  - Years of experience
  - Industry focus
  - Founder signals (checkboxes)
  - Technical signals (checkboxes)
  - Maximum results
- Click "Search Founders"

### 2. Review Results
- View tier-ranked candidates (A/B/C)
- Filter by profile type (Business/Technical)
- Sort by relevance, name, or tier
- Search within results

### 3. Candidate Details
- Click "View Details" on any candidate card
- See full profile information
- Access contact methods
- View source links and evidence
- Export individual candidates

### 4. Export Data
- Export individual candidates from detail modal
- Export all filtered results using "Export All" button
- CSV format with all candidate information

## 📁 Project Structure

```
founder-sourcing-agent/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── services/
│       ├── ai_analyzer.py   # AI analysis service
│       ├── harvest_client.py # Harvest API client
│       └── export_service.py # Export functionality
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.jsx         # Main app
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
```

## 🔧 API Endpoints

### Backend API
- `GET /` - Welcome message and API info
- `GET /health` - System health check
- `POST /search` - Search for founders
- `POST /export` - Export candidates

### Frontend Routes
- `/` - Search page
- `/results` - Results display page

## 🎨 UI Components

### Search Form
- Experience depth input
- Industry dropdown
- Founder signals checkboxes
- Technical signals checkboxes
- Max results selector

### Candidate Cards
- Name and profile type
- Tier badges (A/B/C with colors)
- Summary preview
- Contact information
- Source links
- View details button

### Filter Panel
- Search within results
- Tier filter (A/B/C)
- Profile type filter (Business/Technical)
- Sort options
- Active filters display

### Candidate Modal
- Full profile information
- Match justification
- All contact methods
- Source links
- Export functionality

## 🚀 Deployment

### Backend Deployment
- Deploy to any Python hosting service
- Set environment variables for API keys
- Ensure CORS is configured for frontend domain

### Frontend Deployment
- Build: `npm run build`
- Deploy `dist/` folder to any static hosting
- Update API URL in environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with details

---

**Built with ❤️ for the startup ecosystem**
