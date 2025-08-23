"""
Main FastAPI server for the Founder Sourcing Agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Founder Sourcing Agent",
    description="AI-powered founder discovery for Pioneers",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
harvest_client = HarvestClient()
ai_analyzer = AIAnalyzer()
export_service = ExportService()

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
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Check if all services are working"""
    return {
        "status": "healthy",
        "services": {
            "harvest_api": "configured" if harvest_client.api_key else "mock_mode",
            "gemini_api": "configured" if ai_analyzer.api_key else "mock_mode"
        }
    }

@app.post("/search")
async def search_founders(criteria: SearchCriteria):
    """
    Main search endpoint - this is where the magic happens!
    
    Takes search criteria and returns ranked candidates
    """
    
    try:
        # Step 1: Search LinkedIn profiles using Harvest
        query = f"{criteria.industry or ''} {' '.join(criteria.founder_signals)} {' '.join(criteria.technical_signals)}".strip()
        
        print(f"🔍 Searching for: {query}")
        profiles = harvest_client.search_profiles(query, criteria.max_results,criteria=criteria.dict())
        print(f"📋 Found {len(profiles)} profiles")
        
        # Step 2: Analyze each profile with AI
        candidates = []
        for profile in profiles:
            print(f"🤖 Analyzing: {profile.get('name', 'Unknown')}")
            
            analysis = ai_analyzer.analyze_candidate(
                profile, 
                criteria.dict()
            )
            
            candidates.append(analysis)
        
        # Step 3: Sort by tier (A first, then B, then C)
        tier_order = {"A": 1, "B": 2, "C": 3}
        candidates.sort(key=lambda x: tier_order.get(x.get("tier", "C"), 3))
        
        # Step 4: Export to CSV
        csv_path = export_service.export_to_csv(candidates)
        summary = export_service.get_export_summary(candidates)
        
        print(f"✅ Search complete! Found {len(candidates)} candidates")
        
        return {
            "success": True,
            "candidates": candidates,
            "summary": summary,
            "export_path": csv_path,
            "search_query": query
        }
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_export(filename: str):
    """Download exported CSV files"""
    
    file_path = os.path.join("exports", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=filename
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )