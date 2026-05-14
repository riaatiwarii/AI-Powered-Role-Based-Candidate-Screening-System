"""
Custom exceptions for the application.
"""


class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ResumeProcessingError(AppException):
    """Raised when resume processing fails."""
    def __init__(self, message: str):
        super().__init__(message, "RESUME_PROCESSING_ERROR", 400)


class EmbeddingError(AppException):
    """Raised when embedding generation fails."""
    def __init__(self, message: str):
        super().__init__(message, "EMBEDDING_ERROR", 500)


class RetrievalError(AppException):
    """Raised when retrieval from vector DB fails."""
    def __init__(self, message: str):
        super().__init__(message, "RETRIEVAL_ERROR", 500)


class QuestionGenerationError(AppException):
    """Raised when question generation fails."""
    def __init__(self, message: str):
        super().__init__(message, "QUESTION_GENERATION_ERROR", 500)


class SessionError(AppException):
    """Raised when session operations fail."""
    def __init__(self, message: str):
        super().__init__(message, "SESSION_ERROR", 400)


class ValidationError(AppException):
    """Raised when validation fails."""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)


class NotFoundError(AppException):
    """Raised when resource not found."""
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", "NOT_FOUND", 404)


class KnowledgeBaseError(AppException):
    """Raised when knowledge base operations fail."""
    def __init__(self, message: str):
        super().__init__(message, "KNOWLEDGE_BASE_ERROR", 500)
