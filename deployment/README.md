# Founder Sourcing Agent - Production Deployment Guide

This guide will help you deploy the Founder Sourcing Agent to Google Cloud Platform with essential production features.

## 🏗️ Architecture Overview

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

## 📋 Prerequisites

1. **Google Cloud Account** with billing enabled
2. **GitHub Account** for CI/CD
3. **Firebase Account** for frontend hosting
4. **Google Cloud SDK** installed locally
5. **Docker** installed locally
6. **Node.js** (v18+) installed locally

## 🚀 Quick Start Deployment

### Step 1: Set up GCP Project

```bash
# Clone the repository
git clone <your-repo-url>
cd founder-sourcing-agent

# Run the GCP setup script
chmod +x deployment/scripts/setup-gcp.sh
./deployment/scripts/setup-gcp.sh
```

### Step 2: Configure GitHub Secrets

Add these secrets to your GitHub repository:

```
GCP_SA_KEY=<service-account-key-json>
DB_HOST=<cloud-sql-connection-name>
DB_PORT=5432
DB_NAME=founder_sourcing_agent
DB_USER=founder_app
DB_PASSWORD=<database-password>
SECRET_KEY=<application-secret-key>
HARVEST_API_KEY=<your-harvest-api-key>
GEMINI_API_KEY=<your-gemini-api-key>
FIREBASE_SERVICE_ACCOUNT=<firebase-service-account-json>
```

### Step 3: Deploy with GitHub Actions

1. Push your code to the `main` branch
2. GitHub Actions will automatically:
   - Test the code
   - Build Docker images
   - Deploy backend to Cloud Run
   - Deploy frontend to Firebase Hosting

### Step 4: Access Your Application

- **Frontend**: https://founder-sourcing-agent.web.app
- **Backend API**: https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app
- **API Documentation**: https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app/docs

## 🔧 Manual Deployment

If you prefer manual deployment:

```bash
# Run the deployment script
chmod +x deployment/scripts/deploy.sh
./deployment/scripts/deploy.sh
```

## 📊 Database Setup

### Run Migrations

```bash
# Run database migrations
chmod +x deployment/scripts/migrate-db.sh
./deployment/scripts/migrate-db.sh
```

### Database Schema

The application uses these main tables:
- `users` - User authentication and profiles
- `searches` - Search history and criteria
- `candidates` - Founder candidate data

## 🔐 Security Configuration

### Environment Variables

Copy the template and configure your production environment:

```bash
cp deployment/configs/env.production.template backend/.env.production
# Edit the file with your actual values
```

### CORS Configuration

The backend is configured to allow requests from:
- Firebase Hosting domains
- Local development servers

### Authentication

- JWT-based authentication
- Password hashing with bcrypt
- Secure session management

## 📈 Monitoring and Logging

### Cloud Run Monitoring

- Automatic request/response logging
- Performance metrics
- Error tracking
- Custom metrics support

### Database Monitoring

- Connection monitoring
- Query performance
- Storage usage
- Backup status

## 🔄 CI/CD Pipeline

### Backend Deployment

Triggers on:
- Push to `main` branch
- Changes in `backend/` or `deployment/backend/`

Steps:
1. Run tests
2. Build Docker image
3. Push to Container Registry
4. Deploy to Cloud Run
5. Update environment variables

### Frontend Deployment

Triggers on:
- Push to `main` branch
- Changes in `frontend/` or `deployment/frontend/`

Steps:
1. Run linting and tests
2. Build production bundle
3. Deploy to Firebase Hosting

## 💰 Cost Optimization

### Cloud Run
- **Min instances**: 0 (scale to zero)
- **Max instances**: 10 (limit costs)
- **Memory**: 1Gi (adequate for most workloads)

### Cloud SQL
- **Instance**: db-f1-micro (smallest available)
- **Storage**: 10GB (minimum)
- **Backups**: Enabled (automatic)

### Estimated Monthly Costs
- Cloud Run: $5-20/month (depending on usage)
- Cloud SQL: $7-15/month
- Firebase Hosting: Free tier
- **Total**: $12-35/month

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check Cloud SQL instance is running
   - Verify connection name and credentials
   - Ensure service account has proper permissions

2. **CORS Errors**
   - Verify frontend URL is in allowed origins
   - Check CORS middleware configuration

3. **Authentication Issues**
   - Verify JWT secret key is set
   - Check token expiration settings

4. **Build Failures**
   - Check Docker build logs
   - Verify all dependencies are in requirements-prod.txt

### Useful Commands

```bash
# Check Cloud Run service status
gcloud run services describe founder-sourcing-agent-backend --region=us-central1

# View Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Check Cloud SQL status
gcloud sql instances describe founder-sourcing-db

# Test database connection
gcloud sql connect founder-sourcing-db --user=founder_app
```

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Support

For deployment issues:
1. Check the troubleshooting section
2. Review Cloud Run and Cloud SQL logs
3. Verify all environment variables are set correctly
4. Ensure proper IAM permissions are configured

---

**Note**: This deployment is optimized for demo and internship purposes. For production use, consider additional security measures, monitoring, and scaling configurations.
