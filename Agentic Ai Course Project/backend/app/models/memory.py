from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ProjectMemory(Base):
    __tablename__ = "project_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    memory_type = Column(String(50), default="long_term")  # short_term, long_term, decision, guideline
    tag = Column(String(50), default="general")             # topic, budget, methodology, compliance
    key = Column(String(150), nullable=False)
    value = Column(Text, nullable=False)
    source = Column(String(100), default="agent_inference") # user_input, paper_extract, agent_inference, guideline_doc
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="memories")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=True)
    lab_number = Column(Integer, nullable=True)
    agent_name = Column(String(100), nullable=False)
    action = Column(String(150), nullable=False)
    details = Column(JSON, default=dict)
    prompt_used = Column(Text, nullable=True)
    response_received = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ApprovalRecord(Base):
    __tablename__ = "approval_records"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    stage = Column(String(100), nullable=False)   # e.g., "final_grant_submission", "budget_override"
    requested_action = Column(Text, nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    approved_by = Column(String(100), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)
