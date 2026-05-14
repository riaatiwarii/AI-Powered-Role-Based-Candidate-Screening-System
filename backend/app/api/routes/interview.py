"""
Interview routes for question generation and answer submission.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.interview_service import InterviewService
from app.api.schemas import (
    QuestionGenerateRequest,
    QuestionGenerateResponse,
    CandidateAnswerSubmit,
    AnswerResponse
)
from app.core.exceptions import SessionError, AppException

router = APIRouter(prefix="/api/interview", tags=["interview"])


async def get_interview_service(db: AsyncSession = Depends(get_db)) -> InterviewService:
    """Get interview service instance."""
    from app.main import rag_pipeline, question_generator
    return InterviewService(rag_pipeline, question_generator)


@router.post("/question", response_model=QuestionGenerateResponse)
async def generate_question(
    request: QuestionGenerateRequest,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> QuestionGenerateResponse:
    """
    Generate next interview question.

    Args:
        request: Question generation request
        db: Database session
        interview_service: Interview service

    Returns:
        Generated question
    """
    try:
        question = await interview_service.generate_next_question(
            db=db,
            session_id=request.session_id
        )

        return QuestionGenerateResponse(
            question_id=question.id,
            question_text=question.question_text,
            question_number=question.question_number,
            difficulty=question.difficulty or "medium"
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    request: CandidateAnswerSubmit,
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> AnswerResponse:
    """
    Submit candidate answer.

    Args:
        request: Answer submission request
        db: Database session
        interview_service: Interview service

    Returns:
        Answer confirmation
    """
    try:
        response = await interview_service.submit_answer(
            db=db,
            session_id=request.session_id,
            question_id=request.question_id,
            answer_text=request.answer_text
        )

        return AnswerResponse(
            response_id=response.id,
            session_id=response.session_id,
            question_id=response.question_id,
            submitted_at=response.submitted_at,
            feedback=response.feedback,
            quality_score=response.quality_score
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")
