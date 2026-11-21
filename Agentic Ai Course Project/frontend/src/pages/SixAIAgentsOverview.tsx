import React from 'react';
import { 
  Bot, 
  Search, 
  BookOpen, 
  FileText, 
  DollarSign, 
  ShieldCheck, 
  Send, 
  Cpu, 
  CheckCircle2, 
  Database, 
  Lock,
  Layers,
  ArrowRight
} from 'lucide-react';

export const SixAIAgentsOverview: React.FC = () => {
  const agentSpecs = [
    {
      code: 'A',
      name: 'Funding Discovery Agent',
      role: 'Funding Opportunity Discovery & Eligibility Matchmaker',
      icon: Search,
      color: 'blue',
      goal: 'Continuously identify, evaluate, and rank active national and international research funding opportunities corresponding to the university research topic, eligibility profile, and institutional capacity.',
      instructions: 'Analyze PI domain keywords, research topic, host institution accreditation (UGC/AICTE), and project duration. Filter active funding catalog, compute multi-criteria relevance scores (0-100%), rank matching opportunities, and explain why each grant aligns with the research agenda.',
      inputSchema: '{ research_topic: string, domain: string, institution: string, duration_weeks: int, budget: float }',
      outputSchema: '{ ranked_opportunities: List[FundingOpportunity], total_matched: int, top_match_rationale: string }',
      tools: ['FundingAPIConnectorTool (OpenAlex & SERB/ICMR catalog)', 'NationalCatalogReaderTool (DST/SERB/BIRAC)', 'EligibilityMatcher (UGC accreditation checker)'],
      memoryAccess: 'Reads ProjectContext memory; Writes discovered opportunities to LongTermProjectMemory.',
      errorHandling: 'Falls back to national grant cache and deterministic ranking if external search APIs timeout.'
    },
    {
      code: 'B',
      name: 'Literature Review Agent',
      role: 'Prior Art Synthesis & Research Gap Specialist',
      icon: BookOpen,
      color: 'purple',
      goal: 'Extract empirical claims, methodological approaches, and documented limitations from scholarly papers to synthesize a verifiable literature review and pinpoint genuine research gaps.',
      instructions: 'Ingest uploaded papers (PDF/DOCX/TXT) or query open scientific indexes. Chunk and vectorize text using TF-IDF. Synthesize cross-paper comparison matrices, extract verified citations without hallucination, and isolate unaddressed research challenges.',
      inputSchema: '{ project_id: int, research_topic: string, uploaded_documents: List[DocumentMetadata] }',
      outputSchema: '{ literature_review_summary: string, research_gaps: List[string], evidence_table: List[Claim], citations: List[Citation] }',
      tools: ['DocumentReaderTool (PDF/DOCX parser)', 'TFIDFRetrievalTool (Vector cosine ranking)', 'ClaimExtractor (Empirical finding extraction)'],
      memoryAccess: 'Reads uploaded documents; writes extracted research claims and gaps into scoped SessionMemory.',
      errorHandling: 'Strict rejection of unsupported claims; returns explicit "insufficient empirical evidence" rather than hallucinating.'
    },
    {
      code: 'C',
      name: 'Proposal Drafting Agent',
      role: 'Technical Grant Writer & Section Architect',
      icon: FileText,
      color: 'emerald',
      goal: 'Synthesize project requirements, funding priorities, and literature evidence into a formal, structured, high-scoring research grant proposal with editable sections.',
      instructions: 'Generate formal academic sections: Executive Abstract, Problem Statement, Research Objectives, Literature Review, Methodology, Expected Outcomes, and Milestone Timeline. When researcher provides feedback, mutate the specific affected sections without re-generating from scratch.',
      inputSchema: '{ project_info: Dict, literature_review: Dict, funding_guidelines: Dict, user_feedback: Optional[str] }',
      outputSchema: '{ version: int, title: string, abstract: string, problem_statement: string, objectives: string, methodology: string, outcomes: string, timeline: string }',
      tools: ['ProposalWritingSkill', 'StructuredSchemaValidator', 'DeltaRevisionMutator'],
      memoryAccess: 'Reads project memory and prior draft versions; persists updated ProposalDraft to database.',
      errorHandling: 'Validates completeness against mandatory DST-SERB section schema before saving.'
    },
    {
      code: 'D',
      name: 'Budget Planning Agent',
      role: 'Grant Financial Estimator & Cost Auditor',
      icon: DollarSign,
      color: 'amber',
      goal: 'Prepare itemized, compliant financial estimates across equipment, manpower, travel, software, consumables, and strictly enforce institutional overhead and statutory contingency.',
      instructions: 'Calculate category expenses based on project duration and equipment needs. Automatically apply 10% institutional overhead for KLE Technological University and 5% contingency. Enforce DST/SERB funding ceiling rules and recalculate dynamically upon modification.',
      inputSchema: '{ requested_total: float, duration_weeks: int, equipment_list: List[Item], overhead_rate: float, contingency_rate: float }',
      outputSchema: '{ equipment: float, manpower: float, travel: float, software: float, consumables: float, contingency: float, overhead: float, total: float, justification: string }',
      tools: ['FundingCalculatorTool', 'StatutoryOverheadEnforcer (10% KLE Tech rate)', 'ContingencyValidator (5% standard)'],
      memoryAccess: 'Reads project duration and requested budget; writes verified BudgetPlan to database.',
      errorHandling: 'Deterministic arithmetic checks; rejects allocations exceeding statutory agency caps.'
    },
    {
      code: 'E',
      name: 'Compliance Checking Agent',
      role: 'Regulatory, Eligibility & Completeness Auditor',
      icon: ShieldCheck,
      color: 'indigo',
      goal: 'Verify proposal against funding guidelines, institutional eligibility criteria, mandatory document checklists, and detect compliance risks before submission.',
      instructions: 'Audit PI eligibility, host institution affiliation (KLE Tech UGC status), budget overhead limits (max 10%), required annexures (Endorsement, Bio-data, Quotations), and ethics/safety compliance. Output compliance scorecard and actionable recommendations.',
      inputSchema: '{ proposal_draft: Dict, budget_plan: Dict, project_documents: List, funding_opportunity: Dict }',
      outputSchema: '{ compliance_status: COMPLIANT | WARNINGS | NON_COMPLIANT, compliance_score: float, missing_documents: List[str], warnings: List[str], recommendations: List[str] }',
      tools: ['ComplianceCheckingSkill', 'UGC_AICTE_RuleValidator', 'DocumentCompletenessChecker'],
      memoryAccess: 'Audits all project tables; writes immutable ComplianceReport.',
      errorHandling: 'Fails closed: flags warnings whenever required institutional endorsements are unverified.'
    },
    {
      code: 'F',
      name: 'Submission Agent',
      role: 'Proposal Packaging & Governance Gatekeeper',
      icon: Send,
      color: 'rose',
      goal: 'Aggregate all verified artifacts into a sealed submission dossier, enforce Dean R&D human approval, and generate downloadable proposal packages.',
      instructions: 'Collect verified proposal, budget, and compliance outputs. Block external submission until Dean R&D grants explicit human approval. Upon approval, generate sealed JSON dossier, exportable markdown document, and audit signature.',
      inputSchema: '{ project_id: int, proposal_id: int, budget_id: int, compliance_id: int, approver_credentials: Dict }',
      outputSchema: '{ dossier_status: SEALED, human_approval: APPROVED | PENDING, downloadable_files: List[str], checksum: string }',
      tools: ['DossierPackager', 'GovernanceCheckpointEnforcer', 'DeanApprovalGate'],
      memoryAccess: 'Reads all prior agent outputs; writes ApprovalRecord and AuditLog entries.',
      errorHandling: 'Strict invariant blocker: external dispatch impossible without cryptographic approval record.'
    }
  ];

  return (
    <div className="space-y-6">
      
      {/* Overview Banner */}
      <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-3 mb-2">
          <div className="w-10 h-10 rounded-lg bg-slate-900 text-white flex items-center justify-center">
            <Bot className="w-6 h-6 text-amber-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Six Specialized AI Agents Architecture
            </h1>
            <p className="text-xs text-slate-500 font-medium">
              Autonomous, role-driven agent definitions with structured schemas, deterministic tools, and scoped memory
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-slate-100 text-xs">
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
            <span className="text-slate-500 font-medium block">Orchestrator Mode</span>
            <span className="text-sm font-bold text-slate-800">Centralized Controller</span>
          </div>
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
            <span className="text-slate-500 font-medium block">Decision Engine</span>
            <span className="text-sm font-bold text-slate-800">LLM + OpenCLA Loop</span>
          </div>
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
            <span className="text-slate-500 font-medium block">Tool Validation</span>
            <span className="text-sm font-bold text-slate-800">Deterministic & Verifiable</span>
          </div>
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
            <span className="text-slate-500 font-medium block">Governance Gate</span>
            <span className="text-sm font-bold text-slate-800">Dean R&D Human Approval</span>
          </div>
        </div>
      </div>

      {/* Agents Deep Dive Cards */}
      <div className="space-y-5">
        {agentSpecs.map((agent) => {
          const Icon = agent.icon;
          return (
            <div 
              key={agent.code}
              className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden"
            >
              {/* Header */}
              <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center space-x-3">
                  <div className="w-9 h-9 rounded-lg bg-white border border-slate-200 flex items-center justify-center shadow-xs">
                    <Icon className="w-5 h-5 text-slate-800" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-900 text-white">
                        AGENT {agent.code}
                      </span>
                      <h2 className="text-base font-bold text-slate-900">
                        {agent.name}
                      </h2>
                    </div>
                    <span className="text-xs text-slate-500 font-medium">
                      {agent.role}
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Operational & Registered</span>
                  </span>
                </div>
              </div>

              {/* Grid details */}
              <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {/* Specific Goal */}
                <div className="space-y-1 md:col-span-2">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">Specific Goal</span>
                  <p className="text-slate-700 bg-slate-50/70 p-2.5 rounded border border-slate-100 leading-relaxed">
                    {agent.goal}
                  </p>
                </div>

                {/* System Instructions */}
                <div className="space-y-1 md:col-span-2">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">System Instructions</span>
                  <p className="text-slate-600 bg-slate-50/70 p-2.5 rounded border border-slate-100 leading-relaxed font-sans">
                    {agent.instructions}
                  </p>
                </div>

                {/* Input Schema */}
                <div className="space-y-1">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">Input Schema</span>
                  <pre className="text-[11px] font-mono bg-slate-900 text-slate-200 p-2.5 rounded border border-slate-800 overflow-x-auto">
                    {agent.inputSchema}
                  </pre>
                </div>

                {/* Output Schema */}
                <div className="space-y-1">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">Output Schema</span>
                  <pre className="text-[11px] font-mono bg-slate-900 text-slate-200 p-2.5 rounded border border-slate-800 overflow-x-auto">
                    {agent.outputSchema}
                  </pre>
                </div>

                {/* Assigned Tools */}
                <div className="space-y-1">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">Assigned Tools</span>
                  <div className="space-y-1">
                    {agent.tools.map((tool, i) => (
                      <div key={i} className="flex items-center space-x-1.5 text-blue-700 bg-blue-50 px-2 py-1 rounded border border-blue-100 text-[11px] font-mono">
                        <Cpu className="w-3 h-3 text-blue-500 shrink-0" />
                        <span>{tool}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Memory & Governance */}
                <div className="space-y-1">
                  <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider block">Memory & Safety</span>
                  <div className="space-y-2 text-[11px]">
                    <div className="flex items-start space-x-1.5 text-slate-700 bg-slate-50 p-1.5 rounded border border-slate-100">
                      <Database className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                      <span>{agent.memoryAccess}</span>
                    </div>
                    <div className="flex items-start space-x-1.5 text-slate-700 bg-slate-50 p-1.5 rounded border border-slate-100">
                      <Lock className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                      <span>{agent.errorHandling}</span>
                    </div>
                  </div>
                </div>

              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
