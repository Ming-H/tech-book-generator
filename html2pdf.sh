#!/bin/bash
# Orange Book HTML to PDF Converter
# Opens HTML in default browser and prompts to save as PDF

set -e

HTML_FILE="$1"
PDF_FILE="$2"

if [ -z "$HTML_FILE" ]; then
    echo "Usage: $0 <input.html> [output.pdf]"
    echo ""
    echo "Examples:"
    echo "  $0 tutorial.html"
    echo "  $0 tutorial.html tutorial.pdf"
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: File not found: $HTML_FILE"
    exit 1
fi

# Get absolute path
HTML_PATH="$(cd "$(dirname "$HTML_FILE")" && pwd)/$(basename "$HTML_FILE")"

echo "📖 Opening $HTML_PATH in your default browser..."
echo ""
echo "📋 To save as PDF:"
echo "   1. Wait for the page to load"
echo "   2. Press Cmd+P (or Ctrl+P)"
echo "   3. Choose 'Save as PDF' as the destination"
echo "   4. Click Save"
echo ""

# Open in default browser
open "$HTML_PATH"

# If PDF filename was provided, show where to save
if [ -n "$PDF_FILE" ]; then
    PDF_PATH="$(cd "$(dirname "$PDF_FILE" 2>/dev/null || echo '.')" && pwd)/$(basename "$PDF_FILE")"
    echo "💾 Save the PDF as: $PDF_PATH"
fi
