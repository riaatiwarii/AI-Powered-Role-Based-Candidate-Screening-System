"""
Interview service for managing interview sessions and flow.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import SessionCRUD, QuestionCRUD, ResponseCRUD, MetricsCRUD
from app.db.models import Session, InterviewQuestion, CandidateResponse, SessionMetrics
from app.core.constants import InterviewStatus, JobRole
from app.core.exceptions import SessionError, NotFoundError
from app.ml.rag_pipeline import RAGPipeline
from app.ml.question_generator import QuestionGenerator


class InterviewService:
    """Service for interview session management."""

    def __init__(self, rag_pipeline: RAGPipeline, question_generator: QuestionGenerator):
        """
        Initialize interview service.

        Args:
            rag_pipeline: RAG pipeline instance
            question_generator: Question generator instance
        """
        self.rag_pipeline = rag_pipeline
        self.question_generator = question_generator

    async def create_session(
        self,
        db: AsyncSession,
        candidate_name: str,
        role: str,
        candidate_email: Optional[str] = None
    ) -> Session:
        """
        Create a new interview session.

        Args:
            db: Database session
            candidate_name: Candidate name
            role: Target job role
            candidate_email: Candidate email (optional)

        Returns:
            Created session

        Raises:
            SessionError: If session creation fails
        """
        try:
            session_id = str(uuid.uuid4())

            session = Session(
                id=session_id,
                candidate_name=candidate_name,
                candidate_email=candidate_email,
                role=role,
                status=InterviewStatus.CREATED.value
            )

            return await SessionCRUD.create(db, session)
        except Exception as e:
            raise SessionError(f"Failed to create session: {str(e)}")

    async def get_session(self, db: AsyncSession, session_id: str) -> Session:
        """
        Get session by ID.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            Session object

        Raises:
            NotFoundError: If session not found
        """
        session = await SessionCRUD.get(db, session_id)
        if not session:
            raise NotFoundError("Session")
        return session

    async def update_session_resume(
        self,
        db: AsyncSession,
        session_id: str,
        resume_text: str,
        extracted_skills: Dict,
        experience_level: str
    ) -> Session:
        """
        Update session with resume information.

        Args:
            db: Database session
            session_id: Session ID
            resume_text: Processed resume text
            extracted_skills: Extracted skills
            experience_level: Experience level

        Returns:
            Updated session
        """
        return await SessionCRUD.update(
            db,
            session_id,
            resume_text=resume_text,
            extracted_skills=extracted_skills,
            experience_level=experience_level,
            status=InterviewStatus.RESUME_UPLOADED.value
        )

    async def generate_next_question(
        self,
        db: AsyncSession,
        session_id: str
    ) -> InterviewQuestion:
        """
        Generate the next interview question.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            Generated question

        Raises:
            SessionError: If generation fails
        """
        try:
            session = await self.get_session(db, session_id)

            if not session.resume_text:
                raise SessionError("Resume must be uploaded before generating questions")

            # Get question number
            question_number = session.total_questions + 1

            # Build resume info for question generation
            resume_info = {
                "experience_level": session.experience_level,
                "key_skills": list(session.extracted_skills.get("languages", []))[:5] if session.extracted_skills else [],
                "domains": session.extracted_skills.get("domains", []) if session.extracted_skills else []
            }

            # Retrieve context for question generation
            query = self._build_query(session, resume_info)
            retrieved_chunks = self.rag_pipeline.retrieve(query, k=5)

            if not retrieved_chunks:
                raise SessionError("No relevant context found for question generation")

            context = self.rag_pipeline.build_context(query, retrieved_chunks)

            # Generate question
            question_text = self.question_generator.generate_question(
                context=context,
                resume_info=resume_info,
                role=session.role,
                difficulty="medium",
                previous_questions=[]
            )

            # Save question
            question_id = str(uuid.uuid4())
            question = InterviewQuestion(
                id=question_id,
                session_id=session_id,
                question_text=question_text,
                question_number=question_number,
                difficulty="medium",
                retrieval_context=[chunk["content"][:100] for chunk in retrieved_chunks],
                context_sources=[chunk["chunk_id"] for chunk in retrieved_chunks]
            )

            saved_question = await QuestionCRUD.create(db, question)

            # Update session
            await SessionCRUD.update(db, session_id, total_questions=question_number)

            return saved_question

        except SessionError:
            raise
        except Exception as e:
            raise SessionError(f"Failed to generate question: {str(e)}")

    async def submit_answer(
        self,
        db: AsyncSession,
        session_id: str,
        question_id: str,
        answer_text: str
    ) -> CandidateResponse:
        """
        Submit candidate answer.

        Args:
            db: Database session
            session_id: Session ID
            question_id: Question ID
            answer_text: Answer text

        Returns:
            Response object
        """
        try:
            # Verify session and question
            session = await self.get_session(db, session_id)
            question = await QuestionCRUD.get(db, question_id)

            if not question or question.session_id != session_id:
                raise NotFoundError("Question")

            # Create response
            response_id = str(uuid.uuid4())
            response = CandidateResponse(
                id=response_id,
                session_id=session_id,
                question_id=question_id,
                response_text=answer_text
            )

            saved_response = await ResponseCRUD.create(db, response)

            # Update session
            await SessionCRUD.update(
                db,
                session_id,
                questions_answered=session.questions_answered + 1,
                status=InterviewStatus.IN_PROGRESS.value
            )

            return saved_response

        except Exception as e:
            raise SessionError(f"Failed to submit answer: {str(e)}")

    async def complete_session(
        self,
        db: AsyncSession,
        session_id: str
    ) -> Session:
        """
        Mark session as completed.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            Updated session
        """
        return await SessionCRUD.update(
            db,
            session_id,
            status=InterviewStatus.COMPLETED.value,
            completed_at=datetime.utcnow()
        )

    def _build_query(self, session: Session, resume_info: Dict) -> str:
        """
        Build query for RAG retrieval.

        Args:
            session: Session object
            resume_info: Resume information

        Returns:
            Query string
        """
        parts = [
            f"Role: {session.role}",
            f"Skills: {', '.join(resume_info.get('key_skills', []))}",
            f"Experience: {session.experience_level}"
        ]

        return " ".join(parts)
