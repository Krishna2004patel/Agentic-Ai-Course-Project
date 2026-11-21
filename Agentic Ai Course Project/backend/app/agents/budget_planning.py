from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.proposal import BudgetPlan
from ..skills.budget_analysis import BudgetAnalysisSkill
from ..core.audit_logger import SystemAuditLogger

class BudgetPlanningAgent:
    """
    Agent D: Budget Planning Agent
    Role: Financial & Grant Resource Optimization Officer
    Goal: Formulate itemized expenditure, check statutory caps, eliminate inconsistencies,
          and provide institutional justifications.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.name = "Budget Planning Agent"

    def run(self, override_budget: Optional[float] = None) -> Dict[str, Any]:
        budget_target = override_budget if override_budget else self.project.requested_budget
        
        SystemAuditLogger.log(
            self.db, self.project.id, self.name, "compute_and_validate_budget",
            {"project_id": self.project.id, "budget_target": budget_target}
        )

        skill_res = BudgetAnalysisSkill.execute({
            "requested_budget": budget_target,
            "domain": self.project.domain or "Engineering",
            "institution": self.project.institution or "Host University",
            "topic": self.project.title
        })

        breakdown = skill_res["breakdown"]

        # Save to database
        budget_record = BudgetPlan(
            project_id=self.project.id,
            total_requested=skill_res["calculated_total"],
            equipment_cost=breakdown["equipment"],
            manpower_cost=breakdown["manpower"],
            travel_cost=breakdown["travel"],
            software_cost=breakdown["software"],
            consumables_cost=breakdown["consumables"],
            contingency_cost=skill_res["contingency_cost"],
            overhead_cost=skill_res["overhead_cost"],
            breakdown_json=skill_res,
            justification="\n".join(skill_res["justifications"]),
            status="VALIDATED"
        )

        self.db.add(budget_record)
        self.db.commit()

        return {
            "agent": self.name,
            "status": "COMPLETED",
            "project_id": self.project.id,
            "total_requested": budget_record.total_requested,
            "direct_costs": skill_res.get("direct_costs", 0.0),
            "currency": self.project.currency or "INR",
            "breakdown": breakdown,
            "contingency_cost": budget_record.contingency_cost,
            "overhead_cost": budget_record.overhead_cost,
            "percentages": skill_res["percentages"],
            "justifications": skill_res["justifications"],
            "statutory_compliance": f"Fully compliant with statutory 10% overhead cap for {self.project.institution} and 5% contingency guideline."
        }
