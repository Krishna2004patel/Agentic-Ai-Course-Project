from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class LabExecutionResult(Base):
    __tablename__ = "lab_execution_results"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    lab_number = Column(Integer, nullable=False, index=True)  # 1 to 14
    lab_title = Column(String(200), nullable=False)
    responsible_agent = Column(String(100), nullable=False)
    status = Column(String(50), default="COMPLETED")  # COMPLETED, FAILED, RUNNING
    
    # Specific output structured JSON for this lab's expected output
    execution_output = Column(JSON, default=dict)
    
    # Logs, traces, prompt history
    execution_trace = Column(JSON, default=list)
    prompt_log = Column(JSON, default=list)
    
    # Evaluation metric results
    evaluation_status = Column(String(50), default="PASSED") # PASSED, WARNING, FAILED
    evaluation_results = Column(JSON, default=dict)
    
    # Verification details
    is_verified = Column(Boolean, default=True)
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("ResearchProject", back_populates="lab_results")
