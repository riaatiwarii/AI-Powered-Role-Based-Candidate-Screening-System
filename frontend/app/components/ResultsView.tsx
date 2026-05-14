"""
Results view component.
"""

'use client';

import { useEffect, useState } from 'react';
import { apiService } from '@/app/services/api';
import * as types from '@/app/types';

interface ResultsViewProps {
  sessionId: string;
}

export default function ResultsView({ sessionId }: ResultsViewProps) {
  const [results, setResults] = useState<types.InterviewResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [sessionId]);

  const loadResults = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await apiService.getResults(sessionId);
      setResults(data);
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to load results';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="card text-center loading">Loading results...</div>;
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!results) {
    return <div className="card">No results found</div>;
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">📊 Interview Results</h2>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <p className="text-sm text-gray-600">Candidate</p>
            <p className="text-lg font-semibold">{results.candidate_name}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Role</p>
            <p className="text-lg font-semibold capitalize">{results.role.replace(/_/g, ' ')}</p>
          </div>
        </div>

        <div className="p-4 bg-blue-50 rounded-lg mb-6">
          <p className="text-gray-800">{results.overall_assessment}</p>
        </div>

        <div className="border-t pt-4">
          <p className="text-sm text-gray-600">Status</p>
          <p className="text-lg font-semibold capitalize">{results.status}</p>
        </div>
      </div>

      <div className="card">
        <h3 className="text-xl font-bold mb-4">📋 Q&A Summary</h3>

        <div className="space-y-4">
          {results.questions_and_answers.map((qa, index) => (
            <div key={qa.question_id} className="border rounded-lg p-4">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-semibold">Question {qa.question_number}</h4>
                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                  {qa.difficulty}
                </span>
              </div>

              <p className="text-gray-700 mb-3">{qa.question_text}</p>

              {qa.responses.map((resp) => (
                <div key={resp.response_id} className="bg-gray-50 p-3 rounded">
                  <p className="text-gray-800 mb-2">{resp.response_text}</p>
                  <div className="flex justify-between text-xs text-gray-600">
                    <span>
                      {resp.quality_score && `Quality: ${(resp.quality_score * 100).toFixed(0)}%`}
                    </span>
                    <span>{new Date(resp.submitted_at).toLocaleString()}</span>
                  </div>
                  {resp.feedback && (
                    <p className="text-sm text-blue-600 mt-2">💡 {resp.feedback}</p>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={() => window.location.href = '/'}
        className="btn-primary w-full"
      >
        Start New Interview
      </button>
    </div>
  );
}
