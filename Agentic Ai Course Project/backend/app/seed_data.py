from sqlalchemy.orm import Session
from datetime import datetime
from .database import SessionLocal, Base, engine
from .models.user import User
from .models.project import ResearchProject, ProjectDocument, FundingOpportunity
from .models.proposal import ProposalDraft, BudgetPlan, ComplianceReport
from .models.memory import ProjectMemory, AuditLog, ApprovalRecord
from .models.lab_result import LabExecutionResult
from .agents.lab1_planning import ResearchPlanningAgent
from .agents.lab2_tools import ToolUsingGrantAgent
from .agents.lab3_skills import SkillEvaluationAgent
from .agents.lab4_memory import MemoryEvaluationAgent
from .agents.lab5_mcp import MCPEvaluationAgent
from .agents.lab6_runtime import RuntimeEvaluationAgent
from .agents.lab7_node_graph import NodeGraphEvaluationAgent
from .agents.lab8_swarm import ParallelSwarmEvaluationAgent
from .agents.lab9_rag import DeepResearchRAGAgent
from .agents.lab10_ops import OperationsMonitoringAgent
from .agents.lab11_pipeline import PipelineEvaluationAgent
from .agents.lab12_governance import SafetyEvaluationAgent
from .agents.lab13_discipline import DisciplineSpecificEvaluationAgent
from .agents.lab14_capstone import CapstoneEvaluationAgent

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Seed Users (Researcher and Teacher)
        teacher = db.query(User).filter(User.username == "teacher_evaluator").first()
        if not teacher:
            teacher = User(
                username="teacher_evaluator",
                email="evaluator@kletech.ac.in",
                full_name="Prof. S. R. Kulkarni (Lab Evaluator)",
                role="teacher",
                department="Computer Science & Engineering",
                institution="KLE Technological University"
            )
            db.add(teacher)

        researcher = db.query(User).filter(User.username == "faculty_pi").first()
        if not researcher:
            researcher = User(
                username="faculty_pi",
                email="pi@kletech.ac.in",
                full_name="Dr. A. B. Joshi (Principal Investigator)",
                role="researcher",
                department="CSE (AI)",
                institution="KLE Technological University"
            )
            db.add(researcher)
        db.commit()

        # 2. Seed Default Project (per specification)
        # Topic: AI-based early disease detection
        # Institution: KLE Technological University
        # Duration: 8 weeks
        # Estimated Budget: ₹10,00,000
        project1 = db.query(ResearchProject).filter(ResearchProject.title == "AI-based early disease detection").first()
        if not project1:
            project1 = ResearchProject(
                title="AI-based early disease detection",
                domain="Biomedical AI & Computer Science",
                department="CSE (AI)",
                institution="KLE Technological University",
                pi_name="Dr. A. B. Joshi",
                pi_email="pi@kletech.ac.in",
                duration_weeks=8,
                requested_budget=1000000.0, # ₹10,00,000
                currency="INR",
                objectives="Develop a robust multi-agent diagnostic framework for non-invasive early disease biomarker screening and automated clinical proposal formulation.",
                funding_preferences="DST-SERB, ICMR Ad-hoc Biomedical",
                status="IN_REVIEW"
            )
            db.add(project1)
            db.commit()
            db.refresh(project1)

            # Add sample document reference
            doc = ProjectDocument(
                project_id=project1.id,
                filename="Research_Synopsis_Premature_Graying_and_Biomarkers.docx",
                file_path="./data/Research_Synopsis_Premature_Graying_and_Biomarkers.docx",
                file_type="docx",
                file_size=25980,
                extracted_text="Bharatesh Homoeopathic Medical College & Hospital PG Research Centre. Study on premature graying and physiological stress biomarkers under guidance of Senior Medical Officer."
            )
            db.add(doc)
            db.commit()

            # Execute 5 primary agents dynamically
            from .agents.funding_discovery import FundingDiscoveryAgent
            from .agents.literature_review import LiteratureReviewAgent
            from .agents.proposal_drafting import ProposalDraftingAgent
            from .agents.budget_planning import BudgetPlanningAgent
            from .agents.compliance_checking import ComplianceCheckingAgent

            FundingDiscoveryAgent(db, project1).run()
            LiteratureReviewAgent(db, project1).run()
            ProposalDraftingAgent(db, project1).run()
            BudgetPlanningAgent(db, project1).run()
            ComplianceCheckingAgent(db, project1).run()

            # Execute all 14 labs for the default seed project so teacher dashboard has live data immediately!
            print("Executing all 14 labs for Project 1...")
            ResearchPlanningAgent(db, project1).run_planning_cycle("Focus on non-invasive clinical biomarkers in Week 1")
            ToolUsingGrantAgent(db, project1).execute_all_tools()
            SkillEvaluationAgent(db, project1).execute_and_test_skills()
            MemoryEvaluationAgent(db, project1).execute_memory_lifecycle()
            MCPEvaluationAgent(db, project1).execute_mcp_tests()
            RuntimeEvaluationAgent(db, project1).execute_runtime_test()
            NodeGraphEvaluationAgent(db, project1).execute_node_graph()
            ParallelSwarmEvaluationAgent(db, project1).execute_swarm()
            DeepResearchRAGAgent(db, project1).execute_rag_pipeline()
            OperationsMonitoringAgent(db, project1).execute_monitoring_cycle()
            PipelineEvaluationAgent(db, project1).execute_sdlc_pipeline()
            SafetyEvaluationAgent(db, project1).execute_safety_audit()
            DisciplineSpecificEvaluationAgent(db, project1).execute_discipline_evaluations()
            CapstoneEvaluationAgent(db, project1).execute_capstone()
            print("All 14 labs successfully executed and persisted in database.")

        # Seed Secondary Project (Civil / Structural)
        project2 = db.query(ResearchProject).filter(ResearchProject.title == "Smart Fiber-Optic Sensor Networks for Infrastructure and Construction Safety").first()
        if not project2:
            project2 = ResearchProject(
                title="Smart Fiber-Optic Sensor Networks for Infrastructure and Construction Safety",
                domain="Civil Engineering",
                department="Civil Engineering",
                institution="KLE Technological University",
                pi_name="Dr. V. M. Patil",
                pi_email="vmpatil@kletech.ac.in",
                duration_weeks=12,
                requested_budget=2500000.0, # ₹25 Lakhs
                currency="INR",
                objectives="Deploy real-time optical fiber strain sensors and drone photogrammetry for bridge structural health monitoring.",
                funding_preferences="AICTE RPS, DST-SERB",
                status="DRAFT"
            )
            db.add(project2)
            db.commit()
            db.refresh(project2)

            FundingDiscoveryAgent(db, project2).run()
            LiteratureReviewAgent(db, project2).run()
            ProposalDraftingAgent(db, project2).run()
            BudgetPlanningAgent(db, project2).run()
            ComplianceCheckingAgent(db, project2).run()

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
