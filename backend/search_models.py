"""
Database models for search results and history
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class SearchResult(Base):
    """Model for storing search results"""
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Search criteria
    search_criteria = Column(JSON, nullable=False)  # Store the original search criteria
    search_query = Column(String(500), nullable=False)
    industry = Column(String(100))
    experience_depth = Column(Integer)
    max_results = Column(Integer)
    
    # Results summary
    total_candidates = Column(Integer, default=0)
    tier_distribution = Column(JSON)  # {"A": 2, "B": 3, "C": 1}
    profile_distribution = Column(JSON)  # {"business": 3, "technical": 3}
    
    # Export info
    export_path = Column(String(255))
    csv_filename = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidates = relationship("SearchCandidate", back_populates="search_result", cascade="all, delete-orphan")

class SearchCandidate(Base):
    """Model for storing individual candidates from search results"""
    __tablename__ = "search_candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey("search_results.id"), nullable=False)
    
    # Candidate data
    name = Column(String(255), nullable=False)
    linkedin_url = Column(String(500))
    email = Column(String(255))
    current_company = Column(String(255))
    current_role = Column(String(255))
    
    # Analysis results
    tier = Column(String(10))  # A, B, C
    profile_type = Column(String(50))  # business, technical
    summary = Column(Text)
    match_justification = Column(Text)
    confidence_score = Column(Float)
    
    # Additional data
    contacts = Column(JSON)  # Array of contact links
    source_links = Column(JSON)  # Array of source links
    data_source = Column(String(50))  # linkedin_real, mock, etc.
    source_note = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    search_result = relationship("SearchResult", back_populates="candidates")
