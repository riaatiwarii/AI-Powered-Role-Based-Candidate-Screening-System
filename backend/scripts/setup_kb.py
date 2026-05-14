"""
Setup and seed knowledge base with role-specific content.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_settings
from app.core.constants import JobRole, ROLE_KB_MAPPING
from app.db.database import AsyncSessionLocal, init_db
from app.ml.embeddings import EmbeddingManager
from app.ml.rag_pipeline import RAGPipeline
from app.ml.vector_db import VectorDB
from app.services.kb_service import KnowledgeBaseService


async def setup_knowledge_base():
    """Initialize and setup the knowledge base."""
    print("🔧 Setting up knowledge base...")

    # Initialize database
    await init_db()
    print("✅ Database initialized")

    # Initialize ML components
    embedding_manager = EmbeddingManager()
    vector_db = VectorDB(dimension=embedding_manager.get_embedding_dimension())
    rag_pipeline = RAGPipeline(embedding_manager, vector_db)
    kb_service = KnowledgeBaseService(rag_pipeline)

    # Load knowledge base files
    kb_path = Path(__file__).parent.parent.parent / "knowledge_base"

    async with AsyncSessionLocal() as db:
        for role in JobRole:
            kb_file = kb_path / ROLE_KB_MAPPING[role]

            if kb_file.exists():
                print(f"📚 Loading knowledge base for {role.value}...")

                with open(kb_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Split into chunks
                chunks = _chunk_text(content, chunk_size=1000, overlap=200)
                chunks_dict = {f"chunk_{i}_{role.value}": chunk for i, chunk in enumerate(chunks)}

                # Ingest chunks
                await kb_service.ingest_chunks(
                    db=db,
                    role=role.value,
                    chunks=chunks_dict,
                    source=kb_file.name
                )

                print(f"✅ {len(chunks)} chunks ingested for {role.value}")
            else:
                print(f"⚠️  Knowledge base file not found: {kb_file}")

    print("✅ Knowledge base setup complete!")


def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """
    Split text into chunks with overlap.

    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks


async def seed_default_kb():
    """Seed default knowledge base content."""
    print("🌱 Seeding default knowledge base content...")

    async with AsyncSessionLocal() as db:
        # This would be called after setup if KB files don't exist
        pass


if __name__ == "__main__":
    asyncio.run(setup_knowledge_base())
