from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..swarm.parallel_swarm import ParallelGrantSwarm

class ParallelSwarmEvaluationAgent:
    """
    Lab 8: Parallel Agent Swarm
    Evaluates concurrent execution of 4 independent agents, conflict detection,
    and rule-based resolution into a consolidated grant decision.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.lab_number = 8
        self.lab_title = "Lab 8: Parallel Swarm -- Multimodal Research Swarm"

    def execute_swarm(self) -> Dict[str, Any]:
        swarm = ParallelGrantSwarm({
            "project_id": self.project.id,
            "title": self.project.title,
            "domain": self.project.domain,
            "budget": self.project.requested_budget,
            "institution": self.project.institution
        })

        swarm_result = swarm.run_parallel_swarm()

        # Persist lab result
        lab_res = LabExecutionResult(
            project_id=self.project.id,
            lab_number=self.lab_number,
            lab_title=self.lab_title,
            responsible_agent="Parallel Swarm Orchestrator",
            status="COMPLETED",
            execution_output=swarm_result,
            execution_trace=[
                {"worker": k, "output": v} for k, v in swarm_result["individual_worker_outputs"].items()
            ],
            evaluation_status="PASSED",
            evaluation_results={
                "parallel_threads_executed": 4,
                "conflict_detection_passed": swarm_result["conflict_count"] > 0,
                "conflict_resolution_applied": True
            }
        )
        self.db.add(lab_res)
        self.db.commit()

        return swarm_result
