import unittest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, Base, engine
from app.models.project import ResearchProject
from app.agents.lab1_planning import ResearchPlanningAgent
from app.agents.lab2_tools import ToolUsingGrantAgent
from app.agents.lab3_skills import SkillEvaluationAgent
from app.agents.lab4_memory import MemoryEvaluationAgent
from app.agents.lab5_mcp import MCPEvaluationAgent
from app.agents.lab6_runtime import RuntimeEvaluationAgent
from app.agents.lab7_node_graph import NodeGraphEvaluationAgent
from app.agents.lab8_swarm import ParallelSwarmEvaluationAgent
from app.agents.lab9_rag import DeepResearchRAGAgent
from app.agents.lab10_ops import OperationsMonitoringAgent
from app.agents.lab11_pipeline import PipelineEvaluationAgent
from app.agents.lab12_governance import SafetyEvaluationAgent
from app.agents.lab13_discipline import DisciplineSpecificEvaluationAgent
from app.agents.lab14_capstone import CapstoneEvaluationAgent
from app.agents.funding_discovery import FundingDiscoveryAgent
from app.agents.literature_review import LiteratureReviewAgent
from app.agents.proposal_drafting import ProposalDraftingAgent
from app.agents.budget_planning import BudgetPlanningAgent
from app.agents.compliance_checking import ComplianceCheckingAgent
from app.agents.submission_agent import SubmissionAgent

class TestGrantManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()
        cls.project = cls.db.query(ResearchProject).first()
        if not cls.project:
            cls.project = ResearchProject(
                title="AI-based early disease detection",
                domain="Biomedical AI & Computer Science",
                department="CSE (AI)",
                institution="KLE Technological University",
                pi_name="Dr. A. B. Joshi",
                pi_email="pi@kletech.ac.in",
                duration_weeks=8,
                requested_budget=1000000.0,
                status="DRAFT"
            )
            cls.db.add(cls.project)
            cls.db.commit()
            cls.db.refresh(cls.project)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_lab1_planning_agent(self):
        agent = ResearchPlanningAgent(self.db, self.project)
        res = agent.run_planning_cycle(user_feedback="Expand biomarker survey")
        self.assertTrue(res["goal_satisfied"])
        self.assertIn("milestones", res["revised_plan"])

    def test_02_lab2_tool_using_agent(self):
        agent = ToolUsingGrantAgent(self.db, self.project)
        res = agent.execute_all_tools()
        self.assertGreaterEqual(res["tool_count"], 4)

    def test_03_lab3_skill_creation(self):
        agent = SkillEvaluationAgent(self.db, self.project)
        res = agent.execute_and_test_skills()
        self.assertEqual(len(res["skills_executed"]), 4)
        self.assertTrue(res["reusability_test"]["reusability_verified"])

    def test_04_lab4_memory_retrieval(self):
        agent = MemoryEvaluationAgent(self.db, self.project)
        res = agent.execute_memory_lifecycle()
        self.assertTrue(res["project_isolation_verified"])
        self.assertIn("conflict_detection_demonstration", res)

    def test_05_lab5_mcp_connector(self):
        agent = MCPEvaluationAgent(self.db, self.project)
        res = agent.execute_mcp_tests()
        self.assertTrue(res["security_boundary_enforcement"]["blocked"])

    def test_06_lab6_agent_runtime(self):
        agent = RuntimeEvaluationAgent(self.db, self.project)
        res = agent.execute_runtime_test()
        self.assertEqual(res["stop_reason"], "Goal satisfied")

    def test_07_lab7_node_graph(self):
        agent = NodeGraphEvaluationAgent(self.db, self.project)
        res = agent.execute_node_graph()
        self.assertTrue(res["all_nodes_passed"])
        self.assertEqual(res["completed_nodes"], 9)

    def test_08_lab8_parallel_swarm(self):
        agent = ParallelSwarmEvaluationAgent(self.db, self.project)
        res = agent.execute_swarm()
        self.assertEqual(res["workers_executed"], 4)
        self.assertGreaterEqual(res["conflict_count"], 1)

    def test_09_lab9_deep_research_rag(self):
        agent = DeepResearchRAGAgent(self.db, self.project)
        res = agent.execute_rag_pipeline()
        self.assertGreaterEqual(len(res["citations"]), 1)

    def test_10_lab10_operations_monitoring(self):
        agent = OperationsMonitoringAgent(self.db, self.project)
        res = agent.execute_monitoring_cycle()
        self.assertGreaterEqual(len(res["diagnoses"]), 2)

    def test_11_lab11_pipeline_sdlc(self):
        agent = PipelineEvaluationAgent(self.db, self.project)
        res = agent.execute_sdlc_pipeline()
        self.assertEqual(len(res["stages_executed"]), 6)

    def test_12_lab12_safety_governance(self):
        agent = SafetyEvaluationAgent(self.db, self.project)
        res = agent.execute_safety_audit()
        self.assertIn("LOCKED", res["submission_gate_status"])

    def test_13_lab13_discipline_specific(self):
        agent = DisciplineSpecificEvaluationAgent(self.db, self.project)
        res = agent.execute_discipline_evaluations()
        self.assertEqual(len(res["disciplines_supported"]), 3)

    def test_14_lab14_capstone_integration(self):
        agent = CapstoneEvaluationAgent(self.db, self.project)
        res = agent.execute_capstone()
        self.assertIn("downloadable_artifacts", res)
        self.assertEqual(len(res["regression_evaluation"]), 5)

    def test_15_literature_review_agent_b(self):
        agent = LiteratureReviewAgent(self.db, self.project)
        res = agent.run()
        self.assertEqual(res["status"], "COMPLETED")
        self.assertGreaterEqual(res["uploaded_documents_analyzed"], 1)
        self.assertGreaterEqual(len(res["research_gaps"]), 1)
        self.assertGreaterEqual(len(res["paper_comparison_matrix"]), 1)
        self.assertIn("literature_synthesis", res)

    def test_16_proposal_drafting_literature_connection(self):
        agent_c = ProposalDraftingAgent(self.db, self.project)
        res = agent_c.run()
        self.assertEqual(res["status"], "COMPLETED")
        self.assertIn("Addressing Documented Research Gaps", res["problem_statement"])
        self.assertGreaterEqual(len(res["research_gaps_integrated"]), 1)
        self.assertTrue("literature review" in res["literature_review"].lower())

    def test_17_all_14_labs_generate_four_expected_outputs(self):
        from app.agents.unified_lab_executor import UnifiedLabExecutor
        for lab_num in range(1, 15):
            res = UnifiedLabExecutor.execute_lab(self.db, self.project, lab_num)
            self.assertEqual(res["status"], "COMPLETED", f"Lab {lab_num} failed status check")
            self.assertEqual(res["evaluation_status"], "PASSED", f"Lab {lab_num} failed eval status")
            
            # Check 4 Expected Outputs exist and are populated
            self.assertIn("output1_funding_opportunities", res, f"Lab {lab_num} missing Output 1")
            self.assertIn("output2_proposal_draft", res, f"Lab {lab_num} missing Output 2")
            self.assertIn("output3_budget_plan", res, f"Lab {lab_num} missing Output 3")
            self.assertIn("output4_compliance_report", res, f"Lab {lab_num} missing Output 4")
            
            self.assertGreaterEqual(len(res["output1_funding_opportunities"]["opportunities"]), 1)
            self.assertIn("research_title", res["output2_proposal_draft"])
            self.assertGreater(res["output3_budget_plan"]["total_budget"], 0)
            self.assertIn("compliance_status", res["output4_compliance_report"])
            
            # Check 6 Agent Statuses
            self.assertEqual(len(res["six_agent_statuses"]), 6, f"Lab {lab_num} must have all 6 agent statuses")
            
            # Check Concept Evidence
            self.assertIn("lab_concept_evidence", res, f"Lab {lab_num} missing concept evidence")

if __name__ == "__main__":
    unittest.main()
