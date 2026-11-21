from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models.project import ResearchProject, FundingOpportunity
from ..tools.funding_api import FundingAPIConnectorTool
from ..core.audit_logger import SystemAuditLogger

class FundingDiscoveryAgent:
    """
    Agent A: Funding Discovery Agent
    Role: Senior Grant Discovery Specialist
    Goal: Identify and rank optimal funding opportunities, calculate relevance scores, and explain match rationale.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.name = "Funding Discovery Agent"

    def run(self) -> Dict[str, Any]:
        SystemAuditLogger.log(
            self.db, self.project.id, self.name, "search_funding",
            {"topic": self.project.title, "domain": self.project.domain, "budget": self.project.requested_budget}
        )

        opportunities = FundingAPIConnectorTool.search_funding_opportunities(
            topic=self.project.title,
            domain=self.project.domain or "All",
            requested_budget=self.project.requested_budget,
            institution=self.project.institution or "Host Institution",
            description=self.project.objectives or ""
        )

        # Clear existing matches for this project and persist new matches
        self.db.query(FundingOpportunity).filter(FundingOpportunity.project_id == self.project.id).delete()

        saved_records = []
        for opp in opportunities:
            record = FundingOpportunity(
                project_id=self.project.id,
                agency=opp["agency"],
                scheme_name=opp["scheme_name"],
                max_amount=opp["max_amount"],
                deadline=opp["deadline"],
                eligibility=opp["eligibility"],
                url=opp["url"],
                domain=self.project.domain or "All",
                relevance_score=opp["relevance_score"],
                rationale=opp["rationale"]
            )
            self.db.add(record)
            saved_records.append(record)

        self.db.commit()

        # Identify missing information
        missing_info = []
        if not self.project.pi_email or "@" not in self.project.pi_email:
            missing_info.append("PI Official institutional email is missing or unverified.")
        if self.project.requested_budget <= 0:
            missing_info.append("Estimated grant budget is not specified.")

        top_match = opportunities[0] if opportunities else None

        result = {
            "agent": self.name,
            "status": "COMPLETED",
            "project_id": self.project.id,
            "topic": self.project.title,
            "domain": self.project.domain,
            "total_schemes_evaluated": len(opportunities),
            "top_match": top_match,
            "ranked_opportunities": opportunities,
            "missing_information": missing_info,
            "recommendation": f"Recommend applying for '{top_match['scheme_name']}' by {top_match['agency']} (Score: {round(top_match['relevance_score'] * 100, 1)}%)" if top_match else "No match found."
        }
        return result
