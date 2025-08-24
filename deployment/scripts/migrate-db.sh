#!/bin/bash

# Database Migration Script for Founder Sourcing Agent
# This script runs database migrations on Cloud SQL

set -e

# Configuration
PROJECT_ID="founder-sourcing-agent"
INSTANCE_NAME="founder-sourcing-db"
DATABASE_NAME="founder_sourcing_agent"

echo "🗄️ Running database migrations for Founder Sourcing Agent..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed. Please install it first."
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Get the connection name
CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format="value(connectionName)")

echo "📋 Running migrations on instance: $INSTANCE_NAME"

# Run migrations in order
echo "🔄 Running migration 001_users.sql..."
gcloud sql import sql $INSTANCE_NAME \
    gs://$PROJECT_ID-migrations/001_users.sql \
    --database=$DATABASE_NAME \
    --quiet || echo "Migration 001 already applied or failed"

echo "🔄 Running migration 002_searches.sql..."
gcloud sql import sql $INSTANCE_NAME \
    gs://$PROJECT_ID-migrations/002_searches.sql \
    --database=$DATABASE_NAME \
    --quiet || echo "Migration 002 already applied or failed"

# Initialize database with seed data
echo "🌱 Running database initialization..."
gcloud sql import sql $INSTANCE_NAME \
    gs://$PROJECT_ID-migrations/init.sql \
    --database=$DATABASE_NAME \
    --quiet || echo "Initialization already applied or failed"

echo "✅ Database migrations completed!"

# Show database status
echo "📊 Database status:"
gcloud sql databases list --instance=$INSTANCE_NAME

echo ""
echo "🔗 Connection information:"
echo "Instance: $INSTANCE_NAME"
echo "Database: $DATABASE_NAME"
echo "Connection Name: $CONNECTION_NAME"
