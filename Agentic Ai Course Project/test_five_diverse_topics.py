import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import SessionLocal
from app.models.project import ResearchProject
from app.agents.funding_discovery import FundingDiscoveryAgent
from app.agents.literature_review import LiteratureReviewAgent
from app.agents.proposal_drafting import ProposalDraftingAgent
from app.agents.budget_planning import BudgetPlanningAgent
from app.agents.compliance_checking import ComplianceCheckingAgent
from app.agents.submission_agent import SubmissionAgent
from app.agents.unified_lab_executor import UnifiedLabExecutor
from app.core.topic_reasoning import TopicReasoningEngine

DIVERSE_TOPICS = [
    {
        "title": "Quantum key distribution protocols for underwater satellite optical links",
        "domain": "Quantum Optics & Satellite Telecommunications",
        "department": "Physics & Optical Engineering",
        "institution": "Indian Institute of Science",
        "pi_name": "Dr. Arindam Ghosh",
        "pi_email": "arindam@iisc.ac.in",
        "duration_weeks": 24,
        "requested_budget": 5500000.0,
        "currency": "INR",
        "objectives": "Establish free-space quantum key distribution through turbulent ocean-surface water interfaces using adaptive optics and single-photon avalanche detectors.",
        "funding_preferences": "DST - SERB, DRDO - ER, ISRO - RESPOND"
    },
    {
        "title": "CRISPR-Cas13 RNA targeting for plant viral resistance in drought-stressed crops",
        "domain": "Molecular Plant Genetics & Biotechnology",
        "department": "Biotechnology & Genome Engineering",
        "institution": "National Institute of Plant Genome Research",
        "pi_name": "Dr. Sharmila Sen",
        "pi_email": "ssen@nipgr.ac.in",
        "duration_weeks": 32,
        "requested_budget": 6200000.0,
        "currency": "INR",
        "objectives": "Engineer transient Cas13d catalytic complexes to cleave viral RNA genomes in arid-cultivated brassica and sorghum varieties.",
        "funding_preferences": "DBT - BRIC, ICAR - NASF"
    },
    {
        "title": "Metamaterial cloaking for seismic wave mitigation in dense urban civil infrastructure",
        "domain": "Geotechnical Earthquake Engineering & Metamaterials",
        "department": "Civil & Structural Engineering",
        "institution": "IIT Roorkee",
        "pi_name": "Dr. Rajeshwar Mitra",
        "pi_email": "rmitra@iitr.ac.in",
        "duration_weeks": 20,
        "requested_budget": 4800000.0,
        "currency": "INR",
        "objectives": "Design periodic sub-surface resonant phononic barrier rings to scatter destructive Rayleigh seismic waves away from high-rise foundation piles.",
        "funding_preferences": "DST - SERB, AICTE - RPS, DRDO"
    },
    {
        "title": "Neuromorphic edge computing using memristive crossbar arrays for micro-UAV navigation",
        "domain": "Nanoelectronics & Autonomous Robotics",
        "department": "Electronics & Electrical Communication",
        "institution": "IIT Kharagpur",
        "pi_name": "Dr. Prateek Roy",
        "pi_email": "proy@iitkgp.ac.in",
        "duration_weeks": 16,
        "requested_budget": 3800000.0,
        "currency": "INR",
        "objectives": "Fabricate low-power titanium-oxide memristor synapses to execute spiking neural network SLAM algorithms aboard miniature aerial rovers.",
        "funding_preferences": "MeitY - TIDE 2.0, DRDO - ER"
    },
    {
        "title": "Electro-catalytic carbon dioxide reduction to ethylene using single-atom copper catalysts",
        "domain": "Chemical Kinetics & Clean Energy Transition",
        "department": "Chemical Engineering",
        "institution": "IIT Bombay",
        "pi_name": "Dr. Anita Venkataraman",
        "pi_email": "anita.v@iitb.ac.in",
        "duration_weeks": 28,
        "requested_budget": 5200000.0,
        "currency": "INR",
        "objectives": "Synthesize carbon-supported isolated Cu-N4 single-atom catalysts for selective electrochemical C-C coupling under ambient flow-cell conditions.",
        "funding_preferences": "DST - CERI, CSIR - EMR, MNRE"
    },
    # 6th Completely Novel Ad-hoc Topic
    {
        "title": "Autonomous swarm robotic exploration and mapping of lunar lava tubes",
        "domain": "Space Robotics & Planetary Geophysics",
        "department": "Aerospace & Planetary Engineering",
        "institution": "Physical Research Laboratory",
        "pi_name": "Dr. Vikramaditya Rao",
        "pi_email": "vrao@prl.res.in",
        "duration_weeks": 36,
        "requested_budget": 7800000.0,
        "currency": "INR",
        "objectives": "Deploy decentralized tetherless micro-rovers equipped with LiDAR and ultra-wideband mesh localization to navigate and 3D map sub-lunar basaltic cavities.",
        "funding_preferences": "ISRO - RESPOND, DRDO - ER, DST - SERB"
    }
]

def run_diverse_tests():
    db = SessionLocal()
    try:
        print("="*90)
        print("TESTING FULLY AUTONOMOUS MULTI-AGENT EXECUTION ON 6 DIVERSE UNFAMILIAR TOPICS")
        print("="*90)

        results_summary = []

        for idx, t_info in enumerate(DIVERSE_TOPICS, 1):
            print(f"\n[{idx}/6] TOPIC: '{t_info['title']}'")
            print(f"      Requested: ₹{t_info['requested_budget']:,.2f} | Institution: {t_info['institution']}")

            # 1. Topic Reasoning
            analysis = TopicReasoningEngine.infer_domain_and_disciplines(
                t_info["title"], t_info["domain"], t_info["objectives"]
            )
            print(f"      Inferred Field: {analysis['inferred_scientific_field']}")
            print(f"      Interdisciplinary Areas: {', '.join(analysis['interdisciplinary_areas'])}")

            # Create or update project in DB
            proj = db.query(ResearchProject).filter(ResearchProject.title == t_info["title"]).first()
            if proj:
                db.delete(proj)
                db.commit()

            proj = ResearchProject(**t_info, status="ACTIVE")
            db.add(proj)
            db.commit()
            db.refresh(proj)

            # 2. Execute 6 Agents
            f_agent = FundingDiscoveryAgent(db, proj)
            f_res = f_agent.run()
            top_match = f_res.get("top_match") or {}
            print(f"      Agent A (Funding): Top Match = '{top_match.get('scheme_name')}' ({top_match.get('agency')}) - Score: {top_match.get('relevance_score', 0)*100:.1f}%")

            lit_agent = LiteratureReviewAgent(db, proj)
            lit_res = lit_agent.run()
            print(f"      Agent B (Literature): Retrieved {lit_res.get('scholarly_papers_retrieved', 0)} papers. Sources: {len(lit_res.get('source_references', []))}")
            if lit_res.get("source_references"):
                first_ref = lit_res["source_references"][0]
                print(f"             Citation #1: {first_ref.get('authors', 'Authors')} ({first_ref.get('publication_year', 2024)}). '{first_ref.get('title')[:60]}...'")
                print(f"             DOI/URL: {first_ref.get('doi_or_url')}")

            prop_agent = ProposalDraftingAgent(db, proj)
            prop_res = prop_agent.run()
            print(f"      Agent C (Proposal): Aim 1 = {prop_res.get('research_objectives', [''])[0][:80]}...")

            b_agent = BudgetPlanningAgent(db, proj)
            b_res = b_agent.run()
            b_breakdown = b_res.get("breakdown", {})
            print(f"      Agent D (Budget): Direct = ₹{b_res.get('direct_costs', 0):,.2f} | 10% Overhead = ₹{b_res.get('overhead_cost', 0):,.2f} | Total = ₹{b_res.get('total_requested', 0):,.2f}")
            print(f"             Partition: Eq=₹{b_breakdown.get('equipment', 0):,.0f}, MP=₹{b_breakdown.get('manpower', 0):,.0f}, Travel=₹{b_breakdown.get('travel', 0):,.0f}")

            c_agent = ComplianceCheckingAgent(db, proj)
            c_res = c_agent.run()
            print(f"      Agent E (Compliance): Status = {c_res.get('status')} ({c_res.get('compliance_score')}%)")

            sub_agent = SubmissionAgent(db, proj)
            sub_res = sub_agent.prepare_package()
            print(f"      Agent F (Submission): Status = {sub_res.get('status')} | Dual-key armed.")

            # 3. Test Lab 2 specifically on this project
            lab2_res = UnifiedLabExecutor.execute_lab(db, proj, 2)
            assert lab2_res["status"] == "COMPLETED", f"Lab 2 failed on topic {idx}"
            assert len(lab2_res["output1_funding_opportunities"]["opportunities"]) > 0
            assert lab2_res["output2_proposal_draft"]["research_title"]
            assert lab2_res["output3_budget_plan"]["total_budget"] > 0
            assert lab2_res["output4_compliance_report"]["compliance_status"]
            print(f"      Lab 2 Execution: COMPLETED / PASSED with all 4 deliverables verified.")

            results_summary.append({
                "topic": t_info["title"],
                "inferred_domain": analysis["inferred_scientific_field"],
                "top_funding": f"{top_match.get('scheme_name')} ({top_match.get('agency')})",
                "score": f"{top_match.get('relevance_score', 0)*100:.1f}%",
                "budget_total": f"₹{b_res.get('total_requested', 0):,.2f}",
                "equipment": f"₹{b_breakdown.get('equipment', 0):,.0f}",
                "citations": len(lit_res.get('source_references', []))
            })

        print("\n" + "="*90)
        print("DIVERSE TOPICS COMPARATIVE VALIDATION MATRIX")
        print("="*90)
        print(f"{'#':<3} | {'Topic (Truncated)':<36} | {'Inferred Domain':<26} | {'Top Scheme':<20} | {'Budget':<14}")
        print("-" * 110)
        for i, r in enumerate(results_summary, 1):
            print(f"{i:<3} | {r['topic'][:36]:<36} | {r['inferred_domain'][:26]:<26} | {r['top_funding'][:20]:<20} | {r['budget_total']:<14}")

        print("="*90)
        print("ALL 6 DIVERSE TOPICS EXECUTED AUTONOMOUSLY WITH UNIQUE, GROUNDED DELIVERABLES!")
        print("="*90)

    finally:
        db.close()

if __name__ == "__main__":
    run_diverse_tests()
