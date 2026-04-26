# 🚀 Quick Start Guide

## 30-Second Setup

```bash
# 1. Run setup
chmod +x setup.sh && ./setup.sh

# 2. Add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key" >> .env

# 3. Download NCERT PDFs from https://ncert.nic.in
# Place them in: data/ncert_pdfs/

# 4. Initialize the knowledge base
python init_rag.py

# 5. Launch the app
streamlit run app.py
```

**Visit**: http://localhost:8501

---

## 5-Minute Tutorial

### For Students

1. **Enter your name** and select Class 6-10
2. **Pick a subject** (Mathematics, Science, Social Science)
3. **Click "Start Learning"**
4. **Select a topic** (e.g., "Fractions")
5. **Choose your action**:
   - 💬 **Ask Questions**: Type "What is a fraction?" → Get explanation with analogy
   - 📝 **Test Yourself**: Generate 5-question quiz → Answer → Get feedback
   - 📖 **Learn**: Get comprehensive topic explanation
   - 📊 **View Progress**: See your topic strengths

### For Teachers/Parents

1. **Click "Generate Weekly Report"** in sidebar
2. **Download PDF** with:
   - Student's accuracy percentage
   - Topic strength breakdown (green/yellow/red)
   - Personalized recommendations
   - Time spent learning

---

## Without NCERT PDFs?

Test the system without real PDFs:

```bash
python demo.py
```

This shows:
- ✅ Session management working
- ✅ Language detection working
- ✅ Report generation working
- ℹ️ RAG retrieval (needs PDFs to show real results)

---

## What You Need

### Minimum (Free)
- Python 3.8+
- OpenAI API key (free $5 credit at signup)
- NCERT PDFs (free from ncert.nic.in)

### Optional (Enhanced Features)
- Google Cloud credentials for TTS/STT
- Google Translate API for better translations

---

## Common Commands

```bash
# Test RAG pipeline
python test_rag.py

# Check collection stats
python -c "from rag.retriever import RAGRetriever; print(RAGRetriever().get_collection_stats())"

# Run demo
python demo.py

# Start app
streamlit run app.py

# Rebuild embeddings (if you add new PDFs)
python init_rag.py
```

---

## Troubleshooting

### "No chunks found"
```bash
# 1. Check PDFs are in the right place
ls -la data/ncert_pdfs/

# 2. Re-initialize RAG
python init_rag.py

# 3. Test retrieval
python test_rag.py
```

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
```bash
# Edit .env
nano .env

# Add your key:
# OPENAI_API_KEY=sk-your-api-key
```

### "Permission denied: setup.sh"
```bash
chmod +x setup.sh
./setup.sh
```

---

## Next Steps

1. **Read**: [README.md](README.md) for full documentation
2. **Configure**: Update [config.py](config.py) if needed
3. **Deploy**: Follow production guidelines in PROJECT_STATUS.md
4. **Scale**: Add more NCERT subjects as needed

---

## Features at a Glance

| Feature | Status | Notes |
|---|---|---|
| Ask Questions | ✅ Ready | Type or speak |
| Adaptive Quizzes | ✅ Ready | Auto-adjusts difficulty |
| Real-time Feedback | ✅ Ready | Uses GPT-4 |
| Progress Tracking | ✅ Ready | Radar charts + stats |
| PDF Reports | ✅ Ready | Weekly summaries |
| Multilingual | ✅ Ready | 5 languages |
| Voice Input | ✅ Ready | Needs audio permission |
| Voice Output | ✅ Ready | gTTS or Google TTS |
| WhatsApp (Future) | 🔄 Planned | Twilio integration |
| Mobile App (Future) | 🔄 Planned | React Native/Flutter |

---

**Need help?** Check README.md or PROJECT_STATUS.md

**Ready to teach?** Start with step 1 above! 🎓

