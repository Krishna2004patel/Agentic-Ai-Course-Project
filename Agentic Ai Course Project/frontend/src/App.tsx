import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, DashboardTab } from './components/Sidebar';
import { ResearcherDashboard } from './pages/ResearcherDashboard';
import { ResearchProjectsPage } from './pages/ResearchProjectsPage';
import { ProjectWorkspace } from './pages/ProjectWorkspace';
import { SixAIAgentsOverview } from './pages/SixAIAgentsOverview';
import { TeacherDashboard } from './pages/TeacherDashboard';
import { ReportsDownloadsView } from './pages/ReportsDownloadsView';
import { NewProjectModal } from './pages/NewProjectModal';
import { api } from './services/api';

export const App: React.FC = () => {
  const [currentRole, setCurrentRole] = useState<'researcher' | 'teacher'>('researcher');
  const [currentTab, setCurrentTab] = useState<DashboardTab>('overview_dashboard');
  const [activeProjectId, setActiveProjectId] = useState<number>(1);
  const [isNewProjectModalOpen, setIsNewProjectModalOpen] = useState<boolean>(false);
  const [systemStatus, setSystemStatus] = useState<any>(null);

  useEffect(() => {
    loadSystemStatus();
  }, [activeProjectId]);

  const loadSystemStatus = async () => {
    try {
      const s = await api.getSystemStatus();
      setSystemStatus(s);
    } catch (e) {
      console.error(e);
    }
  };

  const handleRoleChange = (role: 'researcher' | 'teacher') => {
    setCurrentRole(role);
    if (role === 'teacher') {
      setCurrentTab('teacher_dashboard');
    } else {
      setCurrentTab('overview_dashboard');
    }
  };

  const handleSelectProject = (projectId: number) => {
    setActiveProjectId(projectId);
  };

  const handleProjectCreated = (newProject: any) => {
    setActiveProjectId(newProject.id);
    setCurrentTab('project_workspace');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <Navbar 
        currentRole={currentRole}
        onRoleChange={handleRoleChange}
        systemStatus={systemStatus}
      />

      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Sidebar with exactly the 6 requested items */}
        <Sidebar 
          currentTab={currentTab}
          onTabChange={setCurrentTab}
          currentRole={currentRole}
          onOpenNewProject={() => setIsNewProjectModalOpen(true)}
          activeProjectId={activeProjectId}
        />

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="w-full max-w-[1600px] mx-auto space-y-6">
            
            {/* 1. Overview Dashboard (Researcher Dashboard) */}
            {currentTab === 'overview_dashboard' && (
              <ResearcherDashboard 
                onSelectProject={(id) => {
                  setActiveProjectId(id);
                  setCurrentTab('project_workspace');
                }}
                onOpenNewProject={() => setIsNewProjectModalOpen(true)}
              />
            )}

            {/* 2. Research Projects */}
            {currentTab === 'research_projects' && (
              <ResearchProjectsPage 
                activeProjectId={activeProjectId}
                onSelectProject={handleSelectProject}
                onOpenNewProject={() => setIsNewProjectModalOpen(true)}
                onOpenWorkspace={(id) => {
                  setActiveProjectId(id);
                  setCurrentTab('project_workspace');
                }}
              />
            )}

            {/* 3. Project Workspace */}
            {currentTab === 'project_workspace' && (
              <ProjectWorkspace 
                projectId={activeProjectId}
                onOpenNewProject={() => setIsNewProjectModalOpen(true)}
              />
            )}

            {/* 4. Six AI Agents */}
            {currentTab === 'six_ai_agents' && (
              <SixAIAgentsOverview />
            )}

            {/* 5. Teacher Dashboard – 14 Labs */}
            {currentTab === 'teacher_dashboard' && (
              <TeacherDashboard />
            )}

            {/* 6. Reports and Downloads */}
            {currentTab === 'reports_downloads' && (
              <ReportsDownloadsView projectId={activeProjectId} />
            )}

          </div>
        </main>

      </div>

      {/* New Project Modal */}
      <NewProjectModal 
        isOpen={isNewProjectModalOpen}
        onClose={() => setIsNewProjectModalOpen(false)}
        onProjectCreated={handleProjectCreated}
      />

    </div>
  );
};
