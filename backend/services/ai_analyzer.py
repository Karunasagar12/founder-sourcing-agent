"""
AI Analyzer using Google Gemini
This analyzes LinkedIn profiles and determines if they match our criteria
Updated to preserve data source information from harvest client
"""

import requests
import os
import json
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    """AI service for analyzing founder profiles"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
        
    def analyze_candidate(self, profile: Dict, criteria: Dict) -> Dict:
        """
        Analyze a candidate profile against search criteria
        
        Args:
            profile: LinkedIn profile data
            criteria: Search criteria
            
        Returns:
            Analysis with summary, tier, and justification
        """
        
        # Preserve original data source from harvest client
        original_data_source = profile.get('data_source', 'unknown')
        is_real_data = original_data_source == 'linkedin_real'
        
        profile_label = "[REAL]" if is_real_data else "[MOCK]"
        print(f"🤖 GEMINI DEBUG: Analyzing {profile.get('name', 'Unknown')} {profile_label}")
        
        if not self.api_key:
            print("⚠️  No Gemini API key - using mock analysis")
            return self._get_mock_analysis(profile, criteria, original_data_source)
        
        try:
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(profile, criteria)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            # Parse the response
            analysis = self._parse_gemini_response(response, profile)
            
            # CRITICAL: Preserve original data source
            analysis['data_source'] = original_data_source
            
            return analysis
            
        except Exception as e:
            print(f"❌ AI Analysis error: {e}")
            # Fallback to mock analysis but preserve data source
            return self._get_mock_analysis(profile, criteria, original_data_source)
    
    def _create_analysis_prompt(self, profile: Dict, criteria: Dict) -> str:
        """Create an enhanced prompt for AI analysis with clear Tier A criteria"""
        
        prompt = f"""You are an expert founder sourcing analyst. Analyze this candidate against the criteria and assign the appropriate tier.
            CANDIDATE PROFILE:
            Name: {profile.get('name', 'Unknown')}
            Current Role: {profile.get('current_role', 'Unknown')}
            Company: {profile.get('current_company', 'Unknown')}
            Location: {profile.get('location', 'Unknown')}
            Profile Summary: {profile.get('summary', 'No additional info')}

            SEARCH CRITERIA:
            Industry: {criteria.get('industry', 'Any')}
            Required Experience: {criteria.get('experience_depth', 'Any')} years
            Founder Signals Required: {criteria.get('founder_signals', [])}
            Technical Signals Required: {criteria.get('technical_signals', [])}

            TIER ASSIGNMENT RULES:
            **TIER A** (Excellent Match - 85%+ criteria met):
            - Shows MULTIPLE founder signals (founder + CEO/CTO + startup experience)
            - Clear industry match with specific expertise
            - Evidence of significant experience (senior roles, multiple companies, or clear depth)
            - Technical signals present if required (CTO, engineering, product)
            - Strong overall profile indicating proven track record

            **TIER B** (Good Match - 60-84% criteria met):
            - Shows SOME founder signals OR strong technical background
            - Industry relevance but not perfect match
            - Some experience indicators but not fully clear
            - Missing 1-2 key criteria but overall positive

            **TIER C** (Possible Match - 40-59% criteria met):
            - Minimal criteria match
            - Unclear experience or background
            - Weak industry connection
            - Missing most key signals

            ANALYSIS INSTRUCTIONS:
            1. Be generous with Tier A for candidates showing multiple strong signals
            2. Look for implicit signals (CTO implies technical expertise, Co-founder implies startup experience)
            3. Consider compound roles (CTO & Co-founder = multiple signals)
            4. Weight current roles heavily (current CTO at startup = strong technical + startup leadership)

            Respond with ONLY this JSON format:
            {{
                "profile_type": "business|technical",
                "summary": "Compelling 2-line summary highlighting strongest qualifications",
                "tier": "A|B|C", 
                "match_justification": "Detailed explanation focusing on how multiple criteria are met",
                "confidence_score": 0.85
            }}
            """
        
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Make API call to Google Gemini with advanced model"""
        
        print(f"🤖 GEMINI DEBUG: Making API call")
        print(f"🔑 API Key exists: {bool(self.api_key)}")
        
        # Use Gemini 1.5 Pro (better than the basic gemini-pro)
        url = f"{self.base_url}/models/gemini-1.5-pro:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,        # Lower temperature for more consistent JSON
                "topK": 20,                # Fewer tokens for more focused responses
                "topP": 0.8,               # More focused sampling
                "maxOutputTokens": 512,    # Shorter responses
            }
        }
        
        # Add API key to URL
        url += f"?key={self.api_key}"
        
        print(f"📞 Calling: {url}")
        print(f"📋 Payload size: {len(str(data))} characters")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📝 Response headers: {dict(response.headers)}")
        print(f"🔤 Response text (first 1000 chars): {response.text[:1000]}")
        
        if response.status_code != 200:
            print(f"❌ Gemini API error: {response.text}")
            raise requests.RequestException(f"API returned {response.status_code}: {response.text}")
        
        return response.json()
    
    def _parse_gemini_response(self, response: Dict, profile: Dict) -> Dict:
        """Parse Gemini API response"""
        
        try:
            print(f"📄 Gemini response structure: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
            
            # Extract text from Gemini response
            if "candidates" in response and len(response["candidates"]) > 0:
                content = response["candidates"][0]["content"]["parts"][0]["text"]
                print(f"🔤 Gemini raw content: {content[:200]}")
                
                # Clean the content - remove markdown formatting
                content = content.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                # Try to parse as JSON
                analysis = json.loads(content)
                
                # Add profile info WITHOUT overriding data_source
                analysis.update({
                    "name": profile.get("name", "Unknown"),
                    "linkedin_url": profile.get("linkedin_url", ""),
                    "email": profile.get("email", ""),
                    "current_company": profile.get("current_company", ""),
                    "current_role": profile.get("current_role", ""),
                    "contacts": [profile.get("linkedin_url", "")],
                    "source_links": [profile.get("linkedin_url", "")]
                    # NOTE: NOT setting data_source here - preserving from harvest client
                })
                
                print(f"✅ Successfully parsed Gemini response for {profile.get('name')}")
                return analysis
            else:
                print(f"❌ No candidates in Gemini response")
                
        except (KeyError, json.JSONDecodeError, IndexError) as e:
            print(f"❌ Failed to parse Gemini response: {e}")
            if "candidates" in response:
                print(f"📊 Candidates structure: {response['candidates']}")
        
        print(f"🔄 Using mock analysis fallback")
        return self._get_mock_analysis(profile, {}, profile.get('data_source', 'unknown'))
    
    def _get_mock_analysis(self, profile: Dict, criteria: Dict, original_data_source: str = 'unknown') -> Dict:
        """Generate mock analysis for testing - preserving data source"""
        
        name = profile.get("name", "Unknown")
        role = profile.get("current_role", "")
        company = profile.get("current_company", "")
        summary_text = profile.get("summary", "")
        
        # Simple logic for mock analysis
        is_technical = any(word in role.lower() for word in ["cto", "engineer", "technical", "developer", "ai", "tech"])
        is_founder = any(word in role.lower() for word in ["founder", "ceo", "co-founder", "fondatore"])
        has_experience = any(word in role.lower() for word in ["senior", "lead", "director", "vp", "chief"])
        
        # Determine tier based on simple rules
        if is_founder and (is_technical or has_experience):
            tier = "A"
        elif is_founder or (is_technical and has_experience):
            tier = "B"  
        else:
            tier = "C"
        
        analysis = {
            "name": name,
            "profile_type": "technical" if is_technical else "business",
            "summary": f"{name} brings {role} experience at {company}. " + 
                      (summary_text[:80] + "..." if len(summary_text) > 80 else summary_text or "Professional with relevant background."),
            "tier": tier,
            "match_justification": f"Candidate shows {'technical leadership' if is_technical else 'business experience'} " +
                                 f"{'and founder background' if is_founder else ''}. " +
                                 f"Current role as {role} demonstrates relevant expertise for the search criteria.",
            "confidence_score": 0.75,
            "linkedin_url": profile.get("linkedin_url", ""),
            "email": profile.get("email", ""),
            "current_company": company,
            "current_role": role,
            "contacts": [profile.get("linkedin_url", "")],
            "source_links": [profile.get("linkedin_url", "")]
            # NOTE: NOT setting data_source here - will be preserved by caller
        }
        
        return analysis

# Test function
if __name__ == "__main__":
    analyzer = AIAnalyzer()
    
    # Test with mock profile
    test_profile = {
        "name": "Test Founder",
        "current_role": "CEO & Co-founder", 
        "current_company": "StartupCo",
        "summary": "Experienced entrepreneur with 10 years in tech",
        "linkedin_url": "https://linkedin.com/in/test",
        "data_source": "mock_data"  # Test preserving this
    }
    
    test_criteria = {
        "industry": "tech",
        "founder_signals": ["repeat_founder"]
    }
    
    result = analyzer.analyze_candidate(test_profile, test_criteria)
    print(f"Analysis: {result['name']} - Tier {result['tier']} - Source: {result.get('data_source', 'MISSING!')}")