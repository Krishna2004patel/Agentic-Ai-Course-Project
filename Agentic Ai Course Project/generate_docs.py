import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from doc_helpers import set_cell_background, set_cell_margins, set_table_borders, add_callout

def build_document():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Header for normal pages
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("KLE Technological University | Agentic AI (26ECAC401) | Research Grant Management System")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Autonomous Multi-Agent AI System — Complete Technical & Theoretical Explanation Document")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Styles Setup
    NAVY = RGBColor(15, 23, 42)      # #0F172A
    CRIMSON = RGBColor(220, 38, 38)  # #DC2626
    SLATE = RGBColor(71, 85, 105)    # #475569
    DARK_TEXT = RGBColor(30, 41, 59) # #1E293B
    BLUE_ACCENT = RGBColor(37, 99, 235) # #2563EB

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    cov_p1 = doc.add_paragraph()
    cov_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cov_p1.paragraph_format.space_before = Pt(36)
    cov_p1.paragraph_format.space_after = Pt(4)
    r_inst = cov_p1.add_run("KLE TECHNOLOGICAL UNIVERSITY, HUBBALLI / BELAGAVI\n")
    r_inst.bold = True
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = CRIMSON

    r_dept = cov_p1.add_run("SCHOOL OF COMPUTER SCIENCE & ENGINEERING (ARTIFICIAL INTELLIGENCE)\n")
    r_dept.bold = True
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = NAVY

    r_crs = cov_p1.add_run("Course: Agentic AI (26ECAC401) — Capstone & 14-Lab Implementation\n")
    r_crs.font.name = "Calibri"
    r_crs.font.size = Pt(10)
    r_crs.font.color.rgb = SLATE

    # Decorative Line
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(12)
    p_line.paragraph_format.space_after = Pt(24)
    r_line = p_line.add_run("—" * 45)
    r_line.font.color.rgb = CRIMSON

    # Main Document Title
    cov_p2 = doc.add_paragraph()
    cov_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cov_p2.paragraph_format.space_before = Pt(10)
    cov_p2.paragraph_format.space_after = Pt(8)
    r_title = cov_p2.add_run("RESEARCH GRANT MANAGEMENT SYSTEM\nAGENTIC AI ARCHITECTURE")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = NAVY

    cov_p3 = doc.add_paragraph()
    cov_p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cov_p3.paragraph_format.space_before = Pt(4)
    cov_p3.paragraph_format.space_after = Pt(36)
    r_sub = cov_p3.add_run("Comprehensive Technical Documentation, Multi-Agent Collaboration Mechanics,\n14 Laboratory Implementations, Mathematical Scoring Formulas, and Viva Defense Guide")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = SLATE

    # Metadata Card Table
    meta_tbl = doc.add_table(rows=6, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    
    col_widths = [Inches(2.2), Inches(4.3)]
    meta_data = [
        ("Project Title", "Autonomous Multi-Agent AI System for End-to-End Research Grant Management"),
        ("Architecture Model", "Closed-Loop 6-Specialized Agent Ecosystem with OpenAlex Grounding"),
        ("Lab Curriculum", "Complete Hands-on Realization of All 14 Agentic AI Labs (Labs 1 to 14)"),
        ("Key Innovation", "Topic-Independent Reasoning, Real-Time Citations, Statutory 10% Overhead & 5% Contingency"),
        ("Technology Stack", "Python 3.12, FastAPI, React 18, Vite, SQLite, ThreadPool Swarm, Scikit-Learn TF-IDF"),
        ("Academic Term", "Academic Year 2026 — Final Project & Worklet Evaluation")
    ]
    
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = col_widths[0], col_widths[1]
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=90, bottom=90, left=120, right=120)
        set_cell_margins(c1, top=90, bottom=90, left=120, right=120)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = DARK_TEXT

    set_table_borders(meta_tbl, color="CBD5E1", sz="4")
    
    cov_bot = doc.add_paragraph()
    cov_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cov_bot.paragraph_format.space_before = Pt(40)
    r_bot = cov_bot.add_run("CONFIDENTIAL & PROPRIETARY — PREPARED FOR ACADEMIC EVALUATION & LAB WORKLET VIVA")
    r_bot.font.name = "Calibri"
    r_bot.font.size = Pt(8.5)
    r_bot.font.color.rgb = RGBColor(148, 163, 184)

    doc.add_page_break()

    # -------------------------------------------------------------
    # HELPER FORMATTING FUNCTIONS
    # -------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(17)
        r.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.color.rgb = BLUE_ACCENT
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = NAVY
        return p

    def add_body(text, space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT
        return p

    def add_bullet(text, bold_prefix="", space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)
            rb.font.color.rgb = NAVY
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT
        return p

    # -------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    add_h1("Executive Summary")
    add_body(
        "The Research Grant Management System is an enterprise-grade, autonomous Multi-Agent AI system designed "
        "to assist university faculty, researchers, and academic institutions like KLE Technological University in "
        "navigating the highly complex, tedious, and regulation-dense lifecycle of academic research grants. "
        "Securing extramural research funding from statutory national agencies (such as DST-SERB/ANRF, ICMR, DBT, MeitY, "
        "ISRO, DRDO, CSIR, and AICTE) typically demands hundreds of manual faculty hours spent tracking disparate calls, "
        "reading hundreds of academic papers, manually formatting structured proposals, performing complex multi-year "
        "financial calculations, and auditing compliance against rigid statutory guidelines."
    )
    add_body(
        "Unlike passive software or generic conversational chatbots (e.g. ChatGPT, Claude) that merely generate unverified text, "
        "this system embodies true Agentic AI. It deploys six autonomous, specialized AI agents working within an interconnected, "
        "observable loop. Crucially, the system features a topic-independent reasoning engine (TopicReasoningEngine) that accepts "
        "completely novel, previously unseen research domains, connects in real-time to open academic repositories (OpenAlex and Crossref) "
        "to retrieve authentic peer-reviewed publications with genuine DOIs, strictly enforces mandatory statutory financial rules "
        "(such as the 10% institutional overhead ceiling and 5% contingency cap), and provides dual-key governance locks before submission."
    )
    add_body(
        "Furthermore, this project provides a 100% complete, authentic implementation of all 14 Hands-on Labs specified in the "
        "Agentic AI (26ECAC401) curriculum. Each lab is realized directly within the grant management domain, producing verifiable "
        "execution traces, inspectable artifacts, and empirical evidence accessible via a dual-perspective portal: the Researcher Workspace "
        "for day-to-day proposal engineering and the Teacher Dashboard for comprehensive academic review and marking."
    )
    
    add_callout(
        doc,
        "The Research Grant Management System eliminates the 'hardcoded mock problem' completely. It connects real-time OpenAlex/Crossref "
        "metadata APIs, formulates dynamic SMART aims across any scientific discipline, calculates mathematically exact budgets with 10% overhead "
        "capping, and enforces human-in-the-loop authorization gates.",
        title="CORE ARCHITECTURAL BREAKTHROUGH"
    )

    # -------------------------------------------------------------
    # SECTION 1: SIMPLE LANGUAGE PRIMER
    # -------------------------------------------------------------
    add_h1("1. Explaining the Project in Simple Language")
    add_body(
        "When explaining this project to a college faculty examiner, student peer, or conference audience, it is critical to present "
        "the core concepts clearly, logically, and without unnecessary jargon. This section provides an intuitive, conceptual walkthrough."
    )

    add_h2("1.1 What is a Research Grant Management System?")
    add_body(
        "A Research Grant Management System is an end-to-end intelligent platform that helps university professors and scientists "
        "identify government and industry funding opportunities, analyze existing scientific literature, draft formal research proposals, "
        "calculate itemized financial budgets, verify institutional compliance, and compile submission-ready grant dossiers."
    )

    add_h2("1.2 What Problem Does This Project Solve?")
    add_body(
        "Every year, thousands of brilliant academic research ideas fail to receive funding not because the science is weak, but because of "
        "administrative and procedural friction. The primary bottlenecks include:"
    )
    add_bullet("Faculty must constantly monitor dozens of government portals with varying deadlines, eligibility rules, and funding limits.", bold_prefix="1. Fragmented Funding Discovery: ")
    add_bullet("Finding relevant prior art, extracting empirical claims, and finding genuine, unaddressed research gaps takes weeks of manual reading.", bold_prefix="2. Exhaustive Literature Synthesis: ")
    add_bullet("Government agencies require rigid proposal structures (SMART aims, 4-phase technical work breakdowns, risk registers, and deliverables).", bold_prefix="3. Complex Proposal Structuring: ")
    add_bullet("Government norms dictate strict cost partitions (Equipment, Manpower, Software, Travel, Consumables) and enforce a mandatory 10% ceiling on institutional overhead and a 5% contingency cushion. Minor arithmetic errors cause immediate disqualification.", bold_prefix="4. Strict Statutory Budgeting: ")
    add_bullet("Missing mandatory institutional certificates (Form A Endorsement, Form B PI CV) or applying without proper Dean R&D authorization leads to summary administrative rejection.", bold_prefix="5. Administrative Compliance Failures: ")

    add_h2("1.3 Why is Agentic AI Used Instead of Traditional Software?")
    add_body(
        "Traditional software is deterministic and rigid: it can only follow pre-written 'if-else' scripts and forms. If a researcher enters a brand-new "
        "scientific topic (such as 'Quantum key distribution for underwater satellite links' or 'CRISPR-Cas13 RNA targeting for plant viral resistance'), "
        "traditional software cannot understand the topic, cannot formulate search queries, and cannot synthesize custom methodologies.\n\n"
        "Agentic AI provides autonomous cognitive agency: the ability to perceive an arbitrary goal, reason through steps, select and invoke external tools, "
        "evaluate the outputs of those tools, handle unexpected errors, and mutate plans until the goal is satisfied."
    )

    add_h2("1.4 What is the Difference Between a Normal Chatbot and an AI Agent?")
    add_body(
        "A standard conversational chatbot (like basic ChatGPT) is passive and stateless. It receives a text prompt and generates a single predictive "
        "text completion. It cannot take actions in the real world, cannot invoke calculator tools deterministically, cannot query databases safely, "
        "cannot store persistent structured memories across sessions, and cannot self-correct when its text is invalid.\n\n"
        "An AI Agent, by contrast, is an active closed-loop system characterized by four fundamental pillars:"
    )
    add_bullet("An agent does not just chat; it is assigned a high-level objective (e.g. 'Generate a ₹50 Lakh guideline-compliant grant dossier for KLE Tech'). It determines the sub-tasks needed to achieve that goal.", bold_prefix="• Goal-Driven Execution: ")
    add_bullet("An agent is equipped with external tools (calculator, PDF parser, live OpenAlex REST API, database queries). It decides when to invoke each tool and passes structured arguments.", bold_prefix="• Tool Integration: ")
    add_bullet("An agent maintains persistent memory across turns and projects, distinguishing between short-term session state and verified long-term facts.", bold_prefix="• Scoped Memory: ")
    add_bullet("An agent observes the result of its actions. If an API times out or a budget calculation violates a 10% ceiling, it detects the error and executes a replanning loop to correct itself autonomously.", bold_prefix="• Observe & Revise Loop: ")

    add_h2("1.5 High-Level Architectural Flow: How the Complete System Operates")
    add_body(
        "The system functions as a synchronized, autonomous digital research team. When a researcher inputs a research idea, the workflow "
        "unfolds systematically:"
    )
    add_bullet("Extracts scientific concepts, determines the primary academic discipline, and infers interdisciplinary intersections without static keyword rules.", bold_prefix="Step 1 (Intake & Reasoning): ")
    add_bullet("Evaluates verified national schemes (DST, ICMR, MeitY, ISRO, DRDO) and ranks them using semantic overlap and budget compatibility.", bold_prefix="Step 2 (Funding Discovery): ")
    add_bullet("Queries live academic APIs (OpenAlex/Crossref), retrieves genuine publications with DOIs, indexes uploaded documents via TF-IDF, and extracts 3 verifiable research gaps.", bold_prefix="Step 3 (Literature Review): ")
    add_bullet("Synthesizes a complete technical proposal featuring problem statements, SMART aims, a 4-phase technical methodology, and milestone deliverables.", bold_prefix="Step 4 (Proposal Drafting): ")
    add_bullet("Partitions funds into Equipment, Manpower, Software, Travel, and Consumables based on project resource intensity, enforcing 5% contingency and 10% statutory overhead caps.", bold_prefix="Step 5 (Budget Planning): ")
    add_bullet("Verifies host institution accreditation, checks budget caps, audits mandatory documentation (Form A Endorsement, Form B CV), and emits a compliance scorecard.", bold_prefix="Step 6 (Compliance Audit): ")
    add_bullet("Aggregates all artifacts, verifies checksum integrity, compiles submission dossiers (JSON & Markdown), and enforces a mandatory Dean R&D human sign-off lock.", bold_prefix="Step 7 (Packaging & Governance): ")

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 2: THE SIX SPECIALIZED AI AGENTS
    # -------------------------------------------------------------
    add_h1("2. Deep Dive: The Six Specialized AI Agents")
    add_body(
        "The application divides the complex grant development lifecycle into six decoupled, autonomous specialized agents. "
        "Each agent operates with its own specific role, input schema, toolset, internal reasoning logic, and structured output contract."
    )

    agents_info = [
        {
            "code": "Agent A",
            "name": "Funding Discovery Agent",
            "file": "backend/app/agents/funding_discovery.py & tools/funding_api.py",
            "role": "Grant Matchmaker & Opportunity Discovery Specialist",
            "responsibility": "Understands research domains and objectives, discovers active extramural grant schemes, audits eligibility criteria, checks budget ceilings, and ranks opportunities dynamically.",
            "inputs": "Project title, research domain, requested budget, host institution credentials, project objectives.",
            "tools": "FundingAPIConnectorTool, TopicReasoningEngine (Keyword Extractor), National Catalog Reader.",
            "logic": "Extracts up to 10 semantic keywords. Evaluates each scheme in the catalog by calculating semantic keyword overlap ratio (Or). Computes base relevance score: Base = 0.45 + (Or * 0.50). Evaluates budget viability: if requested budget <= max scheme cap, adds +0.04 bonus; if it exceeds cap, applies a -0.15 penalty. Clamps final score between 0.20 and 0.99 and sorts descending.",
            "outputs": "List of ranked funding opportunities (title, agency, deadline, max amount, eligibility, relevance score percentage, and custom rationale citing matched keywords)."
        },
        {
            "code": "Agent B",
            "name": "Literature Review Agent",
            "file": "backend/app/agents/literature_review.py & tools/scholarly_api.py",
            "role": "Prior Art & Gap Extraction Specialist",
            "responsibility": "Searches real-world academic literature, indexes uploaded proposal documents into a TF-IDF vector store, synthesizes comparative prior-art matrices, and extracts verifiable research gaps.",
            "inputs": "Project title, domain, uploaded PDF/DOCX files, project memory context.",
            "tools": "ScholarlyResearchTool (live OpenAlex & Crossref REST APIs), DocumentReaderTool (PDF/DOCX text parser), ResearchRAGStore (Scikit-Learn TF-IDF vector retriever).",
            "logic": "Formulates multi-term academic search queries dynamically. Queries https://api.openalex.org/works without API keys. Extracts authentic paper titles, real authors, publication years, citation counts, and verifiable DOI links. Ingests local uploaded documents, chunks them into 300-word passages, computes TF-IDF embeddings, and performs cosine similarity retrieval. Synthesizes 3 concrete research gaps citing real paper limitations.",
            "outputs": "Complete literature review payload containing real scholarly citations with DOIs, comparative prior-art matrix, empirical claims, documented limitations, and 3 verified research gaps."
        },
        {
            "code": "Agent C",
            "name": "Proposal Drafting Agent",
            "file": "backend/app/agents/proposal_drafting.py & skills/proposal_writing.py",
            "role": "Grant Proposal Synthesizer & Technical Architect",
            "responsibility": "Synthesizes an academic research proposal structured in full alignment with national funding agency templates, incorporating literature review findings and SMART research aims.",
            "inputs": "Project metadata, extracted research gaps from Agent B, matched funding scheme guidelines from Agent A, optional user feedback.",
            "tools": "ProposalWritingSkill, TopicReasoningEngine (synthesize_proposal_architecture).",
            "logic": "Transforms unstructured project objectives into SMART specific aims (Specific, Measurable, Achievable, Relevant, Time-bound). Generates an Executive Summary, Problem Definition citing state-of-the-art limitations, a 4-Phase Technical Methodology (Theoretical Formulation, Benchtop Implementation, Empirical Validation, Laboratory Deployment), a timeline-bound milestone plan, and measurable deliverables.",
            "outputs": "Structured ProposalDraft entity stored in SQLite (versioned) containing title, abstract, problem statement, objectives, methodology, work plan, and expected deliverables."
        },
        {
            "code": "Agent D",
            "name": "Budget Planning Agent",
            "file": "backend/app/agents/budget_planning.py & skills/budget_analysis.py",
            "role": "Financial Planner & Statutory Cost Auditor",
            "responsibility": "Formulates an itemized research budget, partitions expenses based on project technical requirements, and strictly enforces statutory contingency and institutional overhead caps.",
            "inputs": "Requested total budget, project title, domain, host institution name, duration weeks.",
            "tools": "FundingCalculatorTool, BudgetAnalysisSkill, TopicReasoningEngine (analyze_resource_intensity).",
            "logic": "Analyzes project methodology to infer resource intensity (e.g. wet-lab consumables vs. GPU hardware vs. fieldwork). Dynamically allocates direct costs into Equipment (~35%), Manpower (~30%), Software/Licenses (~10%), Consumables (~10%), and Travel (~5%). Strictly applies statutory caps: Contingency = 5% of direct cost, Institutional Overhead = exactly 10% of direct cost. Formulates detailed line-item justifications.",
            "outputs": "Itemized BudgetPlan entity stored in SQLite with direct costs, contingency, institutional overhead, percentage breakdown, line-item justifications, and statutory compliance flag."
        },
        {
            "code": "Agent E",
            "name": "Compliance Checking Agent",
            "file": "backend/app/agents/compliance_checking.py & skills/compliance_checking.py",
            "role": "Regulatory Auditor & Institutional Gatekeeper",
            "responsibility": "Audits proposal completeness, checks PI eligibility and institution credentials, verifies budget caps, and detects missing mandatory documentation before portal dispatch.",
            "inputs": "Host institution name, PI email and credentials, requested budget, project duration, uploaded documents list.",
            "tools": "ComplianceCheckingSkill.",
            "logic": "Executes 5 verification checks: (1) Host institution UGC/AICTE recognition, (2) PI academic credentials, (3) Budget ceiling compliance (<₹50 Lakh standard limit), (4) Duration alignment, (5) Document attachments audit. Checks for Form A (Institutional Endorsement Certificate from Registrar/Dean R&D) and Form B (Detailed PI CV). Computes weighted compliance score (0 to 100). Sets status: COMPLIANT (>=90), WARNINGS (65-89), or NON_COMPLIANT (<65).",
            "outputs": "ComplianceReport entity stored in SQLite featuring compliance status, score, passed checks, missing items list, actionable warnings, and recommendations."
        },
        {
            "code": "Agent F",
            "name": "Submission Agent",
            "file": "backend/app/agents/submission_agent.py",
            "role": "Dossier Packager & Governance Gatekeeper",
            "responsibility": "Aggregates artifacts from Agents A through E, validates cryptographic checksum integrity, prepares downloadable grant packages, and enforces a mandatory human approval governance gate.",
            "inputs": "Project ID, latest ProposalDraft, latest BudgetPlan, latest ComplianceReport, Dean R&D authorization credentials.",
            "tools": "DossierPackager, Cryptographic Checksum Engine, ApprovalRecord State Machine.",
            "logic": "Verifies prerequisite outputs exist. If compliance status is WARNINGS or COMPLIANT, compiles complete submission dossier. Generates two downloadable files on disk: 'submission_dossier.json' and 'grant_proposal_document.md'. Initializes an ApprovalRecord in SQLite with status 'WAITING_APPROVAL'. Physical external dispatch is strictly locked until an authorized human user signs off with approval comments.",
            "outputs": "Compiled grant dossier package, downloadable JSON and Markdown proposal files, approval request ID, and dual-key governance lock status."
        }
    ]

    for ag in agents_info:
        add_h2(f"{ag['code']}: {ag['name']}")
        add_bullet(ag['file'], bold_prefix="Implementation Location: ")
        add_bullet(ag['role'], bold_prefix="Role: ")
        add_bullet(ag['responsibility'], bold_prefix="Core Responsibility: ")
        add_bullet(ag['inputs'], bold_prefix="Inputs Consumed: ")
        add_bullet(ag['tools'], bold_prefix="Tools & Engines Invoked: ")
        add_bullet(ag['logic'], bold_prefix="Internal Reasoning Logic: ")
        add_bullet(ag['outputs'], bold_prefix="Structured Outputs Produced: ")
        add_body("")

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 3: THE FOUR MAIN EXPECTED OUTPUTS
    # -------------------------------------------------------------
    add_h1("3. The Four Main Expected Deliverables")
    add_body(
        "Regardless of whether the researcher runs the complete multi-agent lifecycle or executes individual labs, "
        "the application guarantees the generation of four central deliverables for the active project. "
        "These four outputs appear in the Researcher Workspace, Teacher Dashboard, and exportable reports."
    )

    outputs_data = [
        ("Output 1", "Ranked Funding Opportunities", "Funding Discovery Agent (Agent A)", "Identifies active national/international funding calls, computes semantic keyword overlap, validates budget ceilings, and ranks opportunities with transparent match percentages (e.g. 78%, 74%, 59%) and custom rationales citing project concepts."),
        ("Output 2", "Structured Proposal Draft", "Proposal Drafting Agent (Agent C) + Literature Review Agent (Agent B)", "A complete, guideline-compliant research proposal containing an Executive Summary, State-of-the-Art Limitations, SMART Research Aims, 4-Phase Technical Methodology, Timeline Milestones, and Measurable Deliverables, fully grounded in real literature."),
        ("Output 3", "Itemized Budget Plan", "Budget Planning Agent (Agent D)", "A mathematically exact financial breakdown allocating funds across Equipment (35%), Manpower (30%), Software/Compute (10%), Consumables (10%), and Travel (5%), with statutory 5% contingency and 10% institutional overhead strictly capped."),
        ("Output 4", "Institutional Compliance Report", "Compliance Checking Agent (Agent E)", "A regulatory audit scorecard verifying UGC/AICTE institutional accreditation, PI credentials, budget ceiling adherence, and flagging missing mandatory documentation (Form A Endorsement, Form B CV) with an overall score (e.g. 80.0% - WARNINGS).")
    ]

    out_tbl = doc.add_table(rows=len(outputs_data) + 1, cols=4)
    out_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    out_tbl.autofit = False
    
    col_w = [Inches(1.0), Inches(1.8), Inches(1.7), Inches(2.0)]
    headers = ["Output", "Deliverable Name", "Responsible Agent(s)", "Core Deliverable Description"]
    
    # Header row
    for c_idx, h_text in enumerate(headers):
        cell = out_tbl.cell(0, c_idx)
        cell.width = col_w[c_idx]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, (o_code, o_name, o_agent, o_desc) in enumerate(outputs_data):
        row = out_tbl.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate([o_code, o_name, o_agent, o_desc]):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = CRIMSON
            else:
                r.font.color.rgb = DARK_TEXT

    set_table_borders(out_tbl, color="CBD5E1", sz="4")
    add_body("", space_after=10)

    # -------------------------------------------------------------
    # SECTION 4: THE PERCENTAGE SCORE DECODED (CRITICAL)
    # -------------------------------------------------------------
    add_h1("4. Special Focus: The Percentage Score Decoded")
    add_body(
        "In the Researcher Dashboard and Teacher Overview, funding opportunities display matching scores presented as percentages, "
        "such as 49.0%, 54.0%, 74.0%, 78.0%, or 85.0%. Faculty examiners frequently ask: "
        "'Where does this number come from? Is it an arbitrary LLM hallucination, a statistical confidence interval, or a mathematical formula?'"
    )
    add_body(
        "In our implementation, this percentage is 100% deterministic, mathematically auditable, and computed by "
        "FundingAPIConnectorTool.search_opportunities() in backend/app/tools/funding_api.py. It combines semantic keyword overlap "
        "with statutory budget constraint verification."
    )

    add_h2("4.1 The Exact Mathematical Formula")
    add_body(
        "Let a project have a combined text corpus T = {Title, Domain, Objectives}. "
        "The TopicReasoningEngine extracts a set of N_kw primary keywords (up to 10 keywords):"
    )
    add_bullet("K_project = {k_1, k_2, ..., k_m}, where m <= 10.", bold_prefix="1. Project Keyword Extraction: ")
    add_bullet("K_scheme = text corpus of the funding call (Scheme Name, Agency, Description, Domains, Catalog Keywords).", bold_prefix="2. Funding Scheme Target Corpus: ")
    add_bullet("K_matched = {k in K_project | k in K_scheme}", bold_prefix="3. Keyword Overlap Count: ")
    add_bullet("Overlap Ratio (Or) = |K_matched| / max(1, |K_project|), where 0.0 <= Or <= 1.0", bold_prefix="4. Semantic Overlap Ratio: ")
    
    add_body(
        "The base relevance score is formulated as a linear interpolation starting at a baseline eligibility of 0.45:\n\n"
        "    Base Score = 0.45 + (Overlap Ratio * 0.50)\n\n"
        "Next, the engine performs a budget viability audit comparing requested budget (B_req) with scheme ceiling (B_max):"
    )
    add_bullet("If B_req <= B_max: Base Score is rewarded by +0.04 (+4% budget compliance bonus).", bold_prefix="• Budget Within Ceiling: ")
    add_bullet("If B_req > B_max: Base Score is penalized by -0.15 (-15% budget violation penalty).", bold_prefix="• Budget Exceeds Ceiling: ")
    add_body(
        "Finally, the score is clamped into the valid range [0.20, 0.99] and rounded to two decimal places:\n\n"
        "    Final Relevance Score = round( min(0.99, max(0.20, Base Score + Budget Adjustment)), 2 )\n"
        "    Displayed Percentage = Final Relevance Score * 100%"
    )

    add_h2("4.2 Step-by-Step Numerical Walkthroughs")
    
    add_h3("Scenario A: The 49.0% Match (Baseline Eligibility)")
    add_body(
        "Consider a researcher submitting a project titled 'Solar Energy Grid Optimization' with a budget of ₹10,00,000, "
        "evaluated against an unrelated biological grant call (e.g. 'Biotechnology Research & Innovation Council (BRIC) Grant').\n"
        "• Extracted Project Keywords: ['solar', 'energy', 'grid', 'optimization', 'power', 'inverters'] (6 keywords)\n"
        "• Matched in BRIC Scheme: None matched (0 keywords in BRIC description).\n"
        "• Overlap Ratio (Or) = 0 / 6 = 0.0\n"
        "• Base Score = 0.45 + (0.0 * 0.50) = 0.45\n"
        "• Budget Check: ₹10,00,000 <= ₹75,00,000 scheme ceiling -> Status: Compliant (+0.04 bonus).\n"
        "• Final Score = 0.45 + 0.04 = 0.49 -> Displayed as 49.0%.\n\n"
        "Meaning in Simple English: 49.0% means the project is administratively eligible because the budget is within limits and "
        "the host institution is recognized, but there is zero semantic domain overlap. It tells the researcher: "
        "'You are allowed to apply, but your topic does not fit this call at all.'"
    )

    add_h3("Scenario B: The 74.0% Match (Strong Domain Relevance)")
    add_body(
        "Consider a biomedical research project ('AI-based early disease detection', ₹25,00,000 budget) "
        "evaluated against the 'ICMR Extramural Biomedical Health Research Grant' (₹50,00,000 max).\n"
        "• Extracted Project Keywords: ['disease', 'detection', 'biomedical', 'clinical', 'diagnosis', 'health', 'patients', 'ai'] (8 keywords)\n"
        "• Matched Keywords in ICMR Scheme: ['disease', 'biomedical', 'health', 'clinical'] (4 keywords matched).\n"
        "• Overlap Ratio (Or) = 4 / 8 = 0.50 (50% keyword overlap).\n"
        "• Base Score = 0.45 + (0.50 * 0.50) = 0.45 + 0.25 = 0.70\n"
        "• Budget Check: ₹25,00,000 <= ₹50,00,000 scheme ceiling -> Status: Compliant (+0.04 bonus).\n"
        "• Final Score = 0.70 + 0.04 = 0.74 -> Displayed as 74.0%.\n\n"
        "Meaning in Simple English: 74.0% represents a high-probability grant match. Half of the project's core concepts match the "
        "funding agency's thrust areas, and the budget fits well under the scheme cap."
    )

    add_h3("Scenario C: The 84.0% - 94.0% Match (Exceptional Alignment)")
    add_body(
        "When an AI project matches 7 out of 9 keywords (Or = 0.77) with MeitY TIDE 2.0 and requests ₹35 Lakhs (cap is ₹40 Lakhs):\n"
        "• Base Score = 0.45 + (0.77 * 0.50) = 0.45 + 0.385 = 0.835\n"
        "• Budget Bonus = +0.04\n"
        "• Final Score = 0.835 + 0.04 = 0.875 -> Displayed as 88.0%.\n"
        "This indicates prime strategic alignment with the funding agency's published mandate."
    )

    add_h3("Scenario D: The 34.0% Penalized Match (Budget Violation)")
    add_body(
        "If the researcher requests ₹70,00,000 for a scheme with a strict ₹30,00,000 ceiling, even with zero keyword overlap:\n"
        "• Base Score = 0.45\n"
        "• Budget Penalty = -0.15\n"
        "• Final Score = 0.45 - 0.15 = 0.30 (or 0.34 with partial keyword match).\n"
        "The system visually flags this with a red warning badge indicating the budget exceeds scheme caps."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 5: ALL 14 LABORATORIES
    # -------------------------------------------------------------
    add_h1("5. Comprehensive Deep Dive: All 14 Laboratories")
    add_body(
        "Every single lab from the Agentic AI (26ECAC401) curriculum is fully realized within the Research Grant Management System. "
        "The implementations do not run generic toy scripts; each lab concept is engineered specifically for grant management tasks."
    )

    labs_full = [
        {
            "num": 1,
            "title": "Lab 1 – Goal-Driven Planning & Dynamic Replanning Loop",
            "curriculum": "Agent vs Chatbot: Plan–Act–Observe–Revise cycle with delta plan mutation.",
            "simple_meaning": "A chatbot just answers a question once; an agent creates a multi-step roadmap, checks if goals are achieved, listens to user feedback, and mutates its plan without starting over.",
            "importance": "Without replanning, an AI system is brittle. If a funding agency rejects a clinical timeline, a simple chatbot forgets everything, whereas a goal-driven agent updates only the affected milestones.",
            "implementation": "Engineered in backend/app/agents/lab1_planning.py as ResearchPlanningAgent. Evaluates stopping predicates (topic_clarified, budget_estimated, timeline_defined, references_available). Generates 4-phase milestone roadmaps and executes revise_plan(feedback) to apply delta adjustments.",
            "agents": "Funding Discovery Agent (intake), Proposal Drafting Agent (milestone planning).",
            "execution": "Executed via POST /api/v1/labs/1/execute/{project_id}. Accepts optional feedback string in query parameters.",
            "evidence": "Output contains goal_predicates boolean map, initial_plan with 4 milestones, and revised_plan showing last_mutated timestamp and mutated_milestones array.",
            "contribution": "Establishes the foundational goal-directed planning backbone for all subsequent grant drafting phases."
        },
        {
            "num": 2,
            "title": "Lab 2 – Tool-Integrated Execution & Math Calculations",
            "curriculum": "Tool integration, structured schemas, function calling, and deterministic math.",
            "simple_meaning": "LLMs cannot do reliable arithmetic or read raw PDF files directly. We connect deterministic software tools (calculators, file readers, APIs) that the agent calls whenever precision is required.",
            "importance": "Grant applications with arithmetic errors in overhead or salary breakdowns are immediately disqualified. Deterministic tools guarantee 100% mathematical precision.",
            "implementation": "Engineered in backend/app/agents/lab2_tools.py as ToolUsingGrantAgent. Integrates FundingCalculatorTool, DocumentReaderTool, and FundingAPIConnectorTool with strict input/output Pydantic schemas.",
            "agents": "Budget Planning Agent, Literature Review Agent, Funding Discovery Agent.",
            "execution": "Executed via POST /api/v1/labs/2/execute/{project_id}.",
            "evidence": "JSON response verifies tool_invocations array (tool_name, inputs, status) and tool_results with exact calculations: direct cost ₹8,69,565.22, 5% contingency ₹43,478.26, and 10% statutory overhead ₹86,956.52.",
            "contribution": "Powers all deterministic financial allocations and uploaded PDF/DOCX document text extraction."
        },
        {
            "num": 3,
            "title": "Lab 3 – Reusable Skills Creation & Verification",
            "curriculum": "Reusable skills packaging instructions, workflows, constraints, and schemas tested across multiple domains.",
            "simple_meaning": "Instead of hardcoding code for every new research topic, we build modular 'Skill Packages' that can be picked up and executed for any scientific domain without modifying code.",
            "importance": "Enables modular software design. A budget skill or compliance skill can be reused across biotechnology, civil engineering, and aerospace proposals identically.",
            "implementation": "Engineered in backend/app/agents/lab3_skills.py and backend/app/skills/. Implements ResearchSummarizationSkill, ProposalWritingSkill, BudgetAnalysisSkill, and ComplianceCheckingSkill. Executes automated cross-domain reusability verification against an alternate project.",
            "agents": "All 6 Specialized AI Agents.",
            "execution": "Executed via POST /api/v1/labs/3/execute/{project_id}.",
            "evidence": "Emits skills_executed list and reusability_test object verifying execution across Primary Project and Alternate Project (Clean Energy Grid Optimization) with skill_reusability_verified: true.",
            "contribution": "Decouples cognitive agent workflows from domain-specific data, making the system genuinely topic-independent."
        },
        {
            "num": 4,
            "title": "Lab 4 – Scoped Memory Lifecycle & Isolation",
            "curriculum": "Short-term session state vs. long-term tagged memory, conflict detection, and isolation boundaries.",
            "simple_meaning": "The system remembers what is currently happening on screen (short-term memory) and stores permanent verified facts in the database (long-term memory), while preventing facts from different projects from mixing up.",
            "importance": "Prevents data contamination between professors and projects, and alerts users if two conflicting budget numbers are entered.",
            "implementation": "Engineered in backend/app/agents/lab4_memory.py and backend/app/core/memory_manager.py. Manages transient in-memory dictionaries alongside persistent SQLite ProjectMemory rows tagged with categories (#budget, #equipment). Includes automated conflict detection when keys are overwritten.",
            "agents": "Submission Agent, Proposal Drafting Agent, Budget Planning Agent.",
            "execution": "Executed via POST /api/v1/labs/4/execute/{project_id}.",
            "evidence": "Output proves short_term_session_state, long_term_facts_stored, and conflict_test capturing budget overwrite attempt (₹10L vs ₹12.5L) flagged for human confirmation.",
            "contribution": "Guarantees project data isolation and maintains an auditable knowledge graph of project decisions."
        },
        {
            "num": 5,
            "title": "Lab 5 – MCP Tool Connector & Security Boundaries",
            "curriculum": "Model Context Protocol (MCP) server integration, exposing resources, tools with permission boundaries, and API gateways.",
            "simple_meaning": "A standardized protocol that allows AI agents to securely connect to databases and files. It acts like a secure firewall, allowing read operations but blocking destructive commands like deleting tables.",
            "importance": "Protects university databases. If an AI generates an unsafe query (like 'DROP TABLE'), the MCP security boundary intercepts and blocks it before execution.",
            "implementation": "Engineered in backend/app/agents/lab5_mcp.py and backend/app/mcp/grant_server.py. Implements FastMCP-compatible server exposing URIs (grant://project/{id}/metadata) and read-only SQL querying tools with regex injection filters.",
            "agents": "Funding Discovery Agent, Literature Review Agent.",
            "execution": "Executed via POST /api/v1/labs/5/execute/{project_id}.",
            "evidence": "Output shows manifest_summary (resources, tools), successful read of grant://project/{id}/metadata, and security_boundary_test proving destructive query ('DROP TABLE research_projects;') is blocked with security alert.",
            "contribution": "Provides a standardized, enterprise-safe interface for database interactions and external portal connectivity."
        },
        {
            "num": 6,
            "title": "Lab 6 – Agent Runtime Engine & Stopping Conditions",
            "curriculum": "OpenCLA/OpenClaw-style runtime: task interface, runtime loop, skill registry, tool registry, and audit trail.",
            "simple_meaning": "The operating system for AI agents. It loads tasks, executes skills from a registry, logs every action, and ensures agents stop cleanly when conditions are met instead of running in infinite loops.",
            "importance": "Without a deterministic runtime engine, agents can loop indefinitely, consuming excessive compute or creating endless revisions.",
            "implementation": "Engineered in backend/app/agents/lab6_runtime.py and backend/app/core/agent_runtime.py. Features AgentRuntimeEngine with TaskInterface, formal execution cycles, dynamic hot-plugging of skills (demonstrated via dynamic_risk_assessment), and audit trail logging.",
            "agents": "Centralized Orchestrator and all 6 Specialized Agents.",
            "execution": "Executed via POST /api/v1/labs/6/execute/{project_id}.",
            "evidence": "Output verifies runtime_name ('OpenCLA-GrantEngine-v2'), registered skill invocation, audit trail entries, and stopping_condition_met: true.",
            "contribution": "Serves as the deterministic execution kernel that drives all agent interactions throughout the application."
        },
        {
            "num": 7,
            "title": "Lab 7 – Stateful Node Graph Workflow Orchestration",
            "curriculum": "LangGraph-style graph orchestration: DAG with node owners, inputs, outputs, success predicates, and retry logic.",
            "simple_meaning": "Instead of a simple straight-line pipeline, the workflow is mapped as an interactive flowchart (graph) where each node is owned by an agent. If a node fails, it can loop back or branch to a retry node.",
            "importance": "Complex research grants require conditional branching. For example, if compliance fails, the graph routes back to budget re-planning rather than terminating.",
            "implementation": "Engineered in backend/app/agents/lab7_node_graph.py and backend/app/node_graph/engine.py. Builds a 9-node DAG (Intake, Funding, Prior Art, Gaps, Proposal, Budget, Compliance, Human Gate, Dispatch) with node success predicates.",
            "agents": "All 6 Specialized AI Agents mapped to distinct graph nodes.",
            "execution": "Executed via POST /api/v1/labs/7/execute/{project_id}.",
            "evidence": "JSON trace displays total_nodes (9), full execution_sequence, node-level status reports, and all_passed: true flag.",
            "contribution": "Visualizes and enforces the macro-level state transitions of the entire grant preparation lifecycle."
        },
        {
            "num": 8,
            "title": "Lab 8 – Parallel Multi-Agent Swarm with Reconciliation",
            "curriculum": "Parallel execution, concurrent swarms, thread safety, and fault-tolerant state merge.",
            "simple_meaning": "Instead of waiting for one agent to finish before starting the next, four agents run at the exact same millisecond on parallel threads. A reconciliation algorithm merges their results and resolves conflicts.",
            "importance": "Reduces processing time from minutes to milliseconds, and prevents contradictory agent recommendations from corrupting the proposal.",
            "implementation": "Engineered in backend/app/agents/lab8_swarm.py and backend/app/swarm/parallel_swarm.py. Dispatches 4 parallel threads via concurrent.futures.ThreadPoolExecutor (Market Intelligence, Literature Specialist, Cost Estimator, Policy Auditor). Implements multi-agent conflict resolution algorithm.",
            "agents": "Workers 1 to 4 acting across funding, literature, budgeting, and compliance.",
            "execution": "Executed via POST /api/v1/labs/8/execute/{project_id}.",
            "evidence": "Output displays parallel start/end timestamps proving 12ms concurrent execution, lists 4 completed threads, and details 2 resolved conflicts (budget allocation reconciled to statutory caps).",
            "contribution": "Enables ultra-fast parallel grant synthesis and guarantees conflict-free data reconciliation."
        },
        {
            "num": 9,
            "title": "Lab 9 – Deep Research RAG & Literature Vector Store",
            "curriculum": "Deep research agent with external evidence synthesis, RAG retrieval, and cited evidence tables.",
            "simple_meaning": "The agent connects to live academic search engines, downloads real scientific papers with genuine DOIs, splits uploaded documents into text chunks, and searches for specific answers without making up facts.",
            "importance": "Completely eliminates LLM hallucination in the literature review. Every cited paper exists in the real world with a verifiable DOI.",
            "implementation": "Engineered in backend/app/agents/lab9_rag.py and backend/app/tools/scholarly_api.py. Queries live OpenAlex REST API (https://api.openalex.org) and Crossref. Ingests local files into Scikit-Learn TF-IDF vector space with cosine similarity retrieval. Synthesizes 3 verified research gaps.",
            "agents": "Literature Review Agent (Agent B).",
            "execution": "Executed via POST /api/v1/labs/9/execute/{project_id}.",
            "evidence": "Output contains live search query, retrieved papers with actual author names and DOIs, TF-IDF chunks indexed, and 3 explicit research gaps.",
            "contribution": "Provides the empirical, cited academic foundation for the entire research proposal draft."
        },
        {
            "num": 10,
            "title": "Lab 10 – Operations Monitoring, Drift & Self-Healing",
            "curriculum": "Cloud operations telemetry, SLA drift detection, and automated self-healing runbooks.",
            "simple_meaning": "A 24/7 background monitor that measures CPU, RAM, and API speeds. If an external API becomes too slow or memory leaks occur, it automatically runs repair scripts to heal the system.",
            "importance": "Ensures high availability. If the live OpenAlex API is slow or unavailable, the self-healing monitor automatically switches to local semantic caches without crashing the user interface.",
            "implementation": "Engineered in backend/app/agents/lab10_ops.py. Utilizes psutil and internal telemetry trackers to monitor latency percentiles, error rates, and connection pool health. Triggers automated self-healing runbooks when thresholds are breached.",
            "agents": "Operations Monitoring Agent.",
            "execution": "Executed via POST /api/v1/labs/10/execute/{project_id}.",
            "evidence": "Output shows system_health ('DEGRADED_RECOVERING' -> 'HEALTHY'), telemetry metrics (CPU, RAM, API latency), detected SLA drift (>1500ms), and automated self-healing action ('ACTIVATE_LOCAL_SEMANTIC_CACHE').",
            "contribution": "Maintains operational resilience, telemetry observability, and automated recovery across the entire backend."
        },
        {
            "num": 11,
            "title": "Lab 11 – End-to-End Pipeline Automation & SDLC",
            "curriculum": "Agentic SDLC factory: autonomous transformation from requirements to verified code across structured stages.",
            "simple_meaning": "AI agents act like a software development team: Agent 1 writes requirements, Agent 2 designs architecture, Agent 3 writes Python code, Agent 4 runs unit tests, and Agent 5 signs off for release.",
            "importance": "Demonstrates self-extending AI capabilities. The system can generate its own new software modules to support emerging grant rules without human developer intervention.",
            "implementation": "Engineered in backend/app/agents/lab11_pipeline.py as PipelineEvaluationAgent. Executes 5 sequential stages (Requirements -> Design -> Implementation -> Acceptance Testing -> Release Gate) to construct a statutory calculator class.",
            "agents": "Coordinated SDLC Agent Team.",
            "execution": "Executed via POST /api/v1/labs/11/execute/{project_id}.",
            "evidence": "JSON trace confirms all 5 stages passed: Requirement specs approved, Python class code synthesized, 5 unit tests executed with 0 failures, and Release Review signed off.",
            "contribution": "Validates the agentic software development lifecycle capability for rapid extension of grant compliance features."
        },
        {
            "num": 12,
            "title": "Lab 12 – Safety Governance, Gates & Human Approval",
            "curriculum": "Safety guardrails, human-in-the-loop approval gates, audit logging, and rollback mechanisms.",
            "simple_meaning": "AI should never submit a grant to a government portal on its own. We place a strict security lock that requires the university Dean or PI to physically click 'Approve' with authorized credentials.",
            "importance": "Enforces responsible AI. Prevents accidental submission of draft budgets or unverified claims to official portals.",
            "implementation": "Engineered in backend/app/agents/lab12_governance.py and backend/app/agents/submission_agent.py. Audits proposal risk scorecard, physically locks the external dispatch API, exposes a human decision endpoint, and implements state rollback if rejected.",
            "agents": "Compliance Checking Agent, Submission Agent.",
            "execution": "Executed via POST /api/v1/labs/12/execute/{project_id}.",
            "evidence": "Output proves submission_gate_status: 'LOCKED (Human Approval Mandatory)', risk_scorecard ratings, and human_gate status awaiting Dean R&D sign-off.",
            "contribution": "Provides the institutional governance, ethical guardrails, and compliance boundary for the entire project."
        },
        {
            "num": 13,
            "title": "Lab 13 – Discipline-Specific Engineering Agents",
            "curriculum": "Multi-agent systems tailored to core engineering domains (Mechanical, Civil, Electrical).",
            "simple_meaning": "Civil engineering proposals need strain gauges and concrete codes; mechanical proposals need accelerometers and vibration standards. The agent adapts its technical language and budget for each engineering department.",
            "importance": "Prevents generic, useless proposals. Ensures proposals conform to actual technical codes (e.g. ISO 10816, IS 456, IEEE 1547).",
            "implementation": "Engineered in backend/app/agents/lab13_discipline.py. Implements specialized coordinators that synthesize technical methodologies, specialized hardware, and regulatory standards for Mechanical, Civil, and Electrical engineering.",
            "agents": "Discipline-Specific Engineering Coordinator.",
            "execution": "Executed via POST /api/v1/labs/13/execute/{project_id}.",
            "evidence": "Output generates 3 separate technical proposal architectures: Mechanical (turbomachinery maintenance, ISO 10816), Civil (fiber-optic bridge health, IS 456), and Electrical (microgrid stability, IEEE 1547).",
            "contribution": "Extends the grant management platform across diverse university engineering departments."
        },
        {
            "num": 14,
            "title": "Lab 14 – Capstone System Integration & Submission Dossier",
            "curriculum": "Complete end-to-end integration combining multi-agent loops, tools, skills, memory, swarm, graph, and safety.",
            "simple_meaning": "The grand finale: all 13 lab concepts and all 6 specialized agents execute together in harmony to produce the final, complete, submission-ready grant dossier and downloadable proposal files.",
            "importance": "Proves that all individual laboratory components function together as a unified, enterprise-grade production software system.",
            "implementation": "Engineered in backend/app/agents/lab14_capstone.py and backend/app/capstone/integrated_system.py. Executes full 6-agent lifecycle, verifies 4 core deliverables, executes 5-point regression test suite, and compiles downloadable markdown and JSON dossier files on disk.",
            "agents": "All 6 Specialized AI Agents, Swarm Engine, Node Graph Engine, Safety Gate.",
            "execution": "Executed via POST /api/v1/labs/14/execute/{project_id}.",
            "evidence": "Output confirms multi_agent_orchestration status SUCCESS, four_expected_outputs_verified, regression_tests_passed: '5/5 Checks Passed', and paths to generated submission_dossier.json and grant_proposal_document.md.",
            "contribution": "Culmination of the entire semester worklet, proving production readiness and complete curriculum alignment."
        }
    ]

    for lab in labs_full:
        add_h2(f"Lab {lab['num']} — {lab['title']}")
        add_bullet(lab['curriculum'], bold_prefix="Curriculum Concept: ")
        add_bullet(lab['simple_meaning'], bold_prefix="Simple Meaning: ")
        add_bullet(lab['importance'], bold_prefix="Why It Matters in Agentic AI: ")
        add_bullet(lab['implementation'], bold_prefix="Implementation in This Project: ")
        add_bullet(lab['agents'], bold_prefix="Participating Agents: ")
        add_bullet(lab['execution'], bold_prefix="How to Execute & Inspect: ")
        add_bullet(lab['evidence'], bold_prefix="Verifiable Output & Evidence: ")
        add_bullet(lab['contribution'], bold_prefix="Contribution to Unified System: ")
        add_body("")

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 6: WORKFLOW
    # -------------------------------------------------------------
    add_h1("6. End-to-End Execution Workflow (10-Step Lifecycle)")
    add_body(
        "To understand how the entire system functions in practice, this section walks through the complete 10-step "
        "lifecycle from the moment a researcher logs in to final export."
    )

    steps = [
        ("Step 1: Researcher Project Intake", "The researcher opens the Researcher Workspace, clicks 'New Research Project', and inputs the project title, research domain, duration, estimated budget, objectives, and optional supporting PDF papers. The project receives a permanent unique DB ID and an auto-assigned sequential display number (e.g. Project #1)."),
        ("Step 2: Semantic Topic Reasoning", "TopicReasoningEngine analyzes the project corpus. Without using static hardcoded rules, it determines primary scientific discipline, interdisciplinary connections, extracts 10 semantic keywords, and analyzes resource intensity across hardware, manpower, compute, and fieldwork."),
        ("Step 3: Funding Discovery & Ranking", "Agent A (Funding Discovery Agent) searches verified national and international grant calls. It computes semantic overlap, audits budget compatibility, applies the exact mathematical scoring formula, and ranks opportunities with match percentages and custom rationales."),
        ("Step 4: Real-Time Literature Review & RAG", "Agent B (Literature Review Agent) queries live OpenAlex and Crossref APIs. It retrieves authentic papers with real DOIs. Concurrently, it indexes uploaded local files into a TF-IDF vector space, analyzes empirical claims, and extracts 3 verifiable research gaps."),
        ("Step 5: Structured Proposal Synthesis", "Agent C (Proposal Drafting Agent) synthesizes a complete research proposal draft. It formulates SMART specific aims, an Executive Summary, Problem Definition, a 4-Phase Technical Methodology, milestones, and measurable deliverables, fully incorporating Agent B's literature gaps."),
        ("Step 6: Statutory Budget Partitioning", "Agent D (Budget Planning Agent) uses FundingCalculatorTool to partition direct costs into Equipment (35%), Manpower (30%), Software (10%), Consumables (10%), and Travel (5%). It strictly calculates and enforces the 5% contingency cushion and 10% statutory institutional overhead cap."),
        ("Step 7: Institutional Compliance Audit", "Agent E (Compliance Checking Agent) verifies UGC/AICTE institutional credentials for KLE Tech, audits budget caps, checks PI qualifications, audits document attachments (Form A Endorsement, Form B CV), and emits a compliance scorecard (e.g. 80.0% - WARNINGS)."),
        ("Step 8: Packaging & Governance Gate Enforcement", "Agent F (Submission Agent) compiles all artifacts into a standardized submission dossier. It calculates checksums, writes 'submission_dossier.json' and 'grant_proposal_document.md' to disk, and physically locks external dispatch behind an authorization gate awaiting Dean R&D sign-off."),
        ("Step 9: Researcher Dashboard Presentation", "The Researcher Workspace populates all four interactive output tabs: (1) Ranked Funding Matches, (2) Editable Structured Proposal Draft, (3) Itemized Budget Schedule, and (4) Regulatory Compliance Report, with direct download buttons for .md and .json packages."),
        ("Step 10: Teacher Dashboard Inspection Studio", "Course instructors and examiners switch to the Teacher Dashboard. They can inspect any project, view execution statuses, examine raw agent traces, and run individual labs (Labs 1 to 14) or execute all 14 labs in a single click with verified evidence.")
    ]

    for s_title, s_desc in steps:
        add_h3(s_title)
        add_body(s_desc)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 7: TECHNOLOGY STACK
    # -------------------------------------------------------------
    add_h1("7. Technology Stack & Architectural Rationale")
    add_body(
        "Every technology chosen in this project was selected to solve specific technical challenges in multi-agent orchestration, "
        "deterministic precision, and user experience."
    )

    stack_items = [
        ("Python 3.12 (Backend Kernel)", "The primary programming language for the backend, chosen for its rich ecosystem of AI libraries, asynchronous capabilities, and mathematical precision."),
        ("FastAPI (Asynchronous Web Framework)", "High-performance web API framework with automatic OpenAPI/Swagger documentation, Pydantic validation, and clean async route handlers for multi-agent workflows."),
        ("React 18 & Vite (Frontend UI)", "Modern, reactive frontend framework delivering a single-page application (SPA) with lightning-fast hot module reloading, modular component hierarchy, and instant state synchronization."),
        ("TailwindCSS & Lucide-React (Design System)", "Utility-first CSS styling system providing a clean, enterprise-grade user interface with responsive grids, visual status badges, and accessible typography."),
        ("SQLite & SQLAlchemy ORM (Data Layer)", "Zero-configuration relational database with transactional integrity, foreign-key relationships, and thread-safe session handling, ideal for standalone deployment and reproducible lab evaluations."),
        ("OpenAlex & Crossref REST APIs (Live Scholarly Data)", "Open, unauthenticated global academic metadata APIs that allow the Literature Review Agent to retrieve real publications, authors, citation metrics, and verifiable DOIs without API keys."),
        ("Scikit-Learn TF-IDF & Cosine Similarity (Local RAG)", "Lightweight, deterministic vector retrieval engine that indexes local uploaded PDF/DOCX documents into semantic vector space without requiring heavy GPU clusters."),
        ("Python concurrent.futures (ThreadPool Swarm)", "Provides true multithreaded concurrent execution for Lab 8's parallel agent swarm, achieving millisecond-level parallel execution and conflict reconciliation."),
        ("LangGraph-Style Directed Acyclic Graph (Node Graph)", "Custom stateful workflow engine implementing nodes, edges, state mutation dictionaries, and conditional success predicates for Lab 7."),
        ("Pydantic v2 (Schema Validation & Contracts)", "Strict data validation and contract enforcement across all agent inputs, tool arguments, and API request/response bodies.")
    ]

    for tech_name, tech_desc in stack_items:
        add_bullet(tech_desc, bold_prefix=f"{tech_name}: ")

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 8: VIVA VOCE & PRESENTATION DEFENSE GUIDE
    # -------------------------------------------------------------
    add_h1("8. Viva Voce & Presentation Defense Guide")
    add_body(
        "During your lab review, capstone evaluation, or conference presentation, faculty examiners will ask probing technical "
        "questions to test your understanding. Here are 8 common questions and authoritative model answers."
    )

    qa_list = [
        (
            "Q1: Is your system just a wrapper around ChatGPT/OpenAI?",
            "Answer: No. The system is an autonomous multi-agent software architecture. While LLMs can provide language generation, all core capabilities in our system—including goal-directed plan mutation (Lab 1), deterministic budget calculation (Lab 2), modular skills (Lab 3), scoped database memory (Lab 4), MCP security boundaries (Lab 5), runtime execution loops (Lab 6), LangGraph DAG workflows (Lab 7), parallel multithreaded swarms (Lab 8), and live OpenAlex literature indexing (Lab 9)—are engineered as deterministic Python software components that operate independently of any specific commercial LLM wrapper."
        ),
        (
            "Q2: How do you prevent hallucination in the literature review?",
            "Answer: In Agent B and Lab 9, we connect directly to the live OpenAlex REST API (https://api.openalex.org). We extract verified publications, real author rosters, publication years, and authentic DOIs. For uploaded files, we extract raw text using pypdf/python-docx and perform TF-IDF vector retrieval with cosine similarity. Citations are grounded in real metadata rather than generated from memory."
        ),
        (
            "Q3: Explain the 10% overhead rule and why it matters.",
            "Answer: In Indian national funding schemes (DST, ICMR, MeitY, CSIR), funding agencies mandate an institutional overhead allowance capped at exactly 10% of direct research costs (or 5% in specific schemes). This money is paid to the host university (KLE Tech) for lab infrastructure, electricity, and administrative auditing. If an applicant asks for 15% or forgets overhead, the proposal is rejected. Our FundingCalculatorTool calculates this with exact arithmetic precision: Overhead = Direct Costs * 0.10."
        ),
        (
            "Q4: Where does the matching percentage (e.g. 74% or 49%) come from?",
            "Answer: It is calculated by FundingAPIConnectorTool.search_opportunities() in backend/app/tools/funding_api.py. It extracts up to 10 keywords from the project corpus and computes the overlap ratio with the funding call text. The formula is: Base Score = 0.45 + (Overlap Ratio * 0.50). If the requested budget is within the scheme ceiling, it adds a +0.04 bonus (+4%); if it exceeds the ceiling, it penalizes by -0.15 (-15%). A 49% score means zero keyword overlap but compliant budget (0.45 + 0.04 = 0.49); 74% means 50% keyword overlap with compliant budget."
        ),
        (
            "Q5: How do the agents communicate with each other?",
            "Answer: Agents communicate through structured state handoffs managed by CentralizedAgentOrchestrator, coordinated memory reads/writes in SQLite via MemoryManager, and directed node transitions in AgenticNodeGraphEngine. Output from Agent A (Funding) and Agent B (Literature) feeds directly into Agent C (Proposal Drafting) and Agent D (Budget Planning)."
        ),
        (
            "Q6: What happens if two agents produce conflicting numbers in Lab 8?",
            "Answer: In Lab 8 (Parallel Swarm), Worker 3 (Cost Estimator) and Worker 4 (Policy Auditor) run concurrently. If Worker 3 suggests ₹12.5 Lakhs while Worker 4 recommends capping at ₹10 Lakhs, the swarm's reconcile_results() algorithm intercepts the conflict, applies statutory regulatory precedence, caps the budget at ₹10 Lakhs, and records the resolution in the audit log."
        ),
        (
            "Q7: Why do you have a human approval gate in Lab 12 and Agent F?",
            "Answer: In Agentic AI, safety and governance are critical. An AI system should never possess unilateral authority to dispatch proposals to official government portals without human authorization. The Submission Agent compiles the dossier but physically locks external submission behind an ApprovalRecord state machine awaiting Dean R&D authorization credentials."
        ),
        (
            "Q8: How does the system ensure zero gaps in project display numbering?",
            "Answer: Database primary keys (e.g. ID #48, #55) are permanent foreign keys that must never be renumbered. To provide a clean user interface, our project numbering engine (backend/app/core/project_numbering.py) queries unique projects sorted chronologically (created_at ASC, id ASC) and derives a 1-based sequential display rank (Project #1, #2, ..., #N). When a project is deleted, the remaining projects are re-ranked dynamically, guaranteeing zero gaps and consistent numbering across all dashboards."
        )
    ]

    for q, a in qa_list:
        add_h3(q)
        add_body(a, space_after=8)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 9: CONCLUSION
    # -------------------------------------------------------------
    add_h1("9. Conclusion & Project Summary")
    add_body(
        "The Research Grant Management System demonstrates the profound transformative power of Agentic AI in academic research administration. "
        "By moving beyond passive, hallucination-prone chatbots to an interconnected ecosystem of six specialized agents backed by deterministic tools, "
        "scoped memory, graph orchestration, and real-time scholarly APIs, the project achieves:"
    )
    add_bullet("100% topic-independent reasoning capable of onboarding any scientific discipline without hardcoded rules.", bold_prefix="1. True Autonomy: ")
    add_bullet("Live OpenAlex integration providing verifiable, authentic academic literature with real DOIs.", bold_prefix="2. Academic Grounding: ")
    add_bullet("Exact enforcement of statutory 10% institutional overhead and 5% contingency caps.", bold_prefix="3. Mathematical Precision: ")
    add_bullet("Comprehensive realization of all 14 curriculum labs with live terminal evidence and interactive visual inspection.", bold_prefix="4. Pedagogical Completeness: ")
    add_bullet("Dual-key Dean R&D sign-off locks guaranteeing responsible, governed AI deployment.", bold_prefix="5. Governance & Safety: ")
    add_body(
        "\nThis system stands as a fully operational, academically sound, and enterprise-ready realization of modern Agentic AI engineering."
    )

    # Save document
    output_path = os.path.abspath("Research_Grant_Management_System_Complete_Explanation.docx")
    doc.save(output_path)
    print(f"Document successfully created and saved at: {output_path}")

if __name__ == "__main__":
    build_document()
