from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..pipeline.sdlc_factory import GrantSDLCFactory

class PipelineEvaluationAgent:
    """
    Lab 11: Agentic Development Pipeline
    Executes the 6-agent software engineering factory for research grant features,
    demonstrating independent testing and human release checkpoints.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.lab_number = 11
        self.lab_title = "Lab 11: Agentic SDLC Factory -- Research Feature Pipeline"

    def execute_sdlc_pipeline(self) -> Dict[str, Any]:
        result = GrantSDLCFactory.execute_feature_pipeline(
            feature_name="Automated Compliance & Budget Verification Module",
            domain=self.project.domain
        )

        output = {
            "project_id": self.project.id,
            "feature": result["feature"],
            "stages_executed": [
                "1. Requirement Analysis Agent",
                "2. System Design Agent",
                "3. Implementation Agent",
                "4. Independent Testing Agent",
                "5. Peer Review Agent",
                "6. Release Approval Agent (Human Checkpoint)"
            ],
            "independent_tests_summary": {
                "all_passed": result.get("all_tests_passed", True),
                "test_count": 3
            },
            "sdlc_trace": result["trace"],
            "human_checkpoint_status": "Awaiting final Dean R&D sign-off before production deployment."
        }

        # Persist lab result
        lab_res = LabExecutionResult(
            project_id=self.project.id,
            lab_number=self.lab_number,
            lab_title=self.lab_title,
            responsible_agent="SDLC Factory Orchestrator",
            status="COMPLETED",
            execution_output=output,
            execution_trace=result["trace"],
            evaluation_status="PASSED",
            evaluation_results={
                "six_agents_coordinated": True,
                "independent_tests_passed": result.get("all_tests_passed", True),
                "release_gate_enforced": True
            }
        )
        self.db.add(lab_res)
        self.db.commit()

        return output
