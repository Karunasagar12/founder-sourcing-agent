# 🔌 API Documentation

> **Founder Sourcing Agent API Reference**

**Base URL**: `https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app`  
**API Version**: v1.0.0  
**Authentication**: JWT Bearer Token

---

## 📋 Table of Contents

- [Authentication](#authentication)
- [Health Check](#health-check)
- [Search Endpoints](#search-endpoints)
- [Export Endpoints](#export-endpoints)
- [User Management](#user-management)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

---

## 🔐 Authentication

### JWT Token Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Register
```http
POST /auth/signup
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

## 🏥 Health Check

### Get System Status
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "harvest_api": "configured",
    "gemini_api": "configured"
  },
  "cors": "enabled",
  "message": "All systems operational"
}
```

---

## 🔍 Search Endpoints

### Search Founders
```http
POST /search
```

**Request Body:**
```json
{
  "years_of_experience": 5,
  "industry": "healthcare",
  "location": "United States",
  "founder_signals": ["founder", "co-founder"],
  "technical_signals": ["CTO", "engineering"],
  "max_results": 20
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Search completed successfully",
  "data": {
    "total_candidates": 15,
    "processing_time": "2.3s",
    "candidates": [
      {
        "id": "candidate_001",
        "name": "Sarah Johnson",
        "profile_type": "business",
        "summary": "Experienced healthcare founder with 8+ years in digital health...",
        "tier": "A",
        "confidence_score": 0.92,
        "current_company": "HealthTech Solutions",
        "current_role": "CEO & Co-founder",
        "contacts": {
          "email": "sarah@healthtech.com",
          "linkedin": "https://linkedin.com/in/sarahjohnson"
        },
        "source_links": ["https://linkedin.com/in/sarahjohnson"],
        "match_justification": "Strong founder signals with healthcare expertise...",
        "data_source": "linkedin_real"
      }
    ]
  }
}
```

### Search Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `years_of_experience` | integer | No | Minimum years of experience |
| `industry` | string | No | Target industry (e.g., "healthcare", "fintech") |
| `location` | string | No | Geographic location |
| `founder_signals` | array | No | Founder indicators (e.g., ["founder", "co-founder"]) |
| `technical_signals` | array | No | Technical indicators (e.g., ["CTO", "engineering"]) |
| `max_results` | integer | No | Maximum number of results (default: 10) |

### Candidate Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique candidate identifier |
| `name` | string | Full name |
| `profile_type` | string | "business" or "technical" |
| `summary` | string | AI-generated summary |
| `tier` | string | "A", "B", or "C" ranking |
| `confidence_score` | float | AI confidence (0.0-1.0) |
| `current_company` | string | Current employer |
| `current_role` | string | Current job title |
| `contacts` | object | Contact information |
| `source_links` | array | Source URLs |
| `match_justification` | string | AI explanation of match |
| `data_source` | string | Data source identifier |

---

## 📊 Export Endpoints

### Export Candidates
```http
POST /export
```

**Request Body:**
```json
{
  "candidates": [
    {
      "id": "candidate_001",
      "name": "Sarah Johnson",
      "profile_type": "business",
      "summary": "Experienced healthcare founder...",
      "tier": "A",
      "confidence_score": 0.92
    }
  ],
  "filename": "founder_candidates_20241201"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Export completed successfully",
  "data": {
    "download_url": "/exports/founder_candidates_20241201_143022.csv",
    "filename": "founder_candidates_20241201_143022.csv",
    "record_count": 15
  }
}
```

---

## 👤 User Management

### Get User Profile
```http
GET /auth/profile
```

**Headers:**
```http
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:45:00Z"
}
```

### Update User Profile
```http
PUT /auth/profile
```

**Headers:**
```http
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith"
}
```

### Get Search History
```http
GET /auth/search-history
```

**Headers:**
```http
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "searches": [
    {
      "id": 1,
      "query": "healthcare founders",
      "results_count": 15,
      "created_at": "2024-01-20T14:45:00Z",
      "criteria": {
        "industry": "healthcare",
        "years_of_experience": 5
      }
    }
  ]
}
```

---

## ❌ Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid search criteria",
    "details": {
      "field": "max_results",
      "issue": "Value must be between 1 and 100"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `AUTHENTICATION_ERROR` | 401 | Invalid or missing authentication |
| `AUTHORIZATION_ERROR` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

### Example Error Responses

**Authentication Error:**
```json
{
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Invalid credentials"
  }
}
```

**Validation Error:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid search criteria",
    "details": {
      "field": "max_results",
      "issue": "Value must be between 1 and 100"
    }
  }
}
```

---

## ⚡ Rate Limits

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Limits by Endpoint

| Endpoint | Rate Limit | Window |
|----------|------------|--------|
| `/search` | 10 requests | 1 minute |
| `/export` | 5 requests | 1 minute |
| `/auth/*` | 20 requests | 1 minute |
| `/health` | 100 requests | 1 minute |

### Rate Limit Exceeded Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

---

## 🔧 SDK Examples

### Python Example
```python
import requests

# Base configuration
BASE_URL = "https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app"
API_KEY = "your-jwt-token"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Search for founders
search_data = {
    "industry": "healthcare",
    "years_of_experience": 5,
    "founder_signals": ["founder", "co-founder"],
    "max_results": 10
}

response = requests.post(
    f"{BASE_URL}/search",
    json=search_data,
    headers=headers
)

if response.status_code == 200:
    results = response.json()
    print(f"Found {results['data']['total_candidates']} candidates")
else:
    print(f"Error: {response.json()}")
```

### JavaScript Example
```javascript
const BASE_URL = "https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app";
const API_KEY = "your-jwt-token";

const headers = {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
};

// Search for founders
const searchData = {
    industry: "healthcare",
    years_of_experience: 5,
    founder_signals: ["founder", "co-founder"],
    max_results: 10
};

fetch(`${BASE_URL}/search`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(searchData)
})
.then(response => response.json())
.then(data => {
    if (data.status === "success") {
        console.log(`Found ${data.data.total_candidates} candidates`);
    } else {
        console.error("Error:", data.error);
    }
})
.catch(error => console.error("Request failed:", error));
```

---

## 📚 Additional Resources

- **Interactive API Docs**: https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app/docs
- **OpenAPI Schema**: https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app/openapi.json
- **GitHub Repository**: https://github.com/Karunasagar12/founder-sourcing-agent

---

## 🆘 Support

For API support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/Karunasagar12/founder-sourcing-agent/issues)
- **Developer**: [Karunasagar Mohansundar](https://github.com/Karunasagar12)

---

*Last updated: January 2024*
