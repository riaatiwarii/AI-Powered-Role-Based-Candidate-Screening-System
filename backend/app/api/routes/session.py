"""
Session routes for session management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.services.interview_service import InterviewService
from app.services.session_service import SessionService
from app.api.schemas import (
    SessionCreate,
    SessionResponse,
    InterviewResultsResponse,
    AvailableRolesResponse
)
from app.core.constants import JobRole
from app.core.exceptions import AppException

router = APIRouter(prefix="/api/session", tags=["session"])


async def get_interview_service(db: AsyncSession = Depends(get_db)) -> InterviewService:
    """Get interview service instance."""
    from app.main import rag_pipeline, question_generator
    return InterviewService(rag_pipeline, question_generator)


@router.get("/roles", response_model=AvailableRolesResponse)
async def get_available_roles() -> AvailableRolesResponse:
    """Get available job roles."""
    roles = [role.value for role in JobRole]
    return AvailableRolesResponse(roles=roles, total_count=len(roles))


@router.post("/create", response_model=SessionResponse)
async def create_session(
    request: SessionCreate,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> SessionResponse:
    """
    Create new interview session.

    Args:
        request: Session creation request
        db: Database session
        interview_service: Interview service

    Returns:
        Created session
    """
    try:
        session = await interview_service.create_session(
            db=db,
            candidate_name=request.candidate_name,
            role=request.role,
            candidate_email=request.candidate_email
        )

        return SessionResponse(
            id=session.id,
            candidate_name=session.candidate_name,
            candidate_email=session.candidate_email,
            role=session.role,
            status=session.status,
            extracted_skills=session.extracted_skills,
            experience_level=session.experience_level,
            total_questions=session.total_questions,
            questions_answered=session.questions_answered,
            created_at=session.created_at,
            completed_at=session.completed_at
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> SessionResponse:
    """
    Get session details.

    Args:
        session_id: Session ID
        db: Database session
        interview_service: Interview service

    Returns:
        Session details
    """
    try:
        session = await interview_service.get_session(db=db, session_id=session_id)

        return SessionResponse(
            id=session.id,
            candidate_name=session.candidate_name,
            candidate_email=session.candidate_email,
            role=session.role,
            status=session.status,
            extracted_skills=session.extracted_skills,
            experience_level=session.experience_level,
            total_questions=session.total_questions,
            questions_answered=session.questions_answered,
            created_at=session.created_at,
            completed_at=session.completed_at
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")


@router.post("/{session_id}/complete")
async def complete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
):
    """
    Complete interview session.

    Args:
        session_id: Session ID
        db: Database session
        interview_service: Interview service
    """
    try:
        session = await interview_service.complete_session(db=db, session_id=session_id)
        return {"status": "completed", "session_id": session.id}
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete session: {str(e)}")


@router.get("/{session_id}/results", response_model=InterviewResultsResponse)
async def get_interview_results(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> InterviewResultsResponse:
    """
    Get interview results.

    Args:
        session_id: Session ID
        db: Database session
        interview_service: Interview service

    Returns:
        Interview results
    """
    try:
        session = await interview_service.get_session(db=db, session_id=session_id)
        qa_pairs = await SessionService.get_session_responses(db=db, session_id=session_id)
        metrics = await SessionService.get_candidate_history(db=db, email=session.candidate_email or "")

        return InterviewResultsResponse(
            session_id=session.id,
            candidate_name=session.candidate_name,
            role=session.role,
            status=session.status,
            summary={},  # To be enhanced
            questions_and_answers=qa_pairs,
            overall_assessment="Interview completed successfully"
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get results: {str(e)}")
