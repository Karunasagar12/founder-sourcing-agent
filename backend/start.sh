#!/bin/bash

# Startup script for Founder Sourcing Agent Backend

set -e

echo "🚀 Starting Founder Sourcing Agent Backend..."

# Start the application directly without database setup
echo "🌟 Starting Gunicorn server..."
exec gunicorn main:app --config gunicorn.conf.py
