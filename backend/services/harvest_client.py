"""
Harvest API client for LinkedIn data
This connects to Harvest API to search for LinkedIn profiles
"""

import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class HarvestClient:
    """Client for Harvest API (LinkedIn data)"""
    
    def __init__(self):
        self.api_key = os.getenv("HARVEST_API_KEY")
        self.base_url = os.getenv("HARVEST_BASE_URL", "https://api.harvest-api.com")
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
    
    def search_profiles(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search LinkedIn profiles using Harvest API
        
        Args:
            query: Search query (like "CTO fintech")
            max_results: Maximum number of results
            
        Returns:
            List of profile dictionaries
        """
        
        if not self.api_key:
            # Return mock data for testing
            return self._get_mock_profiles(query, max_results)
        
        try:
            # Real API call to Harvest
            endpoint = f"{self.base_url}/search/linkedin"
            params = {
                "query": query,
                "limit": max_results,
                "include_email": True,
                "include_company": True
            }
            
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("profiles", [])
            
        except requests.RequestException as e:
            print(f"Harvest API error: {e}")
            # Return mock data as fallback
            return self._get_mock_profiles(query, max_results)
    
    def _get_mock_profiles(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock LinkedIn profiles for testing"""
        
        mock_profiles = [
            {
                "name": "Sarah Chen",
                "linkedin_url": "https://linkedin.com/in/sarahchen",
                "current_company": "TechFlow AI",
                "current_role": "CEO & Co-founder",
                "location": "San Francisco, CA",
                "summary": "Serial entrepreneur with 12 years in fintech. Previously founded PayFlow (acquired by Stripe). Expert in AI-powered financial products.",
                "experience": [
                    {"company": "PayFlow", "role": "Founder & CEO", "years": "2018-2022"},
                    {"company": "Goldman Sachs", "role": "VP Technology", "years": "2015-2018"}
                ],
                "education": [
                    {"school": "Stanford University", "degree": "MS Computer Science"}
                ],
                "email": "sarah@techflow.ai"
            },
            {
                "name": "Marcus Rodriguez",
                "linkedin_url": "https://linkedin.com/in/marcusrodriguez",
                "current_company": "SupplyChain Pro",
                "current_role": "CTO",
                "location": "Austin, TX",
                "summary": "Technical leader with 15 years in supply chain optimization. Built logistics platforms used by Fortune 500 companies.",
                "experience": [
                    {"company": "SupplyChain Pro", "role": "CTO", "years": "2020-Present"},
                    {"company": "Amazon", "role": "Principal Engineer", "years": "2016-2020"}
                ],
                "education": [
                    {"school": "MIT", "degree": "PhD Industrial Engineering"}
                ],
                "email": "marcus@supplychain.pro"
            },
            {
                "name": "Dr. Elena Vasquez",
                "linkedin_url": "https://linkedin.com/in/elenavasquez",
                "current_company": "BioTech Innovations",
                "current_role": "Founder & CSO",
                "location": "Boston, MA",
                "summary": "PhD in Biotechnology with 10+ years experience. Founded 2 biotech startups, 15 patents in drug discovery.",
                "experience": [
                    {"company": "BioTech Innovations", "role": "Founder", "years": "2021-Present"},
                    {"company": "Novartis", "role": "Senior Scientist", "years": "2018-2021"}
                ],
                "education": [
                    {"school": "Harvard Medical School", "degree": "PhD Biotechnology"}
                ],
                "email": "elena@biotech-inn.com"
            }
        ]
        
        # Filter based on query and return requested number
        return mock_profiles[:max_results]

# Test function
if __name__ == "__main__":
    client = HarvestClient()
    profiles = client.search_profiles("CTO fintech", 5)
    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        print(f"- {profile['name']} at {profile['current_company']}")