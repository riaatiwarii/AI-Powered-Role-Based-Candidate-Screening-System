"""
Interview session component.
"""

'use client';

import { useState, useEffect } from 'react';
import { apiService } from '@/app/services/api';
import { useInterviewStore } from '@/app/hooks/useInterviewStore';
import * as types from '@/app/types';

interface InterviewSessionProps {
  sessionId: string;
  maxQuestions?: number;
}

export default function InterviewSession({ sessionId, maxQuestions = 5 }: InterviewSessionProps) {
  const [question, setQuestion] = useState<types.QuestionGenerateResponse | null>(null);
  const [answer, setAnswer] = useState('');
  const [isLoadingQuestion, setIsLoadingQuestion] = useState(false);
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const { setCurrentQuestion } = useInterviewStore();

  useEffect(() => {
    loadNextQuestion();
  }, []);

  const loadNextQuestion = async () => {
    if (answeredCount >= maxQuestions) {
      setIsComplete(true);
      return;
    }

    setIsLoadingQuestion(true);
    setError(null);

    try {
      const newQuestion = await apiService.generateQuestion(sessionId);
      setQuestion(newQuestion);
      setCurrentQuestion(newQuestion);
      setAnswer('');
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to load question';
      setError(errorMsg);
    } finally {
      setIsLoadingQuestion(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || !question) {
      setError('Please enter an answer');
      return;
    }

    setIsSubmittingAnswer(true);
    setError(null);

    try {
      await apiService.submitAnswer(sessionId, question.question_id, answer);
      setAnsweredCount(answeredCount + 1);

      if (answeredCount + 1 >= maxQuestions) {
        setIsComplete(true);
      } else {
        await loadNextQuestion();
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'Failed to submit answer';
      setError(errorMsg);
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  if (isComplete) {
    return (
      <div className="card text-center">
        <h2 className="text-2xl font-bold mb-4 text-green-600">✅ Interview Complete!</h2>
        <p className="text-lg mb-4">
          You've answered <strong>{maxQuestions}</strong> questions
        </p>
        <p className="text-gray-600 mb-6">
          Thank you for your participation. Your responses have been recorded.
        </p>
      </div>
    );
  }

  if (isLoadingQuestion && !question) {
    return (
      <div className="card text-center">
        <div className="loading text-xl">Loading question...</div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-bold">
            Question {question?.question_number || 0} of {maxQuestions}
          </h2>
          <span className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
            Difficulty: {question?.difficulty || 'N/A'}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${(answeredCount / maxQuestions) * 100}%` }}
          />
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded error">
          {error}
        </div>
      )}

      {question && (
        <>
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-lg text-gray-800">{question.question_text}</p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Your Answer</label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here..."
              className="input-field min-h-32 resize-none"
              disabled={isSubmittingAnswer}
            />
            <p className="text-xs text-gray-500 mt-1">
              {answer.length} characters
            </p>
          </div>

          <button
            onClick={handleSubmitAnswer}
            disabled={!answer.trim() || isSubmittingAnswer}
            className="btn-primary w-full"
          >
            {isSubmittingAnswer ? 'Submitting...' : 'Submit Answer'}
          </button>
        </>
      )}
    </div>
  );
}
