import { Project, ResearcherMetrics, TeacherOverview } from '../types';

const BASE_URL = '/api/v1';

async function request<T = any>(url: string, options: RequestInit = {}, actionName: string = 'request'): Promise<T> {
  const res = await fetch(url, options);
  const contentType = res.headers.get('content-type') || '';

  if (!res.ok) {
    let errorDetail = `Server returned HTTP ${res.status} (${res.statusText || 'Error'})`;
    let parsedBody: any = null;

    if (contentType.includes('application/json')) {
      try {
        parsedBody = await res.json();
        if (typeof parsedBody === 'object' && parsedBody !== null) {
          errorDetail = parsedBody.detail?.message 
            || (typeof parsedBody.detail === 'string' ? parsedBody.detail : null)
            || parsedBody.message 
            || parsedBody.error 
            || (parsedBody.detail ? JSON.stringify(parsedBody.detail) : null)
            || JSON.stringify(parsedBody);
        }
      } catch (jsonErr) {
        console.error(`[API Error] Failed to parse JSON error for ${actionName}:`, jsonErr);
      }
    } else {
      try {
        const textBody = await res.text();
        if (textBody && textBody.trim().length > 0) {
          const cleanText = textBody.replace(/<[^>]+>/g, '').trim();
          errorDetail = cleanText.slice(0, 300);
        }
      } catch (textErr) {
        console.error(`[API Error] Failed to read text error for ${actionName}:`, textErr);
      }
    }

    console.error(`[API Diagnostic] ${actionName} failed:`, {
      url,
      status: res.status,
      statusText: res.statusText,
      contentType,
      detail: errorDetail,
      rawBody: parsedBody
    });

    throw new Error(`Failed to ${actionName}: ${errorDetail}`);
  }

  if (contentType.includes('application/json')) {
    try {
      return await res.json();
    } catch (parseErr) {
      console.error(`[API Diagnostic] Expected JSON but parsing failed for ${actionName}:`, parseErr);
      throw new Error(`Invalid response format from server during ${actionName}.`);
    }
  }

  return (await res.text()) as unknown as T;
}

export const api = {
  // System Status
  async getSystemStatus() {
    return request(`${BASE_URL}/system/status`, {}, 'fetch system status');
  },

  // Projects
  async getProjects(): Promise<Project[]> {
    return request<Project[]>(`${BASE_URL}/projects`, {}, 'fetch projects');
  },

  async getProject(id: number): Promise<Project> {
    return request<Project>(`${BASE_URL}/projects/${id}`, {}, 'fetch project');
  },

  async createProject(data: Partial<Project>): Promise<Project> {
    return request<Project>(
      `${BASE_URL}/projects`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      },
      'create project'
    );
  },

  async updateProject(id: number, data: Partial<Project>): Promise<Project> {
    return request<Project>(
      `${BASE_URL}/projects/${id}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      },
      'update project'
    );
  },

  async deleteProject(id: number): Promise<{ message: string }> {
    return request<{ message: string }>(
      `${BASE_URL}/projects/${id}`,
      { method: 'DELETE' },
      'delete project'
    );
  },

  async uploadDocument(projectId: number, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return request(
      `${BASE_URL}/projects/${projectId}/documents`,
      {
        method: 'POST',
        body: formData
      },
      'upload document'
    );
  },

  async getProjectDocuments(projectId: number) {
    return request(`${BASE_URL}/projects/${projectId}/documents`, {}, 'fetch project documents');
  },

  // 4 Main Expected Outputs
  async getProjectExpectedOutputs(projectId: number) {
    return request(`${BASE_URL}/projects/${projectId}/expected-outputs`, {}, 'fetch expected outputs');
  },

  async updateProposal(projectId: number, data: any) {
    return request(
      `${BASE_URL}/projects/${projectId}/proposal`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      },
      'update proposal'
    );
  },

  async recalculateBudget(projectId: number, payload: any) {
    return request(
      `${BASE_URL}/projects/${projectId}/recalculate-budget`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      },
      'recalculate budget'
    );
  },

  async generateAllOutputs(projectId: number) {
    return request(
      `${BASE_URL}/projects/${projectId}/generate-all-outputs`,
      { method: 'POST' },
      'generate all expected outputs'
    );
  },

  // Researcher Metrics
  async getResearcherMetrics(): Promise<ResearcherMetrics> {
    return request<ResearcherMetrics>(`${BASE_URL}/researcher/metrics`, {}, 'fetch researcher metrics');
  },

  // Teacher Overview & Labs
  async getTeacherOverview(projectId?: number): Promise<TeacherOverview> {
    const url = projectId ? `${BASE_URL}/teacher/overview?project_id=${projectId}` : `${BASE_URL}/teacher/overview`;
    return request<TeacherOverview>(url, {}, 'fetch teacher overview');
  },

  async getLabDetail(labNumber: number, projectId: number) {
    return request(`${BASE_URL}/labs/${labNumber}/${projectId}`, {}, `fetch Lab ${labNumber} details`);
  },

  async executeLab(labNumber: number, projectId: number, feedback?: string) {
    const url = feedback 
      ? `${BASE_URL}/labs/${labNumber}/execute/${projectId}?feedback=${encodeURIComponent(feedback)}`
      : `${BASE_URL}/labs/${labNumber}/execute/${projectId}`;
    return request(url, { method: 'POST' }, `execute Lab ${labNumber}`);
  },

  async executeAllLabs(projectId: number) {
    return request(
      `${BASE_URL}/labs/execute-all/${projectId}`,
      { method: 'POST' },
      'execute all 14 labs'
    );
  },

  // Specialized Agents
  async runFundingDiscovery(projectId: number) {
    return request(
      `${BASE_URL}/agents/funding-discovery/${projectId}`,
      { method: 'POST' },
      'execute Funding Discovery Agent'
    );
  },

  async runLiteratureReview(projectId: number) {
    return request(
      `${BASE_URL}/agents/literature-review/${projectId}`,
      { method: 'POST' },
      'execute Literature Review Agent'
    );
  },

  async getLiteratureReview(projectId: number) {
    return request(
      `${BASE_URL}/agents/literature-review/${projectId}`,
      {},
      'fetch literature review data'
    );
  },

  async runProposalDrafting(projectId: number, feedback?: string) {
    return request(
      `${BASE_URL}/agents/proposal-drafting/${projectId}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback: feedback || '' })
      },
      'execute Proposal Drafting Agent'
    );
  },

  async runBudgetPlanning(projectId: number, overrideBudget?: number) {
    return request(
      `${BASE_URL}/agents/budget-planning/${projectId}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ override_budget: overrideBudget || null })
      },
      'execute Budget Planning Agent'
    );
  },

  async runComplianceChecking(projectId: number) {
    return request(
      `${BASE_URL}/agents/compliance-checking/${projectId}`,
      { method: 'POST' },
      'execute Compliance Checking Agent'
    );
  },

  async prepareSubmission(projectId: number) {
    return request(
      `${BASE_URL}/agents/submission/${projectId}/prepare`,
      { method: 'POST' },
      'prepare submission package'
    );
  },

  async requestHumanApproval(projectId: number) {
    return request(
      `${BASE_URL}/agents/submission/${projectId}/request-approval`,
      { method: 'POST' },
      'request human approval'
    );
  },

  async decideApproval(projectId: number, approvalId: number, approverName: string, decision: 'APPROVED' | 'REJECTED', comments: string) {
    return request(
      `${BASE_URL}/agents/submission/${projectId}/decide`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approval_id: approvalId,
          approver_name: approverName,
          decision,
          comments
        })
      },
      'record approval decision'
    );
  },

  async runFullLifecycle(projectId: number) {
    return request(
      `${BASE_URL}/agents/orchestrate-full/${projectId}`,
      { method: 'POST' },
      'orchestrate all six specialized agents'
    );
  },

  async getAgentsStatus(projectId: number) {
    return request(
      `${BASE_URL}/agents/status/${projectId}`,
      {},
      'fetch agents status'
    );
  },

  async getAuditLogs(projectId?: number) {
    const url = projectId ? `${BASE_URL}/researcher/audit-logs?project_id=${projectId}` : `${BASE_URL}/researcher/audit-logs`;
    return request(url, {}, 'fetch audit logs');
  },

  getDownloadUrl(projectId: number, fileType: 'json' | 'markdown' | 'md') {
    return `${BASE_URL}/researcher/download-dossier/${projectId}/${fileType}`;
  }
};
