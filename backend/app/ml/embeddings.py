"""
Embeddings module for generating and managing embeddings.
"""

import os
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import get_settings
from app.core.exceptions import EmbeddingError

settings = get_settings()


class EmbeddingManager:
    """Manage embeddings generation and operations."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding manager.

        Args:
            model_name: Sentence transformer model name
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            raise EmbeddingError(f"Failed to load embedding model: {str(e)}")

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as numpy array

        Raises:
            EmbeddingError: If embedding generation fails
        """
        if not text or not isinstance(text, str):
            raise EmbeddingError("Invalid text for embedding")

        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding / np.linalg.norm(embedding)  # Normalize
        except Exception as e:
            raise EmbeddingError(f"Embedding generation failed: {str(e)}")

    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            Matrix of embeddings (n_texts, embedding_dim)

        Raises:
            EmbeddingError: If batch embedding fails
        """
        if not texts:
            raise EmbeddingError("Empty text list for batch embedding")

        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            # Normalize embeddings
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            normalized = embeddings / norms
            return normalized
        except Exception as e:
            raise EmbeddingError(f"Batch embedding generation failed: {str(e)}")

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding
            embedding2: Second embedding

        Returns:
            Similarity score (0-1)
        """
        return float(np.dot(embedding1, embedding2))

    def similarity_batch(self, query_embedding: np.ndarray, embeddings_matrix: np.ndarray) -> np.ndarray:
        """
        Calculate similarity between query and multiple embeddings.

        Args:
            query_embedding: Query embedding
            embeddings_matrix: Matrix of embeddings

        Returns:
            Array of similarity scores
        """
        return np.dot(embeddings_matrix, query_embedding)

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension."""
        return self.embedding_dim
