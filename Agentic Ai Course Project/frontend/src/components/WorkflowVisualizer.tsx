import React from 'react';
import { 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  RefreshCw, 
  ShieldCheck, 
  FileText, 
  DollarSign, 
  Search, 
  Sparkles, 
  Send 
} from 'lucide-react';

interface WorkflowNode {
  id: string;
  label: string;
  agent: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'RETRIED';
  retries: number;
  retry_limit: number;
}

interface WorkflowVisualizerProps {
  nodes?: WorkflowNode[];
  onRetryNode?: (nodeId: string) => void;
  onRunWorkflow?: () => void;
  isRunning?: boolean;
}

const DEFAULT_NODES: WorkflowNode[] = [
  { id: 'node_input', label: 'Researcher Input', agent: 'Intake Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_planning', label: 'Planning & Milestones', agent: 'Research Planning Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_funding', label: 'Funding Discovery', agent: 'Funding Discovery Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_literature', label: 'Literature Review', agent: 'Literature Review Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_proposal', label: 'Proposal Drafting', agent: 'Proposal Drafting Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_budget', label: 'Budget Planning', agent: 'Budget Planning Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_compliance', label: 'Compliance Audit', agent: 'Compliance Checking Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_approval', label: 'Human Approval Checkpoint', agent: 'Dean Governance Gate', status: 'COMPLETED', retries: 0, retry_limit: 2 },
  { id: 'node_submission', label: 'Submission Dossier', agent: 'Submission Agent', status: 'COMPLETED', retries: 0, retry_limit: 2 },
];

export const WorkflowVisualizer: React.FC<WorkflowVisualizerProps> = ({
  nodes = DEFAULT_NODES,
  onRetryNode,
  onRunWorkflow,
  isRunning = false
}) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center space-x-2">
            <span>Agentic Node Graph Workflow (Lab 7)</span>
            <span className="text-xs bg-purple-100 text-purple-700 font-semibold px-2.5 py-0.5 rounded-full">
              Executable DAG Engine
            </span>
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Visual state-machine tracking each specialized agent step, retry policies, and human approval checkpoints.
          </p>
        </div>

        {onRunWorkflow && (
          <button
            onClick={onRunWorkflow}
            disabled={isRunning}
            className="bg-navy-900 hover:bg-slate-800 text-white font-medium px-4 py-2 rounded-lg text-sm flex items-center space-x-2 shadow transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isRunning ? 'animate-spin' : ''}`} />
            <span>{isRunning ? 'Executing Graph...' : 'Re-Execute Node Graph'}</span>
          </button>
        )}
      </div>

      {/* Grid of Workflow Nodes */}
      <div className="relative">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {nodes.map((node, index) => {
            const isCompleted = node.status === 'COMPLETED';
            const isFailed = node.status === 'FAILED';
            const isRunningState = node.status === 'RUNNING';

            return (
              <div
                key={node.id}
                className={`p-4 rounded-xl border transition-all relative overflow-hidden ${
                  node.id === 'node_approval'
                    ? 'border-amber-400 bg-amber-50/40 shadow-sm'
                    : isCompleted
                    ? 'border-emerald-200 bg-emerald-50/30'
                    : isFailed
                    ? 'border-red-300 bg-red-50/50'
                    : 'border-slate-200 bg-slate-50/50'
                }`}
              >
                {/* Step number badge */}
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold tracking-wide uppercase px-2 py-0.5 rounded bg-slate-200 text-slate-700">
                    Step {index + 1}
                  </span>
                  
                  {isCompleted && (
                    <span className="flex items-center text-xs font-semibold text-emerald-600 space-x-1">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Completed</span>
                    </span>
                  )}
                  {isRunningState && (
                    <span className="flex items-center text-xs font-semibold text-blue-600 space-x-1">
                      <Clock className="w-3.5 h-3.5 animate-spin" />
                      <span>Running</span>
                    </span>
                  )}
                  {isFailed && (
                    <span className="flex items-center text-xs font-semibold text-red-600 space-x-1">
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>Failed</span>
                    </span>
                  )}
                </div>

                <h3 className="font-bold text-slate-900 text-sm">{node.label}</h3>
                
                <div className="mt-2 text-xs text-slate-500">
                  <span className="font-medium text-slate-600">Owner Agent:</span> {node.agent}
                </div>

                {node.id === 'node_approval' && (
                  <div className="mt-3 flex items-center space-x-1 text-xs text-amber-700 font-medium bg-amber-100/70 px-2 py-1 rounded">
                    <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
                    <span>Hard Governance Checkpoint</span>
                  </div>
                )}

                {/* Node retry info */}
                <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px] text-slate-400">
                  <span>Retries: {node.retries}/{node.retry_limit}</span>
                  {isFailed && onRetryNode && (
                    <button
                      onClick={() => onRetryNode(node.id)}
                      className="text-red-600 font-semibold hover:underline flex items-center space-x-1"
                    >
                      <RefreshCw className="w-3 h-3" />
                      <span>Retry Node</span>
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-6 p-4 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between text-xs text-slate-600">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          <span className="font-medium text-slate-700">Execution Strategy:</span>
          <span>Deterministic DAG traversal with automatic retry backoff and rollback protection.</span>
        </div>
        <span className="text-slate-400">Graph Schema: 9 Connected Nodes</span>
      </div>
    </div>
  );
};
