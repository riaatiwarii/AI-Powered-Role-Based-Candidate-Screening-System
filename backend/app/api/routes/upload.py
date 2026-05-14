"""
Upload routes for resume handling.
"""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import PyPDF2
import io

from app.db.database import get_db
from app.ml.resume_processor import ResumeProcessor
from app.services.interview_service import InterviewService
from app.api.schemas import ResumeUploadRequest, ResumeAnalysis
from app.core.exceptions import ResumeProcessingError
from app.ml.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/api/upload", tags=["upload"])

# Initialize processors
resume_processor = ResumeProcessor()


async def get_interview_service(db: AsyncSession = Depends(get_db)) -> InterviewService:
    """Get interview service instance."""
    # This should be injected from main app
    from app.main import rag_pipeline, question_generator
    return InterviewService(rag_pipeline, question_generator)


@router.post("/resume")
async def upload_resume(
    session_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    interview_service: InterviewService = Depends(get_interview_service)
) -> ResumeAnalysis:
    """
    Upload and process resume.

    Args:
        session_id: Interview session ID
        file: Resume file (PDF or text)
        db: Database session
        interview_service: Interview service

    Returns:
        Resume analysis result
    """
    try:
        # Read file
        content = await file.read()

        # Extract text based on file type
        if file.filename.endswith(".pdf"):
            text = _extract_pdf_text(content)
        elif file.filename.endswith(".txt"):
            text = content.decode("utf-8")
        elif file.filename.endswith(".docx"):
            text = _extract_docx_text(content)
        else:
            raise ResumeProcessingError("Unsupported file format")

        # Analyze resume
        analysis = resume_processor.analyze_resume(text)

        # Update session with resume info
        await interview_service.update_session_resume(
            db=db,
            session_id=session_id,
            resume_text=analysis["cleaned_text"],
            extracted_skills=analysis["skills"],
            experience_level=analysis["experience_level"]
        )

        return ResumeAnalysis(**analysis)

    except ResumeProcessingError:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume processing failed: {str(e)}")


def _extract_pdf_text(content: bytes) -> str:
    """Extract text from PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ResumeProcessingError(f"PDF extraction failed: {str(e)}")


def _extract_docx_text(content: bytes) -> str:
    """Extract text from DOCX."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise ResumeProcessingError(f"DOCX extraction failed: {str(e)}")
