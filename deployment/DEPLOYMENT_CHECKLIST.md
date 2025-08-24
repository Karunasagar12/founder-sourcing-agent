# Deployment Checklist

## ✅ Pre-Deployment Setup

### GCP Project Setup
- [ ] Create GCP project: `founder-sourcing-agent`
- [ ] Enable billing on the project
- [ ] Install Google Cloud SDK locally
- [ ] Authenticate with `gcloud auth login`
- [ ] Set project: `gcloud config set project founder-sourcing-agent`

### Required APIs
- [ ] Cloud Build API
- [ ] Cloud Run API
- [ ] Cloud SQL Admin API
- [ ] Secret Manager API
- [ ] Cloud Resource Manager API
- [ ] IAM API
- [ ] Container Registry API

### Firebase Setup
- [ ] Create Firebase project: `founder-sourcing-agent`
- [ ] Enable Firebase Hosting
- [ ] Get Firebase service account key
- [ ] Install Firebase CLI: `npm install -g firebase-tools`
- [ ] Login to Firebase: `firebase login`

## ✅ Infrastructure Setup

### Cloud SQL Database
- [ ] Create PostgreSQL instance: `founder-sourcing-db`
- [ ] Create database: `founder_sourcing_agent`
- [ ] Create user: `founder_app`
- [ ] Set secure password
- [ ] Note connection name for environment variables

### Secret Manager
- [ ] Store database password
- [ ] Store application secret key
- [ ] Store API keys (Harvest, Gemini)

### Service Account
- [ ] Create service account: `founder-sourcing-sa`
- [ ] Grant Cloud SQL Client role
- [ ] Grant Secret Manager Secret Accessor role
- [ ] Download service account key

## ✅ GitHub Configuration

### Repository Secrets
- [ ] `GCP_SA_KEY` - Service account JSON key
- [ ] `DB_HOST` - Cloud SQL connection name
- [ ] `DB_PORT` - 5432
- [ ] `DB_NAME` - founder_sourcing_agent
- [ ] `DB_USER` - founder_app
- [ ] `DB_PASSWORD` - Database password
- [ ] `SECRET_KEY` - Application secret key
- [ ] `HARVEST_API_KEY` - Harvest API key
- [ ] `GEMINI_API_KEY` - Gemini API key
- [ ] `FIREBASE_SERVICE_ACCOUNT` - Firebase service account JSON

### Branch Protection
- [ ] Set up branch protection for `main`
- [ ] Require status checks to pass
- [ ] Require pull request reviews

## ✅ Code Preparation

### Backend
- [ ] Update `database.py` for production PostgreSQL
- [ ] Update CORS configuration in `main.py`
- [ ] Verify all environment variables are used
- [ ] Test locally with production environment

### Frontend
- [ ] Update API base URL for production
- [ ] Test build process: `npm run build`
- [ ] Verify environment variables are accessible

### Database Migrations
- [ ] Test migrations locally
- [ ] Verify schema matches application models
- [ ] Prepare seed data

## ✅ Deployment

### Initial Deployment
- [ ] Push code to `main` branch
- [ ] Monitor GitHub Actions workflow
- [ ] Verify backend deployment to Cloud Run
- [ ] Verify frontend deployment to Firebase
- [ ] Test application functionality

### Post-Deployment Verification
- [ ] Test authentication system
- [ ] Test founder search functionality
- [ ] Test database operations
- [ ] Verify CORS is working
- [ ] Check application logs

## ✅ Monitoring & Security

### Monitoring Setup
- [ ] Enable Cloud Run monitoring
- [ ] Set up log aggregation
- [ ] Configure error alerting
- [ ] Monitor database performance

### Security Verification
- [ ] Verify HTTPS is enforced
- [ ] Check CORS configuration
- [ ] Validate JWT token security
- [ ] Review IAM permissions
- [ ] Test rate limiting

### Performance Testing
- [ ] Test application under load
- [ ] Verify auto-scaling works
- [ ] Monitor response times
- [ ] Check database connection pooling

## ✅ Documentation

### User Documentation
- [ ] Update README with deployment info
- [ ] Document API endpoints
- [ ] Create user guide
- [ ] Document troubleshooting steps

### Developer Documentation
- [ ] Document deployment process
- [ ] Update environment variable documentation
- [ ] Document database schema
- [ ] Create maintenance procedures

## ✅ Cost Optimization

### Resource Monitoring
- [ ] Set up billing alerts
- [ ] Monitor Cloud Run usage
- [ ] Monitor Cloud SQL usage
- [ ] Optimize resource allocation

### Cost Controls
- [ ] Set Cloud Run max instances to 10
- [ ] Use smallest Cloud SQL instance
- [ ] Enable scale-to-zero for Cloud Run
- [ ] Monitor monthly costs

## ✅ Backup & Recovery

### Database Backups
- [ ] Verify automatic backups are enabled
- [ ] Test backup restoration
- [ ] Document recovery procedures
- [ ] Set up backup monitoring

### Application Recovery
- [ ] Document rollback procedures
- [ ] Test deployment rollback
- [ ] Verify data integrity after rollback
- [ ] Document disaster recovery plan

---

## 🚨 Emergency Contacts

- **GCP Support**: https://cloud.google.com/support
- **Firebase Support**: https://firebase.google.com/support
- **GitHub Support**: https://support.github.com

## 📞 Quick Commands

```bash
# Check Cloud Run status
gcloud run services describe founder-sourcing-agent-backend --region=us-central1

# View logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Check database status
gcloud sql instances describe founder-sourcing-db

# Deploy manually
./deployment/scripts/deploy.sh
```
