#!/bin/bash
set -e

echo "🎓 AI Tutor Setup Script"
echo "======================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "\n📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "\n📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "\n📁 Creating directories..."
mkdir -p data/ncert_pdfs
mkdir -p data/chroma_db
mkdir -p reports
mkdir -p sessions

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "\n⚙️  Creating .env file..."
    cat > .env << 'ENVEOF'
# OpenAI API Key (required for AI features)
OPENAI_API_KEY=your_api_key_here

# Google Cloud credentials (optional, for advanced features)
GOOGLE_TRANSLATE_API_KEY=your_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Debug mode (optional)
DEBUG=False
ENVEOF
    echo "   📝 .env file created - please update with your API keys"
fi

echo "\n✅ Setup complete!"
echo "\n📌 Next steps:"
echo "   1. Edit .env file with your API keys (OPENAI_API_KEY required)"
echo "   2. Download NCERT PDFs from https://ncert.nic.in"
echo "   3. Place PDFs in data/ncert_pdfs/ directory"
echo "   4. Run: python init_rag.py"
echo "   5. Run: streamlit run app.py"
echo "\n"
