"""
Resume upload component.
"""

'use client';

import { useState } from 'react';
import { apiService } from '@/app/services/api';
import { useInterviewStore } from '@/app/hooks/useInterviewStore';
import * as types from '@/app/types';

interface ResumeUploadProps {
  sessionId: string;
  onUploadComplete: (analysis: types.ResumeAnalysis) => void;
}

export default function ResumeUpload({ sessionId, onUploadComplete }: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { setError: setStoreError } = useInterviewStore();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, TXT, or DOCX file');
        return;
      }
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const analysis = await apiService.uploadResume(sessionId, file);
      onUploadComplete(analysis);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to upload resume';
      setError(errorMsg);
      setStoreError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card max-w-md">
      <h2 className="text-xl font-bold mb-4">📄 Upload Your Resume</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Select Resume File (PDF, TXT, or DOCX)
        </label>
        <input
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={handleFileChange}
          className="input-field"
          disabled={isLoading}
        />
        {file && (
          <p className="text-sm text-gray-600 mt-2">
            Selected: <strong>{file.name}</strong>
          </p>
        )}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded error">
          {error}
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || isLoading}
        className="btn-primary w-full"
      >
        {isLoading ? 'Uploading...' : 'Upload Resume'}
      </button>
    </div>
  );
}
