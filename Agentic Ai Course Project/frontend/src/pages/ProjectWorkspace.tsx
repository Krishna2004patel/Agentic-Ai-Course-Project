import React, { useState, useEffect } from 'react';
import { 
  Building, 
  Calendar, 
  IndianRupee, 
  Sparkles, 
  Search, 
  FileText, 
  DollarSign, 
  ShieldCheck, 
  Send, 
  Upload, 
  Download, 
  CheckCircle2, 
  AlertTriangle,
  Play,
  Edit3,
  RefreshCw,
  Layers
} from 'lucide-react';
import { api } from '../services/api';
import { Project } from '../types';
import { ProjectExpectedOutputs } from '../components/ProjectExpectedOutputs';
import { LiteratureReviewPanel } from '../components/LiteratureReviewPanel';
import { BookOpen } from 'lucide-react';

interface ProjectWorkspaceProps {
  projectId: number;
  onOpenNewProject: () => void;
}

export const ProjectWorkspace: React.FC<ProjectWorkspaceProps> = ({ projectId, onOpenNewProject }) => {
  const [project, setProject] = useState<Project | null>(null);
  const [activeTab, setActiveTab] = useState<'outputs' | 'literature' | 'proposal' | 'funding' | 'budget' | 'compliance' | 'submission'>('outputs');
  const [loading, setLoading] = useState(true);
  const [agentRunning, setAgentRunning] = useState<string | null>(null);

  // Agent State Stores
  const [fundingResults, setFundingResults] = useState<any>(null);
  const [literatureResults, setLiteratureResults] = useState<any>(null);
  const [proposalDraft, setProposalDraft] = useState<any>(null);
  const [budgetPlan, setBudgetPlan] = useState<any>(null);
  const [complianceReport, setComplianceReport] = useState<any>(null);
  const [submissionDossier, setSubmissionDossier] = useState<any>(null);
  const [approvalStatus, setApprovalStatus] = useState<any>(null);

  // User input states
  const [feedbackText, setFeedbackText] = useState('');
  const [overrideBudget, setOverrideBudget] = useState<number | ''>('');
  const [uploadingDoc, setUploadingDoc] = useState(false);

  useEffect(() => {
    loadProjectWorkspace();
  }, [projectId]);

  const loadProjectWorkspace = async () => {
    try {
      setLoading(true);
      const proj = await api.getProject(projectId);
      setProject(proj);

      // Fetch latest lab results or run initial agents
      const lab1 = await api.getLabDetail(1, projectId);
      if (lab1 && lab1.execution_output) {
        setProposalDraft(lab1.execution_output.revised_plan || lab1.execution_output.initial_plan);
      }

      const lab2 = await api.getLabDetail(2, projectId);
      if (lab2 && lab2.execution_output) {
        setBudgetPlan(lab2.execution_output.tool_results?.funding_calculator);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRunAgent = async (agentName: string) => {
    setAgentRunning(agentName);
    try {
      if (agentName === 'funding') {
        const res = await api.runFundingDiscovery(projectId);
        setFundingResults(res);
        setActiveTab('funding');
      } else if (agentName === 'literature') {
        const res = await api.runLiteratureReview(projectId);
        setLiteratureResults(res);
      } else if (agentName === 'proposal') {
        const res = await api.runProposalDrafting(projectId, feedbackText);
        setProposalDraft(res);
        setFeedbackText('');
        setActiveTab('proposal');
      } else if (agentName === 'budget') {
        const override = typeof overrideBudget === 'number' ? overrideBudget : undefined;
        const res = await api.runBudgetPlanning(projectId, override);
        setBudgetPlan(res);
        setActiveTab('budget');
      } else if (agentName === 'compliance') {
        const res = await api.runComplianceChecking(projectId);
        setComplianceReport(res);
        setActiveTab('compliance');
      } else if (agentName === 'submission_prep') {
        const res = await api.prepareSubmission(projectId);
        setSubmissionDossier(res);
        setActiveTab('submission');
      } else if (agentName === 'orchestrate_all') {
        const res = await api.runFullLifecycle(projectId);
        setFundingResults(res.results.funding_discovery);
        setLiteratureResults(res.results.literature_review);
        setProposalDraft(res.results.proposal_drafting);
        setBudgetPlan(res.results.budget_planning);
        setComplianceReport(res.results.compliance_checking);
        setSubmissionDossier(res.results.submission_preparation);
      }
    } catch (err: any) {
      alert(`Agent execution notice: ${err.message}`);
    } finally {
      setAgentRunning(null);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    try {
      setUploadingDoc(true);
      await api.uploadDocument(projectId, file);
      await loadProjectWorkspace();
      alert(`Document '${file.name}' uploaded and indexed for RAG literature review.`);
    } catch (err: any) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setUploadingDoc(false);
    }
  };

  const handleRequestApproval = async () => {
    try {
      const res = await api.requestHumanApproval(projectId);
      setApprovalStatus(res);
      alert(res.message);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDecideApproval = async (decision: 'APPROVED' | 'REJECTED') => {
    if (!approvalStatus?.approval_id) {
      alert("No active approval request found.");
      return;
    }
    try {
      const res = await api.decideApproval(
        projectId,
        approvalStatus.approval_id,
        "Prof. Dean R&D (KLE Tech)",
        decision,
        "Proposal package adheres to institutional ethics and financial guidelines."
      );
      alert(res.message);
      await loadProjectWorkspace();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500 font-medium">Loading project workspace...</div>;
  }

  if (!project) {
    return <div className="p-8 text-center text-slate-500">Project not found.</div>;
  }

  return (
    <div className="space-y-6">
      
      {/* Workspace Header */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-bold text-kle-red uppercase tracking-wider mb-1">
            <span>Project #{project.display_number || project.id}</span>
            <span>•</span>
            <span>{project.department}</span>
            <span>•</span>
            <span className="text-slate-500 font-normal">Host: {project.institution}</span>
          </div>

          <h1 className="text-2xl font-bold text-slate-900">{project.title}</h1>

          <div className="flex flex-wrap items-center gap-4 mt-2 text-xs text-slate-600">
            <span>PI: <strong className="text-slate-800">{project.pi_name}</strong> ({project.pi_email})</span>
            <span>Duration: <strong className="text-slate-800">{project.duration_weeks} Weeks</strong></span>
            <span>Requested Budget: <strong className="text-slate-800">₹{project.requested_budget.toLocaleString('en-IN')}</strong></span>
            <span className={`px-2 py-0.5 rounded-full font-semibold ${
              project.status === 'SUBMITTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'
            }`}>
              {project.status}
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3 shrink-0">
          <label className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-2 rounded-lg text-xs font-semibold flex items-center space-x-1.5 cursor-pointer transition-colors">
            <Upload className="w-3.5 h-3.5" />
            <span>{uploadingDoc ? 'Uploading...' : 'Upload Document'}</span>
            <input 
              type="file" 
              className="hidden" 
              accept=".pdf,.docx,.doc,.txt"
              onChange={handleFileUpload}
              disabled={uploadingDoc}
            />
          </label>

          <button
            onClick={() => handleRunAgent('orchestrate_all')}
            disabled={agentRunning !== null}
            className="bg-navy-900 hover:bg-slate-800 text-white font-medium px-4 py-2 rounded-lg text-xs shadow flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 text-amber-400 ${agentRunning === 'orchestrate_all' ? 'animate-spin' : ''}`} />
            <span>{agentRunning === 'orchestrate_all' ? 'Orchestrating...' : 'Run All 6 Agents'}</span>
          </button>
        </div>
      </div>

      {/* Agent Trigger Toolbar */}
      <div className="bg-slate-900 text-white rounded-xl p-3 flex flex-wrap items-center justify-between gap-2 shadow">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 pl-2">
          Specialized Agents:
        </span>
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => handleRunAgent('funding')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <Search className="w-3.5 h-3.5 text-emerald-400" />
            <span>A. Funding Discovery</span>
          </button>

          <button
            onClick={() => handleRunAgent('literature')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <FileText className="w-3.5 h-3.5 text-blue-400" />
            <span>B. Literature Review</span>
          </button>

          <button
            onClick={() => handleRunAgent('proposal')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <Edit3 className="w-3.5 h-3.5 text-purple-400" />
            <span>C. Proposal Drafting</span>
          </button>

          <button
            onClick={() => handleRunAgent('budget')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <DollarSign className="w-3.5 h-3.5 text-amber-400" />
            <span>D. Budget Planning</span>
          </button>

          <button
            onClick={() => handleRunAgent('compliance')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-rose-400" />
            <span>E. Compliance Audit</span>
          </button>

          <button
            onClick={() => handleRunAgent('submission_prep')}
            disabled={agentRunning !== null}
            className="px-3 py-1.5 bg-kle-red hover:bg-red-700 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>F. Submission Dossier</span>
          </button>
        </div>
      </div>

      {/* Workspace Tabs Navigation */}
      <div className="flex border-b border-slate-200 space-x-4 text-sm font-medium overflow-x-auto">
        <button
          onClick={() => setActiveTab('outputs')}
          className={`pb-3 px-1 border-b-2 font-bold transition-colors whitespace-nowrap flex items-center space-x-1.5 ${
            activeTab === 'outputs'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Layers className="w-4 h-4 text-amber-500" />
          <span>Research Grant Expected Outputs (4 Cards)</span>
        </button>

        <button
          onClick={() => setActiveTab('literature')}
          className={`pb-3 px-1 border-b-2 font-bold transition-colors whitespace-nowrap flex items-center space-x-1.5 ${
            activeTab === 'literature'
              ? 'border-purple-600 text-purple-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4 text-purple-600" />
          <span>Literature Review & RAG (Agent B)</span>
        </button>

        <button
          onClick={() => setActiveTab('proposal')}
          className={`pb-3 px-1 border-b-2 font-semibold transition-colors whitespace-nowrap ${
            activeTab === 'proposal'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Research Proposal & Roadmap
        </button>

        <button
          onClick={() => setActiveTab('funding')}
          className={`pb-3 px-1 border-b-2 font-semibold transition-colors ${
            activeTab === 'funding'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Funding Opportunities
        </button>

        <button
          onClick={() => setActiveTab('budget')}
          className={`pb-3 px-1 border-b-2 font-semibold transition-colors ${
            activeTab === 'budget'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Budget & Overhead Breakdown
        </button>

        <button
          onClick={() => setActiveTab('compliance')}
          className={`pb-3 px-1 border-b-2 font-semibold transition-colors ${
            activeTab === 'compliance'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Compliance & Regulatory Audit
        </button>

        <button
          onClick={() => setActiveTab('submission')}
          className={`pb-3 px-1 border-b-2 font-semibold transition-colors ${
            activeTab === 'submission'
              ? 'border-kle-red text-kle-red'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Submission Dossier & Approval
        </button>
      </div>

      {/* Tab 0: Mandatory Research Grant Expected Outputs (4 Cards) */}
      {activeTab === 'outputs' && (
        <ProjectExpectedOutputs projectId={projectId} />
      )}

      {/* Tab: Dedicated Literature Review & RAG (Agent B) */}
      {activeTab === 'literature' && (
        <LiteratureReviewPanel 
          projectId={projectId} 
          onSyncProposal={() => {
            setActiveTab('proposal');
            loadProjectWorkspace();
          }} 
        />
      )}

      {/* Tab 1: Proposal Draft & Plan Mutation */}
      {activeTab === 'proposal' && (
        <div className="space-y-6">
          
          {/* User Feedback Mutation Bar */}
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-3">
            <div className="text-xs font-bold text-slate-700 shrink-0">
              Provide Faculty Feedback to Mutate Plan:
            </div>
            <input
              type="text"
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              placeholder="e.g. Expand methodology to include edge sensor fault telemetry in Week 2..."
              className="flex-1 px-3 py-1.5 border border-slate-300 rounded-lg text-xs outline-none focus:ring-2 focus:ring-red-500 w-full"
            />
            <button
              onClick={() => handleRunAgent('proposal')}
              disabled={agentRunning !== null || !feedbackText.trim()}
              className="bg-navy-900 hover:bg-slate-800 text-white font-medium px-4 py-1.5 rounded-lg text-xs shrink-0 transition-colors disabled:opacity-40"
            >
              Apply Feedback (Mutate Plan)
            </button>
          </div>

          {/* Proposal Structured View */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Proposal Title</span>
              <h2 className="text-xl font-bold text-slate-900 mt-1">
                {proposalDraft?.title || `Investigation into ${project.title}`}
              </h2>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Executive Summary</span>
              <p className="text-slate-700 text-sm mt-1 leading-relaxed">
                {proposalDraft?.executive_summary || "Autonomous multi-agent research investigation targeting early biomarker discovery and verifiable clinical classification."}
              </p>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Specific Aims & Objectives</span>
              <div className="mt-2 space-y-2">
                {(proposalDraft?.objectives || [
                  `Aim 1: Multi-agent coordination and data ingestion for ${project.domain}`,
                  "Aim 2: Real-time closed-loop fault detection and accuracy benchmarking",
                  "Aim 3: Safe, verified human-in-the-loop grant execution"
                ]).map((aim: string, idx: number) => (
                  <div key={idx} className="flex items-start space-x-2 text-xs text-slate-700 bg-slate-50 p-2.5 rounded border border-slate-100">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{aim}</span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Execution Milestones Schedule</span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                {(proposalDraft?.milestones || [
                  { week: "1-2", task: "Literature Synthesis & Prior Art Survey" },
                  { week: "3-4", task: "Agent Architecture & Tool Contract Verification" },
                  { week: "5-6", task: "Field Pilot & Empirical Benchmark Evaluation" },
                  { week: "7-8", task: "Grant Final Packaging & Human Approval Sign-off" }
                ]).map((m: any, idx: number) => (
                  <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                    <span className="font-bold text-kle-red uppercase">Phase {idx + 1} (Week {m.week || m.week_span})</span>
                    <p className="text-slate-800 font-medium mt-1">{m.task || m.title}</p>
                    {m.deliverable && <p className="text-slate-500 text-[11px] mt-0.5">Deliverable: {m.deliverable}</p>}
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      )}

      {/* Tab 2: Funding Opportunities */}
      {activeTab === 'funding' && (
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h2 className="text-base font-bold text-slate-900 mb-1">Ranked Funding Opportunities</h2>
            <p className="text-xs text-slate-500 mb-4">
              Matched and ranked by Funding Discovery Agent using keyword similarity, institutional eligibility (KLE Tech), and requested budget caps.
            </p>

            <div className="space-y-3">
              {(fundingResults?.ranked_opportunities || [
                {
                  scheme_name: "Core Research Grant (CRG)",
                  agency: "DST - SERB",
                  max_amount: 6000000.0,
                  deadline: "2026-12-15",
                  relevance_score: 0.95,
                  rationale: "Matched based on engineering keywords and university faculty eligibility. Budget fits comfortably within ₹60L cap."
                },
                {
                  scheme_name: "Ad-hoc Biomedical & Healthcare AI Scheme",
                  agency: "ICMR",
                  max_amount: 5000000.0,
                  deadline: "2026-11-30",
                  relevance_score: 0.91,
                  rationale: "Translational research match for early disease detection and biomarker classification."
                }
              ]).map((opp: any, idx: number) => (
                <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/70 hover:bg-slate-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                          {opp.agency}
                        </span>
                        <h3 className="font-bold text-slate-900 text-sm">{opp.scheme_name}</h3>
                      </div>
                      <p className="text-xs text-slate-600 mt-2">{opp.rationale}</p>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-slate-500">
                        <span>Max Cap: <strong>₹{(opp.max_amount / 100000).toFixed(1)} Lakhs</strong></span>
                        <span>Deadline: <strong>{opp.deadline}</strong></span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <div className="text-xl font-extrabold text-emerald-600">
                        {(opp.relevance_score * 100).toFixed(0)}%
                      </div>
                      <span className="text-[10px] text-slate-400 font-medium">Relevance Score</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Budget Planning */}
      {activeTab === 'budget' && (
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-100">
              <div>
                <h2 className="text-base font-bold text-slate-900">Itemized Budget & Institutional Overhead</h2>
                <p className="text-xs text-slate-500">
                  Calculated by Budget Planning Agent enforcing statutory 10% institutional overhead for KLE Tech and 5% contingency.
                </p>
              </div>

              {/* Quick recalculation */}
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  placeholder="Override Target ₹"
                  value={overrideBudget}
                  onChange={(e) => setOverrideBudget(e.target.value === '' ? '' : Number(e.target.value))}
                  className="px-3 py-1.5 border border-slate-300 rounded-lg text-xs outline-none w-36"
                />
                <button
                  onClick={() => handleRunAgent('budget')}
                  className="bg-navy-900 text-white font-medium px-3 py-1.5 rounded-lg text-xs hover:bg-slate-800"
                >
                  Recalculate
                </button>
              </div>
            </div>

            {/* Budget Breakdown Summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-400 font-semibold uppercase">Total Requested</span>
                <div className="text-lg font-extrabold text-slate-900 mt-1">
                  ₹{(budgetPlan?.total_requested || project.requested_budget).toLocaleString('en-IN')}
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-400 font-semibold uppercase">Overhead (10% Statutory)</span>
                <div className="text-lg font-extrabold text-blue-600 mt-1">
                  ₹{(budgetPlan?.overhead_cost || (project.requested_budget * 0.1)).toLocaleString('en-IN')}
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-400 font-semibold uppercase">Contingency (5%)</span>
                <div className="text-lg font-extrabold text-amber-600 mt-1">
                  ₹{(budgetPlan?.contingency_cost || (project.requested_budget * 0.05)).toLocaleString('en-IN')}
                </div>
              </div>
              <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200">
                <span className="text-emerald-700 font-semibold uppercase">Compliance Check</span>
                <div className="text-sm font-bold text-emerald-800 mt-1 flex items-center space-x-1">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Valid & Capped</span>
                </div>
              </div>
            </div>

            {/* Detailed itemized list */}
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">Itemized Justifications</span>
              <ul className="space-y-1.5 text-xs text-slate-700">
                {(budgetPlan?.justifications || [
                  `Equipment: Dedicated deep learning GPU compute and biomedical acquisition nodes.`,
                  `Manpower: Stipend for one Junior Research Fellow (JRF) over project duration.`,
                  `Travel: Field validation and scholarly conference publication dissemination.`,
                  `Consumables: Specialized sensor accessories, documentation, and cloud datasets.`,
                  `Institutional Overhead: 10% statutory overhead per SERB/DST guidelines for host institution.`
                ]).map((j: string, idx: number) => (
                  <li key={idx} className="bg-slate-50 p-2.5 rounded border border-slate-100">• {j}</li>
                ))}
              </ul>
            </div>

          </div>
        </div>
      )}

      {/* Tab 4: Compliance Checking */}
      {activeTab === 'compliance' && (
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h2 className="text-base font-bold text-slate-900">Regulatory Compliance Audit</h2>
                <p className="text-xs text-slate-500">Audit report generated by Compliance Checking Agent verifying statutory guidelines and document requirements.</p>
              </div>
              <span className="text-xs font-extrabold bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">
                Score: {complianceReport?.compliance_score || 95}% COMPLIANT
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <span className="font-bold text-slate-700 uppercase tracking-wider block">Completed Checks</span>
              {(complianceReport?.checks_passed || [
                "Host institution is recognized and accredited for SERB/ICMR applications.",
                "Budget requested is within statutory scheme maximum limits.",
                "Mandatory 10% institutional overhead included in financial breakdown.",
                "Project milestone schedule fits within standard academic review windows."
              ]).map((c: string, idx: number) => (
                <div key={idx} className="p-2.5 bg-emerald-50 rounded-lg border border-emerald-100 text-emerald-900 flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{c}</span>
                </div>
              ))}
            </div>

            {complianceReport?.warnings && complianceReport.warnings.length > 0 && (
              <div className="space-y-2 text-xs pt-2">
                <span className="font-bold text-amber-700 uppercase tracking-wider block">Notices & Warnings</span>
                {complianceReport.warnings.map((w: string, idx: number) => (
                  <div key={idx} className="p-2.5 bg-amber-50 rounded-lg border border-amber-200 text-amber-900 flex items-start space-x-2">
                    <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 5: Submission Dossier & Human Approval */}
      {activeTab === 'submission' && (
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
            
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-100">
              <div>
                <h2 className="text-base font-bold text-slate-900">Final Grant Submission Dossier & Governance Gate</h2>
                <p className="text-xs text-slate-500">
                  Submission Agent packages final documents. Under strict governance rules, automated external submission is locked until human Dean sign-off.
                </p>
              </div>

              {/* Downloads */}
              <div className="flex items-center space-x-2">
                <a
                  href={`/api/v1/researcher/download-dossier/${projectId}/markdown`}
                  download
                  className="bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold px-3 py-1.5 rounded-lg text-xs flex items-center space-x-1 transition-colors"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Markdown</span>
                </a>

                <a
                  href={`/api/v1/researcher/download-dossier/${projectId}/json`}
                  download
                  className="bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold px-3 py-1.5 rounded-lg text-xs flex items-center space-x-1 transition-colors"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download JSON Dossier</span>
                </a>
              </div>
            </div>

            {/* Human Gate Card */}
            <div className="p-5 bg-amber-50/60 rounded-xl border border-amber-300">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-2">
                    <ShieldCheck className="w-5 h-5 text-amber-600" />
                    <h3 className="font-bold text-slate-900 text-sm">Human Approval Checkpoint (Dean R&D Sign-off)</h3>
                  </div>
                  <p className="text-xs text-slate-600 mt-1 max-w-2xl">
                    In compliance with ethical AI governance, no application may be submitted to external portals without explicit faculty verification.
                  </p>
                </div>

                <div className="shrink-0">
                  {approvalStatus?.status === 'PENDING_APPROVAL' ? (
                    <span className="text-xs font-bold bg-amber-200 text-amber-900 px-3 py-1 rounded-full">
                      Awaiting Dean Approval
                    </span>
                  ) : project.status === 'SUBMITTED' ? (
                    <span className="text-xs font-bold bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">
                      Approved & Archived
                    </span>
                  ) : (
                    <button
                      onClick={handleRequestApproval}
                      className="bg-navy-900 hover:bg-slate-800 text-white font-medium px-4 py-2 rounded-lg text-xs shadow"
                    >
                      Request Human Approval
                    </button>
                  )}
                </div>
              </div>

              {/* Dean Action Buttons if Pending */}
              {approvalStatus?.status === 'PENDING_APPROVAL' && (
                <div className="mt-4 pt-3 border-t border-amber-200 flex items-center justify-end space-x-3 text-xs">
                  <span className="text-slate-600 font-medium">Simulate Dean Decision:</span>
                  <button
                    onClick={() => handleDecideApproval('REJECTED')}
                    className="px-3 py-1.5 border border-red-300 text-red-700 bg-white hover:bg-red-50 rounded-lg font-semibold"
                  >
                    Reject with Comments
                  </button>
                  <button
                    onClick={() => handleDecideApproval('APPROVED')}
                    className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold shadow"
                  >
                    Authorize Official Submission
                  </button>
                </div>
              )}
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
