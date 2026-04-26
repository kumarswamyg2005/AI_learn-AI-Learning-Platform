#!/usr/bin/env python3
"""
Quick Setup Script for EduCore
Sets up the entire platform with one command
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def check_python():
    """Check Python version"""
    print_info(f"Python version: {sys.version}")

    if sys.version_info < (3, 8):
        print_error("Python 3.8+ required!")
        return False

    print_success("Python version OK")
    return True

def check_dependencies():
    """Check if requirements can be installed"""
    print_header("Checking Dependencies")

    try:
        import pip
        print_success("pip is available")
    except ImportError:
        print_error("pip not found!")
        return False

    return True

def create_venv():
    """Create virtual environment"""
    print_header("Setting Up Virtual Environment")

    venv_path = "venv"

    if os.path.exists(venv_path):
        print_info("Virtual environment already exists")
        return True

    try:
        subprocess.run(
            [sys.executable, "-m", "venv", venv_path],
            check=True,
            capture_output=True
        )
        print_success("Virtual environment created")
        return True
    except Exception as e:
        print_error(f"Failed to create venv: {e}")
        return False

def install_requirements():
    """Install Python dependencies"""
    print_header("Installing Dependencies")

    requirements_file = "requirements.txt"

    if not os.path.exists(requirements_file):
        print_error(f"{requirements_file} not found!")
        return False

    try:
        # Determine pip command based on OS
        if sys.platform == "win32":
            pip_cmd = "venv\\Scripts\\pip"
        else:
            pip_cmd = "venv/bin/pip"

        # Check if pip exists
        if not os.path.exists(pip_cmd):
            print_info("Installing to system Python (venv not active)")
            pip_cmd = "pip"

        print_info("Installing packages (this may take 2-3 minutes)...")

        result = subprocess.run(
            [pip_cmd, "install", "-r", requirements_file, "-q"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success("Dependencies installed")
            return True
        else:
            print_error(f"Installation failed: {result.stderr}")
            return False

    except Exception as e:
        print_error(f"Failed to install: {e}")
        return False

def create_env_file():
    """Create .env file"""
    print_header("API Configuration")

    env_path = ".env"

    if os.path.exists(env_path):
        print_info(".env file already exists")
        return True

    print_info("You need an API key to run EduCore")
    print("""
📖 Two Options:

1️⃣  FREE - Google Gemini (Recommended)
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2️⃣  PAID - OpenAI GPT-4
   - Visit: https://platform.openai.com/api-keys
   - Create secret key
   - Copy the key

""")

    api_key = input("Enter your API key: ").strip()

    if not api_key:
        print_error("No API key provided!")
        return False

    try:
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")

        print_success(f".env file created at {os.path.abspath(env_path)}")
        return True

    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Setting Up Directories")

    directories = [
        "data",
        "data/ncert_pdfs",
        "data/custom_pdfs",
        "data/chroma_db",
        "sessions",
        "reports"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print_success(f"Directory: {directory}")

    return True

def download_books():
    """Offer to download NCERT books"""
    print_header("Download NCERT Books")

    print_info("NCERT books are needed for the knowledge base")
    print("""
The system will download:
  📚 15 textbooks (Classes 6-10)
  📕 3 subjects each
  💾 ~500 MB total size

⏱️  This may take 10-15 minutes on average connection

""")

    choice = input("Download now? (y/n): ").strip().lower()

    if choice == "y":
        try:
            print("\nStarting download...\n")
            subprocess.run([sys.executable, "download_ncert_books.py"], check=True)
            print_success("Books downloaded and indexed!")
            return True
        except Exception as e:
            print_error(f"Download failed: {e}")
            print_info("You can download books later via the app")
            return True  # Don't fail the entire setup
    else:
        print_info("You can download books later via the app")
        return True

def print_next_steps():
    """Print next steps"""
    print_header("✨ Setup Complete!")

    print("""
🎉 EduCore is ready to use!

NEXT STEPS:

1. Activate the virtual environment:

   On macOS/Linux:
   $ source venv/bin/activate

   On Windows:
   $ venv\\Scripts\\activate

2. Start the application:

   $ streamlit run app.py

3. Open your browser:

   → http://localhost:8501

4. Enter your details and start learning!


📚 FEATURES:
  ✓ AI-powered explanations
  ✓ Adaptive quizzes
  ✓ Multi-language support
  ✓ Voice input/output
  ✓ Progress tracking
  ✓ PDF reports


💡 TIPS:
  • First load may take 30 seconds
  • Check SETUP_GUIDE.md for detailed info
  • See README.md for full features


📖 Documentation:
  • SETUP_GUIDE.md  - Complete setup guide
  • README.md       - Feature overview
  • QUICKSTART.md   - Quick reference

Need help? Check the troubleshooting section in SETUP_GUIDE.md

Happy Learning! 🚀

""")

def main():
    """Run complete setup"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║          🎓 EduCore - AI Learning Platform                     ║
║         Intelligent Tutoring System for NCERT                  ║
╚════════════════════════════════════════════════════════════════╝
    """)

    # Step 1: Check Python
    print_header("Step 1: Python Check")
    if not check_python():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 2: Check dependencies
    if not check_dependencies():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 3: Create venv
    if not create_venv():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 4: Install requirements
    if not install_requirements():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 5: Create directories
    if not create_directories():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 6: Create env file
    if not create_env_file():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 7: Download books
    if not download_books():
        print_error("Setup failed!")
        sys.exit(1)

    # Step 8: Next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
