import React, { useState, useEffect } from 'react';
import { 
  History, 
  RotateCw, 
  Clock, 
  Bot, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertCircle,
  FileCode,
  Calendar
} from 'lucide-react';
import { api } from '../services/api';

interface ExecutionHistoryViewProps {
  projectId: number;
}

export const ExecutionHistoryView: React.FC<ExecutionHistoryViewProps> = ({ projectId }) => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filterAgent, setFilterAgent] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    loadLogs();
  }, [projectId]);

  const loadLogs = async () => {
    try {
      setLoading(true);
      const data = await api.getAuditLogs(projectId);
      setLogs(data);
    } catch (e) {
      console.error('Failed to load audit logs:', e);
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = logs.filter(l => {
    const matchesAgent = filterAgent === 'ALL' || l.agent?.toLowerCase().includes(filterAgent.toLowerCase());
    const matchesSearch = !searchQuery || 
      l.action?.toLowerCase().includes(searchQuery.toLowerCase()) || 
      l.agent?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      JSON.stringify(l.details || '').toLowerCase().includes(searchQuery.toLowerCase());
    return matchesAgent && matchesSearch;
  });

  return (
    <div className="space-y-6">
      
      {/* Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <History className="w-5 h-5 text-teal-600" />
            <h1 className="text-xl font-bold text-slate-900">
              Agentic System Audit & Execution History
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Immutable, project-isolated chronological ledger of agent actions, tool calls, and lab evaluation traces
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={loadLogs}
            disabled={loading}
            className="px-3.5 py-2 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Ledger</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-2xs flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="font-semibold text-slate-700">Filter Agent:</span>
          {['ALL', 'Funding', 'Literature', 'Proposal', 'Budget', 'Compliance', 'Submission'].map(agent => (
            <button
              key={agent}
              onClick={() => setFilterAgent(agent)}
              className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors ${
                filterAgent === agent 
                  ? 'bg-slate-900 text-white font-semibold' 
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {agent}
            </button>
          ))}
        </div>

        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
          <input 
            type="text"
            placeholder="Search action or details..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-8 pr-3 py-1.5 text-xs border border-slate-300 rounded-md focus:outline-none focus:ring-1 focus:ring-slate-900 w-56 bg-slate-50"
          />
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex items-center justify-between text-xs font-semibold text-slate-700">
          <span>Total Recorded Events: {filteredLogs.length}</span>
          <span>Project Workspace Event Stream</span>
        </div>

        {filteredLogs.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs">
            <Clock className="w-8 h-8 text-slate-300 mx-auto mb-2" />
            <p className="font-semibold">No audit events found matching query.</p>
            <p className="text-[11px] text-slate-400 mt-1">Execute an agent or lab to record verifiable execution traces.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100 text-xs">
            {filteredLogs.map((log) => (
              <div key={log.id} className="p-4 hover:bg-slate-50/60 transition-colors space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono text-[10px] font-bold">
                      LOG #{log.id}
                    </span>
                    <span className="font-bold text-slate-900">
                      {log.agent}
                    </span>
                    <span className="text-slate-400">•</span>
                    <span className="font-medium text-slate-700">
                      {log.action}
                    </span>
                  </div>

                  <span className="text-[11px] text-slate-500 font-mono flex items-center space-x-1">
                    <Calendar className="w-3 h-3 text-slate-400" />
                    <span>{log.timestamp ? new Date(log.timestamp).toLocaleString() : 'Recent'}</span>
                  </span>
                </div>

                {log.details && (
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-100 text-[11px] font-mono text-slate-700 overflow-x-auto">
                    {typeof log.details === 'object' 
                      ? JSON.stringify(log.details, null, 2) 
                      : String(log.details)}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
};
