export interface Project {
  id: number;
  display_number?: number;
  title: string;
  domain: string;
  department: string;
  institution: string;
  pi_name: string;
  pi_email: string;
  duration_weeks: number;
  requested_budget: number;
  currency: string;
  objectives: string;
  funding_preferences?: string;
  status: string;
  created_at: string;
  updated_at: string;
  documents?: ProjectDocument[];
}

export interface ProjectDocument {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
}

export interface ResearcherMetrics {
  total_projects: number;
  active_projects: number;
  funding_opportunities_discovered: number;
  proposals_generated: number;
  pending_compliance_checks: number;
  total_estimated_budget: number;
  recent_activities: Array<{
    id: number;
    agent: string;
    action: string;
    project_id: number;
    timestamp: string;
  }>;
}

export interface LabCard {
  lab_number: number;
  title: string;
  concept: string;
  responsible_agent: string;
  expected_output_focus: string;
  status: string;
  evaluation_status: string;
  is_completed: boolean;
  executed_at?: string;
  expected_output_summary?: any;
}

export interface TeacherOverview {
  selected_project_id: number;
  selected_project_display_number?: number;
  available_projects: Array<{
    id: number;
    display_number?: number;
    title: string;
    institution: string;
    pi: string;
  }>;
  total_labs: number;
  completed_labs: number;
  passed_evaluations: number;
  labs: LabCard[];
}
