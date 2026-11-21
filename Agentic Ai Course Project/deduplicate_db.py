import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import SessionLocal
from app.models.project import ResearchProject, ProjectDocument, FundingOpportunity
from app.models.proposal import ProposalDraft, BudgetPlan, ComplianceReport
from app.models.memory import ProjectMemory, AuditLog, ApprovalRecord
from app.models.lab_result import LabExecutionResult
from collections import defaultdict

def cleanup_duplicates():
    db = SessionLocal()
    try:
        projects = db.query(ResearchProject).order_by(ResearchProject.id.asc()).all()
        print(f"Total projects before cleanup: {len(projects)}")

        # Group by normalized title
        grouped = defaultdict(list)
        for p in projects:
            norm_title = p.title.strip().lower()
            grouped[norm_title].append(p)

        deleted_count = 0
        for norm_title, projs in grouped.items():
            if len(projs) > 1:
                print(f"\nFound {len(projs)} duplicates for title: '{projs[0].title}'")
                # Keep the primary project: prefer the one with the smallest ID or most lab results
                def score_project(proj):
                    lab_count = db.query(LabExecutionResult).filter(LabExecutionResult.project_id == proj.id).count()
                    doc_count = db.query(ProjectDocument).filter(ProjectDocument.project_id == proj.id).count()
                    return (lab_count * 10 + doc_count, -proj.id)

                sorted_projs = sorted(projs, key=score_project, reverse=True)
                primary = sorted_projs[0]
                duplicates = sorted_projs[1:]
                print(f"  Keeping primary Project ID: {primary.id}")

                for dup in duplicates:
                    print(f"  Removing duplicate Project ID: {dup.id}")
                    # Reassign or delete dependent records
                    # SQLite cascade will delete them cleanly with db.delete(dup)
                    db.delete(dup)
                    deleted_count += 1

        db.commit()
        remaining = db.query(ResearchProject).all()
        print(f"\nCleanup complete. Deleted {deleted_count} duplicate projects.")
        print(f"Total unique projects remaining: {len(remaining)}")
        for p in remaining:
            print(f"  ID: {p.id} | Domain: {p.domain} | Title: {p.title}")

    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicates()
