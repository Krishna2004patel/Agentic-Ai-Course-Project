from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..agents.funding_discovery import FundingDiscoveryAgent
from ..agents.literature_review import LiteratureReviewAgent
from ..agents.proposal_drafting import ProposalDraftingAgent
from ..agents.budget_planning import BudgetPlanningAgent
from ..agents.compliance_checking import ComplianceCheckingAgent
from ..agents.submission_agent import SubmissionAgent
from ..core.audit_logger import SystemAuditLogger

class CentralizedAgentOrchestrator:
    """
    Centralized Multi-Agent Orchestrator.
    Manages lifecycle, routing, state handoffs, and execution for Agents A through F.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.funding_agent = FundingDiscoveryAgent(db, project)
        self.literature_agent = LiteratureReviewAgent(db, project)
        self.proposal_agent = ProposalDraftingAgent(db, project)
        self.budget_agent = BudgetPlanningAgent(db, project)
        self.compliance_agent = ComplianceCheckingAgent(db, project)
        self.submission_agent = SubmissionAgent(db, project)

    def run_full_lifecycle(self) -> Dict[str, Any]:
        """Runs the complete end-to-end multi-agent grant development pipeline."""
        from datetime import datetime
        t_now = datetime.utcnow().isoformat()
        
        SystemAuditLogger.log(
            self.db, self.project.id, "Orchestrator", "start_full_lifecycle",
            {"project_id": self.project.id, "topic": self.project.title}
        )

        completed_steps = {}
        current_agent = "Funding Discovery Agent"
        current_op = "run_funding_discovery"

        try:
            # Step 1: Funding Discovery
            current_agent = "Funding Discovery Agent"
            current_op = "run_funding_discovery"
            step1 = self.funding_agent.run()
            completed_steps["funding_discovery"] = step1

            # Step 2: Literature Review (Synchronous execution)
            current_agent = "Literature Review Agent"
            current_op = "run_literature_review"
            step2 = self.literature_agent.run()
            completed_steps["literature_review"] = step2

            # Step 3: Proposal Drafting
            current_agent = "Proposal Drafting Agent"
            current_op = "run_proposal_drafting"
            step3 = self.proposal_agent.run()
            completed_steps["proposal_drafting"] = step3

            # Step 4: Budget Planning
            current_agent = "Budget Planning Agent"
            current_op = "run_budget_planning"
            step4 = self.budget_agent.run()
            completed_steps["budget_planning"] = step4

            # Step 5: Compliance Audit
            current_agent = "Compliance Checking Agent"
            current_op = "run_compliance_checking"
            step5 = self.compliance_agent.run()
            completed_steps["compliance_checking"] = step5

            # Step 6: Submission Preparation
            current_agent = "Submission Agent"
            current_op = "prepare_package"
            step6 = self.submission_agent.prepare_package()
            completed_steps["submission_preparation"] = step6

            return {
                "status": "SUCCESS",
                "execution_status": "COMPLETED",
                "orchestrator_status": "COMPLETED",
                "project_id": self.project.id,
                "project_title": self.project.title,
                "execution_timestamp": t_now,
                "agents_executed": [
                    "Funding Discovery Agent",
                    "Literature Review Agent",
                    "Proposal Drafting Agent",
                    "Budget Planning Agent",
                    "Compliance Checking Agent",
                    "Submission Agent"
                ],
                "results": completed_steps,
                "source_references": step2.get("source_references", []) if isinstance(step2, dict) else [],
                "generated_outputs": {
                    "funding_matches_count": len(step1.get("ranked_opportunities", [])) if isinstance(step1, dict) else 0,
                    "proposal_title": step3.get("proposal", {}).get("title") if isinstance(step3, dict) else None,
                    "budget_total": (step4.get("budget_plan", {}).get("total_requested") or step4.get("budget_plan", {}).get("total_budget")) if isinstance(step4, dict) else None,
                    "compliance_status": step5.get("compliance_report", {}).get("status") if isinstance(step5, dict) else None
                }
            }
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            return {
                "status": "ERROR",
                "execution_status": "FAILED",
                "orchestrator_status": "FAILED",
                "error_status": "AGENT_EXECUTION_ERROR",
                "message": f"Orchestration failed at {current_agent}: {str(exc)}",
                "failed_agent": current_agent,
                "failed_operation": current_op,
                "project_id": self.project.id,
                "project_title": self.project.title,
                "execution_timestamp": datetime.utcnow().isoformat(),
                "traceback": tb,
                "partial_results": completed_steps
            }
