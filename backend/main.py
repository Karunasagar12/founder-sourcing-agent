"""
Main FastAPI server for the Founder Sourcing Agent
Updated with proper CORS configuration for frontend connection
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import os
from dotenv import load_dotenv

# Import our services
from services.harvest_client import HarvestClient
from services.ai_analyzer import AIAnalyzer  
from services.export_service import ExportService
from models import SearchCriteria, Candidate

# Import authentication modules (lazy import to avoid database connection during startup)
# from auth_router import router as auth_router
# from database import create_tables
# from auth_models import Base
# from database import engine

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Founder Sourcing Agent",
    description="AI-powered founder discovery for Pioneers",
    version="1.0.0"
)

# CORS Configuration - Environment-based
def get_cors_origins():
    """Get CORS origins based on environment"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        # Production: Only allow Firebase domains
        return [
            "https://founder-sourcing-agent.web.app",
            "https://founder-sourcing-agent.firebaseapp.com",
            "https://founder-sourcing-agent.web.app/",
            "https://founder-sourcing-agent.firebaseapp.com/"
        ]
    else:
        # Development: Allow local development servers
        return [
            "http://localhost:3000",  # React dev server
            "http://localhost:8080",  # Alternative dev server
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8080",
            "http://localhost:5500",  # Live Server
            "http://127.0.0.1:5500",
            "file://",  # For local HTML files
            "*"  # Allow all origins for development
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Optional: Serve static files (frontend) from backend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize services
harvest_client = HarvestClient()
ai_analyzer = AIAnalyzer()
export_service = ExportService()

# Create database tables (only in development)
# if os.getenv("ENVIRONMENT", "development") == "development":
#     Base.metadata.create_all(bind=engine)

# Include authentication router (lazy loading)
# app.include_router(auth_router)

@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "Founder Sourcing Agent API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "health": "/health", 
            "docs": "/docs",
            "auth": "/auth"
        },
        "frontend_url": "Open your index.html file or visit /static/index.html if serving static files"
    }

@app.get("/health")
async def health_check():
    """Check if all services are working"""
    print("🔍 Health check requested")
    
    return {
        "status": "healthy",
        "services": {
            "harvest_api": "disabled_for_debugging",
            "gemini_api": "disabled_for_debugging"
        },
        "cors": "enabled",
        "message": "Basic app is operational"
    }

@app.post("/search")
async def search_founders():
    """Temporary search endpoint for debugging"""
    return {
        "message": "Search endpoint temporarily disabled for debugging",
        "status": "maintenance"
    }

@app.get("/download/{filename:path}")
async def download_export(filename: str):
    """Temporary download endpoint for debugging"""
    return {
        "message": "Download endpoint temporarily disabled for debugging",
        "status": "maintenance"
    }

# Add a test endpoint for frontend debugging
@app.get("/test-connection")
async def test_connection():
    """Simple test endpoint for frontend connectivity"""
    return {
        "status": "connected",
        "message": "Frontend successfully connected to backend!",
        "timestamp": "2025-01-23T12:00:00Z"
    }

# Lazy loading for authentication endpoints
@app.get("/auth/test")
async def auth_test():
    """Test authentication endpoint with lazy loading"""
    try:
        from auth_router import router as auth_router
        return {"message": "Authentication module loaded successfully"}
    except Exception as e:
        return {"message": f"Authentication module failed to load: {str(e)}"}

@app.post("/auth/signup")
async def signup():
    """Lazy loading signup endpoint"""
    try:
        from auth_router import router as auth_router
        # This would normally delegate to the actual signup endpoint
        return {"message": "Signup endpoint available"}
    except Exception as e:
        return {"message": f"Signup endpoint failed to load: {str(e)}"}

@app.post("/auth/login")
async def login():
    """Lazy loading login endpoint"""
    try:
        from auth_router import router as auth_router
        # This would normally delegate to the actual login endpoint
        return {"message": "Login endpoint available"}
    except Exception as e:
        return {"message": f"Login endpoint failed to load: {str(e)}"}

if __name__ == "__main__":
    print("🚀 Starting Founder Sourcing Agent Backend...")
    print("🔗 CORS enabled for frontend connections")
    print("📱 Frontend should now be able to connect!")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )