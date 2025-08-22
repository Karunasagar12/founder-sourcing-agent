"""
Export service for saving results to CSV, database, or Airtable
"""

import csv
import json
import os
from typing import List, Dict
from datetime import datetime

class ExportService:
    """Handle exporting candidate results to various formats"""
    
    def __init__(self):
        self.export_dir = "exports"
        # Create exports directory if it doesn't exist
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_to_csv(self, candidates: List[Dict], filename: str = None) -> str:
        """
        Export candidates to CSV file
        
        Args:
            candidates: List of candidate dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"founder_candidates_{timestamp}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Define CSV columns matching assignment requirements
        fieldnames = [
            'name',
            'profile_type', 
            'summary',
            'contacts',
            'source_links',
            'match_justification',
            'tier',
            'current_company',
            'current_role',
            'confidence_score'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for candidate in candidates:
                # Prepare row data
                row = {}
                for field in fieldnames:
                    value = candidate.get(field, '')
                    
                    # Convert lists to comma-separated strings
                    if isinstance(value, list):
                        value = ', '.join(str(v) for v in value)
                    
                    row[field] = value
                
                writer.writerow(row)
        
        return filepath
    
    def export_to_json(self, candidates: List[Dict], filename: str = None) -> str:
        """Export candidates to JSON file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"founder_candidates_{timestamp}.json"
        
        filepath = os.path.join(self.export_dir, filename)
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "total_candidates": len(candidates),
            "candidates": candidates
        }
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        
        return filepath
    
    def get_export_summary(self, candidates: List[Dict]) -> Dict:
        """Generate summary statistics for export"""
        
        total = len(candidates)
        if total == 0:
            return {"total": 0}
        
        # Count by tier
        tier_counts = {"A": 0, "B": 0, "C": 0}
        profile_counts = {"business": 0, "technical": 0}
        
        for candidate in candidates:
            tier = candidate.get("tier", "C")
            if tier in tier_counts:
                tier_counts[tier] += 1
            
            profile_type = candidate.get("profile_type", "business")
            if profile_type in profile_counts:
                profile_counts[profile_type] += 1
        
        return {
            "total_candidates": total,
            "tier_distribution": tier_counts,
            "profile_distribution": profile_counts,
            "top_tier_percentage": round((tier_counts["A"] / total) * 100, 1)
        }

# Test function
if __name__ == "__main__":
    # Test with sample data
    test_candidates = [
        {
            "name": "Test Founder 1",
            "profile_type": "technical",
            "summary": "Experienced tech entrepreneur",
            "tier": "A",
            "contacts": ["test1@email.com"],
            "source_links": ["https://linkedin.com/in/test1"],
            "match_justification": "Strong technical background with founder experience"
        },
        {
            "name": "Test Founder 2", 
            "profile_type": "business",
            "summary": "Business leader with exits",
            "tier": "B",
            "contacts": ["test2@email.com"],
            "source_links": ["https://linkedin.com/in/test2"],
            "match_justification": "Good business experience and leadership"
        }
    ]
    
    exporter = ExportService()
    csv_path = exporter.export_to_csv(test_candidates)
    summary = exporter.get_export_summary(test_candidates)
    
    print(f"Exported to: {csv_path}")
    print(f"Summary: {summary}")