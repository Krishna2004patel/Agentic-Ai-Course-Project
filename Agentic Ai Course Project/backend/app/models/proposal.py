from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ProposalDraft(Base):
    __tablename__ = "proposal_drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    version = Column(Integer, default=1)
    title = Column(String(255), nullable=False)
    executive_summary = Column(Text, nullable=True)
    problem_statement = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)
    work_plan = Column(Text, nullable=True)
    expected_outcomes = Column(Text, nullable=True)
    references_text = Column(Text, nullable=True)
    sections_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="proposals")

class BudgetPlan(Base):
    __tablename__ = "budget_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    total_requested = Column(Float, nullable=False)
    equipment_cost = Column(Float, default=0.0)
    manpower_cost = Column(Float, default=0.0)
    travel_cost = Column(Float, default=0.0)
    software_cost = Column(Float, default=0.0)
    consumables_cost = Column(Float, default=0.0)
    contingency_cost = Column(Float, default=0.0)
    overhead_cost = Column(Float, default=0.0)
    breakdown_json = Column(JSON, default=dict)
    justification = Column(Text, nullable=True)
    status = Column(String(50), default="ESTIMATED")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="budgets")

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    status = Column(String(50), default="PENDING")  # COMPLIANT, WARNINGS, NON_COMPLIANT
    compliance_score = Column(Float, default=0.0)   # 0 to 100%
    checks_passed = Column(JSON, default=list)
    missing_items = Column(JSON, default=list)
    warnings = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="compliance_reports")
