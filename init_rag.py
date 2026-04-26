"""Initialize RAG pipeline - Load PDFs, embed, store in ChromaDB"""

import sys
from rag.loader import load_ncert
from rag.embedder import EmbeddingManager
from rag.retriever import RAGRetriever
from config import NCERT_PDF_DIR

def initialize_rag():
    """Load NCERT PDFs, embed, and store in ChromaDB"""
    print("🚀 Initializing RAG pipeline...")
    print(f"📁 Looking for PDFs in: {NCERT_PDF_DIR}")

    # Step 1: Load and chunk PDFs
    chunks = load_ncert(NCERT_PDF_DIR)

    if not chunks:
        print("❌ No chunks loaded. Make sure PDFs are in data/ncert_pdfs/")
        print("📥 Download from: https://ncert.nic.in")
        return False

    # Step 2: Embed chunks and store
    embedder = EmbeddingManager()
    embedder.embed_chunks(chunks)

    # Step 3: Verify
    retriever = RAGRetriever()
    stats = retriever.get_collection_stats()
    print(f"📊 Collection stats: {stats}")

    print("✅ RAG pipeline initialized successfully!")
    return True

if __name__ == "__main__":
    success = initialize_rag()
    sys.exit(0 if success else 1)
