from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str = Field(..., example="Smart agriculture and crop disease prediction")
    domain: str = Field("Science & Engineering", example="Agricultural Engineering / AI")
    department: str = Field("Research & Development", example="Department of Agritech")
    institution: str = Field("Host Institution", example="National Institute of Technology")
    pi_name: str = Field("Principal Investigator", example="Dr. R. K. Sharma")
    pi_email: str = Field("pi@university.edu", example="pi@agritech.edu")
    duration_weeks: int = Field(8, example=12)
    requested_budget: float = Field(1000000.0, example=2500000.0)
    currency: str = Field("INR", example="INR")
    objectives: str = Field(..., example="Deploy AI-enabled sensing and predictive diagnosis for early crop disease detection.")
    funding_preferences: Optional[str] = Field(None, example="DST-SERB, ICAR")

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    domain: Optional[str] = None
    department: Optional[str] = None
    institution: Optional[str] = None
    pi_name: Optional[str] = None
    pi_email: Optional[str] = None
    duration_weeks: Optional[int] = None
    requested_budget: Optional[float] = None
    objectives: Optional[str] = None
    funding_preferences: Optional[str] = None
    status: Optional[str] = None

class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    class Config:
        from_attributes = True

class ProjectOut(BaseModel):
    id: int
    display_number: Optional[int] = 1
    title: str
    domain: str
    department: str
    institution: str
    pi_name: str
    pi_email: str
    duration_weeks: int
    requested_budget: float
    currency: str
    objectives: str
    funding_preferences: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    documents: List[DocumentOut] = []

    class Config:
        from_attributes = True
