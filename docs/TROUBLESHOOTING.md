# 🔧 Troubleshooting Guide

> **Founder Sourcing Agent - Common Issues & Solutions**

**Developed by:** [Karunasagar Mohansundar](https://github.com/Karunasagar12)

This guide helps you resolve common issues encountered while developing, deploying, or using the Founder Sourcing Agent.

---

## 📋 Table of Contents

- [Development Issues](#development-issues)
- [Deployment Issues](#deployment-issues)
- [API Issues](#api-issues)
- [Database Issues](#database-issues)
- [Authentication Issues](#authentication-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

---

## 💻 Development Issues

### Frontend Development

#### Issue: `npm install` fails
**Symptoms:**
- Package installation errors
- Version conflicts
- Network timeouts

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use specific Node.js version
nvm use 18.17.0

# Check for network issues
npm config set registry https://registry.npmjs.org/
```

#### Issue: Development server won't start
**Symptoms:**
- Port already in use
- Vite server fails to start
- Hot reload not working

**Solutions:**
```bash
# Check for processes using port 3000
lsof -i :3000
# or on Windows
netstat -ano | findstr :3000

# Kill process using port
kill -9 <PID>

# Start on different port
npm run dev -- --port 3001

# Clear Vite cache
rm -rf node_modules/.vite
```

#### Issue: React components not rendering
**Symptoms:**
- Blank page
- Console errors
- Component not updating

**Solutions:**
```bash
# Check browser console for errors
# Clear browser cache
# Check component imports

# Verify React version compatibility
npm list react react-dom

# Check for TypeScript errors
npx tsc --noEmit
```

### Backend Development

#### Issue: Python dependencies not installing
**Symptoms:**
- pip install errors
- Version conflicts
- Missing packages

**Solutions:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Create fresh virtual environment
python -m venv venv_new
source venv_new/bin/activate  # Windows: venv_new\Scripts\activate

# Install with specific versions
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.11+
```

#### Issue: FastAPI server won't start
**Symptoms:**
- Uvicorn startup errors
- Port conflicts
- Import errors

**Solutions:**
```bash
# Check for port conflicts
lsof -i :8000

# Start with debug mode
uvicorn main:app --reload --log-level debug

# Check for missing environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Verify imports
python -c "from main import app; print('App loaded successfully')"
```

#### Issue: Database connection errors
**Symptoms:**
- Connection refused
- Authentication failed
- Database not found

**Solutions:**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Verify connection string
echo $DATABASE_URL

# Test connection manually
psql $DATABASE_URL

# Create database if missing
createdb founder_sourcing_agent
```

---

## 🚀 Deployment Issues

### GitHub Actions Deployment

#### Issue: CI/CD pipeline fails
**Symptoms:**
- Build failures
- Test failures
- Deployment errors

**Solutions:**
```bash
# Check GitHub Actions logs
# Verify secrets are set correctly
# Check for environment-specific issues

# Common fixes:
# 1. Update Node.js version in workflow
# 2. Check API key permissions
# 3. Verify GCP service account permissions
```

#### Issue: Frontend deployment fails
**Symptoms:**
- Firebase deployment errors
- Build artifacts missing
- Environment variables not set

**Solutions:**
```bash
# Check Firebase configuration
firebase projects:list

# Verify build output
ls -la frontend/dist/

# Check environment variables
cat frontend/.env.production

# Manual deployment test
firebase deploy --only hosting
```

#### Issue: Backend deployment fails
**Symptoms:**
- Docker build errors
- Cloud Run deployment fails
- Container startup issues

**Solutions:**
```bash
# Test Docker build locally
docker build -f deployment/backend/Dockerfile -t test-backend .

# Check container logs
docker logs <container_id>

# Verify environment variables
gcloud run services describe founder-sourcing-agent-backend

# Test locally with production config
ENVIRONMENT=production uvicorn main:app
```

### Production Issues

#### Issue: Application not accessible
**Symptoms:**
- 404 errors
- DNS resolution issues
- SSL certificate problems

**Solutions:**
```bash
# Check service status
gcloud run services list

# Verify domain configuration
firebase hosting:channel:list

# Check SSL certificate
curl -I https://founder-sourcing-agent.web.app

# Test backend health
curl https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app/health
```

#### Issue: Performance problems
**Symptoms:**
- Slow response times
- Timeout errors
- High resource usage

**Solutions:**
```bash
# Check Cloud Run metrics
gcloud run services describe founder-sourcing-agent-backend

# Monitor resource usage
gcloud monitoring metrics list

# Check database performance
# Review query optimization
# Implement caching strategies
```

---

## 🔌 API Issues

### Authentication Problems

#### Issue: JWT token invalid
**Symptoms:**
- 401 Unauthorized errors
- Token expiration
- Invalid signature

**Solutions:**
```bash
# Check token expiration
# Verify SECRET_KEY configuration
# Check token format

# Test authentication endpoint
curl -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

#### Issue: CORS errors
**Symptoms:**
- Browser CORS errors
- Preflight request failures
- Cross-origin blocked

**Solutions:**
```bash
# Check CORS configuration
# Verify allowed origins
# Test with different origins

# Update CORS settings in main.py
ALLOWED_ORIGINS = [
    "https://founder-sourcing-agent.web.app",
    "http://localhost:3000"
]
```

### API Endpoint Issues

#### Issue: Search endpoint fails
**Symptoms:**
- 500 Internal Server Error
- Timeout errors
- Invalid response format

**Solutions:**
```bash
# Check API logs
gcloud logging read "resource.type=cloud_run_revision"

# Test with minimal payload
curl -X POST https://api.example.com/search \
  -H "Content-Type: application/json" \
  -d '{"max_results": 1}'

# Verify external API keys
echo $HARVEST_API_KEY
echo $GOOGLE_GEMINI_API_KEY
```

#### Issue: Export endpoint fails
**Symptoms:**
- File generation errors
- Download link broken
- CSV format issues

**Solutions:**
```bash
# Check file permissions
ls -la backend/exports/

# Verify disk space
df -h

# Test export with minimal data
# Check CSV encoding
# Verify file path configuration
```

---

## 🗄️ Database Issues

### Connection Problems

#### Issue: Database connection timeout
**Symptoms:**
- Connection pool exhausted
- Slow queries
- Connection refused

**Solutions:**
```bash
# Check connection pool settings
# Monitor active connections
# Optimize query performance

# Test connection
psql $DATABASE_URL -c "SELECT version();"

# Check connection limits
SHOW max_connections;
SHOW max_connections_per_user;
```

#### Issue: Migration failures
**Symptoms:**
- Schema update errors
- Data type conflicts
- Constraint violations

**Solutions:**
```bash
# Check migration status
alembic current

# Run migrations manually
alembic upgrade head

# Check for conflicts
alembic check

# Rollback if needed
alembic downgrade -1
```

### Data Issues

#### Issue: Data corruption
**Symptoms:**
- Inconsistent data
- Missing records
- Duplicate entries

**Solutions:**
```bash
# Check data integrity
# Run database consistency checks
# Review application logs

# Backup before fixes
pg_dump $DATABASE_URL > backup.sql

# Check for duplicates
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

---

## 🔐 Authentication Issues

### User Management

#### Issue: User registration fails
**Symptoms:**
- Email already exists
- Password validation errors
- Database constraint violations

**Solutions:**
```bash
# Check email uniqueness
SELECT email FROM users WHERE email = 'test@example.com';

# Verify password requirements
# Check email format validation
# Review registration logs
```

#### Issue: Password reset not working
**Symptoms:**
- Reset email not sent
- Token expiration
- Invalid reset links

**Solutions:**
```bash
# Check email configuration
# Verify SMTP settings
# Test email delivery

# Check token expiration
# Verify reset link format
# Review email templates
```

### Session Management

#### Issue: Users logged out unexpectedly
**Symptoms:**
- Session timeout
- Token refresh failures
- Multiple device conflicts

**Solutions:**
```bash
# Check token expiration settings
# Verify refresh token logic
# Review session management

# Test token refresh
curl -X POST https://api.example.com/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

## ⚡ Performance Issues

### Frontend Performance

#### Issue: Slow page loading
**Symptoms:**
- Long initial load times
- Slow component rendering
- Large bundle size

**Solutions:**
```bash
# Analyze bundle size
npm run build -- --analyze

# Check for unused dependencies
npm audit

# Optimize images and assets
# Implement code splitting
# Add loading states
```

#### Issue: API calls slow
**Symptoms:**
- Long response times
- Request timeouts
- Poor user experience

**Solutions:**
```bash
# Implement request caching
# Add loading indicators
# Optimize API endpoints
# Use request debouncing
```

### Backend Performance

#### Issue: High response times
**Symptoms:**
- Slow API responses
- Database query delays
- External API timeouts

**Solutions:**
```bash
# Profile database queries
# Implement caching
# Optimize external API calls
# Add connection pooling

# Monitor performance
gcloud monitoring metrics list
```

#### Issue: Memory leaks
**Symptoms:**
- Increasing memory usage
- Application crashes
- Poor performance over time

**Solutions:**
```bash
# Monitor memory usage
# Check for resource leaks
# Implement proper cleanup
# Review garbage collection
```

---

## 🛠️ Debugging Tools

### Frontend Debugging

#### Browser Developer Tools
```javascript
// Console debugging
console.log('Debug info:', data);
console.error('Error:', error);

// Network tab for API calls
// Performance tab for bottlenecks
// Application tab for storage
```

#### React Developer Tools
- Install React Developer Tools extension
- Inspect component state
- Monitor re-renders
- Debug hooks

### Backend Debugging

#### Logging
```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add debug statements
logger.debug(f"Processing request: {request_data}")
logger.error(f"Error occurred: {error}")
```

#### FastAPI Debug Mode
```bash
# Enable debug mode
uvicorn main:app --reload --log-level debug

# Check request/response
# Monitor database queries
# Trace external API calls
```

### Database Debugging

#### Query Analysis
```sql
-- Enable query logging
SET log_statement = 'all';

-- Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes;
```

---

## 🆘 Getting Help

### Before Asking for Help

1. **Check existing documentation**
   - [API Documentation](docs/API.md)
   - [Backend README](backend/README.md)
   - [Frontend README](frontend/README.md)

2. **Search existing issues**
   - Check GitHub Issues for similar problems
   - Review closed issues for solutions

3. **Gather information**
   - Error messages and logs
   - Environment details
   - Steps to reproduce

### Creating an Issue

Use the **bug report template**:

```markdown
## Issue Description
Clear description of the problem

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Node.js: [e.g., 18.17.0]
- Python: [e.g., 3.11.0]

## Error Messages
Paste error messages and logs

## Additional Context
Screenshots, configuration files, etc.
```

### Contact Information

- **GitHub Issues**: [Create an issue](https://github.com/Karunasagar12/founder-sourcing-agent/issues)
- **Developer**: [Karunasagar Mohansundar](https://github.com/Karunasagar12)
- **Repository**: [Founder Sourcing Agent](https://github.com/Karunasagar12/founder-sourcing-agent)

---

## 📚 Additional Resources

### Documentation
- [FastAPI Troubleshooting](https://fastapi.tiangolo.com/tutorial/debugging/)
- [React Debugging](https://react.dev/learn/react-developer-tools)
- [PostgreSQL Troubleshooting](https://www.postgresql.org/docs/current/runtime-config-logging.html)

### Tools
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Postman](https://www.postman.com/) - API testing
- [pgAdmin](https://www.pgadmin.org/) - Database management

---

*Last updated: January 2024*
