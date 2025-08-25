"""
Service for managing search history and results
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from search_models import SearchResult, SearchCandidate
from datetime import datetime

class SearchHistoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def save_search_result(self, user_id: int, search_criteria: Dict, search_response: Dict) -> SearchResult:
        """Save a complete search result to the database"""
        
        # Create the search result record
        search_result = SearchResult(
            user_id=user_id,
            search_criteria=search_criteria,
            search_query=search_response.get('search_query', ''),
            industry=search_criteria.get('industry'),
            experience_depth=search_criteria.get('experience_depth'),
            max_results=search_criteria.get('max_results'),
            total_candidates=search_response.get('summary', {}).get('total_candidates', 0),
            tier_distribution=search_response.get('summary', {}).get('tier_distribution', {}),
            profile_distribution=search_response.get('summary', {}).get('profile_distribution', {}),
            export_path=search_response.get('export_path', ''),
            csv_filename=search_response.get('export_path', '').split('/')[-1] if search_response.get('export_path') else None
        )
        
        self.db.add(search_result)
        self.db.commit()
        self.db.refresh(search_result)
        
        # Save individual candidates
        candidates = search_response.get('candidates', [])
        for candidate_data in candidates:
            candidate = SearchCandidate(
                search_result_id=search_result.id,
                name=candidate_data.get('name', 'Unknown'),
                linkedin_url=candidate_data.get('linkedin_url'),
                email=candidate_data.get('email'),
                current_company=candidate_data.get('current_company'),
                current_role=candidate_data.get('current_role'),
                tier=candidate_data.get('tier'),
                profile_type=candidate_data.get('profile_type'),
                summary=candidate_data.get('summary'),
                match_justification=candidate_data.get('match_justification'),
                confidence_score=candidate_data.get('confidence_score'),
                contacts=candidate_data.get('contacts', []),
                source_links=candidate_data.get('source_links', []),
                data_source=candidate_data.get('data_source'),
                source_note=candidate_data.get('source_note')
            )
            self.db.add(candidate)
        
        self.db.commit()
        return search_result
    
    def get_user_search_history(self, user_id: int, limit: int = 20) -> List[SearchResult]:
        """Get search history for a user"""
        return self.db.query(SearchResult)\
            .filter(SearchResult.user_id == user_id)\
            .order_by(SearchResult.created_at.desc())\
            .limit(limit)\
            .all()
    
    def get_search_result_by_id(self, search_result_id: int, user_id: int) -> Optional[SearchResult]:
        """Get a specific search result with candidates"""
        return self.db.query(SearchResult)\
            .filter(SearchResult.id == search_result_id, SearchResult.user_id == user_id)\
            .first()
    
    def delete_search_result(self, search_result_id: int, user_id: int) -> bool:
        """Delete a search result (and all its candidates)"""
        search_result = self.get_search_result_by_id(search_result_id, user_id)
        if search_result:
            self.db.delete(search_result)
            self.db.commit()
            return True
        return False
    
    def get_search_statistics(self, user_id: int) -> Dict:
        """Get search statistics for a user"""
        total_searches = self.db.query(SearchResult)\
            .filter(SearchResult.user_id == user_id)\
            .count()
        
        total_candidates = self.db.query(SearchCandidate)\
            .join(SearchResult)\
            .filter(SearchResult.user_id == user_id)\
            .count()
        
        # Get tier distribution across all searches
        tier_counts = {}
        profile_counts = {}
        
        search_results = self.get_user_search_history(user_id, limit=100)
        for result in search_results:
            if result.tier_distribution:
                for tier, count in result.tier_distribution.items():
                    tier_counts[tier] = tier_counts.get(tier, 0) + count
            
            if result.profile_distribution:
                for profile_type, count in result.profile_distribution.items():
                    profile_counts[profile_type] = profile_counts.get(profile_type, 0) + count
        
        return {
            "total_searches": total_searches,
            "total_candidates": total_candidates,
            "tier_distribution": tier_counts,
            "profile_distribution": profile_counts
        }
