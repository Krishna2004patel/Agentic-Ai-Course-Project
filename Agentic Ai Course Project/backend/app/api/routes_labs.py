from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database import get_db
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult
from ..agents.lab1_planning import ResearchPlanningAgent
from ..agents.lab2_tools import ToolUsingGrantAgent
from ..agents.lab3_skills import SkillEvaluationAgent
from ..agents.lab4_memory import MemoryEvaluationAgent
from ..agents.lab5_mcp import MCPEvaluationAgent
from ..agents.lab6_runtime import RuntimeEvaluationAgent
from ..agents.lab7_node_graph import NodeGraphEvaluationAgent
from ..agents.lab8_swarm import ParallelSwarmEvaluationAgent
from ..agents.lab9_rag import DeepResearchRAGAgent
from ..agents.lab10_ops import OperationsMonitoringAgent
from ..agents.lab11_pipeline import PipelineEvaluationAgent
from ..agents.lab12_governance import SafetyEvaluationAgent
from ..agents.lab13_discipline import DisciplineSpecificEvaluationAgent
from ..agents.lab14_capstone import CapstoneEvaluationAgent

router = APIRouter(prefix="/labs", tags=["14 Agentic AI Labs"])

def get_project_or_404(project_id: int, db: Session) -> ResearchProject:
    p = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@router.get("/results/{project_id}")
def get_all_lab_results(project_id: int, db: Session = Depends(get_db)):
    """Returns the latest execution results for all 14 labs for the given project."""
    results = {}
    for i in range(1, 15):
        lab = db.query(LabExecutionResult).filter(
            LabExecutionResult.project_id == project_id,
            LabExecutionResult.lab_number == i
        ).order_by(LabExecutionResult.executed_at.desc()).first()
        if lab:
            results[i] = {
                "lab_number": lab.lab_number,
                "lab_title": lab.lab_title,
                "responsible_agent": lab.responsible_agent,
                "status": lab.status,
                "evaluation_status": lab.evaluation_status,
                "evaluation_results": lab.evaluation_results,
                "execution_output": lab.execution_output,
                "executed_at": lab.executed_at.isoformat() if lab.executed_at else None
            }
        else:
            results[i] = {
                "lab_number": i,
                "status": "NOT_EXECUTED",
                "message": f"Lab {i} has not been executed yet for project {project_id}."
            }
    return results

@router.get("/{lab_number}/{project_id}")
def get_lab_result(lab_number: int, project_id: int, db: Session = Depends(get_db)):
    """Fetches the latest result for a specific lab."""
    lab = db.query(LabExecutionResult).filter(
        LabExecutionResult.project_id == project_id,
        LabExecutionResult.lab_number == lab_number
    ).order_by(LabExecutionResult.executed_at.desc()).first()
    if not lab:
        return {"status": "NOT_EXECUTED", "lab_number": lab_number, "project_id": project_id}
    return {
        "id": lab.id,
        "project_id": lab.project_id,
        "lab_number": lab.lab_number,
        "lab_title": lab.lab_title,
        "responsible_agent": lab.responsible_agent,
        "status": lab.status,
        "evaluation_status": lab.evaluation_status,
        "evaluation_results": lab.evaluation_results,
        "execution_output": lab.execution_output,
        "execution_trace": lab.execution_trace,
        "executed_at": lab.executed_at.isoformat() if lab.executed_at else None
    }

@router.post("/{lab_number}/execute/{project_id}")
def execute_single_lab(lab_number: int, project_id: int, feedback: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Independently executes any one of the 14 labs.
    Executes the six specialized AI agents and generates all FOUR main research grant outputs
    plus the authentic lab-specific Agentic AI concept evidence!
    """
    proj = get_project_or_404(project_id, db)
    if lab_number < 1 or lab_number > 14:
        raise HTTPException(status_code=400, detail=f"Invalid lab number: {lab_number}. Must be between 1 and 14.")

    from ..agents.unified_lab_executor import UnifiedLabExecutor
    return UnifiedLabExecutor.execute_lab(db=db, project=proj, lab_number=lab_number, feedback=feedback)

@router.post("/execute-all/{project_id}")
def execute_all_labs_sequentially(project_id: int, db: Session = Depends(get_db)):
    """Executes all 14 labs sequentially for a project and persists all results."""
    proj = get_project_or_404(project_id, db)
    from ..agents.unified_lab_executor import UnifiedLabExecutor
    executed = []
    
    for i in range(1, 15):
        try:
            res = UnifiedLabExecutor.execute_lab(db=db, project=proj, lab_number=i, feedback=None)
            executed.append({
                "lab_number": i,
                "status": "SUCCESS",
                "lab_title": res.get("lab_title"),
                "concept": res.get("concept_name")
            })
        except Exception as e:
            executed.append({"lab_number": i, "status": "FAILED", "error": str(e)})

    return {
        "project_id": project_id,
        "project_title": proj.title,
        "total_labs_executed": len(executed),
        "results": executed
    }
