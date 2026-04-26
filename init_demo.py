"""Initialize RAG with demo data (no real PDFs needed)"""

from rag.embedder import EmbeddingManager

def create_demo_collection():
    """Create demo ChromaDB collection for testing"""
    
    demo_chunks = [
        {
            "text": "Photosynthesis is the process by which plants use sunlight, water and carbon dioxide to create oxygen and energy in the form of glucose. It happens in the leaves of plants during the day.",
            "subject": "Science",
            "class": "7",
            "chapter": "Life Processes",
            "source": "demo_science_7.pdf"
        },
        {
            "text": "A fraction is a part of a whole. It is written as a ratio of two numbers separated by a line. The top number is the numerator and the bottom number is the denominator.",
            "subject": "Mathematics",
            "class": "6",
            "chapter": "Fractions",
            "source": "demo_math_6.pdf"
        },
        {
            "text": "India is a large country in South Asia. It has 28 states and 8 union territories. The capital is New Delhi. It is the second most populous country.",
            "subject": "Social Science",
            "class": "6",
            "chapter": "Our Country",
            "source": "demo_social_6.pdf"
        }
    ]
    
    embedder = EmbeddingManager()
    embedder.embed_chunks(demo_chunks)
    
    print("✅ Demo collection created!")
    print("   Try: 'What is photosynthesis?'")

if __name__ == "__main__":
    create_demo_collection()
