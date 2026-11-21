import React, { useState, useEffect } from 'react';
import {
  FolderKanban,
  Search,
  FileText,
  AlertTriangle,
  IndianRupee,
  Activity,
  ArrowUpRight,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Building,
  Bot,
  Play,
  Download,
  Clock,
  User,
  RefreshCw,
  Layers,
  Upload,
  ChevronRight
} from 'lucide-react';
import { api } from '../services/api';
import { Project, ResearcherMetrics } from '../types';
import { ProjectExpectedOutputs } from '../components/ProjectExpectedOutputs';

interface ResearcherDashboardProps {
  onSelectProject: (projectId: number) => void;
  onOpenNewProject: () => void;
}

export const ResearcherDashboard: React.FC<ResearcherDashboardProps> = ({
  onSelectProject,
  onOpenNewProject
}) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number>(1);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [executingAgent, setExecutingAgent] = useState<string | null>(null);
  const [orchestratingAll, setOrchestratingAll] = useState(false);
  const [agentStatuses, setAgentStatuses] = useState<any[]>([]);

  useEffect(() => {
    loadProjectsAndActive();
  }, []);

  useEffect(() => {
    if (selectedProjectId) {
      loadProjectDetails(selectedProjectId);
      loadAgentStatuses(selectedProjectId);
    }
  }, [selectedProjectId]);

  const loadProjectsAndActive = async () => {
    try {
      setLoading(true);
      const projs = await api.getProjects();
      setProjects(projs);
      if (projs.length > 0) {
        setSelectedProjectId(projs[0].id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const loadProjectDetails = async (id: number) => {
    try {
      const p = await api.getProject(id);
      setCurrentProject(p);
    } catch (e) {
      console.error(e);
    }
  };

  const loadAgentStatuses = async (id: number) => {
    try {
      const res = await api.getAgentsStatus(id);
      if (res.agents) {
        setAgentStatuses(res.agents);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunAgent = async (agentKey: string) => {
    try {
      setExecutingAgent(agentKey);
      if (agentKey === 'agent_a') await api.runFundingDiscovery(selectedProjectId);
      else if (agentKey === 'agent_b') await api.runLiteratureReview(selectedProjectId);
      else if (agentKey === 'agent_c') await api.runProposalDrafting(selectedProjectId);
      else if (agentKey === 'agent_d') await api.runBudgetPlanning(selectedProjectId);
      else if (agentKey === 'agent_e') await api.runComplianceChecking(selectedProjectId);
      else if (agentKey === 'agent_f') await api.prepareSubmission(selectedProjectId);

      await loadAgentStatuses(selectedProjectId);
      await loadProjectDetails(selectedProjectId);
    } catch (e: any) {
      alert(`Agent execution notice: ${e.message}`);
    } finally {
      setExecutingAgent(null);
    }
  };

  const handleRunAllAgents = async () => {
    try {
      setOrchestratingAll(true);
      await api.runFullLifecycle(selectedProjectId);
      await loadAgentStatuses(selectedProjectId);
      await loadProjectDetails(selectedProjectId);
    } catch (e: any) {
      alert(`Lifecycle notice: ${e.message}`);
    } finally {
      setOrchestratingAll(false);
    }
  };

  return (
    <div className="space-y-6">

      {/* 1. RESEARCH PROJECT DETAILS & SELECTOR BANNER */}
      <div className="bg-navy-900 rounded-2xl p-6 text-white shadow-lg border border-slate-800">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1">
              <span>Faculty Researcher Portal</span>
              <span>•</span>
              <span>KLE Technological University</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight">Research Grant Management System</h1>
            <p className="text-slate-300 text-xs sm:text-sm mt-1 max-w-3xl">
              End-to-end autonomous multi-agent grant assistant: funding discovery, literature synthesis, proposal drafting, statutory budget optimization, and compliance verification.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            {/* Project Selector */}
            <div className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 flex items-center space-x-2 text-xs">
              <Building className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-400">Active Project:</span>
              <select
                value={selectedProjectId}
                onChange={(e) => setSelectedProjectId(Number(e.target.value))}
                className="bg-transparent text-white font-semibold outline-none cursor-pointer"
              >
                {projects.map((p, idx) => (
                  <option key={p.id} value={p.id} className="bg-slate-800 text-white">
                    Project #{p.display_number || (idx + 1)}: {p.title.slice(0, 35)}...
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={onOpenNewProject}
              className="bg-kle-red hover:bg-red-700 text-white font-medium px-4 py-2 rounded-lg text-xs shadow transition-colors flex items-center space-x-1.5"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>New Research Project</span>
            </button>
          </div>
        </div>

        {/* Selected Project Metadata Strip */}
        {currentProject && (
          <div className="mt-5 pt-4 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
            <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Research Domain</span>
              <span className="text-white font-semibold truncate block mt-0.5">{currentProject.domain}</span>
            </div>
            <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Principal Investigator</span>
              <span className="text-white font-semibold truncate block mt-0.5">{currentProject.pi_name}</span>
            </div>
            <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Institution</span>
              <span className="text-white font-semibold truncate block mt-0.5">{currentProject.institution}</span>
            </div>
            <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Requested Budget</span>
              <span className="text-emerald-400 font-bold block mt-0.5">₹{currentProject.requested_budget?.toLocaleString('en-IN')}</span>
            </div>
            <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Duration</span>
              <span className="text-amber-400 font-bold block mt-0.5">{currentProject.duration_weeks} Weeks</span>
            </div>
          </div>
        )}
      </div>

      {/* 2. SIX SPECIALIZED AI AGENTS & EXECUTION CONTROLS */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <Bot className="w-5 h-5 text-blue-600" />
              <span>Six Specialized AI Agents – Research Grant Lifecycle</span>
            </h2>
            <p className="text-xs text-slate-500">Autonomous agents collaborate to drive discovery, synthesis, budgeting, and compliance</p>
          </div>

          <button
            onClick={handleRunAllAgents}
            disabled={orchestratingAll}
            className="self-start sm:self-center bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg text-xs shadow flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${orchestratingAll ? 'animate-spin' : ''}`} />
            <span>{orchestratingAll ? 'Orchestrating All Agents...' : 'Run All Six Agents'}</span>
          </button>
        </div>

        {/* Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {[
            { id: 'agent_a', code: 'A', name: 'Funding Discovery Agent', role: 'Grant Call Scout & Matcher', desc: 'Ranks national/international calls (DST-SERB, ICMR, AICTE, MeitY).' },
            { id: 'agent_b', code: 'B', name: 'Literature Review Agent', role: 'Prior Art & RAG Specialist', desc: 'Processes PDF/DOCX papers, indexes TF-IDF chunks, identifies research gaps.' },
            { id: 'agent_c', code: 'C', name: 'Proposal Drafting Agent', role: 'Grant Proposal Architect', desc: 'Generates structured proposal integrating Agent B gaps and methodology.' },
            { id: 'agent_d', code: 'D', name: 'Budget Planning Agent', role: 'Financial Estimator & Auditor', desc: 'Allocates itemized expenses with 10% statutory KLE Tech overhead.' },
            { id: 'agent_e', code: 'E', name: 'Compliance Checking Agent', role: 'Policy & Regulatory Auditor', desc: 'Verifies eligibility, Form A endorsement, and funding guidelines.' },
            { id: 'agent_f', code: 'F', name: 'Submission Agent', role: 'Packaging & Sign-off Gatekeeper', desc: 'Compiles final submission package and manages dual-key approval gate.' }
          ].map((ag) => {
            const isRunning = executingAgent === ag.id;
            const liveStatus = agentStatuses.find(s => s.id === ag.id)?.status || 'READY';

            return (
              <div key={ag.id} className="p-4 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:border-blue-300 transition-all flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="w-6 h-6 rounded-md bg-navy-900 text-white font-bold text-xs flex items-center justify-center">
                      {ag.code}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${liveStatus === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'
                      }`}>
                      {liveStatus}
                    </span>
                  </div>
                  <h3 className="font-bold text-slate-900 text-xs">{ag.name}</h3>
                  <div className="text-[11px] text-blue-600 font-medium mb-1">{ag.role}</div>
                  <p className="text-[11px] text-slate-500 mb-3">{ag.desc}</p>
                </div>

                <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between">
                  <button
                    onClick={() => handleRunAgent(ag.id)}
                    disabled={isRunning}
                    className="w-full py-1.5 px-3 bg-white hover:bg-slate-100 text-slate-800 rounded-lg text-xs font-semibold flex items-center justify-center space-x-1 border border-slate-200 transition-colors disabled:opacity-50"
                  >
                    <Play className={`w-3 h-3 text-blue-600 ${isRunning ? 'animate-spin' : ''}`} />
                    <span>{isRunning ? 'Running...' : `Execute Agent ${ag.code}`}</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. FOUR MAIN EXPECTED OUTPUTS (CARDS 1, 2, 3, 4) */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <FileText className="w-5 h-5 text-emerald-600" />
            <span>Four Main Research Grant Expected Outputs</span>
          </h2>
          <span className="text-xs text-slate-500">Driven by the six specialized agents</span>
        </div>

        <ProjectExpectedOutputs projectId={selectedProjectId} />
      </div>

      {/* 4. DOWNLOADABLE PROPOSAL PACKAGE & SUBMISSION DOSSIER */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
              <Download className="w-4 h-4 text-blue-600" />
              <span>Downloadable Research Proposal & Submission Package</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Export verified grant dossier containing structured proposal markdown, budget schedule, and audit certificates.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <a
              href={api.getDownloadUrl(selectedProjectId, 'md')}
              download
              className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-semibold flex items-center space-x-1.5 border border-slate-200 transition-colors"
            >
              <FileText className="w-3.5 h-3.5 text-blue-600" />
              <span>Download Proposal (.md)</span>
            </a>

            <a
              href={api.getDownloadUrl(selectedProjectId, 'json')}
              download
              className="px-3.5 py-2 bg-navy-900 hover:bg-navy-800 text-white rounded-lg text-xs font-semibold flex items-center space-x-1.5 shadow transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-amber-400" />
              <span>Download Full Dossier (.json)</span>
            </a>
          </div>
        </div>
      </div>

    </div>
  );
};
