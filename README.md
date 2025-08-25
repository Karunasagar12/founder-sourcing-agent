# 🚀 Founder Sourcing Agent

> **AI-powered founder discovery system with complete production infrastructure**

**Developed by:** [Karunasagar Mohansundar](https://github.com/Karunasagar12)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20App-blue?style=for-the-badge&logo=firebase)](https://founder-sourcing-agent.web.app)
[![Backend API](https://img.shields.io/badge/API-Documentation-green?style=for-the-badge&logo=fastapi)](https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app/docs)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

## 🎯 Project Overview

A **production-ready, AI-powered founder sourcing platform** built in 30 hours to demonstrate technical competence, rapid prototyping, and scalable architecture decisions. This project showcases full-stack development, cloud deployment, and DevOps practices.

### ✨ Key Features

- 🤖 **AI-Powered Analysis**: Google Gemini AI for intelligent candidate evaluation
- 🎯 **Smart Tier Ranking**: A/B/C classification system for candidate prioritization
- 📊 **Data Integration**: Harvest API for LinkedIn profile data
- 🔐 **User Authentication**: JWT-based secure authentication system
- 📈 **CSV Export**: Professional data export functionality
- 📱 **Responsive Design**: Modern, mobile-first UI/UX
- 🚀 **Live Deployment**: Production-ready cloud infrastructure

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Firebase      │    │   Cloud Run     │    │   Cloud SQL     │
│   Hosting       │◄──►│   Backend       │◄──►│   PostgreSQL    │
│   (Frontend)    │    │   (FastAPI)     │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Secret        │    │   Cloud         │
│   Actions       │    │   Manager       │    │   Monitoring    │
│   (CI/CD)       │    │   (Secrets)     │    │   (Logs)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **React 18** + **Vite** - Modern, fast development
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons
- **React Router** - Client-side routing

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Production database
- **JWT Authentication** - Secure user management

### AI & Data
- **Google Gemini AI** - Advanced AI analysis
- **Harvest API** - LinkedIn profile data
- **Pydantic** - Data validation

### Infrastructure
- **Google Cloud Platform** - Cloud infrastructure
- **Firebase Hosting** - Frontend deployment
- **Cloud Run** - Backend containerization
- **Cloud SQL** - Managed PostgreSQL
- **GitHub Actions** - CI/CD automation
- **Docker** - Containerization

---

## 🚀 Live Application

### 🌐 Frontend
- **URL**: https://founder-sourcing-agent.web.app
- **Features**: Custom domain, HTTPS, global CDN
- **Performance**: Optimized build with caching

### 🔧 Backend API
- **URL**: https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app
- **Documentation**: Auto-generated API docs
- **Features**: Auto-scaling, load balancing, monitoring

---

## 📋 Features

### 🔍 AI-Powered Search
- Intelligent candidate analysis using Google Gemini AI
- Multi-criteria search (industry, location, experience)
- Real-time processing with progress tracking

### 🎯 Smart Ranking System
- **Tier A**: Excellent matches (85%+ criteria met)
- **Tier B**: Good matches (60-84% criteria met)
- **Tier C**: Possible matches (40-59% criteria met)

### 📊 Data Management
- CSV export with comprehensive candidate data
- Search history tracking
- User-specific data persistence

### 🔐 Security & Authentication
- JWT-based authentication
- Secure API key management
- CORS configuration
- Environment-based security

---

## 🏗️ Production Infrastructure

### 🚀 Deployment
- **Automated CI/CD** with GitHub Actions
- **Zero-downtime deployments**
- **Containerized microservices**
- **Auto-scaling infrastructure**

### 📊 Monitoring & Reliability
- **Production logging** and monitoring
- **Health check endpoints**
- **Database connection pooling**
- **Automatic backups**

### 💰 Cost Optimization
- **Scale-to-zero** when not in use
- **Resource limits** and monitoring
- **Efficient caching** strategies
- **Optimized database** queries

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (for production)
- Google Cloud SDK

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Karunasagar12/founder-sourcing-agent.git
   cd founder-sourcing-agent
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

4. **Environment Variables**
   ```bash
   # Create .env files with your API keys
   HARVEST_API_KEY=your_harvest_api_key
   GOOGLE_GEMINI_API_KEY=your_gemini_api_key
   ```

### Production Deployment

The application is automatically deployed via GitHub Actions:

1. **Push to main branch**
2. **GitHub Actions** builds and deploys
3. **Frontend** deploys to Firebase Hosting
4. **Backend** deploys to Cloud Run
5. **Database** migrations run automatically

---

## 📁 Project Structure

```
founder-sourcing-agent/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── contexts/       # React contexts
│   └── public/             # Static assets
├── backend/                 # FastAPI backend application
│   ├── services/           # Business logic services
│   ├── models/             # Data models
│   ├── auth/               # Authentication modules
│   └── exports/            # Generated exports
├── deployment/             # Production deployment configs
│   ├── backend/           # Docker & Cloud Run configs
│   ├── frontend/          # Firebase hosting configs
│   └── .github/           # GitHub Actions workflows
└── docs/                   # Documentation
```

---

## 🎯 Technical Achievements

### 🏆 Production-Ready Features
- ✅ **Live deployment** with custom domain
- ✅ **Automated CI/CD** pipeline
- ✅ **Containerized** microservices
- ✅ **Auto-scaling** infrastructure
- ✅ **Production monitoring** and logging
- ✅ **Database migrations** and backups
- ✅ **Security best practices** implementation

### 🔧 DevOps Excellence
- ✅ **GitHub Actions** automation
- ✅ **Docker** containerization
- ✅ **Cloud-native** architecture
- ✅ **Environment management**
- ✅ **Secret management**
- ✅ **Health checks** and monitoring

### 💻 Development Quality
- ✅ **Type-safe** development
- ✅ **API documentation** (auto-generated)
- ✅ **Responsive design**
- ✅ **Modern UI/UX**
- ✅ **Performance optimization**
- ✅ **Code quality** standards

---

## 🤝 Contributing

This project was built as a technical demonstration and portfolio piece. For questions or collaboration opportunities, please reach out to [Karunasagar Mohansundar](https://github.com/Karunasagar12).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Karunasagar Mohansundar**

- **GitHub**: [@Karunasagar12](https://github.com/Karunasagar12)
- **LinkedIn**: [Connect with me](https://linkedin.com/in/karunasagar-mohansundar)
- **Portfolio**: [View my work](https://founder-sourcing-agent.web.app/about)

### 🎯 About the Developer

Healthcare Data Scientist turned Entrepreneurial Builder with expertise in:
- **AI/ML** (Python, PyTorch, predictive analytics)
- **Full-stack Development** (React, FastAPI, cloud deployment)
- **DevOps** (CI/CD, containerization, cloud infrastructure)
- **Healthcare Technology** (digital health tools, data science)

---

## 🌟 Showcase

This project demonstrates:
- **Rapid prototyping** capabilities
- **Production deployment** skills
- **Cloud architecture** expertise
- **AI integration** proficiency
- **Professional development** practices

**Built in 30 hours to showcase technical competence and rapid development capabilities.**

---

<div align="center">

**🚀 Ready to build something amazing together?**

[View Live Application](https://founder-sourcing-agent.web.app) | [About Me](https://founder-sourcing-agent.web.app/about)

</div>
