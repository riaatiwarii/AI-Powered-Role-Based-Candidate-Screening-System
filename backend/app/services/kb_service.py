"""
Knowledge base service for managing the knowledge base.
"""

from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import KnowledgeBaseCRUD
from app.db.models import KnowledgeBaseChunk
from app.ml.rag_pipeline import RAGPipeline
from app.core.exceptions import KnowledgeBaseError
import uuid


class KnowledgeBaseService:
    """Service for knowledge base management."""

    def __init__(self, rag_pipeline: RAGPipeline):
        """
        Initialize KB service.

        Args:
            rag_pipeline: RAG pipeline instance
        """
        self.rag_pipeline = rag_pipeline

    async def ingest_chunks(
        self,
        db: AsyncSession,
        role: str,
        chunks: Dict[str, str],
        source: str = "default"
    ) -> List[KnowledgeBaseChunk]:
        """
        Ingest knowledge base chunks.

        Args:
            db: Database session
            role: Job role
            chunks: Dictionary of chunk_id to chunk_text
            source: Source document

        Returns:
            List of created chunks
        """
        try:
            created_chunks = []

            for chunk_text in chunks.values():
                chunk_id = str(uuid.uuid4())

                chunk = KnowledgeBaseChunk(
                    id=chunk_id,
                    role=role,
                    chunk_text=chunk_text,
                    source_document=source,
                    chunk_index=len(created_chunks),
                    embedding_stored=True
                )

                saved_chunk = await KnowledgeBaseCRUD.create(db, chunk)
                created_chunks.append(saved_chunk)

                # Add to RAG pipeline
                self.rag_pipeline.add_chunk(chunk_id, chunk_text)

            return created_chunks

        except Exception as e:
            raise KnowledgeBaseError(f"Failed to ingest chunks: {str(e)}")

    async def get_chunks_for_role(self, db: AsyncSession, role: str) -> List[KnowledgeBaseChunk]:
        """
        Get all chunks for a role.

        Args:
            db: Database session
            role: Job role

        Returns:
            List of chunks
        """
        return await KnowledgeBaseCRUD.get_by_role(db, role)

    async def rebuild_index_for_role(
        self,
        db: AsyncSession,
        role: str,
        rag_pipeline: RAGPipeline
    ):
        """
        Rebuild RAG index for a role.

        Args:
            db: Database session
            role: Job role
            rag_pipeline: RAG pipeline to update
        """
        try:
            chunks = await self.get_chunks_for_role(db, role)

            chunks_dict = {chunk.id: chunk.chunk_text for chunk in chunks}
            rag_pipeline.add_chunks_batch(chunks_dict)

        except Exception as e:
            raise KnowledgeBaseError(f"Failed to rebuild index: {str(e)}")
