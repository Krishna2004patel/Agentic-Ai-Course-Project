import React, { useState, useEffect } from 'react';
import { 
  FolderKanban, 
  PlusCircle, 
  Building2, 
  User, 
  Calendar, 
  IndianRupee, 
  CheckCircle2, 
  ArrowRight,
  Search,
  Check,
  Trash2
} from 'lucide-react';
import { api } from '../services/api';

interface ResearchProjectsPageProps {
  activeProjectId: number;
  onSelectProject: (id: number) => void;
  onOpenNewProject: () => void;
  onOpenWorkspace: (id: number) => void;
}

export const ResearchProjectsPage: React.FC<ResearchProjectsPageProps> = ({
  activeProjectId,
  onSelectProject,
  onOpenNewProject,
  onOpenWorkspace
}) => {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await api.getProjects();
      setProjects(data);
    } catch (e) {
      console.error('Failed to load projects:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: number, title: string) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete project "${title}"? This will permanently remove its associated agent outputs and history.`)) {
      return;
    }
    try {
      await api.deleteProject(id);
      await loadProjects();
    } catch (err: any) {
      alert(`Failed to delete project: ${err.message}`);
    }
  };

  const filtered = projects.filter(p => 
    p.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.domain?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.pi_name?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* Top Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <FolderKanban className="w-5 h-5 text-emerald-600" />
            <h1 className="text-xl font-bold text-slate-900">
              Research Grant Projects Directory
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Manage research proposals, track PI submissions, and set active project context for multi-agent workflows
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input 
              type="text"
              placeholder="Filter by title, domain or PI..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-slate-900 w-64 bg-slate-50"
            />
          </div>

          <button
            onClick={onOpenNewProject}
            className="bg-kle-red hover:bg-red-700 text-white font-medium py-2 px-3.5 rounded-lg flex items-center space-x-1.5 text-xs shadow-xs transition-colors"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Create New Project</span>
          </button>
        </div>
      </div>

      {/* Projects Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((proj) => {
          const isActive = proj.id === activeProjectId;
          return (
            <div 
              key={proj.id}
              className={`bg-white rounded-xl border transition-all flex flex-col justify-between overflow-hidden shadow-xs ${
                isActive ? 'border-2 border-emerald-500 ring-4 ring-emerald-500/10' : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              {/* Card Header */}
              <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-800">
                      Project #{proj.display_number || (filtered.indexOf(proj) + 1)} • {proj.domain || 'Engineering'}
                    </span>
                    <h3 className="text-sm font-bold text-slate-900 line-clamp-2 leading-snug">
                      {proj.title}
                    </h3>
                  </div>
                  {isActive && (
                    <span className="bg-emerald-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center space-x-1 shrink-0">
                      <Check className="w-3 h-3" />
                      <span>ACTIVE</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Card Body */}
              <div className="p-4 space-y-2.5 text-xs flex-1">
                <div className="flex items-center space-x-2 text-slate-600">
                  <Building2 className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span className="truncate">{proj.institution || 'KLE Technological University'}</span>
                </div>

                <div className="flex items-center space-x-2 text-slate-600">
                  <User className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span className="truncate">PI: {proj.pi_name || 'Faculty Researcher'}</span>
                </div>

                <div className="flex items-center space-x-2 text-slate-600">
                  <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>Duration: {proj.duration_weeks || 8} weeks</span>
                </div>

                <div className="flex items-center space-x-2 text-slate-900 font-semibold pt-1">
                  <IndianRupee className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                  <span>Estimated Budget: ₹{Number(proj.requested_budget || 0).toLocaleString('en-IN')}</span>
                </div>

                {proj.objectives && (
                  <p className="text-[11px] text-slate-500 line-clamp-2 mt-2 bg-slate-50 p-2 rounded border border-slate-100">
                    {proj.objectives}
                  </p>
                )}
              </div>

              {/* Card Actions */}
              <div className="p-3 border-t border-slate-100 bg-slate-50/50 flex items-center space-x-2">
                {!isActive ? (
                  <button
                    onClick={() => onSelectProject(proj.id)}
                    className="flex-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-medium py-1.5 px-3 rounded text-xs flex items-center justify-center space-x-1"
                  >
                    <span>Set Active Project</span>
                  </button>
                ) : (
                  <div className="flex-1 text-center text-xs font-semibold text-emerald-700 py-1.5 bg-emerald-50 rounded border border-emerald-200">
                    Currently Selected
                  </div>
                )}

                <button
                  onClick={() => {
                    onSelectProject(proj.id);
                    onOpenWorkspace(proj.id);
                  }}
                  className="bg-slate-900 hover:bg-slate-800 text-white font-medium py-1.5 px-3 rounded text-xs flex items-center space-x-1"
                >
                  <span>Workspace</span>
                  <ArrowRight className="w-3 h-3" />
                </button>

                <button
                  onClick={(e) => handleDelete(e, proj.id, proj.title)}
                  title="Delete Project"
                  className="bg-white hover:bg-red-50 text-slate-400 hover:text-red-600 border border-slate-200 font-medium p-1.5 rounded text-xs flex items-center justify-center transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
