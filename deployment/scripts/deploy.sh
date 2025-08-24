#!/bin/bash

# Simple Deployment Script for Founder Sourcing Agent
# This script orchestrates the deployment process

set -e

# Configuration
PROJECT_ID="founder-sourcing-agent"
REGION="us-central1"
SERVICE_NAME="founder-sourcing-agent-backend"

echo "🚀 Starting deployment of Founder Sourcing Agent..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with Google Cloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# 1. Deploy backend to Cloud Run
echo "🔧 Deploying backend to Cloud Run..."
cd backend

# Build and push Docker image
echo "🐳 Building and pushing Docker image..."
docker build -f ../deployment/backend/Dockerfile -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --min-instances 0

# Get backend URL
BACKEND_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
echo "✅ Backend deployed at: $BACKEND_URL"

# 2. Deploy frontend to Firebase
echo "🎨 Deploying frontend to Firebase..."
cd ../frontend

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm ci

# Update production environment with backend URL
echo "⚙️ Updating production environment..."
sed -i "s|https://founder-sourcing-agent-backend-xxxxx-uc.a.run.app|$BACKEND_URL|g" ../deployment/frontend/env.production

# Build for production
echo "🔨 Building frontend for production..."
cp ../deployment/frontend/env.production .env.production
npm run build

# Deploy to Firebase
echo "🔥 Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your application is now live:"
echo "Frontend: https://founder-sourcing-agent.web.app"
echo "Backend API: $BACKEND_URL"
echo "API Documentation: $BACKEND_URL/docs"
