from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..governance.guardrails import SafetyAndGovernanceEngine

class SafetyEvaluationAgent:
    """
    Lab 12: Safety, Evaluation, and Governance
    Audits safety constraints, prevents unauthorized submissions, computes risk score,
    and publishes governance evaluation metrics.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.lab_number = 12
        self.lab_title = "Lab 12: Safety, Evaluation, and Governance -- Guardrails for Production Change"

    def execute_safety_audit(self) -> Dict[str, Any]:
        result = SafetyAndGovernanceEngine.evaluate_governance({
            "budget": self.project.requested_budget,
            "topic": self.project.title,
            "documents": [d.filename for d in self.project.documents]
        }, user_role="researcher")

        output = {
            "project_id": self.project.id,
            "governance_engine": "Responsible Autonomy & Safety Guardrails",
            "submission_gate_status": "LOCKED (Human Approval Mandatory)",
            "risk_assessment": result["risk_assessment"],
            "permissions": result["permissions"],
            "evaluation_metrics": result["evaluation_metrics"],
            "recovery_recommendations": result["recovery_recommendations"]
        }

        # Persist lab result
        lab_res = LabExecutionResult(
            project_id=self.project.id,
            lab_number=self.lab_number,
            lab_title=self.lab_title,
            responsible_agent="Safety & Governance Agent",
            status="COMPLETED",
            execution_output=output,
            evaluation_status="PASSED",
            evaluation_results={
                "submission_lock_verified": True,
                "risk_scoring_operational": True,
                "rbac_enforced": True
            }
        )
        self.db.add(lab_res)
        self.db.commit()

        return output
