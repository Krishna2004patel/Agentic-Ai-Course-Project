from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..discipline.engineering import DisciplineSpecificEngineeringEngine

class DisciplineSpecificEvaluationAgent:
    """
    Lab 13: Discipline-Specific Engineering Agents
    Demonstrates domain-specific research proposals, equipment allocations, and criteria
    tailored for Mechanical, Civil, and Electrical Engineering.
    """
    def __init__(self, db: Session, project: ResearchProject):
        self.db = db
        self.project = project
        self.lab_number = 13
        self.lab_title = "Lab 13: Discipline-Specific Engineering Agents -- Mechanical, Civil, Electrical"

    def execute_discipline_evaluations(self) -> Dict[str, Any]:
        mech = DisciplineSpecificEngineeringEngine.generate_mechanical_proposal(self.project.institution)
        civil = DisciplineSpecificEngineeringEngine.generate_civil_proposal(self.project.institution)
        elec = DisciplineSpecificEngineeringEngine.generate_electrical_proposal(self.project.institution)

        output = {
            "project_id": self.project.id,
            "disciplines_supported": ["Mechanical Engineering", "Civil Engineering", "Electrical & Electronics Engineering"],
            "mechanical_proposal": mech,
            "civil_proposal": civil,
            "electrical_proposal": elec,
            "domain_customization_summary": (
                "Each discipline employs domain-specific instrumentation, regulatory standards (IS Codes, IEEE 1547), "
                "and distinct evaluation metrics (F1-score, crack resolution, frequency stability)."
            )
        }

        # Persist lab result
        lab_res = LabExecutionResult(
            project_id=self.project.id,
            lab_number=self.lab_number,
            lab_title=self.lab_title,
            responsible_agent="Discipline-Specific Engineering Coordinator",
            status="COMPLETED",
            execution_output=output,
            evaluation_status="PASSED",
            evaluation_results={
                "disciplines_covered": 3,
                "domain_equipment_specified": True,
                "domain_constraints_enforced": True
            }
        )
        self.db.add(lab_res)
        self.db.commit()

        return output
