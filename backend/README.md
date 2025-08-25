# 🔧 Backend Documentation

> **Founder Sourcing Agent - FastAPI Backend**

**Developed by:** [Karunasagar Mohansundar](https://github.com/Karunasagar12)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Services](#services)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

---

## 🎯 Overview

The backend is a **FastAPI-based microservice** that provides AI-powered founder discovery capabilities. It integrates with multiple external APIs, processes data through AI analysis, and provides a robust REST API for the frontend.

### Key Features

- 🤖 **AI-Powered Analysis**: Google Gemini AI integration
- 📊 **Data Processing**: Harvest API integration for LinkedIn data
- 🔐 **Authentication**: JWT-based user management
- 📈 **Export Functionality**: CSV export with custom formatting
- 🗄️ **Database Management**: PostgreSQL with SQLAlchemy ORM
- 📝 **API Documentation**: Auto-generated with FastAPI
- 🔒 **Security**: CORS, rate limiting, input validation

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Services      │    │   External      │
│   Application   │◄──►│   Layer         │◄──►│   APIs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Models        │    │   Database      │    │   Authentication│
│   (Pydantic)    │    │   (PostgreSQL)  │    │   (JWT)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Service Architecture

- **FastAPI App**: Main application with routing and middleware
- **Services Layer**: Business logic and external API integration
- **Models Layer**: Data validation and serialization
- **Database Layer**: Data persistence and ORM operations
- **Authentication Layer**: User management and JWT handling

---

## 🛠️ Tech Stack

### Core Framework
- **FastAPI 0.104.1** - High-performance Python web framework
- **Uvicorn 0.24.0** - ASGI server for production
- **Pydantic 2.5.0** - Data validation and serialization

### Database & ORM
- **PostgreSQL** - Production database
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migrations

### Authentication & Security
- **Python-Jose** - JWT token handling
- **Passlib** - Password hashing
- **CORS Middleware** - Cross-origin resource sharing

### External Integrations
- **Google Gemini AI** - AI analysis and candidate ranking
- **Harvest API** - LinkedIn profile data
- **Requests** - HTTP client for API calls

### Development & Testing
- **Pytest** - Testing framework
- **Black** - Code formatting
- **Flake8** - Linting

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Google Cloud SDK (for deployment)
- Docker (for containerization)

### Local Development Setup

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and database settings
   ```

5. **Initialize database**
   ```bash
   # Create database tables
   python -c "from database import create_tables; create_tables()"
   ```

6. **Start development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/founder_sourcing_agent

# API Keys
HARVEST_API_KEY=your_harvest_api_key
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://founder-sourcing-agent.web.app

# Environment
ENVIRONMENT=development
```

---

## 🔧 Services

### AI Analyzer Service (`services/ai_analyzer.py`)

Handles AI-powered candidate analysis using Google Gemini AI.

**Key Methods:**
- `analyze_candidate()` - Analyze individual candidate profiles
- `_create_analysis_prompt()` - Generate AI prompts
- `_call_gemini_api()` - Make API calls to Gemini

**Features:**
- Intelligent candidate ranking (A/B/C tiers)
- Confidence scoring
- Match justification generation
- Rate limiting and error handling

### Harvest Client Service (`services/harvest_client.py`)

Manages LinkedIn profile data retrieval through Harvest API.

**Key Methods:**
- `search_profiles()` - Search for LinkedIn profiles
- `_build_search_query()` - Construct search queries
- `_get_enhanced_mock_profiles()` - Mock data for development

**Features:**
- Multi-parameter search
- Result pagination
- Error handling and retries
- Mock data for development

### Export Service (`services/export_service.py`)

Handles CSV export functionality for candidate data.

**Key Methods:**
- `export_to_csv()` - Export candidates to CSV
- `_format_candidate_data()` - Format data for export
- `_generate_filename()` - Generate timestamped filenames

**Features:**
- Custom CSV formatting
- Timestamped file naming
- Comprehensive candidate data export
- Error handling and validation

### Authentication Service (`auth_service.py`)

Manages user authentication and JWT token handling.

**Key Methods:**
- `authenticate_user()` - Validate user credentials
- `create_access_token()` - Generate JWT tokens
- `get_current_user()` - Extract user from token

**Features:**
- Secure password hashing
- JWT token generation and validation
- User session management
- Password reset functionality

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Search Results Table
```sql
CREATE TABLE search_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    search_criteria JSONB NOT NULL,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Search Candidates Table
```sql
CREATE TABLE search_candidates (
    id SERIAL PRIMARY KEY,
    search_result_id INTEGER REFERENCES search_results(id),
    candidate_data JSONB NOT NULL,
    tier VARCHAR(1) NOT NULL,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 API Endpoints

### Authentication Endpoints
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile

### Search Endpoints
- `POST /search` - Search for founders
- `GET /health` - System health check

### Export Endpoints
- `POST /export` - Export candidates to CSV

### Documentation
- `GET /docs` - Interactive API documentation
- `GET /openapi.json` - OpenAPI schema

---

## 🔐 Authentication

### JWT Token Flow

1. **User Login**: User provides credentials
2. **Token Generation**: Server generates JWT token
3. **Token Storage**: Client stores token securely
4. **API Requests**: Client includes token in Authorization header
5. **Token Validation**: Server validates token on each request

### Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **CORS Protection**: Configured for specific origins
- **Rate Limiting**: API rate limiting implementation
- **Input Validation**: Pydantic model validation

---

## 💻 Development

### Code Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── models.py              # Pydantic data models
├── database.py            # Database connection and setup
├── auth_*.py              # Authentication modules
├── services/              # Business logic services
│   ├── ai_analyzer.py     # AI analysis service
│   ├── harvest_client.py  # Harvest API client
│   └── export_service.py  # Export functionality
├── requirements.txt       # Python dependencies
├── requirements-prod.txt  # Production dependencies
├── Dockerfile            # Container configuration
└── gunicorn.conf.py      # Production server config
```

### Development Guidelines

1. **Code Formatting**
   ```bash
   black .
   flake8 .
   ```

2. **Type Hints**
   - Use type hints for all function parameters and return values
   - Use Pydantic models for data validation

3. **Error Handling**
   - Use proper HTTP status codes
   - Provide meaningful error messages
   - Log errors appropriately

4. **Testing**
   ```bash
   pytest tests/ -v
   ```

---

## 🧪 Testing

### Test Structure
```
tests/
├── test_auth.py          # Authentication tests
├── test_search.py        # Search functionality tests
├── test_export.py        # Export functionality tests
└── conftest.py           # Test configuration
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Categories

- **Unit Tests**: Individual function testing
- **Integration Tests**: API endpoint testing
- **Authentication Tests**: JWT and user management
- **Error Handling Tests**: Exception scenarios

---

## 🚀 Deployment

### Production Deployment

The backend is deployed using Docker containers on Google Cloud Run.

### Docker Configuration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
```

### Environment Configuration

Production environment variables are managed through Google Cloud Secret Manager and GitHub Actions secrets.

### Health Checks

The application includes health check endpoints for monitoring:
- `GET /health` - Basic health check
- Database connectivity verification
- External API status checks

---

## 📊 Monitoring & Logging

### Logging Configuration

- **Structured Logging**: JSON format for production
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Request Logging**: All API requests logged
- **Error Tracking**: Comprehensive error logging

### Performance Monitoring

- **Response Times**: API endpoint performance tracking
- **Database Queries**: Query performance monitoring
- **External API Calls**: Third-party API performance
- **Resource Usage**: CPU and memory monitoring

---

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL configuration
   - Verify PostgreSQL service is running
   - Check network connectivity

2. **API Key Issues**
   - Verify API keys in environment variables
   - Check API key permissions
   - Validate API quotas and limits

3. **CORS Errors**
   - Verify ALLOWED_ORIGINS configuration
   - Check frontend URL in CORS settings
   - Ensure proper CORS headers

### Debug Mode

Enable debug mode for detailed error information:
```bash
export ENVIRONMENT=development
uvicorn main:app --reload --log-level debug
```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Google Gemini AI**: https://ai.google.dev/
- **Harvest API**: https://harvest.io/

---

## 🆘 Support

For backend support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/Karunasagar12/founder-sourcing-agent/issues)
- **Developer**: [Karunasagar Mohansundar](https://github.com/Karunasagar12)

---

*Last updated: January 2024*
