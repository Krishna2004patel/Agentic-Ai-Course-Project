import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import SessionLocal
from app.models.project import ResearchProject
from app.agents.unified_lab_executor import UnifiedLabExecutor

def test_labs():
    db = SessionLocal()
    try:
        project = db.query(ResearchProject).filter(ResearchProject.id == 1).first()
        if not project:
            project = db.query(ResearchProject).first()

        print(f"Testing All 14 Labs Independently on Project #{project.id}: '{project.title}'")
        print("="*85)

        for lab_num in range(1, 15):
            res = UnifiedLabExecutor.execute_lab(db, project, lab_num)
            
            # Assertions
            assert res["status"] == "COMPLETED", f"Lab {lab_num} failed status check"
            assert res["evaluation_status"] == "PASSED", f"Lab {lab_num} failed evaluation status"
            
            opps = res["output1_funding_opportunities"]["opportunities"]
            assert len(opps) > 0, f"Lab {lab_num} missing Output 1 opportunities"
            
            draft = res["output2_proposal_draft"]
            assert draft["research_title"], f"Lab {lab_num} missing Output 2 title"
            assert draft["methodology"], f"Lab {lab_num} missing Output 2 methodology"
            
            budget = res["output3_budget_plan"]
            assert budget["total_budget"] > 0, f"Lab {lab_num} missing Output 3 total_budget"
            assert budget["statutory_overhead_10_percent"] > 0, f"Lab {lab_num} missing Output 3 overhead"
            
            compliance = res["output4_compliance_report"]
            assert compliance["compliance_status"] in ("COMPLIANT", "WARNINGS"), f"Lab {lab_num} invalid compliance status"
            
            evidence = res["lab_concept_evidence"]
            assert evidence is not None, f"Lab {lab_num} missing concept evidence"

            print(f"  [PASS] Lab {lab_num:02d}: {res['lab_title'][:42]:<42} | Opps: {len(opps)} | Budget: ₹{budget['total_budget']:,.2f} | Evidence Keys: {list(evidence.keys())[:3]}")

        print("="*85)
        print("ALL 14 LABS TESTED AND VERIFIED INDEPENDENTLY WITH 4 EXPECTED DELIVERABLES!")

    finally:
        db.close()

if __name__ == "__main__":
    test_labs()
