"""Configuration and constants for AI Tutor"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY")

# LLM Provider configuration
# Options: "gemini" (FREE), "openai" (paid), "groq" (FREE)
LLM_PROVIDER = "gemini"

# Model configuration
GPT_MODEL = "gpt-4"  # Fallback for OpenAI
GEMINI_MODEL = "gemini-2.5-flash"  # FREE, high quality
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# RAG configuration
CHROMA_COLLECTION = "ncert_chunks"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MAX_RETRIEVED_CHUNKS = 5

# Tutor configuration
CONFIDENCE_THRESHOLD_EASY = 0.7
CONFIDENCE_THRESHOLD_HARD = 0.4
DEFAULT_CONFIDENCE = 0.5
MAX_RESPONSE_LENGTH = 150  # words

# Supported languages
SUPPORTED_LANGUAGES = ["en", "hi", "te", "kn", "ml"]

# Curriculum structure
CLASSES = list(range(6, 11))  # 6-10
SUBJECTS = {
    "Mathematics": ["Algebra", "Geometry", "Numbers", "Ratios", "Arithmetic"],
    "Science": ["Physics", "Chemistry", "Biology"],
    "Social Science": ["Geography", "History", "Civics"]
}

# Paths
DATA_DIR = "data"
NCERT_PDF_DIR = os.path.join(DATA_DIR, "ncert_pdfs")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")

# Ensure directories exist
os.makedirs(NCERT_PDF_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
