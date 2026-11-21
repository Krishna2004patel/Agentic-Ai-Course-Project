from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models.project import ResearchProject

def get_chronological_projects(db: Session) -> List[ResearchProject]:
    """
    Returns unique projects sorted chronologically by (created_at ASC, id ASC).
    Deduplicates by title (case-insensitive) to ensure clean display.
    """
    all_p = db.query(ResearchProject).order_by(
        ResearchProject.created_at.asc(),
        ResearchProject.id.asc()
    ).all()
    seen = set()
    unique = []
    for p in all_p:
        t_key = p.title.strip().lower()
        if t_key not in seen:
            seen.add(t_key)
            unique.append(p)
    return unique

def get_project_display_map(db: Session) -> Dict[int, int]:
    """
    Computes a 1-based sequential display number for every unique project:
    Project #1, Project #2, ..., Project #N.
    Independent of DB primary keys.
    When projects are deleted, gaps are automatically closed because display numbers
    are derived dynamically from chronological rank.
    """
    projects = get_chronological_projects(db)
    return {p.id: idx + 1 for idx, p in enumerate(projects)}

def get_project_display_number(db: Session, project_id: int) -> int:
    """
    Returns the sequential display number for a specific project.
    Defaults to 1 if not found.
    """
    mapping = get_project_display_map(db)
    return mapping.get(project_id, 1)

def assign_display_numbers(db: Session, projects: List[ResearchProject]) -> List[ResearchProject]:
    """
    Attaches .display_number to each ResearchProject instance based on its chronological rank.
    """
    mapping = get_project_display_map(db)
    for p in projects:
        setattr(p, "display_number", mapping.get(p.id, 1))
    return projects
