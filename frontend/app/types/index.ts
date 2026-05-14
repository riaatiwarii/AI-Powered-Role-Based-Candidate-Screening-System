"""
Frontend types and interfaces.
"""

export interface Session {
  id: string;
  candidate_name: string;
  candidate_email?: string;
  role: string;
  status: string;
  extracted_skills?: Record<string, string[]>;
  experience_level?: string;
  total_questions: number;
  questions_answered: number;
  created_at: string;
  completed_at?: string;
}

export interface ResumeAnalysis {
  cleaned_text: string;
  skills: Record<string, string[]>;
  experience_level: string;
  domains: string[];
  skill_count: number;
  domains_count: number;
}

export interface Question {
  id: string;
  session_id: string;
  question_text: string;
  question_number: number;
  difficulty: string;
  context_sources?: string[];
  generated_at: string;
}

export interface QuestionGenerateResponse {
  question_id: string;
  question_text: string;
  question_number: number;
  difficulty: string;
}

export interface Answer {
  response_id: string;
  session_id: string;
  question_id: string;
  submitted_at: string;
  feedback?: string;
  quality_score?: number;
}

export interface SessionMetrics {
  average_response_quality?: number;
  technical_depth_score?: number;
  communication_clarity_score?: number;
  problem_solving_score?: number;
  overall_score?: number;
  recommendation?: string;
  strengths?: string[];
  areas_for_improvement?: string[];
}

export interface InterviewResults {
  session_id: string;
  candidate_name: string;
  role: string;
  status: string;
  summary: Record<string, any>;
  questions_and_answers: Array<{
    question_id: string;
    question_text: string;
    question_number: number;
    difficulty: string;
    responses: Array<{
      response_id: string;
      response_text: string;
      quality_score?: number;
      feedback?: string;
      submitted_at: string;
    }>;
  }>;
  overall_assessment: string;
}

export interface AvailableRoles {
  roles: string[];
  total_count: number;
}
