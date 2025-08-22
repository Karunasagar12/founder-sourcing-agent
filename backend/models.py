"""
Data models for the Founder Sourcing Agent
These define the structure of our data
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Literal
from enum import Enum


class ProfileType(str, Enum):
    """Business or technical focus"""
    BUSINESS = "business"
    TECHNICAL = "technical"


class Tier(str, Enum):
    """Match quality ranking"""
    A = "A"  # Best fit
    B = "B"  # Good fit  
    C = "C"  # Okay fit


class SearchCriteria(BaseModel):
    """What we're looking for in founders"""
    experience_depth: Optional[int] = None
    industry: Optional[str] = None
    founder_signals: List[str] = []
    technical_signals: List[str] = []
    max_results: int = 10


class Candidate(BaseModel):
    """Information about potential founders"""
    name: str
    profile_type: ProfileType
    summary: str
    contacts: List[str] = []
    source_links: List[str] = []
    match_justification: str
    tier: Tier