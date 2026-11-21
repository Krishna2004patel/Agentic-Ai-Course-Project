from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject, ProjectDocument
from ..models.proposal import ComplianceReport
from ..skills.compliance_checking import ComplianceCheckingSkill
from ..core.audit_logger import SystemAuditLogger

class ComplianceCheckingAgent:
    """
    Agent E: Compliance Checking Agent
    Role: Institutional Compliance & Regulatory Auditor
    Goal: Verify proposal against statutory guidelines, eligibility rules, document completeness, and deadline proximity.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.name = "Compliance Checking Agent"

    def run(self) -> Dict[str, Any]:
        SystemAuditLogger.log(
            self.db, self.project.id, self.name, "execute_compliance_audit",
            {"project_id": self.project.id, "institution": self.project.institution, "domain": self.project.domain}
        )

        docs = self.db.query(ProjectDocument).filter(ProjectDocument.project_id == self.project.id).all()

        skill_res = ComplianceCheckingSkill.execute({
            "institution": self.project.institution or "Host University",
            "pi_name": self.project.pi_name or "Principal Investigator",
            "pi_email": self.project.pi_email or "",
            "domain": self.project.domain or "Engineering",
            "requested_budget": self.project.requested_budget,
            "duration_weeks": self.project.duration_weeks,
            "documents": docs
        })

        report = ComplianceReport(
            project_id=self.project.id,
            status=skill_res["status"],
            compliance_score=skill_res["compliance_score"],
            checks_passed=skill_res["checks_passed"],
            missing_items=skill_res["missing_items"],
            warnings=skill_res["warnings"],
            recommendations=skill_res["recommendations"]
        )

        self.db.add(report)
        self.db.commit()

        return {
            "agent": self.name,
            "status": skill_res["status"],
            "compliance_score": skill_res["compliance_score"],
            "checks_passed": skill_res["checks_passed"],
            "missing_items": skill_res["missing_items"],
            "warnings": skill_res["warnings"],
            "recommendations": skill_res["recommendations"],
            "required_documents": skill_res["required_documents"],
            "is_submission_ready": skill_res["status"] == "COMPLIANT"
        }
