"""
AI Analyzer using Google Gemini
This analyzes LinkedIn profiles and determines if they match our criteria
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
        
        if not self.api_key:
            # Use mock AI analysis for testing
            return self._get_mock_analysis(profile, criteria)
        
        try:
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(profile, criteria)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            # Parse the response
            return self._parse_gemini_response(response, profile)
            
        except Exception as e:
            print(f"AI Analysis error: {e}")
            # Fallback to mock analysis
            return self._get_mock_analysis(profile, criteria)
    
    def _create_analysis_prompt(self, profile: Dict, criteria: Dict) -> str:
        """Create a prompt for AI analysis"""
        
        prompt = f"""
        Analyze this founder candidate against the given criteria:

        CANDIDATE PROFILE:
        Name: {profile.get('name', 'Unknown')}
        Current Role: {profile.get('current_role', 'Unknown')}
        Company: {profile.get('current_company', 'Unknown')}
        Summary: {profile.get('summary', 'No summary available')}
        Experience: {json.dumps(profile.get('experience', []), indent=2)}
        Education: {json.dumps(profile.get('education', []), indent=2)}

        SEARCH CRITERIA:
        Industry: {criteria.get('industry', 'Any')}
        Experience Required: {criteria.get('experience_depth', 'Any')} years
        Founder Signals: {criteria.get('founder_signals', [])}
        Technical Signals: {criteria.get('technical_signals', [])}

        Please provide:
        1. PROFILE_TYPE: "business" or "technical" 
        2. SUMMARY: 2-4 line compelling summary of this candidate
        3. TIER: "A" (excellent match), "B" (good match), or "C" (okay match)
        4. JUSTIFICATION: Detailed explanation of why they match the criteria
        5. CONFIDENCE: Score from 0.0 to 1.0

        Format your response as JSON:
        {{
            "profile_type": "business|technical",
            "summary": "2-4 line summary here",
            "tier": "A|B|C", 
            "match_justification": "detailed justification",
            "confidence_score": 0.85
        }}
        """
        
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Make API call to Google Gemini"""
        
        url = f"{self.base_url}/models/gemini-pro:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        # Add API key to URL (Gemini uses query parameter)
        url += f"?key={self.api_key}"
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def _parse_gemini_response(self, response: Dict, profile: Dict) -> Dict:
        """Parse Gemini API response"""
        
        try:
            # Extract text from Gemini response
            content = response["candidates"][0]["content"]["parts"][0]["text"]
            
            # Try to parse as JSON
            analysis = json.loads(content)
            
            # Add profile info
            analysis.update({
                "name": profile.get("name", "Unknown"),
                "linkedin_url": profile.get("linkedin_url", ""),
                "email": profile.get("email", ""),
                "current_company": profile.get("current_company", ""),
                "current_role": profile.get("current_role", "")
            })
            
            return analysis
            
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Failed to parse Gemini response: {e}")
            return self._get_mock_analysis(profile, {})
    
    def _get_mock_analysis(self, profile: Dict, criteria: Dict) -> Dict:
        """Generate mock analysis for testing"""
        
        name = profile.get("name", "Unknown")
        role = profile.get("current_role", "")
        company = profile.get("current_company", "")
        summary_text = profile.get("summary", "")
        
        # Simple logic for mock analysis
        is_technical = any(word in role.lower() for word in ["cto", "engineer", "technical", "developer"])
        is_founder = any(word in role.lower() for word in ["founder", "ceo", "co-founder"])
        
        # Determine tier based on simple rules
        if is_founder and (is_technical or "years" in summary_text):
            tier = "A"
        elif is_founder or is_technical:
            tier = "B"  
        else:
            tier = "C"
        
        return {
            "name": name,
            "profile_type": "technical" if is_technical else "business",
            "summary": f"{name} brings {role} experience at {company}. " + 
                      (summary_text[:100] + "..." if len(summary_text) > 100 else summary_text),
            "tier": tier,
            "match_justification": f"Candidate shows {'technical leadership' if is_technical else 'business experience'} " +
                                 f"{'and founder background' if is_founder else ''}. " +
                                 f"Current role as {role} demonstrates relevant expertise.",
            "confidence_score": 0.75,
            "linkedin_url": profile.get("linkedin_url", ""),
            "email": profile.get("email", ""),
            "current_company": company,
            "current_role": role,
            "contacts": [profile.get("linkedin_url", ""), profile.get("email", "")],
            "source_links": [profile.get("linkedin_url", "")]
        }

# Test function
if __name__ == "__main__":
    analyzer = AIAnalyzer()
    
    # Test with mock profile
    test_profile = {
        "name": "Test Founder",
        "current_role": "CEO & Co-founder", 
        "current_company": "StartupCo",
        "summary": "Experienced entrepreneur with 10 years in tech",
        "linkedin_url": "https://linkedin.com/in/test"
    }
    
    test_criteria = {
        "industry": "tech",
        "founder_signals": ["repeat_founder"]
    }
    
    result = analyzer.analyze_candidate(test_profile, test_criteria)
    print(f"Analysis: {result['name']} - Tier {result['tier']}")