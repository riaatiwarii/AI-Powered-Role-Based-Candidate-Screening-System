"""
CRUD operations for database models.
"""

from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Session, InterviewQuestion, CandidateResponse, SessionMetrics, KnowledgeBaseChunk


class SessionCRUD:
    """CRUD operations for Session."""

    @staticmethod
    async def create(db: AsyncSession, session: Session) -> Session:
        """Create a new session."""
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get(db: AsyncSession, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        result = await db.execute(select(Session).where(Session.id == session_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> List[Session]:
        """Get sessions by candidate email."""
        result = await db.execute(
            select(Session).where(Session.candidate_email == email).order_by(desc(Session.created_at))
        )
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, session_id: str, **kwargs) -> Optional[Session]:
        """Update session."""
        result = await db.execute(select(Session).where(Session.id == session_id))
        session = result.scalars().first()
        if session:
            for key, value in kwargs.items():
                setattr(session, key, value)
            await db.commit()
            await db.refresh(session)
        return session

    @staticmethod
    async def delete(db: AsyncSession, session_id: str) -> bool:
        """Delete session."""
        result = await db.execute(select(Session).where(Session.id == session_id))
        session = result.scalars().first()
        if session:
            await db.delete(session)
            await db.commit()
            return True
        return False


class QuestionCRUD:
    """CRUD operations for InterviewQuestion."""

    @staticmethod
    async def create(db: AsyncSession, question: InterviewQuestion) -> InterviewQuestion:
        """Create a new question."""
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question

    @staticmethod
    async def get(db: AsyncSession, question_id: str) -> Optional[InterviewQuestion]:
        """Get question by ID."""
        result = await db.execute(select(InterviewQuestion).where(InterviewQuestion.id == question_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_session(db: AsyncSession, session_id: str) -> List[InterviewQuestion]:
        """Get all questions for a session."""
        result = await db.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_number)
        )
        return result.scalars().all()


class ResponseCRUD:
    """CRUD operations for CandidateResponse."""

    @staticmethod
    async def create(db: AsyncSession, response: CandidateResponse) -> CandidateResponse:
        """Create a new response."""
        db.add(response)
        await db.commit()
        await db.refresh(response)
        return response

    @staticmethod
    async def get(db: AsyncSession, response_id: str) -> Optional[CandidateResponse]:
        """Get response by ID."""
        result = await db.execute(select(CandidateResponse).where(CandidateResponse.id == response_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_session(db: AsyncSession, session_id: str) -> List[CandidateResponse]:
        """Get all responses for a session."""
        result = await db.execute(
            select(CandidateResponse)
            .where(CandidateResponse.session_id == session_id)
            .order_by(CandidateResponse.submitted_at)
        )
        return result.scalars().all()


class MetricsCRUD:
    """CRUD operations for SessionMetrics."""

    @staticmethod
    async def create(db: AsyncSession, metrics: SessionMetrics) -> SessionMetrics:
        """Create session metrics."""
        db.add(metrics)
        await db.commit()
        await db.refresh(metrics)
        return metrics

    @staticmethod
    async def get_by_session(db: AsyncSession, session_id: str) -> Optional[SessionMetrics]:
        """Get metrics for a session."""
        result = await db.execute(
            select(SessionMetrics).where(SessionMetrics.session_id == session_id)
        )
        return result.scalars().first()

    @staticmethod
    async def update(db: AsyncSession, session_id: str, **kwargs) -> Optional[SessionMetrics]:
        """Update session metrics."""
        result = await db.execute(
            select(SessionMetrics).where(SessionMetrics.session_id == session_id)
        )
        metrics = result.scalars().first()
        if metrics:
            for key, value in kwargs.items():
                setattr(metrics, key, value)
            await db.commit()
            await db.refresh(metrics)
        return metrics


class KnowledgeBaseCRUD:
    """CRUD operations for KnowledgeBaseChunk."""

    @staticmethod
    async def create(db: AsyncSession, chunk: KnowledgeBaseChunk) -> KnowledgeBaseChunk:
        """Create a knowledge base chunk."""
        db.add(chunk)
        await db.commit()
        await db.refresh(chunk)
        return chunk

    @staticmethod
    async def get_by_role(db: AsyncSession, role: str) -> List[KnowledgeBaseChunk]:
        """Get all chunks for a role."""
        result = await db.execute(
            select(KnowledgeBaseChunk).where(KnowledgeBaseChunk.role == role)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_role_stored(db: AsyncSession, role: str) -> List[KnowledgeBaseChunk]:
        """Get all chunks with stored embeddings for a role."""
        result = await db.execute(
            select(KnowledgeBaseChunk)
            .where((KnowledgeBaseChunk.role == role) & (KnowledgeBaseChunk.embedding_stored == True))
        )
        return result.scalars().all()
