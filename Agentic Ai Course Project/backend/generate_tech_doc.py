import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_document():
    doc = docx.Document()

    # 1 inch margins
    for section in doc.sections:
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
    run_title = title_p.add_run("EXACT TECHNOLOGIES USED IN LAB 6 TO LAB 10")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(22)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(16, 55, 131)

    # Subtitle
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Comprehensive Technical Specification: Libraries, Frameworks, Protocols & Algorithms")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(12)
    run_sub.italic = True
    run_sub.font.color.rgb = RGBColor(90, 100, 115)

    # Metadata Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Project Name:", "Research Grant Management System (Multi-Agent Agentic AI Application)"),
        ("Scope of Document:", "Detailed Technical Inventory for Labs 6, 7, 8, 9, and 10"),
        ("Primary Programming Language:", "Python 3.14 (Backend) & TypeScript / React 18 (Frontend)"),
        ("Implementation Files:", "backend/app/agents/lab[6-10]_*.py and backend/app/core, node_graph, swarm, rag, ops")
    ]
    for i, (k, v) in enumerate(meta_info):
        r = meta_table.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        c0.paragraphs[0].text = k
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].text = v
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Executive Summary Table
    h1 = doc.add_heading(level=1)
    h1.add_run("1. Master Technology Matrix (Lab 6 to Lab 10)").font.color.rgb = RGBColor(16, 55, 131)

    t_matrix = doc.add_table(rows=6, cols=4)
    t_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Lab Number & Name", "Core Concept", "Exact Python Libraries & Modules", "Algorithms & Architectural Patterns"]
    for j, h in enumerate(headers):
        c = t_matrix.rows[0].cells[j]
        c.paragraphs[0].text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "103783")

    rows_matrix = [
        ("Lab 6:\nAgent Runtime", "Mini Personal Agent Runtime", "• inspect (signature introspection)\n• typing (Callable, Dict, Any)\n• datetime (UTC execution log)", "• OpenCLA / OpenClaw runtime pattern\n• Dynamic Tool & Skill Registry\n• Bounded Step Loop (max_steps=10)\n• Goal Predicate Stopping Criteria"),
        ("Lab 7:\nAgentic Node Graph", "DAG Workflow Engine", "• collections (state dict)\n• typing (Callable, List, Optional)\n• datetime (ISO timestamps)", "• Directed Acyclic Graph (DAG)\n• LangGraph-style state machine\n• Topological execution flow\n• Localized retry mechanics (retry_limit=2)\n• 9-Node sequential pipeline"),
        ("Lab 8:\nParallel Swarm", "Concurrent Multi-Agent Team", "• concurrent.futures (ThreadPoolExecutor)\n• time (time.perf_counter)\n• typing (Dict, Any, List)", "• Multi-threading parallelism\n• Microsecond latency benchmarking\n• Discrepancy & Conflict Detection Engine\n• Precedence-based consensus resolution"),
        ("Lab 9:\nDeep Research RAG", "Agentic RAG & Vector Search", "• pypdf (PDF text chunker)\n• python-docx (DOCX parsing)\n• re (Regex tokenization)\n• collections (Counter)\n• math (log, sqrt calculations)", "• Sliding Window Text Chunking\n• Term Frequency - Inverse Document Frequency (TF-IDF)\n• Cosine Similarity Retrieval\n• Source-cited evidence matrix"),
        ("Lab 10:\nOperations Monitoring", "AgentOps & System Telemetry", "• sqlalchemy (ORM persistence)\n• sqlite3 (database engine)\n• datetime (audit timestamps)\n• typing (Dict, Any, List)", "• Structured Telemetry Ingestion\n• Severity Classification Heuristics\n• Automated Root-Cause Diagnosis\n• Human-in-the-Loop (HITL) Interlock\n• Immutable Audit Logging schema")
    ]

    widths = [Inches(1.4), Inches(1.5), Inches(1.8), Inches(1.8)]
    for i, r_data in enumerate(rows_matrix):
        row = t_matrix.rows[i+1]
        for j, val in enumerate(r_data):
            cell = row.cells[j]
            cell.width = widths[j]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if j == 0:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "F0F4F8")
            else:
                set_cell_background(cell, "FAFAFA" if i%2==0 else "FFFFFF")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Detailed Section for each lab
    labs_details = [
        (
            "2. Lab 6: Agent Runtime — Exact Technologies & Mechanics",
            "backend/app/core/agent_runtime.py and backend/app/agents/lab6_runtime.py",
            "Mini Personal Agent Runtime (OpenCLA / OpenClaw Architecture)",
            [
                ("Python inspect Module:", "Used for runtime function signature reflection. The runtime introspects tool functions using `inspect.iscoroutinefunction(func)` to dynamically determine whether a registered tool is synchronous or asynchronous without hardcoding."),
                ("Typing System (`typing.Callable`, `Dict`, `Any`, `Optional`):", "Enforces formal interface contracts between the runtime execution core and registered external tools and skills."),
                ("Dynamic Tool Registry (`ToolRegistry`):", "Maintains an in-memory dictionary of executable tools with input parameter schemas, natural language descriptions, and exception-safe execution wrappers."),
                ("Dynamic Skill Registry (`SkillRegistry`):", "Enables dynamic registration of multi-step research skills (e.g. `dynamic_risk_assessment`) *at runtime without restarting the server or modifying the underlying execution loop*."),
                ("Scoped Context & Memory Management:", "Maintains an isolated context dictionary (`scoped_context: Dict[str, Any]`) per execution run, preventing state leakage across disparate grant applications."),
                ("Bounded Execution Engine:", "Applies deterministic loop control (`max_steps = 10`) and dynamic stopping predicates (`goal_predicate: Callable[[Dict], bool]`) to eliminate infinite loops and prevent unbounded computational expenditure.")
            ]
        ),
        (
            "3. Lab 7: Agentic Node Graph — Exact Technologies & Mechanics",
            "backend/app/node_graph/engine.py and backend/app/agents/lab7_node_graph.py",
            "Directed Acyclic Graph (DAG) Workflow Engine (LangGraph-Style Architecture)",
            [
                ("Directed Acyclic Graph (DAG) Pattern:", "Models the end-to-end research grant formulation workflow as a formal directed graph of 9 discrete nodes, where each node has strict incoming prerequisites and outgoing transitions."),
                ("LangGraph-Style Centralized State Machine:", "Implements a shared mutable state dictionary (`state: Dict[str, Any]`) that flows sequentially from node to node. Each node reads prior outputs and immutably appends its validated findings."),
                ("Validation Predicates (`Callable[[Dict[str, Any]], bool]`):", "Every node encapsulates an automated predicate function that validates the structural integrity and semantic completeness of its output before permitting graph progression."),
                ("Automatic Retry Engine (`retry_limit=2`):", "If a node fails or fails its validation predicate, the engine catches the exception, records error telemetry, and automatically retries execution up to 2 times before halting the pipeline."),
                ("The 9 Sequential Pipeline Nodes:", "1. Intake Node (Researcher Input) → 2. Planning Node (Milestones) → 3. Funding Discovery Node → 4. Literature Review Node → 5. Proposal Drafting Node → 6. Budget Planning Node → 7. Compliance Checking Node → 8. Human Approval Gate Node → 9. Submission Dossier Packaging Node.")
            ]
        ),
        (
            "4. Lab 8: Parallel Swarm — Exact Technologies & Mechanics",
            "backend/app/swarm/parallel_swarm.py and backend/app/agents/lab8_swarm.py",
            "Multi-Agent Parallel Swarms & Conflict Resolution Engine",
            [
                ("Python `concurrent.futures.ThreadPoolExecutor`:", "Spawns 4 concurrent OS-level worker threads. Rather than running agents in a slow blocking sequence, all 4 workers execute simultaneously across CPU cores."),
                ("Precision Latency Profiling (`time.perf_counter`):", "Calculates the exact elapsed execution latency for every individual worker thread down to hundredths of a millisecond (`elapsed_ms`)."),
                ("The 4 Concurrent Specialist Workers:", "• Worker 1 (Funding Research Specialist): Scans schemes and recommends allocating up to 45% budget to hardware compute.\n• Worker 2 (Literature Analysis Specialist): Evaluates prior art and recommends delaying procurement until week 6.\n• Worker 3 (Budget Specialist): Enforces statutory grant rules capping equipment at 35%.\n• Worker 4 (Review Specialist): Evaluates overall feasibility and risk score."),
                ("Discrepancy & Conflict Detection Engine:", "Analyzes worker payloads simultaneously to detect conflicting recommendations (e.g. Worker 1 demanding 45% equipment vs Worker 3 strictly capping at 35%)."),
                ("Rule-Based Conflict Arbitration:", "Automatically applies regulatory precedence: statutory funding compliance overrides investigator preference, adjusting equipment to 35% and preventing funding agency audit penalties.")
            ]
        ),
        (
            "5. Lab 9: Deep Research Agent / Agentic RAG — Exact Technologies & Mechanics",
            "backend/app/rag/vector_store.py and backend/app/agents/lab9_rag.py",
            "Retrieval-Augmented Generation (RAG) & Vector Information Retrieval",
            [
                ("Document Ingestion Engines (`pypdf` & `python-docx`):", "Extracts raw text streams from investigator-uploaded research proposals and prior publications in both Adobe PDF and Microsoft Word formats with XML tree fallback."),
                ("Sliding Window Text Chunker:", "Splits lengthy academic literature into uniform chunks of 300 words with a 50-word sliding overlap, ensuring semantic context is preserved across chunk boundaries."),
                ("Regex Tokenization (`re` module):", "Sanitizes and tokenizes text into lowercased alphabetical tokens of length >= 3 (`re.findall(r'\\b[a-zA-Z]{3,}\\b', text.lower())`)."),
                ("Mathematical TF-IDF Vector Embeddings (`math` & `Counter`):", "Calculates Term Frequency (TF) normalized by chunk word count and Inverse Document Frequency (IDF) with logarithmic smoothing: IDF = ln(1 + total_chunks / doc_frequency)."),
                ("Cosine Similarity Vector Matching:", "Computes vector dot products divided by Euclidean norms to score semantic relevance between researcher queries and indexed literature chunks."),
                ("Source-Cited Evidence Matrix:", "Retrieves top-k evidence chunks with absolute source document traceability (chunk ID, document title, source type, and similarity score percentage).")
            ]
        ),
        (
            "6. Lab 10: Operations Monitoring Agent (AgentOps) — Exact Technologies & Mechanics",
            "backend/app/ops/monitor.py and backend/app/core/audit_logger.py",
            "AgentOps, Observability, Telemetry & Safety Governance",
            [
                ("Relational Telemetry Storage (`SQLAlchemy` & SQLite):", "Persists all agent execution events, prompt payloads, latency metrics, and execution statuses into the `audit_logs` table in `data/grant_system.db`."),
                ("Structured Telemetry Ingestion:", "Captures operational health signals, execution latency anomalies, HTTP 504 timeouts from external APIs, and document parser warnings."),
                ("Three-Tier Incident Severity Classifier:", "Categorizes operational incidents into `LOW` (e.g. non-standard font in PDF annexure), `HIGH` (e.g. external OpenAlex API gateway timeout), and `CRITICAL` (e.g. proposal requesting 15% overhead exceeding the 10% statutory cap)."),
                ("Automated Root-Cause Diagnostic Heuristics:", "Diagnoses system failures automatically and maps them to verified remediation steps (e.g. switching to local cached catalog during external network timeout; invoking OCR on malformed PDFs)."),
                ("Human-in-the-Loop (HITL) Safety Interlock:", "Enforces the core safety invariant: *destructive or non-compliant actions (such as overriding statutory budget caps) are strictly blocked from automated execution* and halted until manual human approval is received.")
            ]
        )
    ]

    for title, file_path, concept, items in labs_details:
        h = doc.add_heading(level=1)
        h.add_run(title).font.color.rgb = RGBColor(16, 55, 131)

        p_meta = doc.add_paragraph()
        r_f = p_meta.add_run(f"• Source Implementation: {file_path}\n• Foundational Concept: {concept}")
        r_f.font.size = Pt(9.5)
        r_f.italic = True
        r_f.font.color.rgb = RGBColor(80, 90, 105)

        for bold_label, desc in items:
            p_item = doc.add_paragraph(style='List Bullet')
            r_b = p_item.add_run(bold_label + " ")
            r_b.bold = True
            p_item.add_run(desc)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Underlying Stack
    h_stack = doc.add_heading(level=1)
    h_stack.add_run("7. Shared Underlying Platform Stack").font.color.rgb = RGBColor(16, 55, 131)

    stack_table = doc.add_table(rows=6, cols=3)
    stack_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Layer", "Technology / Framework", "Role in Grant Management System"]
    for j, h in enumerate(s_headers):
        c = stack_table.rows[0].cells[j]
        c.paragraphs[0].text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, "103783")

    s_data = [
        ("Backend Web Framework", "FastAPI (Python 3.14) & Uvicorn", "High-performance asynchronous REST API serving agent endpoints and lab runners"),
        ("Database & ORM", "SQLite 3 & SQLAlchemy", "ACID-compliant relational persistence for projects, proposals, budgets, audit logs, and lab outputs"),
        ("Frontend Web Framework", "React 18 & TypeScript", "Component-driven user interface with strict static typing for Researcher and Teacher views"),
        ("Build Tool & Bundler", "Vite 5", "Fast developer server with Hot Module Replacement and production asset bundling"),
        ("Styling & Icons", "Tailwind CSS & Lucide Icons", "Modern responsive layout with interactive cards, badges, modal views, and execution progress bars")
    ]
    for i, r_info in enumerate(s_data):
        row = stack_table.rows[i+1]
        for j, val in enumerate(r_info):
            cell = row.cells[j]
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if j == 0:
                cell.paragraphs[0].runs[0].bold = True
                cell.width = Inches(1.8)
                set_cell_background(cell, "F0F4F8")
            elif j == 1:
                cell.width = Inches(2.2)
                set_cell_background(cell, "FAFAFA" if i%2==0 else "FFFFFF")
            else:
                cell.width = Inches(2.5)
                set_cell_background(cell, "FAFAFA" if i%2==0 else "FFFFFF")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    output_path = r"c:\Users\Admin\Downloads\New folder (3)\Technologies_Used_Lab6_to_Lab10.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
