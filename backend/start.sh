#!/bin/bash

# Startup script for Founder Sourcing Agent Backend

set -e

echo "🚀 Starting Founder Sourcing Agent Backend..."

# Wait for database to be ready (if using Cloud SQL)
if [ -n "$DB_HOST" ]; then
    echo "⏳ Waiting for database connection..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "✅ Database connection established"
fi

# Run database migrations
echo "🔄 Running database migrations..."
python -c "
from database import create_tables
from auth_models import Base
from database import engine
Base.metadata.create_all(bind=engine)
print('Database tables created/updated')
"

# Start the application
echo "🌟 Starting Gunicorn server..."
exec gunicorn main:app --config gunicorn.conf.py
