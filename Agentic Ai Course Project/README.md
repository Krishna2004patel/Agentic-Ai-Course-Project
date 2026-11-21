# Research Grant Management System – Multi-Agent Agentic AI Application
**Course:** AGENTIC AI (26ECAC401)  
**Host Institution:** KLE Technological University, Hubballi, Karnataka  
**Discipline:** Computer Science & Engineering (AI)  

---

## 1. Project Overview

The **Research Grant Management System** is an end-to-end multi-agent AI application designed to assist university faculty and researchers throughout the complete research grant lifecycle:
- Research Topic Discovery & Requirement Clarification
- Funding Opportunity Identification & Relevance Ranking
- Prior Art Synthesis & Academic Literature Review
- Formal Proposal Drafting & In-Place Plan Mutation
- Arithmetic Budget Allocation & 10% Statutory Overhead Capping
- Regulatory & Eligibility Compliance Auditing
- Human-in-the-Loop Governance & Final Submission Dossier Packaging

All **14 Hands-on Labs** from the *Agentic AI Systems Lab Guide* have been mapped and implemented into the **Research Grant Management System** domain.

---

## 2. The Six Specialized AI Agents

1. **Funding Discovery Agent (Agent A):**
   - Matches project scope against DST, SERB, ICMR, AICTE, MeitY, and OpenAlex.
   - Computes normalized relevance scores and match rationales.
2. **Literature Review Agent (Agent B):**
   - Ingests uploaded papers (PDF, DOCX) and scholarly citations.
   - Formulates comparative prior art matrices and extracts research gaps.
3. **Proposal Drafting Agent (Agent C):**
   - Produces structured research proposals (aims, methodology, milestones).
   - Dynamically mutates existing plans upon faculty feedback without re-running from scratch.
4. **Budget Planning Agent (Agent D):**
   - Computes equipment, manpower, travel, software, consumables, 5% contingency, and 10% statutory institutional overhead.
5. **Compliance Checking Agent (Agent E):**
   - Audits proposals against national funding caps, institutional credentials, and required attachments.
6. **Submission Agent (Agent F):**
   - Bundles JSON dossiers and Markdown documents; strictly enforces a **Human Approval Gate (Dean R&D sign-off)** before external transmission.

---

## 3. Mapping of All 14 Labs to the Grant Domain

| Lab # | Lab Title | Grant Domain Implementation | Responsible Agent | Expected Output Focus |
|---|---|---|---|---|
| **L1** | Agent vs Chatbot | Grant Planning Agent with checkable goal predicates | Research Planning Agent | Goal check status, roadmap milestones, and delta plan mutation |
| **L2** | Tool-Using Agent | CSV, JSON, Calculator, Document & Funding API tools | Tool-Using Agent | Arithmetic budget totals, overhead calculation, parsed files |
| **L3** | Skill Creation | Reusable packages: summary, proposal, budget, compliance | Skill Creation Agent | 4 structured skill outputs; reusability verified on 2nd project |
| **L4** | Memory & Retrieval | Project-isolated memory, session vs long-term storage | Memory & Retrieval Agent | Tagged facts, stale warnings (>30 days), conflict detection |
| **L5** | MCP-Style Connector | MCP server exposing resources & read-only SQLite tool | MCP Connector Agent | Manifest schema, authorized query results, blocked DROP queries |
| **L6** | Agent Runtime | OpenCLA-style loop: task interface, skill/tool registry | Agent Runtime Engine | Dynamic skill registration at runtime without altering core loop |
| **L7** | Agentic Node Graph | 9-node DAG workflow from intake to submission | Node Graph Engine | Visual DAG graph with retry strategy and node execution states |
| **L8** | Parallel Swarm | Concurrent ThreadPool execution of 4 agents | Parallel Swarm Orchestrator | Concurrent worker outputs, detected conflicts, resolved decisions |
| **L9** | Agentic RAG | Document chunking, TF-IDF vector retrieval, citations | Deep Research RAG Agent | Evidence synthesis table, chunk citations, contradiction analysis |
| **L10** | Operations Monitoring | Telemetry monitoring, root cause, severity, recovery | Operations Monitoring Agent | Subsystem failure diagnoses, blocked destructive recovery actions |
| **L11** | Agentic SDLC Pipeline | 6-agent software engineering factory for grant features | SDLC Factory Orchestrator | Requirement stories, independent testing from AC, release gates |
| **L12** | Safety & Governance | Invariant submission blocker, RBAC, risk scoring | Safety & Governance Agent | Mandatory human gate status, risk scorecard, rollback plan |
| **L13** | Discipline-Specific Agents | Engineering proposals: Mechanical, Civil, Electrical | Discipline-Specific Coordinator | Predictive maintenance, infrastructure safety, and microgrid plans |
| **L14** | Capstone Integration | Complete end-to-end grant management integration | Capstone System Architect | All 14 labs unified, downloadable dossier package, evaluation suite |

---

## 4. Key Dashboards

### A. Teacher Dashboard
- Independent inspection of each of the 14 labs with dedicated cards.
- Project selector dropdown allowing teachers to view lab results for any research project.
- Shows completion status, execution status, and evaluation status separately.
- Displays only the relevant expected output for each lab.
- Live "Run Lab" and "Execute All 14 Labs" buttons.

### B. Researcher Dashboard
- High-level KPIs: Active projects, funding opportunities discovered, proposals generated, pipeline budget.
- Live agent activity audit stream.
- Research Project Workspace with individual agent triggers (A through F), document uploader (PDF/DOCX), budget calculator, compliance report, and downloadable dossiers.

---

## 5. Quick Start Instructions

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ (Tested on Node.js 22.21.0)

### Running the Application
From the project root directory, run:
```bash
python run_application.py
```
Or on Windows:
```cmd
start_server.bat
```

Open your browser at:
- **Full Application (Web UI):** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **FastAPI Interactive Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Running Automated Test Suite
To verify all 14 labs programmatically:
```bash
python backend/tests/test_all_14_labs.py
```
*(All 14 unit test assertions pass in ~0.5s).*

---

## 6. Demonstration Workflow

1. **Inspect Seeded Project:**
   - Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).
   - View default project: *"AI-based early disease detection"* at KLE Technological University (8 weeks, ₹10,00,000).
2. **Switch to Teacher Dashboard:**
   - Click **Teacher Dashboard (14 Labs)** in the top right navbar.
   - Click through any lab card (e.g. Lab 1, Lab 4, Lab 7, Lab 8, Lab 14) to inspect its exact expected output.
   - Click **Run Lab** on any card to witness live autonomous agent execution.
3. **Create a Dynamic New Project:**
   - Click **New Research Project**.
   - Enter a custom topic (e.g., *"Predictive Maintenance for Wind Turbines"*), budget, and duration.
   - Submit to watch the multi-agent orchestrator create a dedicated isolated context and generate tailored grant results.
4. **Test Human Governance Gate:**
   - In Project Workspace, navigate to the **Submission Dossier & Approval** tab.
   - Notice the submission is locked until the simulated Dean sign-off is granted.
   - Download the final generated grant proposal as Markdown or JSON.
