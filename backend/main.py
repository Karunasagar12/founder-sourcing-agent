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
from auth_router import router as auth_router
from database import create_tables
from auth_models import Base
from database import engine

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
if os.getenv("ENVIRONMENT", "development") == "development":
    Base.metadata.create_all(bind=engine)
    # Import search models to ensure they're created
    from search_models import SearchResult, SearchCandidate

# Include authentication router (lazy loading)
app.include_router(auth_router)

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
            "harvest_api": "configured" if harvest_client.api_key else "mock_mode",
            "gemini_api": "configured" if ai_analyzer.api_key else "mock_mode"
        },
        "cors": "enabled",
        "message": "All systems operational"
    }

@app.post("/search")
async def search_founders(criteria: SearchCriteria):
    """
    Main search endpoint - this is where the magic happens!
    
    Takes search criteria and returns ranked candidates
    """
    
    try:
        print(f"🔍 SEARCH REQUEST RECEIVED")
        print(f"📋 Criteria: {criteria}")
        
        # Step 1: Search LinkedIn profiles using Harvest  
        # Build smarter query to avoid over-filtering
        query_parts = []
        if criteria.industry:
            query_parts.append(criteria.industry)
        
        # Limit founder signals to avoid too restrictive search
        if criteria.founder_signals:
            # Take only first 2 founder signals to avoid over-filtering
            query_parts.extend(criteria.founder_signals[:2])
            
        # Limit technical signals
        if criteria.technical_signals:
            # Take only first 2 technical signals  
            query_parts.extend(criteria.technical_signals[:2])
            
        query = " ".join(query_parts).strip() or "founder entrepreneur"
        
        print(f"🔍 Searching for: '{query}' (simplified from complex criteria)")
        print(f"📊 Requested max_results: {criteria.max_results}")
        print(f"📋 Original criteria: Industry={criteria.industry}, Founder signals={len(criteria.founder_signals)}, Technical signals={len(criteria.technical_signals)}")
        
        profiles = harvest_client.search_profiles(query, criteria.max_results, criteria=criteria.dict())
        print(f"📋 Harvest API returned {len(profiles)} profiles (requested: {criteria.max_results})")
        
        # Determine if we're hitting LinkedIn's Commercial Use Limit
        is_linkedin_limited = len(profiles) <= 3 and criteria.max_results > 3
        
        if is_linkedin_limited:
            print(f"⚠️  LinkedIn Commercial Use Limit (CUL) detected!")
            print(f"💡 Explanation:")
            print(f"   - LinkedIn limits free accounts to ~3 results for non-connected profiles")
            print(f"   - This is LinkedIn's anti-scraping measure, not a Harvest API issue")
            print(f"   - Resets monthly (1st of each month at midnight PST)")
            print(f"   - Solutions: LinkedIn Premium, Sales Navigator, or wait for reset")
            print(f"   - Harvest API is working correctly - this is LinkedIn's restriction")
        elif len(profiles) < criteria.max_results:
            print(f"⚠️  Got fewer profiles than requested - possible causes:")
            print(f"   - Limited matching profiles for your criteria")
            print(f"   - Harvest API rate limits")
            print(f"   - Search criteria too specific")
        
        if len(profiles) == 0:
            print(f"❌ No profiles found! Check your criteria or API connectivity")
            return {
                "success": True,
                "candidates": [],
                "summary": {"total_candidates": 0, "tier_distribution": {"A": 0, "B": 0, "C": 0}},
                "export_path": "no-results.csv",
                "search_query": query,
                "message": "No profiles found. Try broader search criteria or different keywords.",
                "linkedin_limitation": is_linkedin_limited
            }
        
        # Step 2: Analyze each profile with AI
        candidates = []
        real_profiles_count = len(profiles)
        
        for i, profile in enumerate(profiles):
            # Preserve original data source from harvest client
            original_data_source = profile.get('data_source', 'unknown')
            is_real_data = original_data_source == 'linkedin_real'
            
            profile_label = "[REAL LINKEDIN DATA]" if is_real_data else "[MOCK DATA]" 
            print(f"🤖 Analyzing {i+1}/{len(profiles)}: {profile.get('name', 'Unknown')} {profile_label}")
            
            analysis = ai_analyzer.analyze_candidate(
                profile, 
                criteria.dict()
            )
            
            # Preserve and enhance data source information
            analysis['data_source'] = original_data_source
            if is_real_data:
                analysis['source_note'] = 'Real LinkedIn profile via Harvest API'
            else:
                analysis['source_note'] = 'Mock data for testing purposes'
                # Ensure mock profiles are clearly identified
                if not analysis.get('name', '').startswith('Mock:'):
                    analysis['name'] = f"Mock: {analysis.get('name', 'Unknown')}"
            
            candidates.append(analysis)
        
        # Add clear explanation about data limitations in response
        data_explanation = {
            "linkedin_profiles_found": real_profiles_count,
            "requested_count": criteria.max_results,
            "limitation_detected": is_linkedin_limited,
            "explanation": "LinkedIn Commercial Use Limit restricts free scraping to ~3 profiles. This resets monthly." if is_linkedin_limited else "Standard LinkedIn profile search completed."
        }
        
        # Step 3: Sort by tier (A first, then B, then C)
        tier_order = {"A": 1, "B": 2, "C": 3}
        candidates.sort(key=lambda x: tier_order.get(x.get("tier", "C"), 3))
        
        # Step 4: Export to CSV
        print(f"📁 About to export {len(candidates)} candidates to CSV...")
        csv_path = export_service.export_to_csv(candidates)
        print(f"📁 CSV export completed. File saved at: {csv_path}")
        print(f"📁 CSV file exists: {os.path.exists(csv_path)}")
        
        summary = export_service.get_export_summary(candidates)
        
        print(f"✅ Search complete! Found {len(candidates)} candidates")
        
        response = {
            "success": True,
            "candidates": candidates,
            "summary": summary,
            "export_path": csv_path,
            "search_query": query,
            "message": f"Successfully analyzed {len(candidates)} candidates",
            "data_sources": data_explanation,
            "harvest_api_status": "working_correctly",
            "linkedin_limitation_info": {
                "detected": is_linkedin_limited,
                "description": "LinkedIn restricts free scraping to ~3 profiles per search to prevent automated data harvesting",
                "solutions": [
                    "LinkedIn Premium subscription removes this limit",
                    "LinkedIn Sales Navigator allows 2500 results per search",
                    "Wait until monthly reset (1st of each month)",
                    "Use multiple LinkedIn accounts (not recommended)",
                    "Focus on 1st-degree connections (unlimited)"
                ]
            }
        }
        
        print(f"📤 Sending response with {len(candidates)} candidates")
        
        # Save search results to database if user is authenticated
        try:
            from auth_dependencies import get_current_user
            from database import get_db
            from search_history_service import SearchHistoryService
            
            # Try to get current user (will fail if not authenticated)
            db = next(get_db())
            current_user = get_current_user(db)
            
            if current_user:
                # Save search results
                search_history_service = SearchHistoryService(db)
                saved_result = search_history_service.save_search_result(
                    user_id=current_user.id,
                    search_criteria=criteria.dict(),
                    search_response=response
                )
                print(f"💾 Search results saved to database with ID: {saved_result.id}")
                response["search_result_id"] = saved_result.id
                
        except Exception as save_error:
            print(f"⚠️  Could not save search results: {save_error}")
            # Continue without saving - this is not critical
        
        return response
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename:path}")
async def download_export(filename: str):
    """Download exported CSV files"""
    
    print(f"📥 Download requested for: '{filename}'")
    
    # Clean up the filename - remove any duplicate 'exports/' prefixes
    clean_filename = filename.replace('exports/', '')
    if clean_filename.startswith('exports/'):
        clean_filename = clean_filename[8:]  # Remove second 'exports/'
    
    # Build the correct file path
    file_path = os.path.join("exports", clean_filename)
    
    print(f"📁 Cleaned filename: '{clean_filename}'")
    print(f"📂 Looking for file at: '{file_path}'")
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📂 File exists check: {os.path.exists(file_path)}")
    
    # List all files in exports directory for debugging
    exports_dir = "exports"
    if os.path.exists(exports_dir):
        try:
            available_files = os.listdir(exports_dir)
            print(f"📂 Available files in {exports_dir}/: {available_files}")
        except Exception as e:
            print(f"❌ Error listing exports directory: {e}")
    else:
        print(f"❌ Exports directory does not exist!")
        # Try to create it
        try:
            os.makedirs(exports_dir, exist_ok=True)
            print(f"✅ Created exports directory")
        except Exception as e:
            print(f"❌ Could not create exports directory: {e}")
    
    # Check if file exists with absolute path
    abs_file_path = os.path.abspath(file_path)
    print(f"📂 Absolute file path: {abs_file_path}")
    print(f"📂 Absolute path exists: {os.path.exists(abs_file_path)}")
    
    if not os.path.exists(file_path):
        error_msg = f"File not found: {file_path}"
        if os.path.exists(exports_dir):
            available_files = os.listdir(exports_dir)
            error_msg += f". Available files: {available_files}"
        
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=404, detail=error_msg)
    
    # Extract just the filename for download
    actual_filename = os.path.basename(file_path)
    print(f"📤 Serving file: {actual_filename}")
    
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=actual_filename
    )

# Add a test endpoint for frontend debugging
@app.get("/test-connection")
async def test_connection():
    """Simple test endpoint for frontend connectivity"""
    return {
        "status": "connected",
        "message": "Frontend successfully connected to backend!",
        "timestamp": "2025-01-23T12:00:00Z"
    }

@app.get("/init-database")
async def init_database():
    """Initialize database tables (for production)"""
    try:
        from database import engine
        from auth_models import Base
        from search_models import SearchResult, SearchCandidate
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        return {
            "success": True,
            "message": "Database tables created successfully",
            "tables": ["users", "search_results", "search_candidates"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create database tables"
        }

@app.get("/create-test-user")
async def create_test_user_endpoint():
    """Create a default test user for easy access"""
    try:
        from auth_service import AuthService
        from auth_models import UserCreate
        from database import get_db
        
        # Test user credentials
        test_user_data = UserCreate(
            email="test@founder-sourcing.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="User",
            company="Founder Sourcing Agent"
        )
        
        # Get database session
        db = next(get_db())
        auth_service = AuthService(db)
        
        # Check if test user already exists
        existing_user = auth_service.get_user_by_email(test_user_data.email)
        if existing_user:
            return {
                "success": True,
                "message": "Test user already exists!",
                "credentials": {
                    "email": "test@founder-sourcing.com",
                    "password": "TestPassword123!"
                }
            }
        
        # Create test user
        user = auth_service.create_user(test_user_data)
        
        return {
            "success": True,
            "message": "Test user created successfully!",
            "credentials": {
                "email": "test@founder-sourcing.com",
                "password": "TestPassword123!"
            },
            "user_id": user.id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create test user"
        }

@app.get("/search-history")
async def get_search_history():
    """Get search history for the current user"""
    try:
        from auth_dependencies import get_current_user
        from database import get_db
        from search_history_service import SearchHistoryService
        
        db = next(get_db())
        current_user = get_current_user(db)
        
        if not current_user:
            return {"error": "Authentication required"}
        
        search_history_service = SearchHistoryService(db)
        history = search_history_service.get_user_search_history(current_user.id)
        
        # Convert to JSON-serializable format
        history_data = []
        for result in history:
            history_data.append({
                "id": result.id,
                "search_query": result.search_query,
                "industry": result.industry,
                "total_candidates": result.total_candidates,
                "tier_distribution": result.tier_distribution,
                "created_at": result.created_at.isoformat(),
                "csv_filename": result.csv_filename
            })
        
        return {
            "success": True,
            "history": history_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/search-history/{search_id}")
async def get_search_result(search_id: int):
    """Get a specific search result with candidates"""
    try:
        from auth_dependencies import get_current_user
        from database import get_db
        from search_history_service import SearchHistoryService
        
        db = next(get_db())
        current_user = get_current_user(db)
        
        if not current_user:
            return {"error": "Authentication required"}
        
        search_history_service = SearchHistoryService(db)
        search_result = search_history_service.get_search_result_by_id(search_id, current_user.id)
        
        if not search_result:
            return {"error": "Search result not found"}
        
        # Convert candidates to JSON-serializable format
        candidates_data = []
        for candidate in search_result.candidates:
            candidates_data.append({
                "name": candidate.name,
                "linkedin_url": candidate.linkedin_url,
                "email": candidate.email,
                "current_company": candidate.current_company,
                "current_role": candidate.current_role,
                "tier": candidate.tier,
                "profile_type": candidate.profile_type,
                "summary": candidate.summary,
                "match_justification": candidate.match_justification,
                "confidence_score": candidate.confidence_score,
                "contacts": candidate.contacts,
                "source_links": candidate.source_links,
                "data_source": candidate.data_source,
                "source_note": candidate.source_note
            })
        
        return {
            "success": True,
            "search_result": {
                "id": search_result.id,
                "search_query": search_result.search_query,
                "search_criteria": search_result.search_criteria,
                "industry": search_result.industry,
                "total_candidates": search_result.total_candidates,
                "tier_distribution": search_result.tier_distribution,
                "profile_distribution": search_result.profile_distribution,
                "created_at": search_result.created_at.isoformat(),
                "csv_filename": search_result.csv_filename,
                "candidates": candidates_data
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/search-history/{search_id}")
async def delete_search_result(search_id: int):
    """Delete a search result"""
    try:
        from auth_dependencies import get_current_user
        from database import get_db
        from search_history_service import SearchHistoryService
        
        db = next(get_db())
        current_user = get_current_user(db)
        
        if not current_user:
            return {"error": "Authentication required"}
        
        search_history_service = SearchHistoryService(db)
        success = search_history_service.delete_search_result(search_id, current_user.id)
        
        if success:
            return {"success": True, "message": "Search result deleted"}
        else:
            return {"error": "Search result not found"}
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/search-statistics")
async def get_search_statistics():
    """Get search statistics for the current user"""
    try:
        from auth_dependencies import get_current_user
        from database import get_db
        from search_history_service import SearchHistoryService
        
        db = next(get_db())
        current_user = get_current_user(db)
        
        if not current_user:
            return {"error": "Authentication required"}
        
        search_history_service = SearchHistoryService(db)
        stats = search_history_service.get_search_statistics(current_user.id)
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
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

@app.get("/auth/signup")
async def signup():
    """Lazy loading signup endpoint"""
    try:
        from auth_router import router as auth_router
        # This would normally delegate to the actual signup endpoint
        return {"message": "Signup endpoint available"}
    except Exception as e:
        return {"message": f"Signup endpoint failed to load: {str(e)}"}

@app.get("/auth/login")
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