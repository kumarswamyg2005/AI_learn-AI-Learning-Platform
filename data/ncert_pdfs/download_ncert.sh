#!/bin/bash

# Base URL for NCERT books
BASE_URL="https://ncert.nic.in/pdf/English"

echo "📚 Downloading NCERT Textbooks..."

# Class 6
echo "Downloading Class 6 books..."
curl -o "Class_6_Mathematics.pdf" "$BASE_URL/class6/ms.pdf" 2>/dev/null &
curl -o "Class_6_Science.pdf" "$BASE_URL/class6/sc.pdf" 2>/dev/null &
curl -o "Class_6_Social_Science.pdf" "$BASE_URL/class6/ss.pdf" 2>/dev/null &

# Class 7
echo "Downloading Class 7 books..."
curl -o "Class_7_Mathematics.pdf" "$BASE_URL/class7/ms.pdf" 2>/dev/null &
curl -o "Class_7_Science.pdf" "$BASE_URL/class7/sc.pdf" 2>/dev/null &
curl -o "Class_7_Social_Science.pdf" "$BASE_URL/class7/ss.pdf" 2>/dev/null &

# Class 8
echo "Downloading Class 8 books..."
curl -o "Class_8_Mathematics.pdf" "$BASE_URL/class8/ms.pdf" 2>/dev/null &
curl -o "Class_8_Science.pdf" "$BASE_URL/class8/sc.pdf" 2>/dev/null &
curl -o "Class_8_Social_Science.pdf" "$BASE_URL/class8/ss.pdf" 2>/dev/null &

# Class 9
echo "Downloading Class 9 books..."
curl -o "Class_9_Mathematics.pdf" "$BASE_URL/class9/ms.pdf" 2>/dev/null &
curl -o "Class_9_Science.pdf" "$BASE_URL/class9/sc.pdf" 2>/dev/null &
curl -o "Class_9_Social_Science.pdf" "$BASE_URL/class9/ss.pdf" 2>/dev/null &

# Class 10
echo "Downloading Class 10 books..."
curl -o "Class_10_Mathematics.pdf" "$BASE_URL/class10/ms.pdf" 2>/dev/null &
curl -o "Class_10_Science.pdf" "$BASE_URL/class10/sc.pdf" 2>/dev/null &
curl -o "Class_10_Social_Science.pdf" "$BASE_URL/class10/ss.pdf" 2>/dev/null &

wait
echo "✅ Download complete!"
ls -lh *.pdf
