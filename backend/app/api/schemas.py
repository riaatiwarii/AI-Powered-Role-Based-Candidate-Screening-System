"""
Pydantic schemas for API request/response validation.
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# ==================== Session Schemas ====================

class SessionCreate(BaseModel):
    """Create interview session request."""
    candidate_name: str = Field(..., min_length=1, max_length=100)
    candidate_email: Optional[EmailStr] = None
    role: str = Field(..., description="Job role for interview")


class SessionResponse(BaseModel):
    """Session response."""
    id: str
    candidate_name: str
    candidate_email: Optional[str]
    role: str
    status: str
    extracted_skills: Optional[Dict] = None
    experience_level: Optional[str] = None
    total_questions: int
    questions_answered: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Resume Schemas ====================

class ResumeUploadRequest(BaseModel):
    """Resume upload request."""
    session_id: str = Field(..., description="Session ID")
    filename: str = Field(..., description="Original filename")


class ResumeAnalysis(BaseModel):
    """Resume analysis result."""
    cleaned_text: str
    skills: Dict[str, List[str]]
    experience_level: str
    domains: List[str]
    skill_count: int
    domains_count: int


# ==================== Question Schemas ====================

class InterviewQuestion(BaseModel):
    """Interview question."""
    id: str
    session_id: str
    question_text: str
    question_number: int
    difficulty: Optional[str] = None
    context_sources: Optional[List[str]] = None
    generated_at: datetime

    class Config:
        from_attributes = True


class QuestionGenerateRequest(BaseModel):
    """Request to generate next question."""
    session_id: str = Field(..., description="Session ID")


class QuestionGenerateResponse(BaseModel):
    """Response with generated question."""
    question_id: str
    question_text: str
    question_number: int
    difficulty: str


# ==================== Response Schemas ====================

class CandidateAnswerSubmit(BaseModel):
    """Submit candidate answer."""
    session_id: str = Field(..., description="Session ID")
    question_id: str = Field(..., description="Question ID")
    answer_text: str = Field(..., min_length=1, description="Candidate's answer")


class AnswerResponse(BaseModel):
    """Response confirmation."""
    response_id: str
    session_id: str
    question_id: str
    submitted_at: datetime
    feedback: Optional[str] = None
    quality_score: Optional[float] = None

    class Config:
        from_attributes = True


# ==================== Results Schemas ====================

class SessionMetricsResponse(BaseModel):
    """Session performance metrics."""
    average_response_quality: Optional[float] = None
    technical_depth_score: Optional[float] = None
    communication_clarity_score: Optional[float] = None
    problem_solving_score: Optional[float] = None
    overall_score: Optional[float] = None
    recommendation: Optional[str] = None
    strengths: Optional[List[str]] = None
    areas_for_improvement: Optional[List[str]] = None

    class Config:
        from_attributes = True


class SessionSummary(BaseModel):
    """Complete session summary."""
    session: SessionResponse
    metrics: SessionMetricsResponse
    total_questions: int
    answered_questions: int
    session_duration_seconds: int


class InterviewResultsResponse(BaseModel):
    """Final interview results."""
    session_id: str
    candidate_name: str
    role: str
    status: str
    summary: SessionSummary
    questions_and_answers: List[Dict]  # List of Q&A pairs
    overall_assessment: str


# ==================== Role Schemas ====================

class AvailableRolesResponse(BaseModel):
    """Available job roles."""
    roles: List[str]
    total_count: int


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """Error response."""
    code: str
    message: str
    details: Optional[Dict] = None
