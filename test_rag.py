"""Test RAG pipeline with sample queries"""

from rag.retriever import RAGRetriever

def test_retrieval():
    """Test querying the RAG pipeline"""
    retriever = RAGRetriever()

    # Test queries
    test_cases = [
        {
            "query": "What is a fraction?",
            "subject": "Mathematics",
            "class": 6
        },
        {
            "query": "Photosynthesis process",
            "subject": "Science",
            "class": 7
        },
        {
            "query": "Indian independence",
            "subject": "Social Science",
            "class": 8
        }
    ]

    for test in test_cases:
        print(f"\n🔍 Query: {test['query']}")
        print(f"   Subject: {test['subject']}, Class: {test['class']}")

        chunks = retriever.retrieve_context(
            query=test["query"],
            subject=test["subject"],
            class_level=test["class"],
            top_k=3
        )

        if chunks:
            print(f"   Found {len(chunks)} relevant chunks:")
            for i, chunk in enumerate(chunks, 1):
                print(f"   [{i}] (similarity: {chunk['similarity']:.2f})")
                print(f"       Chapter: {chunk['chapter']}")
                print(f"       {chunk['text'][:100]}...")
        else:
            print("   ❌ No chunks found (ensure RAG is initialized)")

if __name__ == "__main__":
    test_retrieval()
