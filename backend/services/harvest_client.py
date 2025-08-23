"""
Harvest API client for LinkedIn data
This connects to Harvest API to search for LinkedIn profiles
Updated with enhanced mock data and clear data source labeling
"""

import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import random

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
            print("⚠️  No API key found - using enhanced mock data only")
            return self._get_enhanced_mock_profiles(query, max_results)
        
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
                                "data_source": "linkedin_real",  # Mark as real LinkedIn data
                                # Add filter match info for debugging
                                "matched_filters": {
                                    "school": params.get("school"),
                                    "title": params.get("title"), 
                                    "location": params.get("location"),
                                    "search": params.get("search")
                                }
                            }
                            
                            print(f"  {idx+1}. {name} - {position[:50]}... [REAL LINKEDIN DATA]")
                            profiles.append(converted_profile)
                    
                    if profiles:
                        print(f"✅ Successfully found {len(profiles)} REAL LinkedIn profiles!")
                        
                        # Smart Supplementation: Add mock data if we didn't get enough real profiles
                        if len(profiles) < max_results:
                            mock_needed = max_results - len(profiles)
                            print(f"📋 Need {mock_needed} more profiles to reach requested {max_results}")
                            print(f"🎭 Adding {mock_needed} mock profiles to supplement real data")
                            
                            mock_profiles = self._get_enhanced_mock_profiles(query, mock_needed)
                            combined_profiles = profiles + mock_profiles
                            
                            print(f"✅ Final result: {len(profiles)} real + {len(mock_profiles)} mock = {len(combined_profiles)} total profiles")
                            return combined_profiles
                        else:
                            print(f"🎯 Got enough real profiles ({len(profiles)}) - no mock data needed")
                            return profiles
                    else:
                        print(f"⚠️  No real profiles found - using enhanced mock data only")
                        return self._get_enhanced_mock_profiles(query, max_results)
                
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
            
            print("🔄 API call failed - using enhanced mock data as complete fallback")
            return self._get_enhanced_mock_profiles(query, max_results)
            
        except requests.RequestException as e:
            print(f"❌ Harvest API error: {e}")
            print(f"🔄 Using enhanced mock data as complete fallback")
            return self._get_enhanced_mock_profiles(query, max_results)
    
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
    
    def _get_enhanced_mock_profiles(self, query: str, max_results: int) -> List[Dict]:
        """Generate enhanced mock LinkedIn profiles with clear labeling"""
        
        print(f"🎭 Generating {max_results} MOCK profiles for query: '{query}'")
        print(f"💡 These profiles are clearly labeled as mock data for testing purposes")
        
        # Enhanced base profiles with variety
        base_profiles = [
            # Fintech founders
            {
                "name": "Mock: Sarah Chen",
                "linkedin_url": "https://linkedin.com/in/mock-sarahchen",
                "current_company": "FinFlow AI (Mock Company)",
                "current_role": "CEO & Co-founder (Mock Profile)",
                "location": "San Francisco, CA",
                "summary": "MOCK DATA: Serial entrepreneur with 12 years in fintech. Previously founded PayFlow (acquired by Stripe). Expert in financial technology and AI-powered payment solutions.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Marcus Rodriguez",
                "linkedin_url": "https://linkedin.com/in/mock-marcusrodriguez", 
                "current_company": "BlockChain Ventures (Mock Company)",
                "current_role": "CTO & Technical Co-founder (Mock Profile)",
                "location": "Austin, TX",
                "summary": "MOCK DATA: Technical leader with 15 years building financial platforms. Led engineering teams at 3 fintech startups, 2 successful exits. Expert in blockchain and distributed systems.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Dr. Elena Vasquez",
                "linkedin_url": "https://linkedin.com/in/mock-elenavasquez",
                "current_company": "MedTech Innovations (Mock Company)", 
                "current_role": "Founder & Chief Science Officer (Mock Profile)",
                "location": "Boston, MA",
                "summary": "MOCK DATA: PhD in Biotechnology with 10+ years experience. Founded 2 biotech startups, 15 patents in drug discovery. Expert in AI-driven pharmaceutical research.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            
            # AI/Tech founders
            {
                "name": "Mock: James Park",
                "linkedin_url": "https://linkedin.com/in/mock-jamespark",
                "current_company": "DeepMind Analytics (Mock Company)",
                "current_role": "Founder & CEO (Mock Profile)",
                "location": "Seattle, WA", 
                "summary": "MOCK DATA: AI researcher turned entrepreneur. Former Google Brain scientist, founded 3 AI startups. Expert in machine learning and computer vision applications.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Lisa Thompson",
                "linkedin_url": "https://linkedin.com/in/mock-lisathompson",
                "current_company": "SaaS Growth Partners (Mock Company)",
                "current_role": "Serial Entrepreneur & Investor (Mock Profile)",
                "location": "New York, NY",
                "summary": "MOCK DATA: Built and sold 4 SaaS companies over 18 years. Current angel investor and board member at 12 startups. Expert in B2B software and growth strategies.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: David Kim",
                "linkedin_url": "https://linkedin.com/in/mock-davidkim",
                "current_company": "Quantum Computing Lab (Mock Company)",
                "current_role": "CTO & Co-founder (Mock Profile)", 
                "location": "Palo Alto, CA",
                "summary": "MOCK DATA: MIT PhD in Computer Science, 8 years at IBM Research. Co-founded quantum computing startup with $50M Series A. 25 patents in quantum algorithms.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            
            # Industry-specific founders
            {
                "name": "Mock: Maria Santos",
                "linkedin_url": "https://linkedin.com/in/mock-mariasantos",
                "current_company": "CleanTech Ventures (Mock Company)",
                "current_role": "Founder & President (Mock Profile)",
                "location": "Denver, CO",
                "summary": "MOCK DATA: Clean energy entrepreneur with 14 years experience. Founded 2 renewable energy companies, raised $200M+ in funding. Board member at 5 cleantech startups.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Ahmed Hassan",
                "linkedin_url": "https://linkedin.com/in/mock-ahmedhassan",
                "current_company": "EdTech Solutions (Mock Company)",
                "current_role": "Founder & Chief Product Officer (Mock Profile)",
                "location": "Chicago, IL",
                "summary": "MOCK DATA: Former teacher turned edtech entrepreneur. Built learning platforms used by 2M+ students. Expert in educational technology and product development.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Jennifer Wu",
                "linkedin_url": "https://linkedin.com/in/mock-jenniferwu",
                "current_company": "BioAI Labs (Mock Company)",
                "current_role": "Founder & CTO (Mock Profile)",
                "location": "San Diego, CA",
                "summary": "MOCK DATA: Biotech engineer with Stanford PhD. Founded AI-powered drug discovery platform. Former Genentech researcher with 20+ publications in Nature/Science.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Robert Johnson",
                "linkedin_url": "https://linkedin.com/in/mock-robertjohnson", 
                "current_company": "Enterprise Software Co (Mock Company)",
                "current_role": "Serial Founder & Board Chairman (Mock Profile)",
                "location": "Atlanta, GA",
                "summary": "MOCK DATA: 20-year enterprise software veteran. Founded and sold 3 companies (total exits: $500M+). Currently chairman at 4 B2B software startups.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            
            # International founders  
            {
                "name": "Mock: Pierre Dubois",
                "linkedin_url": "https://linkedin.com/in/mock-pierredubois",
                "current_company": "European Fintech Hub (Mock Company)",
                "current_role": "Co-founder & Managing Director (Mock Profile)",
                "location": "London, UK",
                "summary": "MOCK DATA: INSEAD MBA, former Goldman Sachs. Founded 2 fintech companies in Europe. Expert in financial regulations and cross-border payment systems.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Priya Sharma",
                "linkedin_url": "https://linkedin.com/in/mock-priyasharma",
                "current_company": "Mumbai Tech Ventures (Mock Company)", 
                "current_role": "Founder & Technical Director (Mock Profile)",
                "location": "Mumbai, India",
                "summary": "MOCK DATA: IIT graduate with 12 years in software development. Founded 3 tech startups serving Indian market. Expert in mobile-first product development.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Klaus Mueller",
                "linkedin_url": "https://linkedin.com/in/mock-klausmueller",
                "current_company": "German Innovation Labs (Mock Company)",
                "current_role": "Founder & Chief Engineer (Mock Profile)", 
                "location": "Berlin, Germany",
                "summary": "MOCK DATA: Technical University Munich PhD. Founded IoT startup acquired by Siemens. Expert in industrial automation and Industry 4.0 technologies.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            
            # Diverse experience levels
            {
                "name": "Mock: Emily Carter",
                "linkedin_url": "https://linkedin.com/in/mock-emilycarter",
                "current_company": "NextGen Startups (Mock Company)",
                "current_role": "Founder & CEO (Mock Profile)",
                "location": "Portland, OR",
                "summary": "MOCK DATA: Former McKinsey consultant, 8 years in startup ecosystem. Founded sustainability-focused marketplace. Expertise in business strategy and operations.",
                "profile_type": "business",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            },
            {
                "name": "Mock: Michael Brown",
                "linkedin_url": "https://linkedin.com/in/mock-michaelbrown",
                "current_company": "Cloud Infrastructure Inc (Mock Company)",
                "current_role": "Co-founder & VP Engineering (Mock Profile)", 
                "location": "Dallas, TX",
                "summary": "MOCK DATA: Former Amazon engineer with 10 years experience. Co-founded cloud security startup. Expert in distributed systems and cybersecurity.",
                "profile_type": "technical",
                "data_source": "mock_data",
                "mock_note": "This is simulated data for testing purposes"
            }
        ]
        
        # Filter profiles based on query for more realistic results
        filtered_profiles = []
        query_lower = query.lower()
        
        for profile in base_profiles:
            # Check if profile matches query criteria
            match_score = 0
            profile_text = f"{profile['summary']} {profile['current_role']} {profile['current_company']}".lower()
            
            # Industry matching
            if any(term in profile_text for term in ['fintech', 'financial']) and 'fintech' in query_lower:
                match_score += 3
            if any(term in profile_text for term in ['ai', 'artificial intelligence', 'machine learning']) and ('ai' in query_lower or 'artificial' in query_lower):
                match_score += 3
            if 'technology' in query_lower and any(term in profile_text for term in ['tech', 'software', 'engineering']):
                match_score += 2
                
            # Founder signals  
            if 'founder' in query_lower and 'founder' in profile_text:
                match_score += 2
            if 'cto' in query_lower and 'cto' in profile_text:
                match_score += 2
            if 'serial' in query_lower and ('serial' in profile_text or 'founded' in profile_text):
                match_score += 1
                
            # Add some randomness for variety
            match_score += random.random()
            
            filtered_profiles.append((profile, match_score))
        
        # Sort by match score and take top results
        filtered_profiles.sort(key=lambda x: x[1], reverse=True)
        selected_profiles = [p[0] for p in filtered_profiles[:max_results]]
        
        # If we still don't have enough, add some generic profiles
        while len(selected_profiles) < max_results and len(selected_profiles) < len(base_profiles):
            remaining = [p for p in base_profiles if p not in selected_profiles]
            if remaining:
                selected_profiles.extend(remaining[:max_results - len(selected_profiles)])
            else:
                break
                
        print(f"✅ Generated {len(selected_profiles)} MOCK profiles matching '{query}'")
        print(f"🎭 All mock profiles clearly labeled with 'Mock:' prefix and data source")
        return selected_profiles[:max_results]

# Test function
if __name__ == "__main__":
    client = HarvestClient()
    profiles = client.search_profiles("founder France INSEAD fintech", 3)
    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        print(f"- {profile['name']} at {profile['current_company']} [{profile.get('data_source', 'unknown')}]")