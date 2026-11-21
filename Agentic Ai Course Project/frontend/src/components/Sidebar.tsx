import React from 'react';
import { 
  LayoutDashboard, 
  FolderKanban, 
  Briefcase,
  Bot,
  GraduationCap,
  Download,
  PlusCircle
} from 'lucide-react';

export type DashboardTab = 
  | 'overview_dashboard'
  | 'research_projects'
  | 'project_workspace'
  | 'six_ai_agents'
  | 'teacher_dashboard'
  | 'reports_downloads';

interface SidebarProps {
  currentTab: string;
  onTabChange: (tab: DashboardTab) => void;
  currentRole: 'researcher' | 'teacher';
  onOpenNewProject: () => void;
  activeProjectId?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onTabChange,
  onOpenNewProject,
}) => {
  const navItems = [
    {
      id: 'overview_dashboard' as DashboardTab,
      label: '1. Overview Dashboard',
      icon: LayoutDashboard,
      badge: null,
      color: 'text-blue-400'
    },
    {
      id: 'research_projects' as DashboardTab,
      label: '2. Research Projects',
      icon: FolderKanban,
      badge: null,
      color: 'text-emerald-400'
    },
    {
      id: 'project_workspace' as DashboardTab,
      label: '3. Project Workspace',
      icon: Briefcase,
      badge: null,
      color: 'text-indigo-400'
    },
    {
      id: 'six_ai_agents' as DashboardTab,
      label: '4. Six AI Agents',
      icon: Bot,
      badge: '6 Agents',
      color: 'text-sky-400'
    },
    {
      id: 'teacher_dashboard' as DashboardTab,
      label: '5. Teacher Dashboard – 14 Labs',
      icon: GraduationCap,
      badge: '14 Labs',
      color: 'text-amber-400'
    },
    {
      id: 'reports_downloads' as DashboardTab,
      label: '6. Reports and Downloads',
      icon: Download,
      badge: 'Export',
      color: 'text-teal-400'
    }
  ];

  return (
    <aside className="w-72 bg-slate-900 text-slate-300 min-h-[calc(100vh-4rem)] flex flex-col border-r border-slate-800 shrink-0 select-none">
      
      {/* Quick Project Action */}
      <div className="p-3.5 border-b border-slate-800">
        <button
          onClick={onOpenNewProject}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-3 rounded-lg flex items-center justify-center space-x-2 text-sm shadow transition-colors"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Research Project</span>
        </button>
      </div>

      {/* Main Navigation Links - Exactly 6 items */}
      <nav className="flex-1 p-3 space-y-1.5 overflow-y-auto">
        <div className="px-3 pt-2 pb-1 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
          System Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-slate-800 text-white font-semibold border-l-4 border-blue-500 shadow-sm'
                  : 'hover:bg-slate-800/60 text-slate-400 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center space-x-2.5 truncate">
                <Icon className={`w-4 h-4 shrink-0 ${item.color}`} />
                <span className="truncate">{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono shrink-0 ml-1.5 ${
                  isActive ? 'bg-blue-600/30 text-blue-200' : 'bg-slate-800 text-slate-400'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer info without university branding */}
      <div className="p-3 border-t border-slate-800 text-[11px] text-slate-500 bg-slate-950/40">
        <p className="font-semibold text-slate-400">Research Grant Management System</p>
        <p className="text-slate-600">6 Specialized Agents • 14 Concept Labs</p>
      </div>

    </aside>
  );
};
