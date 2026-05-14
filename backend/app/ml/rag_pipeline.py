"""
RAG (Retrieval-Augmented Generation) pipeline implementation.
"""

import re
from typing import List, Dict, Optional
from app.ml.embeddings import EmbeddingManager
from app.ml.vector_db import VectorDB
from app.core.config import get_settings
from app.core.exceptions import RetrievalError

settings = get_settings()


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(self, embedding_manager: EmbeddingManager, vector_db: VectorDB):
        """
        Initialize RAG pipeline.

        Args:
            embedding_manager: Embedding manager instance
            vector_db: Vector database instance
        """
        self.embedding_manager = embedding_manager
        self.vector_db = vector_db
        self.chunk_store = {}  # Store chunks by ID for reference

    def add_chunk(self, chunk_id: str, chunk_text: str):
        """
        Add a chunk to the retrieval system.

        Args:
            chunk_id: Unique chunk identifier
            chunk_text: Chunk content
        """
        self.chunk_store[chunk_id] = chunk_text
        embedding = self.embedding_manager.generate_embedding(chunk_text)
        self.vector_db.add_embeddings(embedding.reshape(1, -1), [chunk_id])

    def add_chunks_batch(self, chunks: Dict[str, str]):
        """
        Add multiple chunks to the retrieval system.

        Args:
            chunks: Dictionary mapping chunk_id to chunk_text
        """
        if not chunks:
            return

        chunk_ids = list(chunks.keys())
        chunk_texts = list(chunks.values())

        # Store chunks
        self.chunk_store.update(chunks)

        # Generate embeddings
        embeddings = self.embedding_manager.generate_embeddings_batch(chunk_texts)

        # Add to vector DB
        self.vector_db.add_embeddings(embeddings, chunk_ids)

    def retrieve(self, query: str, k: int = 5, threshold: float = 0.0) -> List[Dict]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: Query text
            k: Number of results to return
            threshold: Minimum similarity threshold

        Returns:
            List of retrieved chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_manager.generate_embedding(query)

            # Search
            results = self.vector_db.search(query_embedding, k=k)

            # Filter by threshold and format
            retrieved_chunks = []
            for chunk_id, similarity in results:
                if similarity >= threshold:
                    chunk_text = self.chunk_store.get(chunk_id, "")
                    retrieved_chunks.append({
                        "chunk_id": chunk_id,
                        "content": chunk_text,
                        "similarity": similarity,
                        "rank": len(retrieved_chunks) + 1
                    })

            return retrieved_chunks
        except Exception as e:
            raise RetrievalError(f"Retrieval failed: {str(e)}")

    def build_context(self, query: str, retrieved_chunks: List[Dict], max_length: int = 2000) -> str:
        """
        Build context string from retrieved chunks.

        Args:
            query: Original query
            retrieved_chunks: Retrieved chunks
            max_length: Maximum context length

        Returns:
            Formatted context string
        """
        context_parts = [f"Query: {query}\n\nRelevant Context:\n"]

        total_length = len(context_parts[0])
        for chunk in retrieved_chunks:
            chunk_text = f"\n[Source: {chunk['chunk_id']}]\n{chunk['content']}\n"
            if total_length + len(chunk_text) <= max_length:
                context_parts.append(chunk_text)
                total_length += len(chunk_text)
            else:
                break

        return "".join(context_parts)

    def get_chunk(self, chunk_id: str) -> Optional[str]:
        """Get a specific chunk by ID."""
        return self.chunk_store.get(chunk_id)

    def clear(self):
        """Clear all stored data."""
        self.chunk_store.clear()
        self.vector_db = VectorDB(self.embedding_manager.get_embedding_dimension())
