from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database import get_db
from ..models.project import ResearchProject
from ..models.lab_result import LabExecutionResult

router = APIRouter(prefix="/teacher", tags=["Teacher Dashboard"])

LAB_METADATA = {
    1: {
        "title": "Lab 1 – Agent vs Chatbot",
        "concept": "Goal -> Plan -> Act -> Observe -> Revise loop with delta plan mutation",
        "responsible_agent": "Research Planning Agent",
        "expected_output_focus": "Research plan, goal check predicate, and mutated revised plan based on feedback."
    },
    2: {
        "title": "Lab 2 – Tool-Using Agent",
        "concept": "Tools with structured contracts, dynamic planner-driven tool selection, and output validation",
        "responsible_agent": "Tool-Using Agent",
        "expected_output_focus": "Funding tool results, calculated funding totals, and parsed project documents."
    },
    3: {
        "title": "Lab 3 – Skill Creation",
        "concept": "Reusable skill packages (instructions, workflow, constraints, schema) tested across different projects",
        "responsible_agent": "Skill Creation Agent",
        "expected_output_focus": "Research summaries, structured proposals, budget breakdowns, and reusability verification."
    },
    4: {
        "title": "Lab 4 – Memory and Retrieval",
        "concept": "Separates session memory, long-term tagged memory, conflict detection, and permission boundaries",
        "responsible_agent": "Memory and Retrieval Agent",
        "expected_output_focus": "Retrieved project memories, source attribution, and conflict resolution details."
    },
    5: {
        "title": "Lab 5 – MCP-Style Connector",
        "concept": "Model Context Protocol integration server exposing resources, SQLite tool with permission boundary, and API",
        "responsible_agent": "MCP Connector Agent",
        "expected_output_focus": "Connector manifest, read-only SQL query results, and security boundary test logs."
    },
    6: {
        "title": "Lab 6 – Agent Runtime",
        "concept": "OpenCLA/OpenClaw-style runtime: task interface, runtime loop, skill registry, tool registry, scoped memory",
        "responsible_agent": "Agent Runtime Engine",
        "expected_output_focus": "Runtime execution cycle, dynamically registered skill execution, and audit trail."
    },
    7: {
        "title": "Lab 7 – Agentic Node Graph",
        "concept": "Executable DAG workflow with node owners, inputs, outputs, success predicates, and retry logic",
        "responsible_agent": "Node Graph Engine",
        "expected_output_focus": "Visual workflow DAG, node completion states, and execution trace."
    },
    8: {
        "title": "Lab 8 – Parallel Agent Swarm",
        "concept": "Genuine concurrent ThreadPool execution of 4 agents, followed by conflict detection and explicit resolution",
        "responsible_agent": "Parallel Swarm Orchestrator",
        "expected_output_focus": "Individual worker outputs, detected conflicts, and consolidated resolution recommendation."
    },
    9: {
        "title": "Lab 9 – Agentic RAG",
        "concept": "Document chunking, vector indexing, top-k retrieval, multi-source evidence extraction, and citation mapping",
        "responsible_agent": "Deep Research RAG Agent",
        "expected_output_focus": "Evidence-supported research synthesis, chunk-traceable citations, and contradiction analysis."
    },
    10: {
        "title": "Lab 10 – Operations Monitoring Agent",
        "concept": "Telemetry observation, root-cause diagnosis, severity classification, and human approval before high-risk recovery",
        "responsible_agent": "Operations Monitoring Agent",
        "expected_output_focus": "Subsystem incident diagnoses, severity ratings, and blocked destructive actions awaiting human approval."
    },
    11: {
        "title": "Lab 11 – Agentic Development Pipeline",
        "concept": "SDLC factory: Requirement -> Design -> Implementation -> Independent Testing -> Peer Review -> Release Gate",
        "responsible_agent": "SDLC Factory Orchestrator",
        "expected_output_focus": "Requirement stories, independent AC tests, security review, and release checkpoint status."
    },
    12: {
        "title": "Lab 12 – Safety, Evaluation and Governance",
        "concept": "Access controls, external submission invariant blocker, risk assessment scoring, and evaluation metrics",
        "responsible_agent": "Safety & Governance Agent",
        "expected_output_focus": "Submission lock status, risk scorecard, permissions enforcement, and rollback recommendations."
    },
    13: {
        "title": "Lab 13 – Discipline-Specific Engineering Agents",
        "concept": "Domain-specific research support tailored for Mechanical, Civil, and Electrical Engineering disciplines",
        "responsible_agent": "Discipline-Specific Engineering Coordinator",
        "expected_output_focus": "Mechanical predictive maintenance, Civil infrastructure safety, and Electrical grid optimization proposals."
    },
    14: {
        "title": "Lab 14 – Capstone Project Integration",
        "concept": "End-to-end integration combining multi-agent orchestration, tools, skills, memory, swarm, graph, and safety",
        "responsible_agent": "Capstone System Architect",
        "expected_output_focus": "Full end-to-end grant dossier package, regression evaluation suite, and downloadable proposal files."
    }
}

@router.get("/overview")
def get_teacher_overview(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Provides high-level dashboard data for teachers to inspect all 14 labs across projects."""
    from ..core.project_numbering import get_chronological_projects, get_project_display_map
    unique_projects = get_chronological_projects(db)
    display_map = get_project_display_map(db)

    selected_id = project_id if project_id else (unique_projects[0].id if unique_projects else 1)
    
    lab_cards = []
    for num in range(1, 15):
        meta = LAB_METADATA.get(num, {})
        record = db.query(LabExecutionResult).filter(
            LabExecutionResult.project_id == selected_id,
            LabExecutionResult.lab_number == num
        ).order_by(LabExecutionResult.executed_at.desc()).first()

        history = db.query(LabExecutionResult).filter(
            LabExecutionResult.project_id == selected_id,
            LabExecutionResult.lab_number == num
        ).order_by(LabExecutionResult.executed_at.desc()).limit(5).all()

        lab_cards.append({
            "lab_number": num,
            "title": meta.get("title"),
            "concept": meta.get("concept"),
            "responsible_agent": meta.get("responsible_agent"),
            "implementation_status": "IMPLEMENTED & OPERATIONAL",
            "expected_output_focus": meta.get("expected_output_focus"),
            "status": record.status if record else "NOT_EXECUTED",
            "evaluation_status": record.evaluation_status if record else "PENDING",
            "evaluation_results": record.evaluation_results if record else {},
            "is_completed": bool(record and record.status == "COMPLETED"),
            "executed_at": record.executed_at.isoformat() if record and record.executed_at else None,
            "execution_history": [
                {
                    "timestamp": h.executed_at.strftime("%Y-%m-%d %H:%M:%S") if h.executed_at else "N/A",
                    "status": h.status,
                    "evaluation": h.evaluation_status
                }
                for h in history
            ],
            "execution_result": record.execution_trace if record and record.execution_trace else [],
            "execution_output": record.execution_output if record else {},
            # Filter output strictly to relevant expected output for teacher
            "expected_output_summary": _extract_teacher_focused_output(num, record.execution_output if record else {})
        })

    return {
        "selected_project_id": selected_id,
        "selected_project_display_number": display_map.get(selected_id, 1),
        "available_projects": [
            {
                "id": p.id,
                "display_number": display_map.get(p.id, idx + 1),
                "title": p.title,
                "institution": p.institution,
                "pi": p.pi_name
            }
            for idx, p in enumerate(unique_projects)
        ],
        "total_labs": 14,
        "completed_labs": sum(1 for c in lab_cards if c["is_completed"]),
        "passed_evaluations": sum(1 for c in lab_cards if c["evaluation_status"] == "PASSED"),
        "labs": lab_cards
    }

def _extract_teacher_focused_output(lab_num: int, output: Dict[str, Any]) -> Dict[str, Any]:
    """Filters the execution output to highlight only the specific expected outputs per lab."""
    if not output:
        return {"note": "No execution data recorded yet."}
    
    # Extract concept evidence if wrapped inside unified output
    evidence = output.get("lab_concept_evidence") or output
    
    if lab_num == 1:
        return {
            "initial_plan": evidence.get("initial_plan"),
            "revised_plan": evidence.get("revised_plan"),
            "goal_satisfied": evidence.get("goal_satisfied"),
            "user_feedback_applied": evidence.get("user_feedback_applied")
        }
    elif lab_num == 2:
        return {
            "tool_invocations": evidence.get("tool_invocations"),
            "funding_totals": evidence.get("tool_results", {}).get("funding_calculator"),
            "explanation": evidence.get("agent_explanation")
        }
    elif lab_num == 3:
        return {
            "skills_executed": evidence.get("skills_executed"),
            "reusability_test": evidence.get("reusability_test")
        }
    elif lab_num == 4:
        return {
            "retrieved_memories": evidence.get("topic_retrieval_results"),
            "conflict_detection": evidence.get("conflict_detection_demonstration"),
            "permission_check": evidence.get("permission_boundary_enforcement")
        }
    elif lab_num == 5:
        return {
            "manifest": evidence.get("manifest_summary"),
            "database_query_result": evidence.get("authorized_sql_tool_result"),
            "security_boundary_check": evidence.get("security_boundary_enforcement"),
            "external_paper_tool": evidence.get("paper_tool_result")
        }
    elif lab_num == 6:
        return {
            "dynamic_skill_registered": evidence.get("dynamic_skill_registered"),
            "iterations": evidence.get("runtime_iterations"),
            "stop_reason": evidence.get("stop_reason"),
            "audit_trail_preview": evidence.get("audit_trail", [])[:3]
        }
    elif lab_num == 7:
        return {
            "workflow_name": evidence.get("workflow_name"),
            "nodes": evidence.get("graph_nodes"),
            "all_nodes_passed": evidence.get("all_nodes_passed"),
            "execution_trace": evidence.get("execution_trace")
        }
    elif lab_num == 8:
        return {
            "worker_outputs": evidence.get("individual_worker_outputs"),
            "conflicts_detected": evidence.get("conflicts_detected"),
            "consolidated_result": evidence.get("consolidated_recommendation")
        }
    elif lab_num == 9:
        return {
            "evidence_table": evidence.get("evidence_table"),
            "evidence_supported_synthesis": evidence.get("evidence_supported_synthesis"),
            "citations": evidence.get("citations"),
            "contradictions": evidence.get("contradictory_findings_detected")
        }
    elif lab_num == 10:
        return {
            "system_health": evidence.get("system_health"),
            "diagnoses": evidence.get("diagnoses"),
            "actions_requiring_human_approval": evidence.get("high_risk_actions_paused_for_approval")
        }
    elif lab_num == 11:
        return {
            "feature": evidence.get("feature"),
            "independent_tests": evidence.get("independent_tests_summary"),
            "sdlc_trace": evidence.get("sdlc_trace"),
            "release_gate": evidence.get("human_checkpoint_status")
        }
    elif lab_num == 12:
        return {
            "submission_lock": evidence.get("submission_gate_status"),
            "risk_assessment": evidence.get("risk_assessment"),
            "evaluation_metrics": evidence.get("evaluation_metrics"),
            "recovery_recommendations": evidence.get("recovery_recommendations")
        }
    elif lab_num == 13:
        return {
            "mechanical_proposal": evidence.get("mechanical_proposal"),
            "civil_proposal": evidence.get("civil_proposal"),
            "electrical_proposal": evidence.get("electrical_proposal")
        }
    elif lab_num == 14:
        return {
            "capstone_title": evidence.get("capstone_title"),
            "orchestration": evidence.get("multi_agent_orchestration"),
            "tools": evidence.get("tools_demonstrated"),
            "safety_gate": evidence.get("safety_and_governance"),
            "downloadable_artifacts": evidence.get("downloadable_artifacts"),
            "regression_evaluation": evidence.get("regression_evaluation")
        }
    return evidence

@router.post("/execute-lab/{lab_number}")
def teacher_execute_lab(lab_number: int, project_id: Optional[int] = 1, db: Session = Depends(get_db)):
    """Teacher convenience endpoint to execute any of the 14 labs."""
    from .routes_labs import execute_single_lab
    return execute_single_lab(lab_number=lab_number, project_id=project_id or 1, feedback=None, db=db)

@router.post("/execute-all")
def teacher_execute_all_labs(project_id: Optional[int] = 1, db: Session = Depends(get_db)):
    """Teacher convenience endpoint to execute all 14 labs sequentially."""
    from .routes_labs import execute_all_labs_sequentially
    return execute_all_labs_sequentially(project_id=project_id or 1, db=db)

