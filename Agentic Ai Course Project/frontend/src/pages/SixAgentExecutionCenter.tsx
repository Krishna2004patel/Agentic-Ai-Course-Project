import React, { useState, useEffect } from 'react';
import {
  Bot,
  Play,
  RotateCw,
  CheckCircle2,
  Clock,
  AlertTriangle,
  ShieldCheck,
  FileText,
  DollarSign,
  Search,
  BookOpen,
  Send,
  Sparkles,
  Terminal,
  ChevronDown,
  ChevronUp,
  UserCheck
} from 'lucide-react';
import { api } from '../services/api';

interface AgentData {
  id: string;
  code: string;
  name: string;
  role: string;
  goal: string;
  status: 'IDLE' | 'RUNNING' | 'COMPLETED' | 'WAITING_APPROVAL' | 'FAILED';
  current_task: string;
  tools_used: string[];
  results_summary: string;
  logs: string[];
  [key: string]: any;
}

interface SixAgentExecutionCenterProps {
  projectId: number;
  onProjectChange?: (projectId: number) => void;
}

export const SixAgentExecutionCenter: React.FC<SixAgentExecutionCenterProps> = ({
  projectId,
  onProjectChange
}) => {
  const [agents, setAgents] = useState<AgentData[]>([]);
  const [projectTitle, setProjectTitle] = useState<string>('');
  const [projectDisplayNumber, setProjectDisplayNumber] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [executingAgent, setExecutingAgent] = useState<string | null>(null);
  const [isExecutingAll, setIsExecutingAll] = useState<boolean>(false);
  const [expandedLogs, setExpandedLogs] = useState<{ [key: string]: boolean }>({});
  const [approvalLoading, setApprovalLoading] = useState<boolean>(false);
  const [feedbackInput, setFeedbackInput] = useState<string>('');

  useEffect(() => {
    loadAgentsStatus();
  }, [projectId]);

  const loadAgentsStatus = async () => {
    try {
      setLoading(true);
      const data = await api.getAgentsStatus(projectId);
      setAgents(data.agents || []);
      setProjectTitle(data.project_title || '');
      setProjectDisplayNumber(data.project_display_number || null);
    } catch (err) {
      console.error('Failed to load agents status:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleLog = (agentId: string) => {
    setExpandedLogs(prev => ({ ...prev, [agentId]: !prev[agentId] }));
  };

  const handleExecuteAgent = async (agentCode: string) => {
    setExecutingAgent(agentCode);
    try {
      if (agentCode === 'A') {
        await api.runFundingDiscovery(projectId);
      } else if (agentCode === 'B') {
        await api.runLiteratureReview(projectId);
      } else if (agentCode === 'C') {
        await api.runProposalDrafting(projectId, feedbackInput);
      } else if (agentCode === 'D') {
        await api.runBudgetPlanning(projectId);
      } else if (agentCode === 'E') {
        await api.runComplianceChecking(projectId);
      } else if (agentCode === 'F') {
        await api.prepareSubmission(projectId);
      }
      await loadAgentsStatus();
    } catch (e: any) {
      alert(`Agent execution error: ${e.message}`);
    } finally {
      setExecutingAgent(null);
    }
  };

  const handleExecuteAll = async () => {
    setIsExecutingAll(true);
    try {
      await api.runFullLifecycle(projectId);
      await loadAgentsStatus();
      alert('Complete Multi-Agent Grant Workflow executed and synchronized across all 6 specialized agents.');
    } catch (e: any) {
      alert(`Workflow error: ${e.message}`);
    } finally {
      setIsExecutingAll(false);
    }
  };

  const handleRequestApproval = async () => {
    setApprovalLoading(true);
    try {
      await api.requestHumanApproval(projectId);
      await loadAgentsStatus();
    } catch (e: any) {
      alert(`Approval request error: ${e.message}`);
    } finally {
      setApprovalLoading(false);
    }
  };

  const handleDecideApproval = async (decision: 'APPROVED' | 'REJECTED') => {
    setApprovalLoading(true);
    try {
      const agentF = agents.find(a => a.code === 'F');
      const approvalId = agentF?.approval_id || 1;
      await api.decideApproval(
        projectId,
        approvalId,
        'Dr. B. K. Murali (Dean R&D, KLE Tech)',
        decision,
        'Proposal meets all DST-SERB and KLE Tech institutional parameters.'
      );
      await loadAgentsStatus();
    } catch (e: any) {
      alert(`Approval decision error: ${e.message}`);
    } finally {
      setApprovalLoading(false);
    }
  };

  const getAgentIcon = (code: string) => {
    switch (code) {
      case 'A': return <Search className="w-5 h-5 text-blue-500" />;
      case 'B': return <BookOpen className="w-5 h-5 text-purple-500" />;
      case 'C': return <FileText className="w-5 h-5 text-emerald-500" />;
      case 'D': return <DollarSign className="w-5 h-5 text-amber-500" />;
      case 'E': return <ShieldCheck className="w-5 h-5 text-indigo-500" />;
      case 'F': return <Send className="w-5 h-5 text-rose-500" />;
      default: return <Bot className="w-5 h-5 text-slate-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return (
          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Completed</span>
          </span>
        );
      case 'RUNNING':
        return (
          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            <RotateCw className="w-3.5 h-3.5 animate-spin" />
            <span>Running</span>
          </span>
        );
      case 'WAITING_APPROVAL':
        return (
          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <Clock className="w-3.5 h-3.5" />
            <span>Waiting for Approval</span>
          </span>
        );
      case 'FAILED':
        return (
          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-red-50 text-red-700 border border-red-200">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Failed</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-200">
            <Clock className="w-3.5 h-3.5" />
            <span>Idle</span>
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">

      {/* Top Banner / Actions */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 text-xs font-bold bg-slate-900 text-white rounded">
              Project #{projectDisplayNumber || projectId}
            </span>
            <h1 className="text-xl font-bold text-slate-900">
              Six-Agent Execution Center
            </h1>
          </div>
          <p className="text-sm text-slate-600 mt-1">
            Active Project: <span className="font-semibold text-slate-800">{projectTitle || 'Loading project...'}</span>
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={loadAgentsStatus}
            disabled={loading}
            className="px-3.5 py-2 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh State</span>
          </button>

          <button
            onClick={handleExecuteAll}
            disabled={isExecutingAll}
            className="px-4 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-lg flex items-center space-x-2 shadow-sm transition-colors"
          >
            {isExecutingAll ? (
              <>
                <RotateCw className="w-3.5 h-3.5 animate-spin text-amber-400" />
                <span>Orchestrating 6 Agents...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>Execute Complete Grant Workflow</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* 6 Specialized Agent Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {agents.map((agent) => {
          const isRunning = executingAgent === agent.code || (isExecutingAll && agent.status === 'RUNNING');
          const isLogsOpen = expandedLogs[agent.id];

          return (
            <div
              key={agent.id}
              className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between hover:border-slate-300 transition-all overflow-hidden"
            >
              {/* Card Header */}
              <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2.5">
                    <div className="w-9 h-9 rounded-lg bg-white border border-slate-200 flex items-center justify-center shadow-xs">
                      {getAgentIcon(agent.code)}
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-200 text-slate-800">
                          AGENT {agent.code}
                        </span>
                        <h3 className="text-sm font-bold text-slate-900">
                          {agent.name}
                        </h3>
                      </div>
                      <p className="text-[11px] text-slate-500 font-medium">
                        {agent.role}
                      </p>
                    </div>
                  </div>
                  <div>
                    {isRunning ? getStatusBadge('RUNNING') : getStatusBadge(agent.status)}
                  </div>
                </div>
              </div>

              {/* Card Body */}
              <div className="p-4 space-y-3.5 flex-1 text-xs">
                {/* Specific Goal */}
                <div>
                  <span className="font-semibold text-slate-700">Specific Goal:</span>
                  <p className="text-slate-600 mt-0.5 leading-relaxed">
                    {agent.goal}
                  </p>
                </div>

                {/* Current Task */}
                <div>
                  <span className="font-semibold text-slate-700">Current Task:</span>
                  <p className="text-slate-600 font-mono text-[11px] bg-slate-50 p-2 rounded border border-slate-100 mt-1">
                    {agent.current_task}
                  </p>
                </div>

                {/* Tools Used */}
                <div>
                  <span className="font-semibold text-slate-700">Tools Assigned:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {agent.tools_used?.map((tool, tIdx) => (
                      <span
                        key={tIdx}
                        className="px-2 py-0.5 bg-blue-50 text-blue-700 text-[10px] font-mono rounded border border-blue-100"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Execution Results Summary */}
                <div className="bg-slate-50/80 p-2.5 rounded-lg border border-slate-100">
                  <span className="font-semibold text-slate-800 block mb-1">Latest Output:</span>
                  <p className="text-slate-600 text-[11px] leading-relaxed">
                    {agent.results_summary}
                  </p>

                  {/* Agent-specific widgets */}
                  {agent.code === 'F' && agent.approval_status && (
                    <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between">
                      <span className="text-[11px] font-semibold text-slate-700">Dean R&D Gate:</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${agent.approval_status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' :
                        agent.approval_status === 'AWAITING_APPROVAL' ? 'bg-amber-100 text-amber-800' : 'bg-slate-200 text-slate-700'
                        }`}>
                        {agent.approval_status}
                      </span>
                    </div>
                  )}
                </div>

                {/* Expandable Trace / Logs */}
                {agent.logs && agent.logs.length > 0 && (
                  <div>
                    <button
                      onClick={() => toggleLog(agent.id)}
                      className="text-[11px] text-blue-600 hover:text-blue-800 flex items-center space-x-1 font-medium"
                    >
                      <Terminal className="w-3.5 h-3.5" />
                      <span>{isLogsOpen ? 'Hide Execution Trace' : `View Trace (${agent.logs.length} events)`}</span>
                      {isLogsOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </button>

                    {isLogsOpen && (
                      <div className="mt-2 bg-slate-900 text-slate-300 p-2.5 rounded-md font-mono text-[10px] space-y-1 max-h-32 overflow-y-auto">
                        {agent.logs.map((log, lIdx) => (
                          <div key={lIdx} className="flex items-start space-x-1.5">
                            <span className="text-emerald-400 select-none">›</span>
                            <span>{log}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Card Footer Actions */}
              <div className="p-3 border-t border-slate-100 bg-slate-50/50">
                {agent.code === 'F' && agent.approval_status === 'AWAITING_APPROVAL' ? (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleDecideApproval('APPROVED')}
                      disabled={approvalLoading}
                      className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-1.5 px-3 rounded text-xs flex items-center justify-center space-x-1"
                    >
                      <UserCheck className="w-3.5 h-3.5" />
                      <span>Approve (Dean R&D)</span>
                    </button>
                    <button
                      onClick={() => handleDecideApproval('REJECTED')}
                      disabled={approvalLoading}
                      className="px-2.5 py-1.5 bg-red-100 text-red-700 hover:bg-red-200 font-medium rounded text-xs"
                    >
                      Reject
                    </button>
                  </div>
                ) : agent.code === 'F' && agent.status === 'COMPLETED' && agent.approval_status === 'NOT_REQUESTED' ? (
                  <button
                    onClick={handleRequestApproval}
                    disabled={approvalLoading}
                    className="w-full bg-amber-600 hover:bg-amber-700 text-white font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 shadow-xs"
                  >
                    <UserCheck className="w-3.5 h-3.5" />
                    <span>Request Dean R&D Approval</span>
                  </button>
                ) : (
                  <button
                    onClick={() => handleExecuteAgent(agent.code)}
                    disabled={isRunning || isExecutingAll}
                    className="w-full bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 shadow-2xs transition-colors"
                  >
                    {isRunning ? (
                      <>
                        <RotateCw className="w-3.5 h-3.5 animate-spin text-blue-600" />
                        <span>Running Agent {agent.code}...</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-3.5 h-3.5 text-kle-red fill-kle-red" />
                        <span>Execute Agent {agent.code}</span>
                      </>
                    )}
                  </button>
                )}
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
