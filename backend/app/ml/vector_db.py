"""
Vector database wrapper for FAISS (could be extended for other vector DBs).
"""

import os
import pickle
import numpy as np
from typing import List, Tuple, Optional
import faiss
from app.core.config import get_settings
from app.core.exceptions import RetrievalError

settings = get_settings()


class VectorDB:
    """Vector database wrapper using FAISS."""

    def __init__(self, dimension: int = 384):
        """
        Initialize vector database.

        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        self.index = None
        self.id_mapping = {}  # Map internal IDs to chunk IDs
        self.next_id = 0

    def create_index(self):
        """Create a new FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)

    def add_embeddings(self, embeddings: np.ndarray, chunk_ids: List[str]):
        """
        Add embeddings to the index.

        Args:
            embeddings: Array of embeddings (n_embeddings, dimension)
            chunk_ids: List of chunk IDs
        """
        if self.index is None:
            self.create_index()

        if embeddings.shape[0] != len(chunk_ids):
            raise RetrievalError("Mismatch between embeddings and chunk IDs")

        # Convert to float32 for FAISS
        embeddings = np.asarray(embeddings, dtype=np.float32)

        self.index.add(embeddings)
        for chunk_id in chunk_ids:
            self.id_mapping[self.next_id] = chunk_id
            self.next_id += 1

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for similar embeddings.

        Args:
            query_embedding: Query embedding
            k: Number of results to return

        Returns:
            List of (chunk_id, similarity_score) tuples
        """
        if self.index is None or self.index.ntotal == 0:
            raise RetrievalError("Index is empty")

        query_embedding = np.asarray([query_embedding], dtype=np.float32)

        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < 0:  # Invalid index from FAISS
                continue
            chunk_id = self.id_mapping.get(int(idx))
            if chunk_id:
                # Convert L2 distance to similarity (higher is better)
                similarity = 1 / (1 + distance)
                results.append((chunk_id, float(similarity)))

        return results

    def save(self, path: str):
        """Save index to disk."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if self.index:
            faiss.write_index(self.index, path + ".faiss")
        with open(path + ".pkl", "wb") as f:
            pickle.dump(self.id_mapping, f)

    def load(self, path: str):
        """Load index from disk."""
        try:
            self.index = faiss.read_index(path + ".faiss")
            with open(path + ".pkl", "rb") as f:
                self.id_mapping = pickle.load(f)
            self.next_id = len(self.id_mapping)
        except Exception as e:
            raise RetrievalError(f"Failed to load index: {str(e)}")

    def get_ntotal(self) -> int:
        """Get number of embeddings in index."""
        return self.index.ntotal if self.index else 0
