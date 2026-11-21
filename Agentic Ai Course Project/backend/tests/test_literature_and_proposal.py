import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.project import ResearchProject, ProjectDocument
from app.models.proposal import ProposalDraft
from app.models.memory import ProjectMemory
from app.agents.literature_review import LiteratureReviewAgent
from app.agents.proposal_drafting import ProposalDraftingAgent
import asyncio

class TestLiteratureAndProposalIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()
        self.project = ResearchProject(
            id=1,
            title="AI-based early disease detection",
            domain="Computer Science & Biomedical",
            institution="KLE Technological University",
            pi_name="Faculty Researcher",
            duration_weeks=8,
            requested_budget=1000000.0,
            status="DRAFT"
        )
        self.db.add(self.project)
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_literature_review_and_proposal_integration(self):
        # 1. Attach sample PDF and DOCX document records
        pdf_path = os.path.abspath("data/uploads/project_1/Deep_Learning_Biomarkers_Disease_Detection_2025.pdf")
        docx_path = os.path.abspath("data/uploads/project_1/Edge_AI_Sensors_Clinical_Monitoring_2024.docx")
        
        if os.path.exists(pdf_path):
            doc1 = ProjectDocument(
                project_id=self.project.id,
                filename="Deep_Learning_Biomarkers_Disease_Detection_2025.pdf",
                file_path=pdf_path,
                file_type="pdf",
                file_size=os.path.getsize(pdf_path),
                extracted_text="Investigation of Multi-Modal Deep Learning Biomarkers for Early Disease Detection. Authors: Dr. P. K. Kulkarni (2025). Sensitivity 94.6% on 650 clinical cohort sessions. Limitation: Requires edge hardware acceleration.",
                metadata_json={"title": "Multi-Modal Deep Learning Biomarkers", "year": 2025, "authors": "Dr. P. K. Kulkarni"}
            )
            self.db.add(doc1)

        if os.path.exists(docx_path):
            doc2 = ProjectDocument(
                project_id=self.project.id,
                filename="Edge_AI_Sensors_Clinical_Monitoring_2024.docx",
                file_path=docx_path,
                file_type="docx",
                file_size=os.path.getsize(docx_path),
                extracted_text="Wearable Edge-AI Biosensors for Continuous Clinical Telemetry. Authors: Dr. Ramesh N. Deshpande (2024). Retains 91.8% precision with 4.2x power reduction. Limitation: Lacks closed-loop multi-agent governance and 10% overhead cap verification.",
                metadata_json={"title": "Wearable Edge-AI Biosensors", "year": 2024, "authors": "Dr. Ramesh N. Deshpande"}
            )
            self.db.add(doc2)

        self.db.commit()

        # 2. Run Literature Review Agent (Agent B)
        agent_b = LiteratureReviewAgent(self.db, self.project)
        lit_res = asyncio.run(agent_b.run())

        self.assertEqual(lit_res["status"], "COMPLETED")
        self.assertGreaterEqual(lit_res["uploaded_documents_analyzed"], 1)
        self.assertGreaterEqual(len(lit_res["research_gaps"]), 1)
        self.assertGreaterEqual(len(lit_res["paper_comparison_matrix"]), 1)
        self.assertIn("literature_synthesis", lit_res)

        # Verify saved in ProjectMemory
        mem = self.db.query(ProjectMemory).filter(
            ProjectMemory.project_id == self.project.id,
            ProjectMemory.key == "literature_review_data"
        ).first()
        self.assertIsNotNone(mem)

        # 3. Run Proposal Drafting Agent (Agent C)
        agent_c = ProposalDraftingAgent(self.db, self.project)
        prop_res = agent_c.run()

        self.assertEqual(prop_res["status"], "COMPLETED")
        self.assertIn("Addressing Documented Research Gaps", prop_res["problem_statement"])
        self.assertGreaterEqual(len(prop_res["research_gaps_integrated"]), 1)
        self.assertIn("A comprehensive literature review", prop_res["literature_review"])

        # 4. Verify in ProposalDraft record in SQLite
        draft = self.db.query(ProposalDraft).filter(ProposalDraft.project_id == self.project.id).first()
        self.assertIsNotNone(draft)
        self.assertIn("literature_review", draft.sections_json)
        self.assertIn("research_gaps", draft.sections_json)

if __name__ == "__main__":
    unittest.main()
