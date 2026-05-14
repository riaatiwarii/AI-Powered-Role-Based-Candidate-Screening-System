"""
API service for frontend-backend communication.
"""

import axios, { AxiosInstance } from 'axios';
import * as types from '@/app/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Session endpoints
  async createSession(candidateName: string, role: string, candidateEmail?: string): Promise<types.Session> {
    const response = await this.client.post('/api/session/create', {
      candidate_name: candidateName,
      role,
      candidate_email: candidateEmail,
    });
    return response.data;
  }

  async getSession(sessionId: string): Promise<types.Session> {
    const response = await this.client.get(`/api/session/${sessionId}`);
    return response.data;
  }

  async completeSession(sessionId: string): Promise<{ status: string; session_id: string }> {
    const response = await this.client.post(`/api/session/${sessionId}/complete`);
    return response.data;
  }

  async getResults(sessionId: string): Promise<types.InterviewResults> {
    const response = await this.client.get(`/api/session/${sessionId}/results`);
    return response.data;
  }

  async getAvailableRoles(): Promise<types.AvailableRoles> {
    const response = await this.client.get('/api/session/roles');
    return response.data;
  }

  // Resume endpoints
  async uploadResume(sessionId: string, file: File): Promise<types.ResumeAnalysis> {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('file', file);
    formData.append('filename', file.name);

    const response = await this.client.post('/api/upload/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Interview endpoints
  async generateQuestion(sessionId: string): Promise<types.QuestionGenerateResponse> {
    const response = await this.client.post('/api/interview/question', {
      session_id: sessionId,
    });
    return response.data;
  }

  async submitAnswer(sessionId: string, questionId: string, answerText: string): Promise<types.Answer> {
    const response = await this.client.post('/api/interview/answer', {
      session_id: sessionId,
      question_id: questionId,
      answer_text: answerText,
    });
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiService = new ApiService();
