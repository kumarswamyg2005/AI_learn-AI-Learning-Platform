"""
Download NCERT Textbooks from official sources
Supports Classes 6-10, all subjects
More robust downloader with fallback mechanisms
"""

import os
import requests
from pathlib import Path
import time

# NCERT official download URLs - Primary sources
NCERT_BOOKS = {
    6: {
        "Mathematics": "https://ncert.nic.in/pdf/publications/flexi2024/Mathematics_Class-VI.pdf",
        "Science": "https://ncert.nic.in/pdf/publications/flexi2024/Science_Class-VI.pdf",
        "Social Science": "https://ncert.nic.in/pdf/publications/flexi2024/Social-Science_Class-VI.pdf",
    },
    7: {
        "Mathematics": "https://ncert.nic.in/pdf/publications/flexi2024/Mathematics_Class-VII.pdf",
        "Science": "https://ncert.nic.in/pdf/publications/flexi2024/Science_Class-VII.pdf",
        "Social Science": "https://ncert.nic.in/pdf/publications/flexi2024/Social-Science_Class-VII.pdf",
    },
    8: {
        "Mathematics": "https://ncert.nic.in/pdf/publications/flexi2024/Mathematics_Class-VIII.pdf",
        "Science": "https://ncert.nic.in/pdf/publications/flexi2024/Science_Class-VIII.pdf",
        "Social Science": "https://ncert.nic.in/pdf/publications/flexi2024/Social-Science_Class-VIII.pdf",
    },
    9: {
        "Mathematics": "https://ncert.nic.in/pdf/publications/flexi2024/Mathematics_Class-IX.pdf",
        "Science": "https://ncert.nic.in/pdf/publications/flexi2024/Science_Class-IX.pdf",
        "Social Science": "https://ncert.nic.in/pdf/publications/flexi2024/Social-Science_Class-IX.pdf",
    },
    10: {
        "Mathematics": "https://ncert.nic.in/pdf/publications/flexi2024/Mathematics_Class-X.pdf",
        "Science": "https://ncert.nic.in/pdf/publications/flexi2024/Science_Class-X.pdf",
        "Social Science": "https://ncert.nic.in/pdf/publications/flexi2024/Social-Science_Class-X.pdf",
    }
}

def is_valid_pdf(filepath):
    """Check if file is a valid PDF"""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
            return header.startswith(b'%PDF')
    except:
        return False

def download_ncert_books(output_dir="data/ncert_pdfs", verbose=True):
    """
    Download all NCERT textbooks to output directory

    Returns:
        tuple: (successful_count, failed_count)
    """
    os.makedirs(output_dir, exist_ok=True)

    successful = 0
    failed = 0
    skipped = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for class_num, subjects in NCERT_BOOKS.items():
        if verbose:
            print(f"\n📚 Class {class_num}:")

        for subject, url in subjects.items():
            filename = f"NCERT_Class{class_num}_{subject.replace(' ', '_')}.pdf"
            filepath = os.path.join(output_dir, filename)

            # Skip if already downloaded
            if os.path.exists(filepath) and is_valid_pdf(filepath):
                if verbose:
                    size = os.path.getsize(filepath) / (1024 * 1024)
                    print(f"  ✓ {subject} ({size:.1f} MB) - already exists")
                skipped += 1
                continue

            if verbose:
                print(f"  ⏳ Downloading {subject}...", end=" ")

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=60,
                    verify=True,
                    allow_redirects=True
                )

                # Check if response is valid
                if response.status_code == 200 and len(response.content) > 10000:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    # Verify it's a valid PDF
                    if is_valid_pdf(filepath):
                        file_size = os.path.getsize(filepath) / (1024 * 1024)
                        if verbose:
                            print(f"✓ ({file_size:.1f} MB)")
                        successful += 1
                    else:
                        os.remove(filepath)
                        if verbose:
                            print(f"✗ (Invalid PDF)")
                        failed += 1
                else:
                    if verbose:
                        print(f"✗ (HTTP {response.status_code})")
                    failed += 1

            except requests.exceptions.Timeout:
                if verbose:
                    print(f"✗ (Timeout)")
                failed += 1
            except requests.exceptions.ConnectionError:
                if verbose:
                    print(f"✗ (Connection Error)")
                failed += 1
            except Exception as e:
                if verbose:
                    print(f"✗ ({str(e)[:40]}...)")
                failed += 1

            # Rate limiting to be respectful to the server
            time.sleep(2)

    if verbose:
        print(f"\n{'='*60}")
        print(f"📥 Download Summary")
        print(f"{'='*60}")
        print(f"✓ Downloaded: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"⊘ Skipped (already exist): {skipped}")
        print(f"📂 Location: {os.path.abspath(output_dir)}")
        print(f"{'='*60}\n")

    return successful, failed

def get_available_books(directory="data/ncert_pdfs"):
    """List all downloaded NCERT books"""
    books = {}

    if os.path.exists(directory):
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.pdf'):
                filepath = os.path.join(directory, filename)
                try:
                    size = os.path.getsize(filepath) / (1024 * 1024)
                    books[filename] = {
                        'path': filepath,
                        'size_mb': round(size, 2),
                        'valid': is_valid_pdf(filepath)
                    }
                except:
                    pass

    return books

if __name__ == "__main__":
    import sys

    print("\n🎓 NCERT Textbook Downloader")
    print("="*60)
    print("Downloading official NCERT books for Classes 6-10...\n")

    # Download all books
    successful, failed = download_ncert_books()

    # List available books
    books = get_available_books()
    if books:
        print("📖 Available Books:")
        total_size = 0
        for name, info in books.items():
            status = "✓" if info['valid'] else "⚠"
            print(f"  {status} {name} ({info['size_mb']} MB)")
            total_size += info['size_mb']

        print(f"\n📊 Total: {len(books)} books, {total_size:.1f} MB")
    else:
        print("⚠️  No books found. Please check your internet connection and try again.")
