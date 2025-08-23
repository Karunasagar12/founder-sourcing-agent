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
            # Correct authentication header for Harvest API
            self.session.headers.update({
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            })
    
    def search_profiles(self, query: str, max_results: int = 10, criteria: Dict = None) -> List[Dict]:
        """
        Search LinkedIn profiles using Harvest API with full parameter support
        Parameters: search, currentCompany, pastCompany, school, firstName, lastName, title, location, geoId, industryId, page
        """
        
        print(f"🔍 HARVEST DEBUG: Starting enhanced search")
        print(f"📋 Query: '{query}'")
        print(f"📊 Criteria: {criteria}")
        print(f"🔑 API Key exists: {bool(self.api_key)}")
        
        if not self.api_key:
            print("⚠️  No API key found - using mock data")
            return self._get_mock_profiles(query, max_results)
        
        try:
            # Use the exact endpoint from documentation
            endpoint = f"{self.base_url}/linkedin/profile-search"
            
            # Build comprehensive parameters using ALL available filters
            params = {"page": 1}
            
            # Parse query and criteria for specific parameters
            query_lower = query.lower()
            
            # 1. SCHOOL parameter - for business schools
            schools_detected = []
            french_schools = {
                "insead": "INSEAD",
                "hec": "HEC Paris", 
                "essec": "ESSEC Business School",
                "edhec": "EDHEC Business School",
                "em lyon": "EM Lyon",
                "polytechnique": "École Polytechnique",
                "sciences po": "Sciences Po"
            }
            
            for school_key, school_full in french_schools.items():
                if school_key in query_lower:
                    schools_detected.append(school_full)
            
            if schools_detected:
                params["school"] = ",".join(schools_detected[:2])  # Max 2 schools
                print(f"🏫 Targeting schools: {params['school']}")
            
            # 2. TITLE parameter - for specific roles
            titles_detected = []
            title_keywords = {
                "founder": "Founder",
                "ceo": "CEO", 
                "cto": "CTO",
                "chief technology officer": "Chief Technology Officer",
                "co-founder": "Co-founder",
                "president": "President",
                "director": "Director"
            }
            
            for title_key, title_full in title_keywords.items():
                if title_key in query_lower:
                    titles_detected.append(title_full)
            
            if titles_detected:
                params["title"] = ",".join(titles_detected[:2])  # Max 2 titles
                print(f"💼 Targeting titles: {params['title']}")
            
            # 3. LOCATION parameter
            if "france" in query_lower or "french" in query_lower:
                params["location"] = "France"
                print(f"📍 Targeting location: France")
            elif "paris" in query_lower:
                params["location"] = "Paris, France"
                print(f"📍 Targeting location: Paris")
            
            # 4. INDUSTRY filtering (if we can map to LinkedIn industry IDs)
            # Note: We'd need to look up LinkedIn industry IDs, but for now use search
            industry_terms = []
            if any(term in query_lower for term in ["fintech", "financial technology"]):
                industry_terms.append("fintech")
            if any(term in query_lower for term in ["artificial intelligence", "ai", "machine learning"]):
                industry_terms.append("artificial intelligence")
            if any(term in query_lower for term in ["technology", "tech", "software"]):
                industry_terms.append("technology")
            
            # 5. SEARCH parameter - for general terms not covered by specific filters
            search_terms = []
            remaining_words = query.split()
            
            # Remove words already captured by specific filters
            for word in remaining_words:
                word_lower = word.lower()
                if (word_lower not in [s.lower() for s in french_schools.keys()] and
                    word_lower not in [t.lower() for t in title_keywords.keys()] and
                    word_lower not in ["france", "french", "paris"] and
                    word_lower not in ["fintech", "ai", "technology", "tech"]):
                    search_terms.append(word)
            
            # Add industry terms and important keywords to search
            search_terms.extend(industry_terms)
            if criteria:
                if criteria.get("founder_signals"):
                    search_terms.extend(["startup", "entrepreneurship"])
                if criteria.get("technical_signals"):
                    search_terms.extend(["technical", "engineering"])
            
            if search_terms:
                params["search"] = " ".join(search_terms[:4])  # Max 4 terms
                print(f"🔍 General search terms: {params['search']}")
            
            # 6. CURRENTCOMPANY parameter - could target specific types
            if "startup" in query_lower:
                # We could add logic here to target startup companies
                # For now, we'll rely on other filters
                pass
            
            print(f"📞 Making API call to: {endpoint}")
            print(f"📋 With comprehensive params: {params}")
            
            response = self.session.get(endpoint, params=params)
            
            print(f"📊 Response status: {response.status_code}")
            print(f"📝 Response headers: {dict(response.headers)}")
            print(f"🔤 Response text (first 500 chars): {response.text[:500]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📄 JSON keys in response: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    # Extract profiles from Harvest API response structure
                    profiles = []
                    if isinstance(data, dict) and "elements" in data:
                        raw_profiles = data["elements"]
                        total_found = data.get("pagination", {}).get("totalElements", 0)
                        
                        print(f"📊 Found {total_found} total profiles matching specific filters")
                        print(f"📋 Processing {len(raw_profiles)} profiles from this page")
                        
                        # Convert Harvest format to our internal format
                        for idx, profile in enumerate(raw_profiles[:max_results]):
                            name = profile.get("name", "LinkedIn Member")
                            position = profile.get("position", "")
                            location_data = profile.get("location", {})
                            
                            converted_profile = {
                                "name": name,
                                "linkedin_url": self._build_linkedin_url(profile),
                                "current_company": self._extract_company_from_position(position),
                                "current_role": position or "Unknown Role",
                                "location": location_data.get("linkedinText", "") if isinstance(location_data, dict) else str(location_data),
                                "summary": self._create_profile_summary(profile),
                                "experience": self._infer_experience_from_role(position),
                                "education": self._extract_education_hints(position),
                                "email": None,  # Not provided by basic search
                                "profile_id": profile.get("id", ""),
                                "photo": profile.get("photo", ""),
                                "hidden": profile.get("hidden", True),
                                # Add filter match info for debugging
                                "matched_filters": {
                                    "school": params.get("school"),
                                    "title": params.get("title"), 
                                    "location": params.get("location"),
                                    "search": params.get("search")
                                }
                            }
                            
                            print(f"  {idx+1}. {name} - {position[:50]}...")
                            profiles.append(converted_profile)
                    
                    if profiles:
                        print(f"✅ Successfully found {len(profiles)} profiles using targeted filters!")
                        return profiles
                    else:
                        print(f"⚠️  No profiles found with current filters")
                        print(f"💡 Suggestion: Try broader search terms or different filter combinations")
                        print(f"📊 Full response structure: {data}")
                
                except ValueError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"🔤 Raw response: {response.text}")
            
            elif response.status_code == 401:
                print(f"❌ Authentication failed - check API key")
            elif response.status_code == 429:
                print(f"❌ Rate limit exceeded - try again later")  
            else:
                print(f"❌ API returned status {response.status_code}")
                print(f"🔤 Error response: {response.text}")
            
            print("🔄 Using mock data as fallback")
            return self._get_mock_profiles(query, max_results)
            
        except requests.RequestException as e:
            print(f"❌ Harvest API error: {e}")
            print(f"🔄 Falling back to mock data")
            return self._get_mock_profiles(query, max_results)
    
    def _build_linkedin_url(self, profile: Dict) -> str:
        """Build LinkedIn URL from profile data"""
        if profile.get("linkedinUrl"):
            return profile["linkedinUrl"]
        elif profile.get("publicIdentifier"):
            return f"https://www.linkedin.com/in/{profile['publicIdentifier']}"
        else:
            # For hidden profiles, return a placeholder
            return f"https://linkedin.com/in/profile-{profile.get('id', 'hidden')}"
    
    def _extract_company_from_position(self, position: str) -> str:
        """Extract company name from position string"""
        if not position:
            return "Unknown Company"
        
        # Common patterns in different languages
        separators = [" at ", " presso ", " @ ", " - ", " chez ", " bei ", " en "]
        
        for separator in separators:
            if separator in position:
                parts = position.split(separator)
                if len(parts) > 1:
                    company = parts[-1].strip()
                    # Remove common suffixes
                    for suffix in [" | ", " |"]:
                        if suffix in company:
                            company = company.split(suffix)[0]
                    return company[:50]  # Limit length
        
        # If no separator found, try to extract from role patterns
        if "|" in position:
            # Format like "Role | Company | Description"
            parts = [p.strip() for p in position.split("|")]
            if len(parts) >= 2:
                # Usually company is the second part
                return parts[1][:50]
        
        return "Unknown Company"
    
    def _create_profile_summary(self, profile: Dict) -> str:
        """Create a comprehensive profile summary"""
        name = profile.get("name", "Professional")
        position = profile.get("position", "")
        location_data = profile.get("location", {})
        location = location_data.get("linkedinText", "") if isinstance(location_data, dict) else str(location_data)
        
        summary_parts = []
        
        # Name handling
        if name and name != "LinkedIn Member":
            summary_parts.append(f"{name} is a professional")
        else:
            summary_parts.append("LinkedIn professional")
        
        # Role analysis
        if position:
            role_lower = position.lower()
            if any(word in role_lower for word in ["founder", "ceo", "fondatore"]):
                summary_parts.append("with entrepreneurial leadership experience")
            elif any(word in role_lower for word in ["cto", "technical", "engineer", "developer"]):
                summary_parts.append("with strong technical background")
            elif any(word in role_lower for word in ["director", "manager", "vp", "chief"]):
                summary_parts.append("in senior management role")
            
            summary_parts.append(f"currently working as {position[:100]}")
        
        # Location
        if location:
            summary_parts.append(f"based in {location}")
        
        # Industry insights
        if position:
            position_lower = position.lower()
            if any(word in position_lower for word in ["ai", "artificial intelligence", "machine learning"]):
                summary_parts.append("specializing in AI/ML technologies")
            elif any(word in position_lower for word in ["fintech", "financial technology", "payments"]):
                summary_parts.append("working in fintech sector")
            elif any(word in position_lower for word in ["startup", "innovation", "venture"]):
                summary_parts.append("focused on innovation and startups")
        
        return ". ".join(summary_parts) + "."
    
    def _infer_experience_from_role(self, position: str) -> List[Dict]:
        """Infer experience level from role"""
        if not position:
            return []
        
        experience = []
        position_lower = position.lower()
        
        # Infer seniority level
        if any(word in position_lower for word in ["founder", "ceo", "chief"]):
            experience.append({
                "level": "executive",
                "type": "leadership",
                "years_inferred": "10+",
                "source": "role_analysis"
            })
        elif any(word in position_lower for word in ["director", "vp", "head"]):
            experience.append({
                "level": "senior",
                "type": "management", 
                "years_inferred": "7-15",
                "source": "role_analysis"
            })
        elif any(word in position_lower for word in ["senior", "lead", "principal"]):
            experience.append({
                "level": "senior",
                "type": "specialist",
                "years_inferred": "5-10",
                "source": "role_analysis"
            })
        
        return experience
    
    def _extract_education_hints(self, position: str) -> List[Dict]:
        """Try to extract education hints from position"""
        education = []
        if not position:
            return education
        
        # French business schools
        french_schools = {
            "INSEAD": "INSEAD Business School",
            "HEC": "HEC Paris", 
            "ESSEC": "ESSEC Business School",
            "EDHEC": "EDHEC Business School",
            "EM Lyon": "EM Lyon Business School",
            "Polytechnique": "École Polytechnique",
            "Sciences Po": "Sciences Po Paris"
        }
        
        position_upper = position.upper()
        for short_name, full_name in french_schools.items():
            if short_name.upper() in position_upper:
                education.append({
                    "school": full_name,
                    "degree": "Business/Engineering (inferred)",
                    "source": "profile_text",
                    "confidence": "medium"
                })
                break
        
        return education
    
    def _get_mock_profiles(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock LinkedIn profiles for testing"""
        
        # Create mock profiles based on query
        mock_profiles = []
        
        if "france" in query.lower() or "french" in query.lower():
            mock_profiles = [
                {
                    "name": "Marie Dubois",
                    "linkedin_url": "https://linkedin.com/in/mariedubois",
                    "current_company": "French Tech Startup",
                    "current_role": "Co-founder & CEO",
                    "location": "Paris, France",
                    "summary": "INSEAD MBA graduate, serial entrepreneur in fintech. Founded 2 startups, 8 years experience in financial technology.",
                    "experience": [{"company": "French Tech Startup", "role": "Co-founder", "years": "2020-Present"}],
                    "education": [{"school": "INSEAD", "degree": "MBA"}],
                    "email": "marie@frenchtech.fr"
                },
                {
                    "name": "Pierre Martin",
                    "linkedin_url": "https://linkedin.com/in/pierremartin",
                    "current_company": "AI Innovation Lab",
                    "current_role": "CTO & Co-founder", 
                    "location": "Lyon, France",
                    "summary": "HEC Paris alumnus, technical founder with 12 years in AI and machine learning. Expert in deep learning applications.",
                    "experience": [{"company": "AI Innovation Lab", "role": "CTO", "years": "2018-Present"}],
                    "education": [{"school": "HEC Paris", "degree": "Grande École"}],
                    "email": "pierre@ailab.fr"
                }
            ]
        else:
            # Default mock profiles
            mock_profiles = [
                {
                    "name": "Sarah Chen",
                    "linkedin_url": "https://linkedin.com/in/sarahchen",
                    "current_company": "TechFlow AI",
                    "current_role": "CEO & Co-founder",
                    "location": "San Francisco, CA",
                    "summary": "Serial entrepreneur with 12 years in fintech. Previously founded PayFlow (acquired by Stripe).",
                    "experience": [{"company": "PayFlow", "role": "Founder & CEO", "years": "2018-2022"}],
                    "education": [{"school": "Stanford University", "degree": "MS Computer Science"}],
                    "email": "sarah@techflow.ai"
                }
            ]
        
        return mock_profiles[:max_results]

# Test function
if __name__ == "__main__":
    client = HarvestClient()
    profiles = client.search_profiles("founder France INSEAD fintech", 3)
    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        print(f"- {profile['name']} at {profile['current_company']}")