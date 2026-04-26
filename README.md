# AI Tutor for Underprivileged Students

An adaptive AI tutoring system for NCERT Class 6-10 curriculum, designed for students in India with limited resources. Supports text, voice, and multilingual interactions.

## Features

- **Adaptive Learning Engine**: Adjusts difficulty based on student performance
- **RAG-powered Explanations**: Retrieves NCERT content and explains in simple language
- **Voice Support**: Speech-to-text (Whisper) and text-to-speech (gTTS)
- **Multilingual**: Detects and responds in Hindi, Telugu, English, etc.
- **Progress Tracking**: Radar charts showing strength per topic
- **Quiz Mode**: Generates MCQ and short-answer questions
- **Parent/Teacher Dashboard**: Weekly progress reports (PDF)

## Project Structure

```
ai-tutor/
├── rag/                    # Knowledge base (NCERT PDFs)
│   ├── loader.py          # Load and chunk NCERT PDFs
│   ├── embedder.py        # Embed chunks using sentence-transformers
│   └── retriever.py       # Query ChromaDB with metadata filtering
├── tutor/                  # Adaptive tutoring engine
│   ├── session.py         # Student session management
│   ├── quiz.py            # Question generation
│   ├── explain.py         # RAG-powered explanations
│   └── adapt.py           # Difficulty adaptation logic
├── utils/
│   ├── translate.py       # Language detection & translation
│   ├── speech.py          # Whisper (input) + gTTS (output)
│   └── report.py          # PDF report generation
├── app.py                 # Streamlit main application
├── config.py              # Configuration & constants
└── requirements.txt       # Python dependencies
```

## Setup

1. **Clone and install**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NCERT PDFs**:
   - Visit [ncert.nic.in](https://ncert.nic.in)
   - Download Class 6-10 PDFs for: Mathematics, Science, Social Science
   - Place in a `data/ncert_pdfs/` folder

3. **Environment variables** (create `.env`):
   ```
   OPENAI_API_KEY=your_key_here
   GOOGLE_TRANSLATE_API_KEY=your_key_here
   GOOGLE_TTS_API_KEY=your_key_here
   ```

4. **Initialize RAG**:
   ```bash
   python -c "from rag.loader import load_ncert; load_ncert('data/ncert_pdfs')"
   ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage

### Student Flow
1. Select subject and class
2. Choose a topic to learn
3. Ask questions via text or voice
4. Receive AI explanations with analogies
5. Test yourself with generated quizzes
6. View progress on radar chart

### Teacher/Parent View
- Weekly progress PDF report
- Topic strength breakdown
- Performance trends

## Performance Optimizations

- **Cached embeddings**: All NCERT chunks embedded once, stored locally
- **Metadata filtering**: Only searches relevant subject/class
- **Response length**: Limited to 150 words by default
- **Lazy loading**: PDFs loaded on-demand per subject

## Curriculum Coverage

- **Mathematics**: Algebra, Geometry, Numbers, Ratios
- **Science**: Physics, Chemistry, Biology
- **Social Science**: Geography, History, Civics

## Future: WhatsApp Integration

Deploy via Twilio WhatsApp Business API for maximum reach in rural India:
```
Student → WhatsApp → Twilio → Tutor Engine → gTTS → WhatsApp
```

## License

MIT - Built for education equity

