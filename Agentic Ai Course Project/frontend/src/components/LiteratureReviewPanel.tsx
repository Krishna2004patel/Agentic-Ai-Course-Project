import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Upload, 
  FileText, 
  Play, 
  RotateCw, 
  CheckCircle2, 
  AlertTriangle, 
  Database, 
  Layers, 
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Send,
  Sparkles,
  Info
} from 'lucide-react';
import { api } from '../services/api';

interface LiteratureReviewPanelProps {
  projectId: number;
  onSyncProposal?: () => void;
}

export const LiteratureReviewPanel: React.FC<LiteratureReviewPanelProps> = ({
  projectId,
  onSyncProposal
}) => {
  const [data, setData] = useState<any>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [executing, setExecuting] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);
  const [syncingProposal, setSyncingProposal] = useState<boolean>(false);
  const [showTrace, setShowTrace] = useState<boolean>(false);

  useEffect(() => {
    loadData();
  }, [projectId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [litRes, docsRes] = await Promise.all([
        api.getLiteratureReview(projectId),
        api.getProjectDocuments(projectId)
      ]);
      setData(litRes);
      setDocuments(docsRes || []);
    } catch (e) {
      console.error('Failed to load literature review data:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async () => {
    try {
      setExecuting(true);
      const res = await api.runLiteratureReview(projectId);
      setData(res);
      const docsRes = await api.getProjectDocuments(projectId);
      setDocuments(docsRes || []);
      alert('Literature Review Agent executed: semantic chunking, TF-IDF vector retrieval, and prior-art matrix synthesized.');
    } catch (e: any) {
      alert(`Literature review execution error: ${e.message}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pdf' && ext !== 'docx' && ext !== 'txt') {
      alert('Supported file formats for research papers are PDF, DOCX, and TXT.');
      return;
    }

    try {
      setUploading(true);
      await api.uploadDocument(projectId, file);
      alert(`Paper '${file.name}' uploaded successfully. Running Literature Review Agent on updated corpus...`);
      await handleExecute();
    } catch (e: any) {
      alert(`Upload error: ${e.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleTransferToProposal = async () => {
    try {
      setSyncingProposal(true);
      await api.runProposalDrafting(projectId);
      if (onSyncProposal) onSyncProposal();
      alert('Literature review findings, extracted research gaps, and evidence citations successfully transferred to Proposal Drafting Agent (Agent C).');
    } catch (e: any) {
      alert(`Transfer error: ${e.message}`);
    } finally {
      setSyncingProposal(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 text-xs font-bold bg-purple-700 text-white rounded">
              Agent B Implementation
            </span>
            <h1 className="text-xl font-bold text-slate-900">
              Literature Review & Semantic RAG Agent
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
            Extracts claims, evidence, and limitations from uploaded PDF/DOCX research papers, splits documents into semantic chunks, indexes with TF-IDF vector retrieval, and synthesizes a comparative prior-art matrix.
          </p>
          <p className="text-xs text-slate-800 font-semibold mt-1">
            Research Topic: <span className="text-purple-900">{data?.topic || 'AI-based early disease detection'}</span>
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={handleExecute}
            disabled={executing || uploading}
            className="bg-purple-700 hover:bg-purple-800 text-white font-medium py-2 px-3.5 rounded-lg text-xs flex items-center space-x-1.5 shadow-sm transition-colors disabled:opacity-50"
          >
            {executing ? (
              <>
                <RotateCw className="w-3.5 h-3.5 animate-spin" />
                <span>Extracting & Chunking...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
                <span>Execute Literature Review</span>
              </>
            )}
          </button>

          <button
            onClick={handleTransferToProposal}
            disabled={syncingProposal || executing}
            className="bg-slate-900 hover:bg-slate-800 text-white font-medium py-2 px-3.5 rounded-lg text-xs flex items-center space-x-1.5 shadow-sm transition-colors disabled:opacity-50"
          >
            {syncingProposal ? (
              <>
                <RotateCw className="w-3.5 h-3.5 animate-spin" />
                <span>Syncing with Agent C...</span>
              </>
            ) : (
              <>
                <Send className="w-3.5 h-3.5 text-amber-400" />
                <span>Transfer to Proposal Drafting (Agent C)</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Upload & Ingestion Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        {/* Upload Box */}
        <div className="bg-white rounded-xl border border-dashed border-purple-300 p-5 shadow-2xs text-center flex flex-col items-center justify-center space-y-3 bg-purple-50/20">
          <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-700">
            <Upload className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900">Upload Research Papers (PDF / DOCX)</h3>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Files are automatically parsed by DocumentReaderTool and indexed into TF-IDF vector memory
            </p>
          </div>
          <label className="cursor-pointer bg-purple-700 hover:bg-purple-800 text-white text-xs font-medium py-1.5 px-4 rounded-lg shadow-xs transition-colors">
            {uploading ? 'Processing File...' : 'Choose Research Paper'}
            <input 
              type="file" 
              accept=".pdf,.docx,.doc,.txt" 
              onChange={handleFileUpload} 
              disabled={uploading}
              className="hidden" 
            />
          </label>
        </div>

        {/* Uploaded Documents List */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs md:col-span-2 space-y-2.5">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-900 flex items-center space-x-1.5">
              <FileText className="w-4 h-4 text-purple-600" />
              <span>Project Research Documents ({documents.length} Files Ingested)</span>
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-50 text-purple-700 border border-purple-200">
              {data?.chunks_indexed || 0} Semantic Chunks Vectorized
            </span>
          </div>

          {documents.length === 0 ? (
            <div className="p-6 text-center text-slate-500 text-xs bg-slate-50 rounded-lg border border-slate-100">
              <p className="font-semibold">No local research papers uploaded yet.</p>
              <p className="text-[11px] text-slate-400 mt-1">Upload a PDF or DOCX research paper above to perform local RAG extraction.</p>
            </div>
          ) : (
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {documents.map((doc: any) => (
                <div key={doc.id} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                  <div className="flex items-center space-x-2.5 truncate">
                    <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold font-mono ${
                      doc.file_type === 'pdf' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                    }`}>
                      {doc.file_type?.toUpperCase()}
                    </span>
                    <span className="font-semibold text-slate-800 truncate" title={doc.filename}>
                      {doc.filename}
                    </span>
                  </div>
                  <div className="flex items-center space-x-3 text-[11px] text-slate-500 shrink-0">
                    <span>{(doc.file_size / 1024).toFixed(1)} KB</span>
                    <span className="text-emerald-700 font-medium">✓ Parsed</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>

      {/* Extracted Paper Information Cards */}
      {data?.extracted_paper_information && data.extracted_paper_information.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-1.5">
            <BookOpen className="w-4 h-4 text-purple-600" />
            <span>Extracted Paper Metadata & Scope</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.extracted_paper_information.map((paper: any, idx: number) => (
              <div key={idx} className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs space-y-2">
                <div className="flex items-start justify-between">
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-100 text-purple-800">
                    PAPER #{idx + 1} • {paper.file_type}
                  </span>
                  <span className="text-xs font-mono text-slate-500">{paper.publication_year}</span>
                </div>
                <h3 className="text-xs font-bold text-slate-900 line-clamp-2">
                  {paper.title}
                </h3>
                <p className="text-[11px] text-slate-600">
                  <strong className="text-slate-700">Authors:</strong> {paper.authors}
                </p>
                <div className="text-[10px] font-mono text-slate-500 pt-1 border-t border-slate-100 flex items-center justify-between">
                  <span>Source File: {paper.filename}</span>
                  <span>{paper.character_count?.toLocaleString()} chars</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Comparative Literature Matrix */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden space-y-2">
        <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-1.5">
            <Layers className="w-4 h-4 text-purple-600" />
            <span>Comparative Literature & Prior-Art Matrix</span>
          </h2>
          <span className="text-xs text-slate-500">
            {data?.paper_comparison_matrix?.length || 0} Sources Analyzed
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="bg-slate-100/70 text-slate-700 text-[11px] font-bold uppercase">
              <tr>
                <th className="p-3 border-b">Research Source</th>
                <th className="p-3 border-b">Authors & Year</th>
                <th className="p-3 border-b">Methodological Approach</th>
                <th className="p-3 border-b">Key Findings / Evidence</th>
                <th className="p-3 border-b">Documented Limitations</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data?.paper_comparison_matrix?.map((row: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                  <td className="p-3 font-semibold text-slate-900">
                    <span className="block">{row.source}</span>
                    <span className="text-[10px] text-purple-700 font-mono font-normal">{row.type}</span>
                  </td>
                  <td className="p-3 text-slate-600 whitespace-nowrap">
                    <div>{row.authors}</div>
                    <div className="text-[10px] text-slate-400">({row.year})</div>
                  </td>
                  <td className="p-3 text-slate-700 leading-relaxed">{row.methodological_approach}</td>
                  <td className="p-3 text-emerald-800 font-medium leading-relaxed bg-emerald-50/30">
                    {row.key_findings}
                  </td>
                  <td className="p-3 text-amber-800 leading-relaxed bg-amber-50/30">
                    {row.limitations}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Research Gaps & Limitations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        {/* Identified Research Gaps */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
          <div className="flex items-center space-x-2 text-rose-700">
            <AlertTriangle className="w-4 h-4" />
            <h3 className="text-sm font-bold">Identified Empirical Research Gaps</h3>
          </div>
          <p className="text-xs text-slate-500">
            Explicit unaddressed challenges isolated across the reviewed academic corpus:
          </p>
          <div className="space-y-2">
            {data?.research_gaps?.map((gap: string, idx: number) => (
              <div key={idx} className="p-2.5 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-950 leading-relaxed font-medium">
                {gap}
              </div>
            ))}
          </div>
        </div>

        {/* Retrieved Evidence Passages (TF-IDF Vector Chunks) */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-purple-700">
              <Database className="w-4 h-4" />
              <h3 className="text-sm font-bold">Top Retrieved Evidence Chunks</h3>
            </div>
            <span className="text-[10px] font-mono text-slate-500">TF-IDF Vector Cosine Similarity</span>
          </div>
          <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
            {data?.retrieved_evidence?.map((chunk: any, idx: number) => (
              <div key={idx} className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1">
                <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
                  <span className="font-bold text-slate-700">{chunk.chunk_id || `CHUNK #${idx + 1}`} ({chunk.doc_title})</span>
                  <span className="text-purple-700 font-bold">Sim: {chunk.similarity_score}</span>
                </div>
                <p className="text-slate-700 text-[11px] leading-relaxed">
                  "{chunk.snippet || chunk.text}"
                </p>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Structured Literature Synthesis */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
        <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-1.5">
          <FileText className="w-4 h-4 text-purple-600" />
          <span>Structured Academic Literature Review Synthesis</span>
        </h2>
        <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line font-sans">
          {data?.literature_synthesis}
        </div>
      </div>

      {/* References & Citations */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
        <h2 className="text-sm font-bold text-slate-900">Source References & Academic Citations</h2>
        <div className="divide-y divide-slate-100 text-xs">
          {data?.source_references?.map((ref: any, idx: number) => (
            <div key={idx} className="py-2.5 flex items-start justify-between gap-3">
              <div>
                <span className="font-bold text-slate-900">[{idx + 1}] {ref.authors} ({ref.year}). </span>
                <span className="text-slate-800 font-medium">"{ref.title}". </span>
                <span className="text-slate-500 font-mono text-[11px]">{ref.doi_or_url}</span>
              </div>
              <span className="px-2 py-0.5 rounded text-[9px] font-bold font-mono bg-slate-100 text-slate-600 shrink-0">
                {ref.source_type}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Execution Trace Toggle */}
      {data?.execution_trace && (
        <div className="bg-slate-900 text-slate-300 rounded-xl p-4 text-xs font-mono">
          <button
            onClick={() => setShowTrace(!showTrace)}
            className="w-full flex items-center justify-between text-slate-300 hover:text-white"
          >
            <span>Agent B Execution Trace ({data.execution_trace.length} Steps Recorded)</span>
            {showTrace ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
          {showTrace && (
            <div className="mt-3 space-y-1.5 border-t border-slate-800 pt-3">
              {data.execution_trace.map((step: any, idx: number) => (
                <div key={idx} className="flex items-start space-x-2 text-[11px]">
                  <span className="text-emerald-400 select-none">›</span>
                  <span className="font-bold text-slate-200">{step.step}:</span>
                  <span className="text-slate-400">{step.detail}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
};
