# 🎉 Using FREE Google Gemini 2.5 Flash

Your AI Tutor now uses **100% FREE Google Gemini 2.5 Flash**!

## ✨ Why Gemini?

| Feature | Cost | Quality |
|---|---|---|
| **Gemini 2.5 Flash** | 🟢 **FREE** (1,500/day) | ⭐⭐⭐⭐⭐ Within 5% of GPT-4o |
| GPT-4 | 🔴 $0.03/1K tokens | ⭐⭐⭐⭐⭐ Best reasoning |
| GPT-3.5-turbo | 🟡 $0.0015/1K tokens | ⭐⭐⭐⭐ Fast |

**No credit card needed. No costs. Just pure free AI.**

---

## 🚀 5-Minute Setup

### Step 1: Get Your Free API Key

1. **Go to**: https://makersuite.google.com/app/apikey
2. **Click**: "Create API Key"
3. **Copy**: Your API key (looks like: `AIzaSy...`)

### Step 2: Add to .env

```bash
# Edit your .env file
nano .env

# Add this line:
GEMINI_API_KEY=your-api-key-here

# Save (Ctrl+O, Enter, Ctrl+X)
```

### Step 3: Install Dependencies

```bash
pip install google-generativeai
```

### Step 4: Done! ✅

Your system is now FREE and ready to use!

```bash
streamlit run app.py
```

---

## 💡 How Many Students Can I Support?

### Free Tier: 1,500 requests/day

- **Per student session**: ~5-10 API calls (explanations, quizzes, evaluations)
- **Daily capacity**: 150-300 students per day
- **Monthly**: Thousands of students

### Example Usage
```
100 students × 10 calls each = 1,000 calls = ✅ WITHIN FREE TIER
```

---

## 📊 Quality Comparison

### Gemini 2.5 Flash (FREE)
```python
Question: "What is photosynthesis?"

Response: "Photosynthesis is like cooking - plants use sunlight as heat,
water as ingredients, and CO2 to create their own food (glucose).
It happens in leaves during the day."
```

✅ Simple, accurate, age-appropriate  
✅ Includes analogies  
✅ Works great for education  

---

## 🔄 Switching Providers (Optional)

If you want to use OpenAI or Groq instead:

### Edit `config.py`
```python
# For OpenAI (paid):
LLM_PROVIDER = "openai"

# For Gemini (free):
LLM_PROVIDER = "gemini"

# For Groq (free, fastest):
LLM_PROVIDER = "groq"
```

That's it! The system auto-switches providers.

---

## ❓ FAQ

### Q: Will my API key be exposed?
**A**: No! It's stored only in your `.env` file (not committed to git).

### Q: Can I use this in production?
**A**: Yes! 1,500 requests/day is enough for ~300 daily active students.

### Q: What if I exceed 1,500 requests?
**A**: Additional requests are charged at ~$0.075/1M tokens (very cheap).

### Q: Is Gemini good enough for education?
**A**: Yes! It's within 5% of GPT-4o on most tasks. Perfect for K-12.

### Q: How do I get more requests?
**A**: The free tier is per API key. You can create multiple keys if needed.

### Q: What languages does Gemini support?
**A**: All of them! Including English, Hindi, Telugu, etc.

---

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Check if .env exists and has the key
cat .env

# If not, add it:
echo "GEMINI_API_KEY=your-key" >> .env
```

### "Invalid API key"
```bash
# Get a new key from: https://makersuite.google.com/app/apikey
# Make sure it's correct with no extra spaces
```

### "Quota exceeded"
- You've used 1,500+ requests today
- Wait for quota to reset (24 hours)
- Or switch to OpenAI for overflow

---

## 📈 Scaling to Many Students

### For 1,000+ students/day:

**Option 1: Use Groq (also FREE, faster)**
```python
LLM_PROVIDER = "groq"  # Unlimited free requests!
```

**Option 2: Use OpenAI with batch API**
```python
LLM_PROVIDER = "openai"  # 50% discount with batch API
```

**Option 3: Mix providers**
```python
# Use Gemini for most requests
# Use Groq for high-traffic times
# Pay OpenAI only for overflow
```

---

## 🎓 For Schools/NGOs

**Special programs** for educational use:
- Google Cloud for Nonprofits (free credits)
- OpenAI for Education (reduced costs)
- Consider contacting them for bulk educational usage

---

## 📞 Support

**Issue?** Check:
1. API key is correct (no spaces)
2. Internet connection is working
3. Rate limit hasn't been exceeded
4. Check Google Gemini status page

**Still stuck?**  
Create an issue or check the README.md for more help.

---

**You're all set!** 🎉 Your AI Tutor is now completely FREE!

Next: Download NCERT PDFs and start teaching! 📚

