"""Retrieve relevant NCERT chunks for queries"""

from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict

from config import CHROMA_COLLECTION, CHROMA_DB_DIR, EMBEDDING_MODEL, MAX_RETRIEVED_CHUNKS


class RAGRetriever:
    """Retrieve relevant NCERT chunks for a query"""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.client.get_collection(name=CHROMA_COLLECTION)

    def retrieve_context(
        self,
        query: str,
        subject: str,
        class_level: int,
        top_k: int = MAX_RETRIEVED_CHUNKS
    ) -> List[Dict]:
        """
        Retrieve top-k relevant chunks for a query with subject/class filtering.

        Args:
            query: Student's question or topic
            subject: Subject (e.g., "Mathematics")
            class_level: Class (6-10)
            top_k: Number of chunks to retrieve

        Returns:
            List of relevant chunks with scores
        """
        # Embed the query
        query_embedding = self.model.encode(query)

        # Build where filter for subject and class
        where_filter = {
            "$and": [
                {"subject": subject},
                {"class": str(class_level)}
            ]
        }

        try:
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )

            # Format results
            chunks = []
            if results["documents"] and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    distance = results["distances"][0][i]
                    # Convert distance to similarity score (1 - distance for cosine)
                    similarity = 1 - distance

                    chunks.append({
                        "text": doc,
                        "subject": metadata["subject"],
                        "class": metadata["class"],
                        "chapter": metadata["chapter"],
                        "source": metadata["source"],
                        "similarity": similarity
                    })

            return chunks

        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return []

    def retrieve_by_chapter(
        self,
        subject: str,
        class_level: int,
        chapter: str,
        top_k: int = MAX_RETRIEVED_CHUNKS
    ) -> List[Dict]:
        """
        Retrieve all chunks from a specific chapter.

        Args:
            subject: Subject
            class_level: Class
            chapter: Chapter name
            top_k: Max chunks to return

        Returns:
            List of chunks from the chapter
        """
        where_filter = {
            "$and": [
                {"subject": subject},
                {"class": str(class_level)},
                {"chapter": chapter}
            ]
        }

        try:
            results = self.collection.get(
                where=where_filter,
                limit=top_k,
                include=["documents", "metadatas"]
            )

            chunks = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"]):
                    metadata = results["metadatas"][i]
                    chunks.append({
                        "text": doc,
                        "subject": metadata["subject"],
                        "class": metadata["class"],
                        "chapter": metadata["chapter"],
                        "source": metadata["source"]
                    })

            return chunks

        except Exception as e:
            print(f"❌ Error retrieving chapter: {e}")
            return []

    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            data = self.collection.get(limit=1, include=[])
            return {
                "total_chunks": count,
                "collection_name": CHROMA_COLLECTION,
                "embedding_model": EMBEDDING_MODEL
            }
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}
