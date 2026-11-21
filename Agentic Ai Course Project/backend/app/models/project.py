from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ResearchProject(Base):
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    domain = Column(String(100), default="Computer Science & Engineering")
    department = Column(String(100), default="CSE (AI)")
    institution = Column(String(150), default="KLE Technological University")
    pi_name = Column(String(100), default="Dr. A. B. Joshi")
    pi_email = Column(String(100), default="pi@kletech.ac.in")
    duration_weeks = Column(Integer, default=8)
    requested_budget = Column(Float, default=1000000.0)  # in INR (₹10,00,000)
    currency = Column(String(10), default="INR")
    objectives = Column(Text, default="Develop multi-agent AI system for automated diagnosis and early biomarker analysis.")
    funding_preferences = Column(String(255), default="DST-SERB, ICMR, AICTE, MeitY")
    status = Column(String(50), default="DRAFT")  # DRAFT, IN_REVIEW, COMPLIANT, SUBMITTED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    funding_matches = relationship("FundingOpportunity", back_populates="project", cascade="all, delete-orphan")
    proposals = relationship("ProposalDraft", back_populates="project", cascade="all, delete-orphan")
    budgets = relationship("BudgetPlan", back_populates="project", cascade="all, delete-orphan")
    compliance_reports = relationship("ComplianceReport", back_populates="project", cascade="all, delete-orphan")
    memories = relationship("ProjectMemory", back_populates="project", cascade="all, delete-orphan")
    lab_results = relationship("LabExecutionResult", back_populates="project", cascade="all, delete-orphan")

class ProjectDocument(Base):
    __tablename__ = "project_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), default="pdf")  # pdf, docx, txt, csv
    file_size = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=True)
    metadata_json = Column(JSON, default=dict)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="documents")

class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=True)
    agency = Column(String(100), nullable=False)  # SERB, ICMR, DST, DBT, MeitY, Indo-US
    scheme_name = Column(String(255), nullable=False)
    max_amount = Column(Float, nullable=False)
    deadline = Column(String(50), nullable=False)
    eligibility = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)
    domain = Column(String(100), default="All")
    relevance_score = Column(Float, default=0.0)
    rationale = Column(Text, nullable=True)
    matched_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="funding_matches")
