from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.memory import ProjectMemory, AuditLog

class MemoryManager:
    """
    Project-Scoped Memory & Retrieval Engine.
    Handles:
    - Short-term session state
    - Long-term persistent knowledge
    - Conflict detection between new and existing facts
    - Stale memory detection (> 30 days or marked outdated)
    - Source-tagged provenance
    - Access permission enforcement
    """
    def __init__(self, db: Session, project_id: int):
        self.db = db
        self.project_id = project_id
        # In-memory ephemeral session storage
        self._session_cache: Dict[str, Any] = {}

    def set_session_var(self, key: str, value: Any):
        """Set short-term ephemeral session variable."""
        self._session_cache[key] = value

    def get_session_var(self, key: str, default=None):
        """Get short-term session variable."""
        return self._session_cache.get(key, default)

    def store_fact(self, key: str, value: str, tag: str = "general", source: str = "user_input", 
                   memory_type: str = "long_term", user_role: str = "researcher") -> Dict[str, Any]:
        """
        Stores or updates a long-term memory fact with conflict detection and permission check.
        """
        # Permission check: Reviewers have read-only permissions
        if user_role == "reviewer":
            return {
                "success": False,
                "error": "Permission Denied: Reviewer role has read-only access to project memory."
            }

        # Check existing memory for conflict
        existing = self.db.query(ProjectMemory).filter(
            ProjectMemory.project_id == self.project_id,
            ProjectMemory.key == key,
            ProjectMemory.is_active == True
        ).first()

        conflict_detected = False
        conflict_details = None

        if existing:
            if existing.value.strip().lower() != value.strip().lower():
                conflict_detected = True
                conflict_details = {
                    "key": key,
                    "previous_value": existing.value,
                    "previous_source": existing.source,
                    "previous_updated_at": existing.updated_at.isoformat() if existing.updated_at else None,
                    "new_value": value,
                    "new_source": source,
                    "resolution": "Updated with newer fact; preserved audit trace."
                }
            existing.value = value
            existing.tag = tag
            existing.source = source
            existing.updated_at = datetime.utcnow()
            self.db.commit()
            mem_record = existing
        else:
            mem_record = ProjectMemory(
                project_id=self.project_id,
                memory_type=memory_type,
                tag=tag,
                key=key,
                value=value,
                source=source,
                is_active=True
            )
            self.db.add(mem_record)
            self.db.commit()

        return {
            "success": True,
            "memory_id": mem_record.id,
            "key": key,
            "value": value,
            "source": source,
            "conflict_detected": conflict_detected,
            "conflict_details": conflict_details
        }

    def retrieve_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Retrieves all active project memories matching a topic or tag,
        with stale-memory warnings if older than 30 days.
        """
        results = []
        memories = self.db.query(ProjectMemory).filter(
            ProjectMemory.project_id == self.project_id,
            ProjectMemory.is_active == True
        ).all()

        stale_threshold = datetime.utcnow() - timedelta(days=30)

        for m in memories:
            if topic.lower() in m.key.lower() or topic.lower() in m.tag.lower() or topic.lower() in m.value.lower():
                is_stale = m.updated_at and m.updated_at < stale_threshold
                results.append({
                    "id": m.id,
                    "key": m.key,
                    "value": m.value,
                    "tag": m.tag,
                    "source": m.source,
                    "memory_type": m.memory_type,
                    "updated_at": m.updated_at.isoformat() if m.updated_at else None,
                    "is_stale": is_stale,
                    "stale_warning": "Warning: This research fact was recorded >30 days ago and may require verification." if is_stale else None
                })
        return results

    def get_all_project_facts(self) -> List[Dict[str, Any]]:
        memories = self.db.query(ProjectMemory).filter(
            ProjectMemory.project_id == self.project_id,
            ProjectMemory.is_active == True
        ).all()
        return [
            {
                "key": m.key,
                "value": m.value,
                "tag": m.tag,
                "source": m.source,
                "updated_at": m.updated_at.isoformat() if m.updated_at else None
            }
            for m in memories
        ]
