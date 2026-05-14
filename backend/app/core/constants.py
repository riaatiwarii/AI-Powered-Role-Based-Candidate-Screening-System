"""
Application constants and enumerations.
"""

from enum import Enum


class JobRole(str, Enum):
    """Available job roles for interview."""
    BACKEND_ENGINEER = "backend_engineer"
    AI_ML_ENGINEER = "ai_ml_engineer"
    FRONTEND_ENGINEER = "frontend_engineer"
    FULLSTACK_ENGINEER = "fullstack_engineer"
    DATA_ENGINEER = "data_engineer"


class InterviewStatus(str, Enum):
    """Interview session status."""
    CREATED = "created"
    RESUME_UPLOADED = "resume_uploaded"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class QuestionDifficulty(str, Enum):
    """Question difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ResponseQuality(str, Enum):
    """Response quality assessment."""
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


# Role-specific knowledge base files
ROLE_KB_MAPPING = {
    JobRole.BACKEND_ENGINEER: "backend_engineer.md",
    JobRole.AI_ML_ENGINEER: "ai_ml_engineer.md",
    JobRole.FRONTEND_ENGINEER: "frontend_engineer.md",
    JobRole.FULLSTACK_ENGINEER: "fullstack_engineer.md",
    JobRole.DATA_ENGINEER: "data_engineer.md",
}

# Skills mapping for resume extraction
TECHNICAL_SKILLS = {
    "languages": [
        "python", "java", "javascript", "typescript", "c++", "golang", "rust",
        "php", "ruby", "scala", "kotlin", "swift", "csharp", "c#"
    ],
    "frameworks": [
        "django", "fastapi", "flask", "spring", "spring boot", "express",
        "react", "vue", "angular", "nextjs", "next.js", "nestjs",
        "tensorflow", "pytorch", "keras"
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "firebase"
    ],
    "devops": [
        "docker", "kubernetes", "jenkins", "gitlab", "github", "aws",
        "azure", "gcp", "terraform", "ansible"
    ],
    "ml_techniques": [
        "nlp", "computer vision", "deep learning", "machine learning",
        "transformers", "bert", "rag", "embeddings", "vector database"
    ]
}

# Default system prompts
SYSTEM_PROMPTS = {
    "question_generator": """You are an expert technical interviewer. Generate insightful, 
        role-specific interview questions that assess both conceptual understanding and practical 
        application. Questions should be grounded in the provided context and reflect the 
        candidate's background when available. Avoid generic questions.""",
    
    "resume_analyzer": """You are an expert at analyzing technical resumes. Extract key 
        information including skills, technologies, experience level, and domain expertise. 
        Focus on technical depth and relevant experience.""",
}
