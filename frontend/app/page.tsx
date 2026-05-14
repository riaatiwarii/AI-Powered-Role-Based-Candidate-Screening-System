"""
Main page component.
"""

'use client';

import { useState, useEffect } from 'react';
import { useInterviewStore } from '@/app/hooks/useInterviewStore';
import { apiService } from '@/app/services/api';
import ResumeUpload from '@/app/components/ResumeUpload';
import RoleSelector from '@/app/components/RoleSelector';
import InterviewSession from '@/app/components/InterviewSession';
import ResultsView from '@/app/components/ResultsView';
import * as types from '@/app/types';

type PageState = 'initial' | 'resume' | 'interview' | 'results';

export default function HomePage() {
  const [pageState, setPageState] = useState<PageState>('initial');
  const [candidateName, setCandidateName] = useState('');
  const [selectedRole, setSelectedRole] = useState('');
  const [candidateEmail, setCandidateEmail] = useState('');
  const [resumeAnalysis, setResumeAnalysis] = useState<types.ResumeAnalysis | null>(null);
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { session, setSession, setError: setStoreError } = useInterviewStore();

  const handleCreateSession = async () => {
    if (!candidateName || !selectedRole) {
      setError('Please fill in all required fields');
      return;
    }

    setIsCreatingSession(true);
    setError(null);

    try {
      const newSession = await apiService.createSession(
        candidateName,
        selectedRole,
        candidateEmail
      );
      setSession(newSession);
      setPageState('resume');
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to create session';
      setError(errorMsg);
      setStoreError(errorMsg);
    } finally {
      setIsCreatingSession(false);
    }
  };

  const handleResumeUploadComplete = (analysis: types.ResumeAnalysis) => {
    setResumeAnalysis(analysis);
    setPageState('interview');
  };

  const handleInterviewComplete = () => {
    setPageState('results');
  };

  const handleStartOver = () => {
    setCandidateName('');
    setSelectedRole('');
    setCandidateEmail('');
    setResumeAnalysis(null);
    setPageState('initial');
  };

  // Initial state - Candidate entry
  if (pageState === 'initial') {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">🚀 AI-Powered Interview</h1>
          <p className="text-gray-600 text-lg">
            Get interviewed by an intelligent system tailored to your target role
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="text-xl font-bold mb-4">👤 Candidate Information</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Full Name *</label>
                <input
                  type="text"
                  value={candidateName}
                  onChange={(e) => setCandidateName(e.target.value)}
                  placeholder="John Doe"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Email (Optional)</label>
                <input
                  type="email"
                  value={candidateEmail}
                  onChange={(e) => setCandidateEmail(e.target.value)}
                  placeholder="john@example.com"
                  className="input-field"
                />
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded error">
                  {error}
                </div>
              )}

              <button
                onClick={handleCreateSession}
                disabled={isCreatingSession}
                className="btn-primary w-full"
              >
                {isCreatingSession ? 'Creating...' : 'Continue'}
              </button>
            </div>
          </div>

          <RoleSelector selectedRole={selectedRole} onRoleChange={setSelectedRole} />
        </div>
      </div>
    );
  }

  // Resume upload state
  if (pageState === 'resume' && session) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <button
            onClick={handleStartOver}
            className="text-blue-600 hover:text-blue-700 mb-4"
          >
            ← Start Over
          </button>
          <h1 className="text-3xl font-bold">📝 Upload Your Resume</h1>
          <p className="text-gray-600 mt-2">
            Candidate: <strong>{session.candidate_name}</strong> | Role:{' '}
            <strong>{session.role.replace(/_/g, ' ')}</strong>
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <ResumeUpload
            sessionId={session.id}
            onUploadComplete={handleResumeUploadComplete}
          />

          {resumeAnalysis && (
            <div className="card">
              <h2 className="text-lg font-bold mb-4">📊 Resume Analysis</h2>

              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Experience Level</p>
                  <p className="font-semibold capitalize">
                    {resumeAnalysis.experience_level}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-gray-600">Skills Found</p>
                  <p className="font-semibold">{resumeAnalysis.skill_count}</p>
                </div>

                {resumeAnalysis.domains.length > 0 && (
                  <div>
                    <p className="text-sm text-gray-600">Domains</p>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {resumeAnalysis.domains.map((domain) => (
                        <span
                          key={domain}
                          className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded"
                        >
                          {domain}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {resumeAnalysis.skills.languages.length > 0 && (
                  <div>
                    <p className="text-sm text-gray-600">Programming Languages</p>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {resumeAnalysis.skills.languages.slice(0, 5).map((lang) => (
                        <span
                          key={lang}
                          className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded"
                        >
                          {lang}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Interview state
  if (pageState === 'interview' && session && resumeAnalysis) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold">🎤 Interview Session</h1>
          <p className="text-gray-600 mt-2">
            {session.candidate_name} - {session.role.replace(/_/g, ' ')}
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <InterviewSession sessionId={session.id} maxQuestions={5} />
          </div>

          <div className="card">
            <h3 className="font-bold mb-3">Resume Info</h3>
            <div className="space-y-2 text-sm">
              <div>
                <p className="text-gray-600">Level</p>
                <p className="font-semibold capitalize">
                  {resumeAnalysis.experience_level}
                </p>
              </div>
              <div>
                <p className="text-gray-600">Skills</p>
                <p className="font-semibold">{resumeAnalysis.skill_count}</p>
              </div>
              <div>
                <p className="text-gray-600">Domains</p>
                <p className="font-semibold">{resumeAnalysis.domains_count}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Results state
  if (pageState === 'results' && session) {
    return (
      <div className="max-w-4xl mx-auto">
        <ResultsView sessionId={session.id} />
      </div>
    );
  }

  return null;
}
