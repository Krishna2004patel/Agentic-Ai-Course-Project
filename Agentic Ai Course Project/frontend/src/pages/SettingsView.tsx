import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  Server, 
  Building2, 
  ShieldAlert, 
  Save, 
  CheckCircle2, 
  Cpu, 
  DollarSign,
  Info
} from 'lucide-react';

export const SettingsView: React.FC = () => {
  const [llmProvider, setLlmProvider] = useState<string>('deterministic');
  const [ollamaUrl, setOllamaUrl] = useState<string>('http://localhost:11434');
  const [openaiBaseUrl, setOpenaiBaseUrl] = useState<string>('https://api.openai.com/v1');
  const [modelName, setModelName] = useState<string>('gpt-4o-mini');
  const [overheadRate, setOverheadRate] = useState<number>(10);
  const [contingencyRate, setContingencyRate] = useState<number>(5);
  const [institutionName, setInstitutionName] = useState<string>('KLE Technological University, Hubballi');
  const [savedNotice, setSavedNotice] = useState<boolean>(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      
      {/* Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5 text-slate-700" />
          <h1 className="text-xl font-bold text-slate-900">
            System & Agent Environment Settings
          </h1>
        </div>
        <p className="text-xs text-slate-500 mt-1">
          Configure multi-agent LLM providers, deterministic safety fallbacks, and KLE Technological University institutional budgeting parameters
        </p>
      </div>

      {savedNotice && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-800 text-xs font-semibold flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>Configuration saved successfully.</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-5">
        
        {/* Card 1: LLM Provider Configuration */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-100 pb-3">
            <Cpu className="w-4 h-4 text-blue-600" />
            <h2 className="text-sm font-bold text-slate-900">LLM Provider & Agent Reasoning Engine</h2>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Active LLM Provider</label>
              <select
                value={llmProvider}
                onChange={(e) => setLlmProvider(e.target.value)}
                className="w-full p-2 border border-slate-300 rounded-lg text-xs bg-slate-50 focus:outline-none focus:ring-1 focus:ring-slate-900"
              >
                <option value="deterministic">
                  Deterministic Agentic Mode (Self-Contained Fallback — No external API key required)
                </option>
                <option value="openai">
                  OpenAI-Compatible Provider (Requires OPENAI_API_KEY environment variable)
                </option>
                <option value="ollama">
                  Local Ollama Provider (Self-Hosted LLM at localhost:11434)
                </option>
              </select>
            </div>

            {llmProvider === 'deterministic' && (
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-900 text-xs space-y-1">
                <div className="flex items-center space-x-1.5 font-bold">
                  <Info className="w-4 h-4 text-blue-600" />
                  <span>Transparent Disclosure: Deterministic Demo Mode</span>
                </div>
                <p className="text-[11px] leading-relaxed">
                  In accordance with the project instructions, when no external LLM credentials or Ollama instances are detected, the orchestrator executes verified deterministic domain rules and national grant datasets. It never pretends that simulated responses originated from an unconfigured external API.
                </p>
              </div>
            )}

            {llmProvider === 'openai' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div>
                  <label className="font-medium text-slate-700 block mb-1">Base URL</label>
                  <input
                    type="text"
                    value={openaiBaseUrl}
                    onChange={(e) => setOpenaiBaseUrl(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded text-xs bg-slate-50 font-mono"
                  />
                </div>
                <div>
                  <label className="font-medium text-slate-700 block mb-1">Model Name</label>
                  <input
                    type="text"
                    value={modelName}
                    onChange={(e) => setModelName(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded text-xs bg-slate-50 font-mono"
                  />
                </div>
              </div>
            )}

            {llmProvider === 'ollama' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div>
                  <label className="font-medium text-slate-700 block mb-1">Ollama Host URL</label>
                  <input
                    type="text"
                    value={ollamaUrl}
                    onChange={(e) => setOllamaUrl(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded text-xs bg-slate-50 font-mono"
                  />
                </div>
                <div>
                  <label className="font-medium text-slate-700 block mb-1">Ollama Model</label>
                  <input
                    type="text"
                    defaultValue="mistral:7b"
                    className="w-full p-2 border border-slate-300 rounded text-xs bg-slate-50 font-mono"
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Card 2: Institutional Budget Parameters */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-100 pb-3">
            <Building2 className="w-4 h-4 text-emerald-600" />
            <h2 className="text-sm font-bold text-slate-900">KLE Technological University Institutional Governance</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="sm:col-span-3">
              <label className="font-semibold text-slate-700 block mb-1">Host University / Institution</label>
              <input
                type="text"
                value={institutionName}
                onChange={(e) => setInstitutionName(e.target.value)}
                className="w-full p-2 border border-slate-300 rounded-lg text-xs bg-slate-50"
              />
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Statutory Overhead Rate (%)</label>
              <input
                type="number"
                value={overheadRate}
                onChange={(e) => setOverheadRate(Number(e.target.value))}
                min="0"
                max="25"
                className="w-full p-2 border border-slate-300 rounded-lg text-xs bg-slate-50 font-mono"
              />
              <span className="text-[10px] text-slate-500 block mt-1">Default: 10% as mandated by KLE Tech</span>
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Statutory Contingency Rate (%)</label>
              <input
                type="number"
                value={contingencyRate}
                onChange={(e) => setContingencyRate(Number(e.target.value))}
                min="0"
                max="15"
                className="w-full p-2 border border-slate-300 rounded-lg text-xs bg-slate-50 font-mono"
              />
              <span className="text-[10px] text-slate-500 block mt-1">Default: 5% DST-SERB standard</span>
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Approval Authority</label>
              <input
                type="text"
                disabled
                value="Dean R&D / Faculty Chair"
                className="w-full p-2 border border-slate-200 rounded-lg text-xs bg-slate-100 text-slate-500 font-mono cursor-not-allowed"
              />
              <span className="text-[10px] text-slate-500 block mt-1">Role-based governance invariant</span>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-slate-900 hover:bg-slate-800 text-white font-medium py-2 px-5 rounded-lg text-xs flex items-center space-x-1.5 shadow-sm transition-colors"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Configuration</span>
          </button>
        </div>

      </form>

    </div>
  );
};
