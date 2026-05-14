"""
Zustand store for global state management.
"""

import { create } from 'zustand';
import * as types from '@/app/types';

interface InterviewStore {
  session: types.Session | null;
  currentQuestion: types.QuestionGenerateResponse | null;
  answers: types.Answer[];
  results: types.InterviewResults | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setSession: (session: types.Session) => void;
  setCurrentQuestion: (question: types.QuestionGenerateResponse) => void;
  addAnswer: (answer: types.Answer) => void;
  setResults: (results: types.InterviewResults) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  resetStore: () => void;
}

export const useInterviewStore = create<InterviewStore>((set) => ({
  session: null,
  currentQuestion: null,
  answers: [],
  results: null,
  isLoading: false,
  error: null,

  setSession: (session) => set({ session }),
  setCurrentQuestion: (question) => set({ currentQuestion: question }),
  addAnswer: (answer) => set((state) => ({ answers: [...state.answers, answer] })),
  setResults: (results) => set({ results }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  resetStore: () =>
    set({
      session: null,
      currentQuestion: null,
      answers: [],
      results: null,
      isLoading: false,
      error: null,
    }),
}));
