from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ProposalRevisionRequest(BaseModel):
    feedback: Optional[str] = ""

class BudgetRecalculateRequest(BaseModel):
    override_budget: Optional[float] = None

class HumanApprovalDecision(BaseModel):
    approval_id: int
    approver_name: str
    decision: str  # APPROVED, REJECTED
    comments: Optional[str] = ""
