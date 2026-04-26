# 🎓 AI Tutor for Underprivileged Students

An adaptive AI tutoring system for NCERT Class 6-10 curriculum, designed for students in India with limited resources. Supports text, voice, and multilingual interactions (English, Hindi, Telugu).

## ✨ Features

- **🧠 Adaptive Learning Engine**: Adjusts difficulty based on student performance
- **📚 RAG-Powered Explanations**: Retrieves NCERT content and explains in simple language with real-world analogies
- **🎤 Voice Support**: Speech-to-text (Whisper) and text-to-speech (gTTS/Google Cloud)
- **🌐 Multilingual**: Auto-detect and respond in English, Hindi, Telugu, Kannada, Malayalam
- **📊 Progress Tracking**: Radar charts showing strength per topic, session stats
- **📝 Adaptive Quizzes**: MCQ and short-answer questions that adjust difficulty
- **📄 PDF Reports**: Weekly progress reports for parents/teachers with recommendations
- **⚡ Offline-Ready**: Cached embeddings, lazy-loading, optimized for low bandwidth

## 📂 Project Structure

```
ai-tutor/
├── rag/                    # Knowledge base (NCERT PDFs)
│   ├── loader.py          # Load and chunk NCERT PDFs with metadata
│   ├── embedder.py        # Embed using sentence-transformers, store in ChromaDB
│   └── retriever.py       # Query ChromaDB with subject/class filtering
├── tutor/                  # Adaptive tutoring engine
│   ├── session.py         # Student session, confidence tracking, statistics
│   ├── quiz.py            # Generate adaptive MCQ/short-answer questions
│   ├── explain.py         # RAG-powered explanations with analogies
│   └── adapt.py           # Difficulty adaptation logic
├── utils/
│   ├── translate.py       # Language detection & translation (Google/googletrans)
│   ├── speech.py          # Whisper (STT) + gTTS/Google TTS (TTS)
│   └── report.py          # PDF report generation (reportlab)
├── app.py                 # Streamlit UI (4 tabs: Ask, Quiz, Learn, Progress)
├── config.py              # Configuration & constants
├── init_rag.py            # One-command RAG initialization
├── test_rag.py            # Test RAG retrieval
├── demo.py                # Demo script showing system capabilities
├── setup.sh               # Automated setup script
└── requirements.txt       # All dependencies
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**:
   ```bash
   cat > .env << 'ENVEOF'
   OPENAI_API_KEY=your_api_key_here
   ENVEOF
   ```

4. **Create directories**:
   ```bash
   mkdir -p data/ncert_pdfs data/chroma_db reports sessions
   ```

5. **Download NCERT PDFs**:
   - Visit [ncert.nic.in](https://ncert.nic.in)
   - Download textbooks for Classes 6-10: Mathematics, Science, Social Science
   - Place PDFs in `data/ncert_pdfs/`
   - Supported formats: Class_6_Mathematics.pdf, Science_Class_7.pdf, etc.

6. **Initialize RAG Pipeline**:
   ```bash
   python init_rag.py
   # This loads PDFs, chunks them, and builds ChromaDB embeddings
   ```

7. **Run the application**:
   ```bash
   streamlit run app.py
   ```

8. **Visit the app**:
   ```
   http://localhost:8501
   ```

## 📖 Usage Guide

### For Students

1. **Start Learning**:
   - Enter your name
   - Select your class (6-10)
   - Select subject (Mathematics, Science, Social Science)
   - Click "Start Learning"

2. **Ask Questions** (💬 Tab):
   - Type any question about the current topic
   - Get AI-powered explanations with real-world analogies
   - Switch response language as needed

3. **Test Yourself** (📝 Tab):
   - Click "Generate 5-Question Quiz"
   - Questions adapt in difficulty based on answers
   - Receive instant feedback and explanations
   - Track accuracy and see confidence levels

4. **Learn** (📖 Tab):
   - Get comprehensive explanations for the topic
   - Includes real-world examples and analogies
   - Key points to remember for exams

5. **View Progress** (📊 Tab):
   - Topic strength radar chart
   - Overall accuracy percentage
   - Learning level (Easy/Medium/Hard)
   - Save sessions for later review

### For Teachers/Parents

1. **Generate Weekly Report**:
   - Click "Generate Weekly Report" in sidebar
   - Download PDF with:
     - Student performance summary
     - Topic-by-topic strength breakdown
     - Personalized recommendations
     - Trends and patterns

2. **Monitor Progress**:
   - View radar chart of topic strengths
   - Track accuracy and question count
   - See current learning level
   - Identify areas needing more practice

## 🔧 Configuration

### Key Settings (`config.py`)

```python
# Model Configuration
GPT_MODEL = "gpt-4"              # Change to "gpt-3.5-turbo" for cost savings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, efficient embeddings

# Thresholds for Difficulty Adaptation
CONFIDENCE_THRESHOLD_EASY = 0.7  # Move to harder questions at >70%
CONFIDENCE_THRESHOLD_HARD = 0.4  # Move to easier questions at <40%

# Response Limits (for low bandwidth)
MAX_RESPONSE_LENGTH = 150  # Words per explanation

# Supported Classes and Subjects
CLASSES = [6, 7, 8, 9, 10]
SUBJECTS = {
    "Mathematics": ["Algebra", "Geometry", "Numbers", "Ratios", "Arithmetic"],
    "Science": ["Physics", "Chemistry", "Biology"],
    "Social Science": ["Geography", "History", "Civics"]
}
```

### Environment Variables (`.env`)

```bash
# Required
OPENAI_API_KEY=sk-...                          # Get from https://platform.openai.com

# Optional - for advanced features
GOOGLE_TRANSLATE_API_KEY=...                   # For Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json  # For TTS/STT
```

## 📊 How It Works

### 1. RAG Pipeline (Knowledge Base)

```
NCERT PDFs → Load & Chunk (500 words) → Embed (sentence-transformers)
                                              ↓
                                         ChromaDB (persistent)
                                         
Query: "What is photosynthesis?" → Embed → Find similar chunks → Return context
```

### 2. Adaptive Learning

```
Student Answer → Evaluate (GPT-4) → Update Confidence → Adjust Difficulty
     ↓              ↓                    ↓                    ↓
  Record         is_correct?         EMA Update          Easy/Med/Hard
```

### 3. Question Generation

```
Topic + Difficulty → GPT-4 + RAG Context → MCQ/Short-Answer
                                ↓
                        Student Response
                                ↓
                        Auto-Evaluate + Feedback
```

## 🌐 Language Support

Auto-detect and respond in:

- 🇬🇧 English
- 🇮🇳 Hindi
- 🇦🇵 Telugu
- 🇰🇳 Kannada
- 🇲🇱 Malayalam

## ⚡ Performance Optimizations

| Optimization | Benefit |
|---|---|
| Local ChromaDB | No cloud calls for embeddings |
| Cached embeddings | All NCERT chunks pre-embedded |
| Metadata filtering | Only search relevant subject/class |
| Response limits | 150 words max (low bandwidth friendly) |
| Lazy PDF loading | Load only needed subjects |
| Efficient model | sentence-transformers (370MB) |

## 📋 Test the System

```bash
# Run demo (tests all components)
python demo.py

# Test RAG retrieval only
python test_rag.py
```

## 📱 Future: WhatsApp Integration

Deploy via Twilio WhatsApp Business API for rural reach:

```
Student → WhatsApp (text/voice) → Twilio → Flask Backend → Tutor Engine
                                                                 ↓
                                       gTTS → WhatsApp (audio response)
```

## 🛠️ Tech Stack

| Component | Tech | Why |
|---|---|---|
| **LLM** | OpenAI GPT-4 | SOTA reasoning, safe content |
| **Embeddings** | sentence-transformers | Fast, efficient, local |
| **Vector DB** | ChromaDB | Simple, persistent, metadata filters |
| **Web UI** | Streamlit | Fast prototyping, interactive |
| **Speech** | Whisper + gTTS | Open, widely available |
| **PDF Reports** | reportlab | Pure Python, no dependencies |

## 📄 License

MIT - Built for education equity in India

## 🙏 Acknowledgments

- NCERT for free, open textbooks
- OpenAI for GPT-4 API
- Sentence-transformers for efficient embeddings
- Streamlit for incredible UI speed

---

**🌟 Help make quality education accessible to every student in India!**

Last updated: 2026-04-26
