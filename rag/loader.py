"""Load and chunk NCERT PDFs"""

import os
import re
from pathlib import Path
from pypdf import PdfReader
from typing import List, Dict

def load_ncert(pdf_dir: str) -> List[Dict]:
    """
    Load all NCERT PDFs from directory and chunk them.
    Returns list of chunks with metadata (subject, class, chapter, text).
    """
    if not os.path.exists(pdf_dir):
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    all_chunks = []
    pdf_files = list(Path(pdf_dir).glob("*.pdf"))

    if not pdf_files:
        print(f"⚠️  No PDFs found in {pdf_dir}")
        return []

    print(f"📚 Loading {len(pdf_files)} PDFs...")

    for pdf_path in pdf_files:
        print(f"   Processing: {pdf_path.name}")
        chunks = chunk_pdf(str(pdf_path))
        all_chunks.extend(chunks)

    print(f"✅ Loaded {len(all_chunks)} chunks from {len(pdf_files)} PDFs")
    return all_chunks


def chunk_pdf(pdf_path: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """
    Extract text from PDF and split into chunks with metadata.

    Args:
        pdf_path: Path to PDF file
        chunk_size: Words per chunk
        overlap: Overlapping words between chunks

    Returns:
        List of chunks with metadata (subject, class, chapter, text)
    """
    chunks = []

    try:
        reader = PdfReader(pdf_path)
        filename = Path(pdf_path).stem

        # Extract subject and class from filename
        # Expected format: subject_class.pdf or Class_6_Mathematics.pdf
        subject, class_level = extract_metadata_from_filename(filename)

        # Extract all text
        full_text = ""
        current_chapter = "Introduction"

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()

            # Try to detect chapter from text
            chapter = detect_chapter(text)
            if chapter:
                current_chapter = chapter

            full_text += text + "\n"

        # Split into chunks with overlap
        words = full_text.split()
        step = chunk_size - overlap

        for i in range(0, len(words), step):
            chunk_words = words[i:i + chunk_size]
            if len(chunk_words) < 50:  # Skip very small chunks
                continue

            chunk_text = " ".join(chunk_words)
            chunks.append({
                "text": chunk_text,
                "subject": subject,
                "class": class_level,
                "chapter": current_chapter,
                "source": Path(pdf_path).name
            })

    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

    return chunks


def extract_metadata_from_filename(filename: str) -> tuple:
    """
    Extract subject and class from filename.
    Handles formats: "Mathematics_Class_6", "Class_6_Math", etc.
    """
    filename_lower = filename.lower()

    # Try to find class number
    class_match = re.search(r'class\s*(\d+|six|seven|eight|nine|ten)', filename_lower)
    class_level = 6  # Default

    if class_match:
        class_str = class_match.group(1)
        if class_str.isdigit():
            class_level = int(class_str)
        else:
            class_words = {"six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
            class_level = class_words.get(class_str, 6)

    # Extract subject
    subjects = ["mathematics", "math", "science", "social", "english", "hindi"]
    subject = "General"

    for subj in subjects:
        if subj in filename_lower:
            subject = subj.capitalize()
            if subj == "math":
                subject = "Mathematics"
            elif subj == "social":
                subject = "Social Science"
            break

    return subject, class_level


def detect_chapter(text: str) -> str | None:
    """
    Detect chapter name from text (e.g., "Chapter 1: Fractions").
    """
    match = re.search(r'chapter\s+\d+[:\s]+(.+?)(?:\n|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
