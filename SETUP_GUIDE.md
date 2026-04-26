# 🚀 EduCore Setup Guide

Complete setup instructions for the AI Tutoring Platform.

## Prerequisites
- Python 3.8 or higher
- Internet connection (for API keys and book downloads)

## 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

## 2. Get Your API Key

### Option A: Free - Google Gemini API (Recommended)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key
4. Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-api-key-here
```

**Benefits:**
- ✅ Completely FREE
- ✅ 1,500 free requests per day (~100 students)
- ✅ High-quality responses
- ✅ No credit card required

### Option B: Paid - OpenAI GPT-4 (Alternative)
1. Visit: https://platform.openai.com/api-keys
2. Create new secret key
3. Add to `.env`:

```
OPENAI_API_KEY=sk-your-key-here
```

Then modify `config.py`:
```python
LLM_PROVIDER = "openai"
```

## 3. Download NCERT Textbooks

Run one of these commands:

```bash
# Automatic download via app (recommended)
streamlit run app.py
# Then click "📚 Study Materials" → "Download" → "⬇️ Download All NCERT Books"

# OR via command line
python3 download_ncert_books.py
```

**What gets downloaded:**
- 📚 15 textbooks (Classes 6-10, 3 subjects each)
- ~500 MB total
- Indexed automatically into knowledge base
- Location: `data/ncert_pdfs/`

## 4. Start the Application

```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501**

## 5. First Run

1. **Enter Student Details**
   - Name or ID (any identifier)
   - Class Level (6-10)
   - Subject (Mathematics, Science, Social Science)

2. **Click "🚀 Start Learning Session"**

3. **Choose a Topic** and explore:
   - 💬 **Ask & Learn** - Ask questions about topics
   - 📝 **Practice Quiz** - Adaptive quiz questions
   - 📖 **Study** - Detailed explanations with analogies
   - 📊 **Progress** - Track your learning analytics

## Features Overview

### 🎯 Adaptive Learning
- Difficulty adjusts based on your performance
- Questions get harder as you improve
- Tracks confidence for each topic

### 🧠 AI-Powered Explanations
- Simple, age-appropriate language
- Real-world analogies
- Practical examples
- Key points to remember

### 📚 Comprehensive Curriculum
- Official NCERT textbooks (Classes 6-10)
- Three main subjects
- Multiple sub-topics per subject

### 🎯 Smart Analytics
- Accuracy tracking
- Topic mastery visualization
- Performance radar charts
- Progress reports (PDF)

### 🌐 Multilingual Support
- English, Hindi, Telugu, Kannada, Malayalam
- Automatic language detection
- Real-time translation

### 🎤 Voice Features
- Speech-to-text for questions
- Text-to-speech for responses
- Hands-free learning mode

## Troubleshooting

### "No such file or directory: .env"
**Solution:** Create `.env` file with your API key

### "GEMINI_API_KEY is None"
**Solution:** 
- Check .env file exists
- Verify key is correct
- Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

### "ChromaDB collection not found"
**Solution:** Run `python3 download_ncert_books.py` to index books

### "API rate limit exceeded"
**Solution:**
- Gemini: Free tier has 1,500 requests/day
- Wait until next day or switch to paid OpenAI
- Consider caching responses locally

### "PDF upload failed"
**Solution:**
- Ensure PDF is a valid textbook format
- Try smaller PDFs first
- Check available disk space

## Customization

### Change LLM Provider
Edit `config.py`:
```python
LLM_PROVIDER = "gemini"  # or "openai"
```

### Change Model
```python
GEMINI_MODEL = "gemini-2.5-flash"  # Current
GEMINI_MODEL = "gemini-pro"  # Alternative
```

### Adjust Difficulty Thresholds
```python
CONFIDENCE_THRESHOLD_EASY = 0.7   # Easy if < 0.7
CONFIDENCE_THRESHOLD_HARD = 0.4   # Hard if < 0.4
```

### Add More Languages
```python
SUPPORTED_LANGUAGES = ["en", "hi", "te", "kn", "ml", "ur"]
```

## Performance Tips

1. **First Load** (~30 seconds)
   - System initializes models and RAG
   - Subsequent loads are instant

2. **Quiz Generation** (~15 seconds)
   - LLM generates unique questions
   - Concurrent requests speed this up

3. **Large PDF Upload**
   - Split large PDFs into smaller chunks
   - Process during off-peak hours

## System Requirements

| Component | Requirement |
|-----------|-------------|
| RAM | 4+ GB |
| Disk | 2+ GB (including books) |
| Python | 3.8+ |
| Internet | Required (API access) |

## Architecture

```
ai-tutor/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration & settings
├── download_ncert_books.py   # NCERT book downloader
│
├── rag/                      # Retrieval-Augmented Generation
│   ├── loader.py            # PDF loading & chunking
│   ├── embedder.py          # Embedding & ChromaDB
│   └── retriever.py         # Semantic search
│
├── tutor/                    # Core tutoring engine
│   ├── session.py           # Student progress tracking
│   ├── quiz.py              # Question generation
│   └── explain.py           # Explanation engine
│
├── utils/                    # Utilities
│   ├── translate.py         # Multi-language support
│   ├── speech.py            # Voice I/O
│   └── report.py            # PDF reporting
│
└── data/
    ├── ncert_pdfs/          # Downloaded textbooks
    ├── custom_pdfs/         # User-uploaded PDFs
    └── chroma_db/           # Vector database
```

## API Cost

### Free (Recommended)
- **Google Gemini 2.5 Flash**: 1,500 requests/day
- **Monthly potential**: 45,000 requests
- **Cost**: $0

### Paid (Optional)
- **OpenAI GPT-4**: $0.03 per 1K tokens
- **1000 student questions**: ~$1-5

## Support

- **Issues**: Check TROUBLESHOOTING section above
- **Feature Requests**: Update `config.py` to customize
- **Documentation**: See README.md for full features

---

**Ready to start?** Run `streamlit run app.py` and begin learning! 🚀
