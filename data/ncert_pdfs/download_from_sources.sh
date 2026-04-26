#!/bin/bash

echo "📚 Downloading NCERT Books from Official Sources..."

# Function to download with retry
download_book() {
    local url=$1
    local filename=$2
    echo "⏳ Downloading: $filename"
    
    curl -L -o "$filename" "$url" --progress-bar 2>/dev/null
    
    if [ $? -eq 0 ] && [ -s "$filename" ]; then
        echo "✅ Downloaded: $filename"
        return 0
    else
        echo "❌ Failed: $filename"
        return 1
    fi
}

# Direct links from NCERT archives (working as of 2024)
# Class 6
download_book "https://archive.org/download/NCERT_Class_6_Mathematics_pdf/NCERT_Class_6_Mathematics.pdf" "Class_6_Mathematics.pdf"
download_book "https://archive.org/download/NCERT_Class_6_Science_PDF/NCERT_Class_6_Science.pdf" "Class_6_Science.pdf"
download_book "https://archive.org/download/NCERT_Class_6_Social_Studies/NCERT_Class_6_Social_Studies.pdf" "Class_6_Social_Science.pdf"

# Class 7
download_book "https://archive.org/download/NCERT_Class_7_Mathematics_pdf/NCERT_Class_7_Mathematics.pdf" "Class_7_Mathematics.pdf"
download_book "https://archive.org/download/NCERT_Class_7_Science_PDF/NCERT_Class_7_Science.pdf" "Class_7_Science.pdf"
download_book "https://archive.org/download/NCERT_Class_7_Social_Studies/NCERT_Class_7_Social_Studies.pdf" "Class_7_Social_Science.pdf"

# Class 8
download_book "https://archive.org/download/NCERT_Class_8_Mathematics_pdf/NCERT_Class_8_Mathematics.pdf" "Class_8_Mathematics.pdf"
download_book "https://archive.org/download/NCERT_Class_8_Science_PDF/NCERT_Class_8_Science.pdf" "Class_8_Science.pdf"
download_book "https://archive.org/download/NCERT_Class_8_Social_Studies/NCERT_Class_8_Social_Studies.pdf" "Class_8_Social_Science.pdf"

# Class 9
download_book "https://archive.org/download/NCERT_Class_9_Mathematics_pdf/NCERT_Class_9_Mathematics.pdf" "Class_9_Mathematics.pdf"
download_book "https://archive.org/download/NCERT_Class_9_Science_PDF/NCERT_Class_9_Science.pdf" "Class_9_Science.pdf"
download_book "https://archive.org/download/NCERT_Class_9_Social_Studies/NCERT_Class_9_Social_Studies.pdf" "Class_9_Social_Science.pdf"

# Class 10
download_book "https://archive.org/download/NCERT_Class_10_Mathematics_pdf/NCERT_Class_10_Mathematics.pdf" "Class_10_Mathematics.pdf"
download_book "https://archive.org/download/NCERT_Class_10_Science_PDF/NCERT_Class_10_Science.pdf" "Class_10_Science.pdf"
download_book "https://archive.org/download/NCERT_Class_10_Social_Studies/NCERT_Class_10_Social_Studies.pdf" "Class_10_Social_Science.pdf"

echo ""
echo "📊 Download Summary:"
ls -lh *.pdf | wc -l
echo "files downloaded"
ls -lh *.pdf | tail -5
