from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.memory import AuditLog

class SystemAuditLogger:
    @staticmethod
    def log(db: Session, project_id: Optional[int], agent_name: str, action: str, 
            details: Dict[str, Any], prompt_used: Optional[str] = None, 
            response_received: Optional[str] = None, lab_number: Optional[int] = None):
        """
        Persists an immutable audit log record for agent execution and compliance auditing.
        """
        record = AuditLog(
            project_id=project_id,
            lab_number=lab_number,
            agent_name=agent_name,
            action=action,
            details=details,
            prompt_used=prompt_used,
            response_received=response_received,
            timestamp=datetime.utcnow()
        )
        db.add(record)
        try:
            db.commit()
            return record.id
        except Exception:
            db.rollback()
            return None

    @staticmethod
    def get_logs(db: Session, project_id: Optional[int] = None, limit: int = 50):
        query = db.query(AuditLog)
        if project_id:
            query = query.filter(AuditLog.project_id == project_id)
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
