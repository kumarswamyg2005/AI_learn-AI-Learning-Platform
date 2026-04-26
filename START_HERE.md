# 🚀 START HERE - EduCore Setup

## Quick Start (5 minutes)

### 1️⃣ Install Everything
```bash
python3 quick_setup.py
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Set up API keys
- ✅ Create directories
- ✅ Download NCERT books (optional)

### 2️⃣ Start the App
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

streamlit run app.py
```

### 3️⃣ Open in Browser
Visit: **http://localhost:8501**

---

## What You'll See

### First Time Setup
1. **Enter your name/ID**
2. **Select class level** (6-10)
3. **Select subject** (Math/Science/Social)
4. **Click "Start Learning"**

### Four Main Features
- 💬 **Ask & Learn** - Ask questions, get instant answers
- 📝 **Practice Quiz** - Adaptive questions that adjust difficulty
- 📖 **Study** - Detailed explanations with analogies
- 📊 **Progress** - Track your performance with charts

---

## API Key Setup

### ⭐ Free Option (Recommended)
1. Visit: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key
4. Paste when prompted during setup

**Benefits:**
- Free forever
- 1,500 requests/day
- High quality responses
- No credit card needed

### Paid Option
- OpenAI GPT-4 (costs ~$1-5 per month)
- More detailed responses
- Higher rate limits

---

## Download NCERT Books

### Option A: During Setup
When running `quick_setup.py`, choose "y" when asked

### Option B: In the App
1. Click sidebar "📚 Study Materials"
2. Click "Download" tab
3. Click "⬇️ Download All NCERT Books"
4. Wait 10-15 minutes

### Option C: Command Line
```bash
python3 download_ncert_books.py
```

---

## Upload Your Own Books

1. Click "📚 Study Materials" in sidebar
2. Click "Upload" tab
3. Drag-drop a PDF or click to select
4. Click "🔄 Process & Index PDF"
5. Done! Now usable in learning

---

## Troubleshooting

### "Python not found"
**Solution:** Install Python 3.8+ from python.org

### "Module not found"
**Solution:** Activate venv first:
```bash
source venv/bin/activate  # macOS/Linux
```

### "API key not working"
**Solution:** 
1. Check .env file exists in project root
2. Verify key is correct
3. Restart Streamlit (Ctrl+C, then `streamlit run app.py`)

### "Slow first load"
**Normal!** First run loads models (~30 seconds). Subsequent loads are instant.

### "Books won't download"
**Check:**
- Internet connection working
- NCERT server is up (try in browser)
- Disk space available (~1 GB)
- Run again, it will skip existing files

---

## System Requirements

| Item | Requirement |
|------|-------------|
| **Python** | 3.8 or higher |
| **RAM** | 4 GB minimum |
| **Disk** | 2 GB (including books) |
| **Internet** | Required for API |

---

## Files Overview

```
ai-tutor/
├── app.py                 ← Main application (run this!)
├── quick_setup.py         ← One-command setup (run first!)
├── config.py              ← Settings and configuration
├── download_ncert_books.py ← Download books script
├── requirements.txt       ← Python dependencies
├── .env                   ← API key (auto-created)
└── data/
    ├── ncert_pdfs/       ← Downloaded textbooks
    ├── custom_pdfs/      ← Your uploaded PDFs
    └── chroma_db/        ← AI knowledge base
```

---

## Feature Walkthrough

### 💬 Ask & Learn Tab
- Type a question about any topic
- Get instant AI-powered answers
- View source textbook pages
- Learn from real-world analogies

**Example:**
```
Q: "What is photosynthesis?"
A: "Plants use sunlight to make food from water and CO2.
   Think of it like cooking - the plant is a kitchen!"
```

### 📝 Practice Quiz Tab
- Get 5 questions per session
- Difficulty adapts to your level
- Mix of multiple-choice and essays
- Instant feedback on answers
- See explanations for every question

**How Difficulty Works:**
- Start: Easy questions
- Correct answer: Next gets harder
- Wrong answer: Next stays same level
- Eventually: Very hard challenge questions

### 📖 Study Tab
- Read detailed explanations
- See real-world analogies
- Get practical examples
- Learn key points

**Great for:**
- Deep understanding
- Pre-quiz preparation
- Reference material

### 📊 Progress Tab
- See your accuracy percentage
- View mastered topics
- Track questions answered
- Visualize your learning journey
- Download progress report (PDF)

---

## Settings & Customization

Edit `config.py` to change:

```python
# Change AI model
LLM_PROVIDER = "gemini"  # or "openai"

# Change difficulty thresholds
CONFIDENCE_THRESHOLD_EASY = 0.7
CONFIDENCE_THRESHOLD_HARD = 0.4

# Add languages
SUPPORTED_LANGUAGES = ["en", "hi", "te", "kn", "ml"]

# Adjust quiz size
MAX_RESPONSE_LENGTH = 150  # words
```

---

## Performance Tips

1. **First Load (30 seconds)**
   - Loading AI models
   - Initializing database
   - This is normal!

2. **Quiz Generation (15 seconds)**
   - Creating unique questions
   - Checking difficulty
   - Be patient!

3. **Large PDFs**
   - Upload smaller files first
   - Check file validity
   - Wait for indexing

4. **Multiple Sessions**
   - Use different student names
   - Each gets own progress tracking
   - Share computer? Use different IDs

---

## Next Steps

### Short-term
1. ✅ Run setup script
2. ✅ Download NCERT books
3. ✅ Start first learning session
4. ✅ Try all 4 tabs
5. ✅ Check progress dashboard

### Medium-term
- Upload your own study materials
- Track progress for 1 week
- Try different subjects
- Generate a PDF report

### Long-term
- Complete all topics
- Achieve 90%+ accuracy
- Download final report
- Share with teachers/parents

---

## FAQ

**Q: Is it really free?**
A: Yes! Gemini API tier is 1,500 free requests/day

**Q: Do I need internet?**
A: Yes, for AI features. Downloaded books can be used offline after initial setup

**Q: How many students can use this?**
A: One per login. You can create multiple student profiles

**Q: Can I use my own books?**
A: Yes! Upload any PDF via "Study Materials" panel

**Q: Is my data saved?**
A: Yes, in `sessions/` folder locally. Never uploaded

**Q: What if I forget password?**
A: There's no password - just use your student ID

**Q: Can teachers use this?**
A: Yes! Track multiple students' progress

**Q: Is it safe?**
A: All data stays local. API key only used for AI calls

---

## Getting Help

### Resources
- 📖 **SETUP_GUIDE.md** - Detailed setup instructions
- 🔧 **IMPROVEMENTS.md** - What's new and improved
- 🚀 **README.md** - Full feature list
- 💡 **QUICKSTART.md** - Quick reference

### Troubleshooting
1. Check SETUP_GUIDE.md troubleshooting section
2. Review error messages carefully
3. Try restarting Streamlit
4. Check your .env file

---

## Ready? Let's Go! 🎓

```bash
# One-command setup
python3 quick_setup.py

# Then start learning!
streamlit run app.py
```

Visit **http://localhost:8501** and begin your journey! ✨

---

**Version**: 2.0  
**Status**: ✅ Production Ready  
**Last Updated**: April 2026
