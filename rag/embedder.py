"""Embed NCERT chunks using sentence-transformers"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os

from config import CHROMA_COLLECTION, CHROMA_DB_DIR, EMBEDDING_MODEL


class EmbeddingManager:
    """Manage embeddings and ChromaDB storage"""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = None

    def get_or_create_collection(self) -> chromadb.Collection:
        """Get or create ChromaDB collection for NCERT chunks"""
        if self.collection is None:
            self.collection = self.client.get_or_create_collection(
                name=CHROMA_COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
        return self.collection

    def embed_chunks(self, chunks: List[Dict]) -> None:
        """
        Embed chunks and store in ChromaDB.

        Args:
            chunks: List of dicts with keys: text, subject, class, chapter, source
        """
        if not chunks:
            print("⚠️  No chunks to embed")
            return

        collection = self.get_or_create_collection()

        print(f"🧠 Embedding {len(chunks)} chunks...")

        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True)

        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        documents = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{chunk['source']}_{i}"
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({
                "subject": chunk["subject"],
                "class": str(chunk["class"]),
                "chapter": chunk["chapter"],
                "source": chunk["source"]
            })

        # Add to ChromaDB
        collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas
        )

        print(f"✅ Stored {len(chunks)} chunks in ChromaDB")

    def clear_collection(self) -> None:
        """Clear all data from collection (use with caution)"""
        collection = self.get_or_create_collection()
        collection.delete(where={})  # Delete all
        print("🗑️  Collection cleared")
