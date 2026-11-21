import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.project import ResearchProject, ProjectDocument, FundingOpportunity
from ..models.proposal import ProposalDraft, BudgetPlan, ComplianceReport
from ..models.memory import AuditLog, ApprovalRecord

router = APIRouter(prefix="/researcher", tags=["Researcher Dashboard"])

@router.get("/metrics")
def get_researcher_metrics(db: Session = Depends(get_db)):
    """Computes high-level researcher statistics."""
    from ..core.project_numbering import get_chronological_projects
    projects = get_chronological_projects(db)
    total_projects = len(projects)
    active_projects = sum(1 for p in projects if p.status != "SUBMITTED")
    funding_opportunities = db.query(FundingOpportunity).count()
    proposals_generated = db.query(ProposalDraft).count()
    pending_compliance = db.query(ComplianceReport).filter(ComplianceReport.status != "COMPLIANT").count()
    
    # Calculate total budget requested across all unique projects
    total_budget = sum(p.requested_budget for p in projects)
    
    # Recent activity logs
    recent_logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(8).all()
    
    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "funding_opportunities_discovered": funding_opportunities,
        "proposals_generated": proposals_generated,
        "pending_compliance_checks": pending_compliance,
        "total_estimated_budget": total_budget,
        "recent_activities": [
            {
                "id": log.id,
                "agent": log.agent_name,
                "action": log.action,
                "project_id": log.project_id,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None
            }
            for log in recent_logs
        ]
    }

@router.get("/audit-logs")
def get_audit_logs(project_id: Optional[int] = None, limit: int = 50, db: Session = Depends(get_db)):
    """Fetches system and agent audit logs, optionally filtered by project."""
    query = db.query(AuditLog)
    if project_id:
        query = query.filter(AuditLog.project_id == project_id)
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "agent": log.agent_name,
            "action": log.action,
            "project_id": log.project_id,
            "details": log.details,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None
        }
        for log in logs
    ]

@router.get("/download-dossier/{project_id}/{file_type}")
def download_grant_dossier(project_id: int, file_type: str, db: Session = Depends(get_db)):
    """Allows downloading the proposal package as JSON or Markdown."""
    proj = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    out_dir = f"./data/dossiers/project_{project_id}"
    if file_type == "json":
        path = os.path.join(out_dir, "submission_dossier.json")
        filename = f"Grant_Proposal_Project_{project_id}.json"
        media = "application/json"
    elif file_type == "markdown" or file_type == "md":
        path = os.path.join(out_dir, "grant_proposal_document.md")
        filename = f"Grant_Proposal_Project_{project_id}.md"
        media = "text/markdown"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use 'json' or 'markdown'")
        
    if not os.path.exists(path):
        # Auto-generate if missing
        from ..agents.submission_agent import SubmissionAgent
        agent = SubmissionAgent(db, proj)
        agent.prepare_package()
        
    return FileResponse(path, filename=filename, media_type=media)
