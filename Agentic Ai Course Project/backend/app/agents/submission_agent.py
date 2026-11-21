import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.proposal import ProposalDraft, BudgetPlan, ComplianceReport
from ..models.memory import ApprovalRecord
from ..core.audit_logger import SystemAuditLogger

class SubmissionAgent:
    """
    Agent F: Submission Agent
    Role: Proposal Finalization & Gateway Dispatcher
    Goal: Aggregate all artifacts, verify integrity, generate downloadable submission dossier,
          and strictly enforce human-in-the-loop approval before external dispatch.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.name = "Submission Agent"

    def prepare_package(self) -> Dict[str, Any]:
        """Collects outputs from Agents A through E."""
        proposal = self.db.query(ProposalDraft).filter(
            ProposalDraft.project_id == self.project.id
        ).order_by(ProposalDraft.version.desc()).first()

        budget = self.db.query(BudgetPlan).filter(
            BudgetPlan.project_id == self.project.id
        ).order_by(BudgetPlan.created_at.desc()).first()

        compliance = self.db.query(ComplianceReport).filter(
            ComplianceReport.project_id == self.project.id
        ).order_by(ComplianceReport.generated_at.desc()).first()

        ready = bool(proposal and budget and compliance and compliance.status in ("COMPLIANT", "WARNINGS"))

        dossier = {
            "project_id": self.project.id,
            "title": self.project.title,
            "domain": self.project.domain,
            "host_institution": self.project.institution,
            "pi_name": self.project.pi_name,
            "pi_email": self.project.pi_email,
            "duration_weeks": self.project.duration_weeks,
            "proposal": {
                "version": proposal.version if proposal else None,
                "title": proposal.title if proposal else None,
                "executive_summary": proposal.executive_summary if proposal else None,
                "methodology": proposal.methodology if proposal else None
            } if proposal else "Pending Generation",
            "budget": {
                "total_requested": budget.total_requested if budget else None,
                "equipment": budget.equipment_cost if budget else None,
                "manpower": budget.manpower_cost if budget else None,
                "overhead": budget.overhead_cost if budget else None
            } if budget else "Pending Generation",
            "compliance": {
                "status": compliance.status if compliance else None,
                "score": compliance.compliance_score if compliance else None
            } if compliance else "Pending Generation",
            "is_ready_for_approval": ready,
            "package_generated_at": datetime.utcnow().isoformat()
        }

        # Save downloadable dossier file
        out_dir = f"./data/dossiers/project_{self.project.id}"
        os.makedirs(out_dir, exist_ok=True)
        json_path = os.path.join(out_dir, "submission_dossier.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dossier, f, indent=2)

        md_path = os.path.join(out_dir, "grant_proposal_document.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._format_markdown_dossier(dossier))

        return {
            "agent": self.name,
            "status": "PACKAGE_PREPARED",
            "is_ready_for_approval": ready,
            "dossier": dossier,
            "downloadable_json_path": json_path,
            "downloadable_markdown_path": md_path
        }

    def _format_markdown_dossier(self, dossier: Dict[str, Any]) -> str:
        prop = dossier.get('proposal') if isinstance(dossier.get('proposal'), dict) else {}
        budg = dossier.get('budget') if isinstance(dossier.get('budget'), dict) else {}
        comp = dossier.get('compliance') if isinstance(dossier.get('compliance'), dict) else {}
        return f"""# RESEARCH GRANT PROPOSAL DOSSIER
**Title:** {dossier.get('title')}
**Host Institution:** {dossier.get('host_institution')}
**Principal Investigator:** {dossier.get('pi_name')} ({dossier.get('pi_email')})
**Domain:** {dossier.get('domain')} | **Duration:** {dossier.get('duration_weeks')} Weeks

---

## 1. Executive Summary
{prop.get('executive_summary', 'N/A')}

## 2. Technical Methodology
{prop.get('methodology', 'N/A')}

## 3. Financial Budget Summary
- Total Requested: ₹{budg.get('total_requested', 0):,.2f}
- Equipment: ₹{budg.get('equipment', 0):,.2f}
- Manpower: ₹{budg.get('manpower', 0):,.2f}
- Institutional Overhead (10%): ₹{budg.get('overhead', 0):,.2f}

## 4. Compliance Verification
- Status: {comp.get('status', 'PENDING')}
- Score: {comp.get('score', 0)}%

---
*Notice: Under strict governance rules, this grant dossier requires explicit human sign-off before transmission to external portals.*
"""

    def request_human_approval(self, requested_by: str = "Principal Investigator") -> Dict[str, Any]:
        """Creates an approval checkpoint record."""
        record = ApprovalRecord(
            project_id=self.project.id,
            stage="final_grant_submission",
            requested_action="Authorize automated submission of final grant dossier to funding agency portal.",
            status="PENDING",
            approved_by=None,
            comments="Awaiting final human verification by Dean R&D / Department Chair."
        )
        self.db.add(record)
        self.db.commit()

        SystemAuditLogger.log(
            self.db, self.project.id, self.name, "human_approval_requested",
            {"approval_id": record.id, "requested_by": requested_by}
        )

        return {
            "approval_id": record.id,
            "stage": record.stage,
            "status": "PENDING_APPROVAL",
            "message": "Human approval checkpoint initiated. Automated dispatch is paused until Dean/PI grants approval."
        }

    def submit_application(self, approval_id: int, approver_name: str, decision: str, comments: str = "") -> Dict[str, Any]:
        """Executes submission ONLY after explicit human approval."""
        record = self.db.query(ApprovalRecord).filter(ApprovalRecord.id == approval_id).first()
        if not record:
            return {"success": False, "error": "Approval record not found."}

        if decision.upper() != "APPROVED":
            record.status = "REJECTED"
            record.approved_by = approver_name
            record.comments = comments
            record.decided_at = datetime.utcnow()
            self.db.commit()
            return {
                "success": False,
                "status": "SUBMISSION_REJECTED",
                "message": f"Proposal submission was rejected by {approver_name}. Comments: {comments}"
            }

        # Human approved
        record.status = "APPROVED"
        record.approved_by = approver_name
        record.comments = comments
        record.decided_at = datetime.utcnow()

        self.project.status = "SUBMITTED"
        self.db.commit()

        SystemAuditLogger.log(
            self.db, self.project.id, self.name, "final_submission_authorized",
            {"approved_by": approver_name, "decided_at": record.decided_at.isoformat()}
        )

        return {
            "success": True,
            "status": "SUBMISSION_DISPATCHED",
            "submission_timestamp": datetime.utcnow().isoformat(),
            "approved_by": approver_name,
            "message": "Proposal successfully approved and archived into official university grant registry."
        }
