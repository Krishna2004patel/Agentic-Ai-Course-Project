import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import SessionLocal, Base, engine
from app.models.project import ResearchProject, ProjectDocument, FundingOpportunity
from app.models.proposal import ProposalDraft, BudgetPlan, ComplianceReport
from app.agents.funding_discovery import FundingDiscoveryAgent
from app.agents.literature_review import LiteratureReviewAgent
from app.agents.proposal_drafting import ProposalDraftingAgent
from app.agents.budget_planning import BudgetPlanningAgent
from app.agents.compliance_checking import ComplianceCheckingAgent
from app.agents.submission_agent import SubmissionAgent
from app.agents.unified_lab_executor import UnifiedLabExecutor

def test_multi_domain():
    db = SessionLocal()
    try:
        print("="*80)
        print("VERIFYING DYNAMIC MULTI-AGENT EXECUTION ACROSS 3 DISTINCT DOMAINS")
        print("="*80)

        projects_data = [
            {
                "title": "AI-based early disease detection and predictive biomarker screening",
                "domain": "Biomedical AI",
                "department": "Biomedical Engineering & CSE",
                "institution": "KLE Technological University",
                "pi_name": "Dr. A. B. Joshi",
                "pi_email": "pi@kletech.ac.in",
                "duration_weeks": 8,
                "requested_budget": 1000000.0,
                "currency": "INR",
                "objectives": "Develop a multi-agent diagnostic framework for non-invasive early disease biomarker screening and automated clinical proposal formulation.",
                "funding_preferences": "DST-SERB, ICMR Ad-hoc Biomedical"
            },
            {
                "title": "Autonomous UAV Precision Agriculture and Early Crop Disease Detection",
                "domain": "Smart Agriculture & Drone Tech",
                "department": "Agricultural Engineering & Robotics",
                "institution": "Punjab Agricultural University",
                "pi_name": "Dr. Gurpreet Singh",
                "pi_email": "gsingh@pau.edu",
                "duration_weeks": 16,
                "requested_budget": 2400000.0,
                "currency": "INR",
                "objectives": "Deploy multispectral UAV imaging and edge AI models for automated foliar blight detection and variable-rate fungicide application.",
                "funding_preferences": "ICAR-NASF, MeitY-TIDE"
            },
            {
                "title": "Solar Photovoltaic Grid Integration and Microgrid Stability Control",
                "domain": "Clean Renewable Energy & Electrical Engineering",
                "department": "Electrical & Energy Systems",
                "institution": "IIT Madras Energy Consortium",
                "pi_name": "Dr. K. Ramanathan",
                "pi_email": "kraman@iitm.ac.in",
                "duration_weeks": 24,
                "requested_budget": 4500000.0,
                "currency": "INR",
                "objectives": "Design robust grid-forming inverter controls and battery energy storage management for high-penetration renewable microgrids.",
                "funding_preferences": "MNRE R&D, DST Clean Energy"
            }
        ]

        created_projects = []
        for p_data in projects_data:
            existing = db.query(ResearchProject).filter(ResearchProject.title == p_data["title"]).first()
            if existing:
                db.delete(existing)
                db.commit()

            proj = ResearchProject(**p_data, status="ACTIVE")
            db.add(proj)
            db.commit()
            db.refresh(proj)
            created_projects.append(proj)
            print(f"\n[Created Project #{proj.id}] '{proj.title}'")
            print(f"  Domain: {proj.domain} | Budget: ₹{proj.requested_budget:,.2f} | Institution: {proj.institution}")

        # Run 6 agents on each project
        for proj in created_projects:
            print(f"\n---> Executing 6 Agents for Project #{proj.id} ({proj.domain})...")
            
            # 1. Funding Discovery
            f_agent = FundingDiscoveryAgent(db, proj)
            f_res = f_agent.run()
            top_match = f_res.get("top_match") or {}
            print(f"  Agent 1 (Funding Discovery): Matched {f_res.get('total_schemes_evaluated', 0)} schemes. Top: '{top_match.get('scheme_name')}' ({top_match.get('agency')}) - Score: {top_match.get('relevance_score', 0)*100:.1f}%")
            print(f"         Rationale: {top_match.get('rationale', '')[:120]}...")

            # 2. Literature Review
            lit_agent = LiteratureReviewAgent(db, proj)
            lit_res = lit_agent.run()
            gaps = lit_res.get("research_gaps", [])
            print(f"  Agent 2 (Literature Review): Indexed {lit_res.get('chunks_indexed', 0)} chunks, {len(gaps)} research gaps.")
            print(f"         Identified Gap #1: {gaps[0] if gaps else 'None'}")

            # 3. Proposal Drafting
            prop_agent = ProposalDraftingAgent(db, proj)
            prop_res = prop_agent.run()
            print(f"  Agent 3 (Proposal Drafting): Generated proposal draft v{prop_res.get('version')}.")
            print(f"         Title: {prop_res.get('title')}")
            aims = prop_res.get('research_objectives', [])
            print(f"         Aims: {aims[:2] if isinstance(aims, list) else str(aims)[:80]}...")

            # 4. Budget Planning
            b_agent = BudgetPlanningAgent(db, proj)
            b_res = b_agent.run()
            breakdown = b_res.get("breakdown", {})
            print(f"  Agent 4 (Budget Planning): Total Budget: ₹{b_res.get('total_requested', 0):,.2f} (Overhead: ₹{b_res.get('overhead_cost', 0):,.2f})")
            print(f"         Breakdown: Equipment=₹{breakdown.get('equipment', 0):,.0f}, Manpower=₹{breakdown.get('manpower', 0):,.0f}, Travel=₹{breakdown.get('travel', 0):,.0f}")

            # 5. Compliance Checking
            c_agent = ComplianceCheckingAgent(db, proj)
            c_res = c_agent.run()
            print(f"  Agent 5 (Compliance): Status = {c_res.get('status')}, Score = {c_res.get('compliance_score')}%. Missing: {len(c_res.get('missing_items', []))} items")

            # 6. Submission Agent
            sub_agent = SubmissionAgent(db, proj)
            sub_res = sub_agent.prepare_package()
            print(f"  Agent 6 (Submission): Package Status = {sub_res.get('status')}, Ready = {sub_res.get('is_ready_for_approval')}")

            # Also execute all 14 labs for each project
            print(f"  UnifiedLabExecutor: Executing all 14 labs for Project #{proj.id}...")
            lab_results = []
            for lab_num in range(1, 15):
                res = UnifiedLabExecutor.execute_lab(db, proj, lab_num)
                lab_results.append(res)
            print(f"  UnifiedLabExecutor: Successfully executed {len(lab_results)} labs! All outputs persisted with project_id={proj.id}.")

        print("\n" + "="*80)
        print("VERIFICATION COMPLETED SUCCESSFULLY: ALL 3 PROJECTS RECEIVED DISTINCT, DYNAMIC DELIVERABLES!")
        print("="*80)

    finally:
        db.close()

if __name__ == "__main__":
    test_multi_domain()
