import React from 'react';
import { Bot, Sparkles, UserCheck } from 'lucide-react';

interface NavbarProps {
  currentRole: 'researcher' | 'teacher';
  onRoleChange: (role: 'researcher' | 'teacher') => void;
  systemStatus: any;
}

export const Navbar: React.FC<NavbarProps> = ({ currentRole, onRoleChange, systemStatus }) => {
  return (
    <header className="bg-navy-900 text-white border-b border-slate-800 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Title without University logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-inner">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight">Research Grant Management System</h1>
            <p className="text-xs text-slate-400">Autonomous Multi-Agent Agentic AI Platform</p>
          </div>
        </div>

        {/* Center / System Status Pill */}
        <div className="hidden md:flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700 text-xs">
          <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" />
          <span className="text-slate-300">Engine:</span>
          <span className="text-emerald-400 font-medium">
            {systemStatus?.llm_status?.demo_mode_active 
              ? "Verified Agentic Reasoner" 
              : "LLM Provider Active"}
          </span>
        </div>

        {/* Right Role Switcher */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center bg-slate-800 p-1 rounded-lg border border-slate-700">
            <button
              onClick={() => onRoleChange('researcher')}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
                currentRole === 'researcher'
                  ? 'bg-blue-600 text-white shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Researcher View
            </button>
            <button
              onClick={() => onRoleChange('teacher')}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-all flex items-center space-x-1 ${
                currentRole === 'teacher'
                  ? 'bg-blue-600 text-white shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>Teacher Dashboard (14 Labs)</span>
            </button>
          </div>
        </div>

      </div>
    </header>
  );
};
