"""
Database models for the application.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Session(Base):
    """Interview session model."""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    candidate_name = Column(String, nullable=False)
    candidate_email = Column(String, nullable=True)
    role = Column(String, nullable=False, index=True)
    
    # Resume data
    resume_text = Column(Text, nullable=True)
    extracted_skills = Column(JSON, nullable=True)  # List of extracted skills
    experience_level = Column(String, nullable=True)
    
    # Session tracking
    status = Column(String, default="created", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Session metadata
    total_questions = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    session_duration_seconds = Column(Integer, default=0)
    
    # Relationships
    questions = relationship("InterviewQuestion", back_populates="session", cascade="all, delete-orphan")
    responses = relationship("CandidateResponse", back_populates="session", cascade="all, delete-orphan")
    metrics = relationship("SessionMetrics", back_populates="session", uselist=False, cascade="all, delete-orphan")


class InterviewQuestion(Base):
    """Interview question model."""
    __tablename__ = "interview_questions"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    
    # Question content
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=True)  # easy, medium, hard
    
    # RAG context
    retrieval_context = Column(JSON, nullable=True)  # Retrieved chunks used to generate question
    context_sources = Column(JSON, nullable=True)  # Source documents/chunks
    
    # Question generation metadata
    generated_at = Column(DateTime, default=datetime.utcnow)
    generation_prompt = Column(Text, nullable=True)  # For traceability
    
    # Relationships
    session = relationship("Session", back_populates="questions")
    responses = relationship("CandidateResponse", back_populates="question", cascade="all, delete-orphan")


class CandidateResponse(Base):
    """Candidate response model."""
    __tablename__ = "candidate_responses"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    question_id = Column(String, ForeignKey("interview_questions.id"), nullable=False, index=True)
    
    # Response content
    response_text = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Response analysis
    quality_score = Column(Float, nullable=True)  # 0-1
    quality_assessment = Column(String, nullable=True)  # poor, fair, good, excellent
    feedback = Column(Text, nullable=True)
    key_insights = Column(JSON, nullable=True)  # List of insights from response
    
    # Relationships
    session = relationship("Session", back_populates="responses")
    question = relationship("InterviewQuestion", back_populates="responses")


class SessionMetrics(Base):
    """Session performance metrics model."""
    __tablename__ = "session_metrics"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, unique=True, index=True)
    
    # Metrics
    average_response_quality = Column(Float, nullable=True)
    technical_depth_score = Column(Float, nullable=True)  # 0-1
    communication_clarity_score = Column(Float, nullable=True)  # 0-1
    problem_solving_score = Column(Float, nullable=True)  # 0-1
    
    # Overall assessment
    overall_score = Column(Float, nullable=True)  # 0-1
    recommendation = Column(String, nullable=True)  # strong_yes, yes, maybe, no
    strengths = Column(JSON, nullable=True)  # List of strengths
    areas_for_improvement = Column(JSON, nullable=True)  # List of areas
    
    # Calculations timestamp
    calculated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="metrics")


class KnowledgeBaseChunk(Base):
    """Knowledge base chunks for RAG."""
    __tablename__ = "kb_chunks"

    id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False, index=True)
    
    # Chunk content
    chunk_text = Column(Text, nullable=False)
    source_document = Column(String, nullable=False)  # File name or source
    chunk_index = Column(Integer, nullable=False)  # Position in document
    
    # Metadata
    topics = Column(JSON, nullable=True)  # List of topics covered
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Embedding (stored as text for FAISS compatibility)
    embedding_stored = Column(Boolean, default=False, index=True)
