"""
Session service for general session management.
"""

from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import SessionCRUD, ResponseCRUD, MetricsCRUD
from app.db.models import Session, SessionMetrics
from app.core.exceptions import NotFoundError


class SessionService:
    """Service for session operations."""

    @staticmethod
    async def get_session_details(db: AsyncSession, session_id: str) -> Dict:
        """
        Get complete session details.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            Session details dictionary
        """
        session = await SessionCRUD.get(db, session_id)
        if not session:
            raise NotFoundError("Session")

        responses = await ResponseCRUD.get_by_session(db, session_id)
        metrics = await MetricsCRUD.get_by_session(db, session_id)

        return {
            "session": session,
            "responses": responses,
            "metrics": metrics,
            "question_count": len(session.questions),
            "answer_count": len(responses)
        }

    @staticmethod
    async def get_session_responses(db: AsyncSession, session_id: str) -> List[Dict]:
        """
        Get all responses for a session.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            List of Q&A pairs
        """
        session = await SessionCRUD.get(db, session_id)
        if not session:
            raise NotFoundError("Session")

        qa_pairs = []
        for question in session.questions:
            qa_pair = {
                "question_id": question.id,
                "question_text": question.question_text,
                "question_number": question.question_number,
                "difficulty": question.difficulty,
                "responses": []
            }

            # Find responses for this question
            for response in session.responses:
                if response.question_id == question.id:
                    qa_pair["responses"].append({
                        "response_id": response.id,
                        "response_text": response.response_text,
                        "quality_score": response.quality_score,
                        "feedback": response.feedback,
                        "submitted_at": response.submitted_at
                    })

            qa_pairs.append(qa_pair)

        return qa_pairs

    @staticmethod
    async def create_session_metrics(
        db: AsyncSession,
        session_id: str,
        **kwargs
    ) -> SessionMetrics:
        """
        Create or update session metrics.

        Args:
            db: Database session
            session_id: Session ID
            **kwargs: Metrics to set

        Returns:
            SessionMetrics object
        """
        existing = await MetricsCRUD.get_by_session(db, session_id)

        if existing:
            return await MetricsCRUD.update(db, session_id, **kwargs)
        else:
            metrics = SessionMetrics(
                id=f"metrics_{session_id}",
                session_id=session_id,
                **kwargs
            )
            return await MetricsCRUD.create(db, metrics)

    @staticmethod
    async def get_candidate_history(
        db: AsyncSession,
        email: str
    ) -> List[Session]:
        """
        Get interview history for a candidate.

        Args:
            db: Database session
            email: Candidate email

        Returns:
            List of sessions
        """
        return await SessionCRUD.get_by_email(db, email)
