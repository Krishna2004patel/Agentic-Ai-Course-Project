import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_document():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(40, 44, 52)
    
    # Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_run = title_p.add_run("RESEARCH GRANT MANAGEMENT SYSTEM")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(22)
    title_run.bold = True
    title_run.font.color.rgb = RGBColor(16, 55, 131) # Deep Blue
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(18)
    sub_run = subtitle_p.add_run("System Overview, Technical Architecture & Comprehensive Data Sources Guide")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(13)
    sub_run.italic = True
    sub_run.font.color.rgb = RGBColor(90, 100, 115)
    
    # Metadata Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Title:", "Research Grant Management System (Multi-Agent Agentic AI Application)"),
        ("System Architecture:", "Autonomous Multi-Agent System (6 Specialized Agents + 14 Lab Concepts)"),
        ("Primary Deliverables:", "Ranked Funding Opportunities, Structured Proposal Draft, Budget Plan, Compliance Report"),
        ("Data Origin Modes:", "Live OpenAlex API, Curated Grant Catalog, SQLite ORM, Uploaded Docs (PDF/DOCX), Deterministic Calculators")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        c0.paragraphs[0].text = k
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].text = v
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "F8FAFC")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Heading 1: Project Overview
    h1 = doc.add_heading(level=1)
    h1_run = h1.add_run("1. Executive Project Overview: What is this Application?")
    h1_run.font.color.rgb = RGBColor(16, 55, 131)
    
    p = doc.add_paragraph(
        "The Research Grant Management System is an enterprise-grade, Multi-Agent Agentic AI application designed to support "
        "academic faculty, research investigators, and institutional research offices through the entire lifecycle of competitive "
        "research grant formulation. Unlike conventional CRUD management platforms or simplistic chatbot wrappers that merely "
        "generate isolated text blocks, this platform operates as a collaborative ecosystem of autonomous, goal-directed AI agents."
    )
    
    p = doc.add_paragraph(
        "The application addresses the significant administrative and cognitive burden faced by faculty investigators when applying "
        "for competitive research grants from national and international funding agencies (such as DST-SERB, ICMR, AICTE, MeitY, and BIRAC). "
        "By orchestrating specialized agents that execute planning loops, tool use, memory retrieval, RAG, and compliance verification, "
        "the system accelerates proposal turnaround time while eliminating eligibility mismatches and budgetary compliance errors."
    )
    
    # Key Capabilities List
    p = doc.add_paragraph("Key Capabilities of the System:")
    capabilities = [
        ("End-to-End Grant Lifecycle Automation:", "From research topic definition and literature gap discovery to financial modeling and submission packaging."),
        ("Multi-Agent Collaborative Reasoning:", "Six specialized AI agents communicate via a shared memory bus, passing structured context across stages."),
        ("Dual-Role User Interface:", "Dedicated Researcher View for faculty investigators and Teacher/Evaluator View to inspect lab-by-lab concept implementations."),
        ("Integration of 14 Agentic AI Labs:", "Demonstrates 14 core foundational paradigms of Agentic AI (loops, tools, skills, memory, MCP, DAGs, swarms, RAG, ops, safety, and capstone).")
    ]
    for bold_prefix, text in capabilities:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(bold_prefix + " ")
        r1.bold = True
        bp.add_run(text)
        
    # Heading 2: The Six Specialized AI Agents
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    h2 = doc.add_heading(level=1)
    h2_run = h2.add_run("2. The Six Specialized AI Agents")
    h2_run.font.color.rgb = RGBColor(16, 55, 131)
    
    doc.add_paragraph(
        "The platform's intelligence is distributed across six specialized, autonomous agents. Each agent possesses a distinct domain of responsibility, "
        "deterministic validation tools, and private/shared memory stores:"
    )
    
    agents_table = doc.add_table(rows=7, cols=3)
    agents_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Agent Designation", "Primary Responsibility", "Core Tools & Methodology"]
    for j, h in enumerate(headers):
        cell = agents_table.rows[0].cells[j]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "103783")
        
    agents_info = [
        ("Agent A: Funding Discovery Agent", "Scans national/international grant calls, analyzes eligibility, matches research topics against grant priorities, and ranks schemes with an explainable relevance score.", "FundingAPIConnectorTool, Keyword Overlap, Scheme Cap Filter, OpenAlex API"),
        ("Agent B: Literature Review Agent", "Synthesizes scholarly literature, extracts research gaps, catalogs state-of-the-art methodology, and parses investigator-uploaded proposal synopses.", "DocumentReaderTool (PDF/DOCX parser), TF-IDF Semantic Search, OpenAlex Scholarly Citation Engine"),
        ("Agent C: Proposal Drafting Agent", "Generates complete structured proposal drafts containing title, abstract, problem statement, objectives, work packages, methodology, and citations.", "ProjectMemory Bus (consumes Agent B synthesis), Structured Prompt Composition, Academic Markdown Formatter"),
        ("Agent D: Budget Planning Agent", "Constructs mathematically rigorous, statutory-compliant financial budgets including equipment, manpower, consumables, travel, contingency, and institutional overhead.", "FundingCalculatorTool, Statutory Overheads Engine (10% institutional overhead, 5% contingency limit)"),
        ("Agent E: Compliance Checking Agent", "Conducts regulatory audit across eligibility rules, budget caps, duration boundaries, mandatory endorsements, and ethical approvals.", "Institutional Checklist Rules Engine, Risk Matrix Evaluator, Threshold Comparator"),
        ("Agent F: Submission Agent", "Compiles all finalized deliverables into an official, verifiable submission dossier with cryptographic integrity hash (SHA-256) and audit logs.", "Dossier Packaging Engine, SHA-256 Checksum Generator, Audit Trail Logger")
    ]
    
    for i, row_data in enumerate(agents_info):
        row = agents_table.rows[i+1]
        for j, text in enumerate(row_data):
            c = row.cells[j]
            c.paragraphs[0].text = text
            c.paragraphs[0].runs[0].font.size = Pt(9)
            if j == 0:
                c.paragraphs[0].runs[0].bold = True
                c.width = Inches(2.2)
                set_cell_background(c, "F0F4F8")
            elif j == 1:
                c.width = Inches(2.3)
                set_cell_background(c, "FAFAFA" if i%2==0 else "FFFFFF")
            else:
                c.width = Inches(2.0)
                set_cell_background(c, "FAFAFA" if i%2==0 else "FFFFFF")

    # Heading 3: The Four Main Expected Outputs
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    h3 = doc.add_heading(level=1)
    h3_run = h3.add_run("3. The Four Main Expected Deliverables")
    h3_run.font.color.rgb = RGBColor(16, 55, 131)
    
    doc.add_paragraph(
        "Regardless of whether the application is executed from the Researcher Dashboard or via any of the 14 individual labs in the Teacher Dashboard, "
        "the six agents collaborate to produce four standardized, mandatory project deliverables:"
    )
    
    outputs_data = [
        ("1. Ranked Funding Opportunities:", "An ordered catalog of matching grant schemes (e.g. DST-SERB CRG, ICMR Ad-hoc, DST-CSRI, AICTE RPS, MeitY TIDE 2.0) displaying funding agency, grant ceiling amount, application deadline, faculty eligibility criteria, relevance score (0-100%), and a detailed matching rationale explanation."),
        ("2. Structured Proposal Draft:", "A publication-grade research grant document containing Proposal Title, Executive Abstract, Comprehensive Problem Statement, Literature Review & Prior Art, Identified Research Gaps, Specific Measurable Objectives, Proposed Technical Methodology, Work Breakdown Packages, Milestones Timeline, and Scholarly References."),
        ("3. Comprehensive Budget Plan:", "An itemized financial spreadsheet breakdown categorized into Direct Costs (Major & Minor Equipment, Personnel/JRF/SRF Manpower, Consumables, Travel, Software/Cloud licenses) plus automated computation of a 5.0% Contingency fund and a 10.0% Statutory Institutional Overhead per DST/SERB guidelines, with total requested grant amount and line-item justifications."),
        ("4. Compliance Verification Report:", "A regulatory checklist audit detailing Principal Investigator eligibility, institutional accreditation status, budget ceiling compliance, project duration limits, required documentation (Endorsement certificate, Bio-data, Quotations), identified compliance warnings, quantified risk score, and an overall compliance verdict (COMPLIANT, CONDITIONAL, or REJECTED).")
    ]
    for bold_p, txt in outputs_data:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(bold_p + " ")
        r.bold = True
        bp.add_run(txt)

    # Heading 4: DATA FETCHING DEEP-DIVE
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    h4 = doc.add_heading(level=1)
    h4_run = h4.add_run("4. Comprehensive Data Sources Guide: Where Does the Project Fetch All Its Data?")
    h4_run.font.color.rgb = RGBColor(16, 55, 131)
    
    doc.add_paragraph(
        "A critical strength of the Research Grant Management System is its robust, multi-tiered data acquisition architecture. "
        "The system fetches and synthesizes data from seven distinct, interconnected sources:"
    )
    
    # Source A
    doc.add_heading(level=2).add_run("Data Source 1: Live External Scholarly API (OpenAlex REST API)")
    doc.add_paragraph(
        "• Endpoint: https://api.openalex.org/works\n"
        "• Implementation File: backend/app/tools/funding_api.py (Method: FundingAPIConnectorTool.search_openalex_papers)\n"
        "• Data Fetched: Real academic publications, research articles, peer-reviewed journals, publication years, author listings, citation counts, DOI hyperlinks, and primary repository landing pages.\n"
        "• How It Works: When Agent B (Literature Review Agent) or Lab 9 (RAG) is invoked, the query terms extracted from the project topic are sent via an HTTP GET request to OpenAlex. When the system operates in offline/sandboxed demo mode, a curated scholarly citation fallback engine ensures guaranteed deterministic retrieval without network failures."
    )
    
    # Source B
    doc.add_heading(level=2).add_run("Data Source 2: National & International Funding Opportunities Catalog")
    doc.add_paragraph(
        "• Location: backend/app/tools/funding_api.py (Data Object: FUNDING_OPPORTUNITIES_CATALOG)\n"
        "• Agencies Covered: DST-SERB (Department of Science & Technology - Science and Engineering Research Board), ICMR (Indian Council of Medical Research), AICTE (All India Council for Technical Education), MeitY (Ministry of Electronics & Information Technology), and DST-CSRI.\n"
        "• Data Fields Extracted: Agency acronym, scheme name, maximum grant amount (₹25,00,000 to ₹1,00,00,000), project duration (24 to 36 months), application deadlines, faculty eligibility guidelines, relevant engineering domains, keyword match triggers, and official scheme URLs.\n"
        "• How It Works: The Funding Discovery Agent matches the investigator's research topic tokens against domain keywords, verifies if the requested budget is within the scheme ceiling, verifies institutional faculty eligibility, and scores each scheme using a weighted relevance algorithm."
    )
    
    # Source C
    doc.add_heading(level=2).add_run("Data Source 3: Relational Persistence Database (SQLite via SQLAlchemy ORM)")
    doc.add_paragraph(
        "• Database File: data/grant_system.db\n"
        "• Connection Config: backend/app/database.py & backend/app/config.py\n"
        "• Models Defined In: backend/app/models/ (project.py, proposal.py, memory.py, user.py, lab_result.py)\n"
        "• Stored Information:\n"
        "    - Users Table: Authenticated faculty PIs and teacher evaluators with institutional affiliations.\n"
        "    - Research Projects Table: Project ID, title, domain, department, PI name, duration, requested budget, status.\n"
        "    - Proposal Drafts Table: Generated abstracts, problem statements, objectives, work packages.\n"
        "    - Budget Plans Table: Equipment, manpower, consumables, travel, overhead amounts, and justifications.\n"
        "    - Compliance Reports Table: Checklist flags, warnings, risk scores, and approval timestamps.\n"
        "    - Lab Execution Results Table: Execution outputs, statuses, latencies, and concept evidence for all 14 labs.\n"
        "    - Project Memory Table: Key-value associative memory and shared inter-agent communication scratchpads."
    )
    
    # Source D
    doc.add_heading(level=2).add_run("Data Source 4: Document Upload & Multi-Format Parsing Engine")
    doc.add_paragraph(
        "• Implementation File: backend/app/tools/doc_reader.py (Class: DocumentReaderTool)\n"
        "• Formats Supported: Portable Document Format (.pdf via pypdf), Word Documents (.docx via python-docx and zipfile XML parsing), Plain Text (.txt), and Markdown (.md).\n"
        "• Sample Ingested Document: data/Research_Synopsis_Premature_Graying_and_Biomarkers.docx (synopsis of medical research with clinical biomarker methodology).\n"
        "• How It Works: When an investigator uploads prior research papers, institutional guidelines, or project synopses, DocumentReaderTool extracts text up to 15,000 characters, sanitizes encoding, and indexes the text chunks into ProjectMemory for Agent B and Agent C."
    )
    
    # Source E
    doc.add_heading(level=2).add_run("Data Source 5: Deterministic Financial & Regulatory Math Calculator")
    doc.add_paragraph(
        "• Implementation File: backend/app/tools/funding_calculator.py (Class: FundingCalculatorTool)\n"
        "• Mathematical Rules Applied:\n"
        "    - Direct Cost = Equipment + Manpower + Consumables + Travel + Software\n"
        "    - Contingency = Direct Cost × 5.0%\n"
        "    - Institutional Overhead = Direct Cost × 10.0% (standard DST-SERB statutory allowance for technical universities)\n"
        "    - Total Requested Grant = Direct Cost + Contingency + Institutional Overhead\n"
        "• Verification: Compares total requested grant against the selected funding agency ceiling and computes exact budget surplus or shortfall."
    )
    
    # Source F
    doc.add_heading(level=2).add_run("Data Source 6: Multi-Agent Episodic & Shared Working Memory Bus")
    doc.add_paragraph(
        "• Implementation File: backend/app/core/memory_manager.py (Class: MemoryManager & ProjectMemory)\n"
        "• Mechanism: Short-term scratchpad memory maintains active turn logs during agent execution loops. Long-term episodic memory indexes literature synthesis results, extracted keywords, and compliance rules in SQLite. When Agent C (Proposal Drafting) executes, it fetches its literature context directly from Agent B's indexed memory slice."
    )
    
    # Source G
    doc.add_heading(level=2).add_run("Data Source 7: Automated Database Seeding Engine")
    doc.add_paragraph(
        "• Implementation File: backend/app/seed_data.py (Function: seed_database)\n"
        "• Data Initialized:\n"
        "    - Primary Faculty Investigator: Dr. A. B. Joshi (CSE AI, Project: 'AI-based early disease detection', ₹10,00,000 budget, 8 weeks duration).\n"
        "    - Secondary Project: Dr. V. M. Patil (Civil Engineering, 'Smart Fiber-Optic Sensor Networks', ₹25,00,000 budget).\n"
        "    - Initial Lab Runs: Pre-executes baseline runs across labs so the Teacher Dashboard contains verified data immediately upon first launch."
    )
    
    # Summary Table of Data Sources
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    st = doc.add_table(rows=8, cols=3)
    st.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Data Source Name", "Type / Protocol", "Primary Contribution to Grant System"]
    for j, h in enumerate(s_headers):
        cell = st.rows[0].cells[j]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "103783")
        
    s_rows = [
        ("OpenAlex API", "External REST (HTTPS)", "Real academic citations, papers, DOIs, authors, publication years"),
        ("Grant Scheme Catalog", "Structured Python Dicts", "National grant schemes, deadlines, funding ceilings, eligibility criteria"),
        ("SQLite Database", "Local Relational ORM", "Persistent storage for projects, drafts, budgets, audit logs, lab outputs"),
        ("Document Reader Tool", "File Parser (PyPDF/docx)", "Ingestion of uploaded research proposals, PDFs, DOCX synopses"),
        ("Funding Calculator", "Deterministic Math Tool", "Statutory financial models, 10% overhead, 5% contingency, line-item costs"),
        ("Project Memory Bus", "Episodic Shared Memory", "Cross-agent state transfer (e.g. Agent B literature -> Agent C proposal)"),
        ("Database Seeder", "Automated Python Script", "Default users, projects, documents, and baseline execution data")
    ]
    for i, r_data in enumerate(s_rows):
        row = st.rows[i+1]
        for j, val in enumerate(r_data):
            c = row.cells[j]
            c.paragraphs[0].text = val
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
            if j == 0:
                c.paragraphs[0].runs[0].bold = True
                c.width = Inches(1.8)
                set_cell_background(c, "F0F4F8")
            elif j == 1:
                c.width = Inches(1.8)
                set_cell_background(c, "FAFAFA" if i%2==0 else "FFFFFF")
            else:
                c.width = Inches(2.9)
                set_cell_background(c, "FAFAFA" if i%2==0 else "FFFFFF")

    # Heading 5: 14 Labs Architecture
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    h5 = doc.add_heading(level=1)
    h5_run = h5.add_run("5. The 14 Labs Architecture: How Every Lab Generates All Four Outputs")
    h5_run.font.color.rgb = RGBColor(16, 55, 131)
    
    doc.add_paragraph(
        "A foundational architectural achievement of this project is the Unified Lab Execution Engine (backend/app/agents/unified_lab_executor.py). "
        "In traditional academic projects, different lab exercises often produce fragmented, disjointed outputs. In this platform, "
        "every single lab from Lab 1 to Lab 14 applies its distinctive Agentic AI concept to coordinate the six specialized agents and generate "
        "the same four standardized project deliverables:"
    )
    
    labs_data = [
        ("Lab 1: Agent vs Chatbot", "Agents execute in an autonomous feedback loop, mutating plans dynamically based on funding feasibility."),
        ("Lab 2: Tool-Using Agents", "Agents invoke deterministic calculation tools and external search tools via function calling."),
        ("Lab 3: Reusable Skills", "Agents compose reusable modular skill files (literature_searcher, budget_builder, compliance_auditor)."),
        ("Lab 4: Memory & Retrieval", "Agents persist intermediate discoveries into short-term working memory and long-term episodic memory."),
        ("Lab 5: Model Context Protocol (MCP)", "Agents communicate through standardized MCP tool servers and protocol schemas."),
        ("Lab 6: Agent Runtime & Lifecycle", "Agents execute within a lifecycle sandbox with strict token, step, and timeout limits."),
        ("Lab 7: Node Graph & DAG Engine", "Agent execution is modeled as a Directed Acyclic Graph (DAG) with dependency resolution."),
        ("Lab 8: Multi-Agent Parallel Swarms", "Agents execute in parallel swarms (e.g. Literature and Budget agents running concurrently)."),
        ("Lab 9: Multi-Agent RAG", "Deep research RAG retrieves relevant scholarly literature and injects grounded evidence into the proposal."),
        ("Lab 10: AgentOps & Observability", "Tracks execution latency, token consumption, audit traces, and agent reliability metrics."),
        ("Lab 11: Agentic Software Engineering", "Implements an SDLC pipeline: Requirements analysis, Specification, Code generation, and Verification."),
        ("Lab 12: Safety, Security & Guardrails", "Enforces input guardrails, PII redaction, prompt injection defense, and budget safety constraints."),
        ("Lab 13: Agentic Discipline & HITL", "Incorporates Human-in-the-Loop approval gates for budget approval and compliance sign-off."),
        ("Lab 14: Integrated Capstone System", "End-to-end integration of all 13 concepts into an enterprise-grade grant formulation suite.")
    ]
    for lab_title, lab_desc in labs_data:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(lab_title + ": ")
        r.bold = True
        bp.add_run(lab_desc)

    # Heading 6: Technology Stack & Execution
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    h6 = doc.add_heading(level=1)
    h6_run = h6.add_run("6. Technical Stack & Execution Instructions")
    h6_run.font.color.rgb = RGBColor(16, 55, 131)
    
    doc.add_paragraph(
        "• Backend Framework: FastAPI (Python 3.14) with Uvicorn ASGI server\n"
        "• Frontend Framework: React 18 with TypeScript, Vite build tool, and TailwindCSS\n"
        "• Database: SQLite with SQLAlchemy ORM\n"
        "• Document Extraction: PyPDF for PDF parsing, python-docx and XML parser for DOCX\n"
        "• External HTTP Client: HTTPX with async and sync support\n"
        "• Test Suite: Python unittest with 17 automated integration tests (all passing)"
    )
    
    doc.add_paragraph("Commands to Run the Platform:")
    code_p = doc.add_paragraph()
    code_p.paragraph_format.left_indent = Inches(0.5)
    code_run = code_p.add_run(
        "# Start Backend Server (Serves API and bundled React frontend on port 8000):\n"
        "python run_application.py\n\n"
        "# Start Frontend Development Server (with hot module reload on port 3000):\n"
        "npm --prefix frontend run dev\n\n"
        "# Run Automated Test Suite (Verifies all 14 labs):\n"
        "python -m unittest backend/tests/test_all_14_labs.py"
    )
    code_run.font.name = 'Consolas'
    code_run.font.size = Pt(9.5)
    code_run.font.color.rgb = RGBColor(30, 41, 59)
    
    output_path = r"c:\Users\Admin\Downloads\New folder (3)\Project_Information.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
