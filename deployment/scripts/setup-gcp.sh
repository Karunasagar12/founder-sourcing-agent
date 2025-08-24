#!/bin/bash

# GCP Project Setup Script for Founder Sourcing Agent
# This script sets up all necessary GCP services for production deployment

set -e

# Configuration
PROJECT_ID="founder-sourcing-agent"
REGION="us-central1"
ZONE="us-central1-a"

echo "🚀 Setting up GCP project for Founder Sourcing Agent..."

# 1. Create or set project
echo "📋 Setting up project..."
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com \
    iam.googleapis.com \
    containerregistry.googleapis.com

# 3. Create Cloud SQL instance
echo "🗄️ Creating Cloud SQL PostgreSQL instance..."
gcloud sql instances create founder-sourcing-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=$REGION \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup-start-time=02:00 \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=03:00 \
    --availability-type=zonal \
    --root-password="$(openssl rand -base64 32)"

# 4. Create database
echo "📊 Creating database..."
gcloud sql databases create founder_sourcing_agent \
    --instance=founder-sourcing-db

# 5. Create database user
echo "👤 Creating database user..."
DB_PASSWORD=$(openssl rand -base64 32)
gcloud sql users create founder_app \
    --instance=founder-sourcing-db \
    --password="$DB_PASSWORD"

# 6. Store secrets in Secret Manager
echo "🔐 Storing secrets in Secret Manager..."
echo "$DB_PASSWORD" | gcloud secrets create db-password --data-file=-
echo "$(openssl rand -base64 32)" | gcloud secrets create secret-key --data-file=-

# 7. Create service account for Cloud Run
echo "🔑 Creating service account..."
gcloud iam service-accounts create founder-sourcing-sa \
    --display-name="Founder Sourcing Agent Service Account"

# 8. Grant necessary permissions
echo "🔓 Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:founder-sourcing-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:founder-sourcing-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# 9. Configure Cloud Run to use service account
echo "⚙️ Configuring Cloud Run..."
gcloud run services update founder-sourcing-agent-backend \
    --service-account="founder-sourcing-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --region=$REGION || echo "Service doesn't exist yet, will be configured during deployment"

# 10. Get connection info
echo "📋 Getting connection information..."
DB_HOST=$(gcloud sql instances describe founder-sourcing-db --format="value(connectionName)")
DB_INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe founder-sourcing-db --format="value(connectionName)")

echo "✅ GCP setup completed!"
echo ""
echo "📋 Connection Information:"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Database Host: $DB_HOST"
echo "Database Name: founder_sourcing_agent"
echo "Database User: founder_app"
echo "Database Password: [stored in Secret Manager]"
echo "Secret Key: [stored in Secret Manager]"
echo ""
echo "🔗 Next steps:"
echo "1. Update your GitHub secrets with the connection information"
echo "2. Deploy your application using the GitHub Actions workflows"
echo "3. Configure Firebase project for frontend hosting"
