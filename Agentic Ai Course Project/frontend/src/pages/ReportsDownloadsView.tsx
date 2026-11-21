import React, { useState, useEffect } from 'react';
import { 
  Download, 
  FileText, 
  FileSpreadsheet, 
  ShieldCheck, 
  Layers, 
  FileCode, 
  CheckCircle2, 
  Building2,
  Calendar,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';

interface ReportsDownloadsViewProps {
  projectId: number;
}

export const ReportsDownloadsView: React.FC<ReportsDownloadsViewProps> = ({ projectId }) => {
  const [project, setProject] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadProjectDetails();
  }, [projectId]);

  const loadProjectDetails = async () => {
    try {
      setLoading(true);
      const data = await api.getProject(projectId);
      setProject(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadBudget = async () => {
    try {
      const data = await api.getProjectExpectedOutputs(projectId);
      const blob = new Blob([JSON.stringify(data.budget_plan, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Budget_Plan_Project_${projectId}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e: any) {
      alert(`Download failed: ${e.message}`);
    }
  };

  const handleDownloadCompliance = async () => {
    try {
      const data = await api.getProjectExpectedOutputs(projectId);
      const blob = new Blob([JSON.stringify(data.compliance_report, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Compliance_Report_Project_${projectId}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e: any) {
      alert(`Download failed: ${e.message}`);
    }
  };

  const handleDownload14LabsAudit = async () => {
    try {
      const data = await api.getTeacherOverview(projectId);
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Teacher_14_Labs_Audit_Report_Project_${projectId}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e: any) {
      alert(`Download failed: ${e.message}`);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-2">
          <Download className="w-5 h-5 text-emerald-600" />
          <h1 className="text-xl font-bold text-slate-900">
            Research Grant Reports & Export Center
          </h1>
        </div>
        <p className="text-xs text-slate-500 mt-1">
          Export verified research grant dossiers, structured proposals, budget schedules, and lab evaluation audit logs
        </p>
        <p className="text-xs text-slate-700 font-medium mt-1">
          Active Project: <span className="font-semibold text-slate-900">{project?.title || `Project #${project?.display_number || projectId}`}</span>
        </p>
      </div>

      {/* Export Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        
        {/* Item 1: Proposal Document (Markdown) */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="w-9 h-9 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Research Proposal Document</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Complete academic proposal draft in GitHub Flavored Markdown format with Abstract, Objectives, Literature Review, Methodology, Outcomes, and Milestones.
            </p>
          </div>
          <a
            href={`http://127.0.0.1:8000/api/v1/researcher/download-dossier/${projectId}/markdown`}
            download
            className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Proposal (.MD)</span>
          </a>
        </div>

        {/* Item 2: Submission Dossier (JSON) */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="w-9 h-9 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center">
              <FileCode className="w-5 h-5 text-emerald-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Complete Submission Dossier</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Sealed JSON package containing project metadata, proposal draft, verified budget breakdown, compliance status, and Dean R&D governance approval record.
            </p>
          </div>
          <a
            href={`http://127.0.0.1:8000/api/v1/researcher/download-dossier/${projectId}/json`}
            download
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Dossier (.JSON)</span>
          </a>
        </div>

        {/* Item 3: Itemized Budget Schedule */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="w-9 h-9 rounded-lg bg-amber-50 border border-amber-100 flex items-center justify-center">
              <FileSpreadsheet className="w-5 h-5 text-amber-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Itemized Budget Schedule</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Category expenses (Equipment, Manpower, Travel, Software, Consumables) with verified 10% KLE Tech overhead and 5% contingency calculations.
            </p>
          </div>
          <button
            onClick={handleDownloadBudget}
            className="w-full bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-amber-600" />
            <span>Export Budget Schedule (.JSON)</span>
          </button>
        </div>

        {/* Item 4: Compliance Verification Certificate */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="w-9 h-9 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5 text-indigo-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Compliance Audit Certificate</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Full verification audit records: UGC/AICTE institutional checks, PI eligibility, required annexures checklist, and risk assessment scorecard.
            </p>
          </div>
          <button
            onClick={handleDownloadCompliance}
            className="w-full bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-indigo-600" />
            <span>Export Compliance Report (.JSON)</span>
          </button>
        </div>

        {/* Item 5: 14 Labs Evaluation Audit Report */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="w-9 h-9 rounded-lg bg-purple-50 border border-purple-100 flex items-center justify-center">
              <Layers className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Teacher 14-Lab Evaluation Audit</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Complete instructor audit report for KLE Technological University Course 26ECAC401, including individual outputs and pass/fail evaluations for Labs 1 through 14.
            </p>
          </div>
          <button
            onClick={handleDownload14LabsAudit}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-3 rounded text-xs flex items-center justify-center space-x-1.5 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export 14-Lab Audit (.JSON)</span>
          </button>
        </div>

      </div>

    </div>
  );
};
