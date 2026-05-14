"""
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.db.database import init_db, close_db
from app.ml.embeddings import EmbeddingManager
from app.ml.rag_pipeline import RAGPipeline
from app.ml.vector_db import VectorDB
from app.ml.question_generator import QuestionGenerator
from app.api.routes import upload, interview, session

settings = get_settings()

# Initialize ML components at module level
embedding_manager = EmbeddingManager()
vector_db = VectorDB(dimension=embedding_manager.get_embedding_dimension())
rag_pipeline = RAGPipeline(embedding_manager, vector_db)
question_generator = QuestionGenerator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Runs startup tasks and cleanup tasks.
    """
    # Startup
    print("🚀 Starting up the application...")
    await init_db()
    print("✅ Database initialized")
    print("✅ ML components loaded")

    yield

    # Shutdown
    print("🛑 Shutting down the application...")
    await close_db()
    print("✅ Database connections closed")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered role-based candidate screening system",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """Handle application-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle validation exceptions."""
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": exc.errors(),
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


# Include routers
app.include_router(upload.router)
app.include_router(interview.router)
app.include_router(session.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI-Powered Candidate Screening System",
        "version": settings.app_version,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
    )
