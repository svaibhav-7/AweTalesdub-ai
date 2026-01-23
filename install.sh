#!/bin/bash
# Installation script for Audio Dubbing System (Linux/Mac)

echo "================================================"
echo "Audio Dubbing System - Installation"
echo "================================================"
echo ""

# Check Python
echo "[1/3] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
python3 --version
echo ""

# Check FFmpeg
echo "[2/3] Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg is not installed"
    echo ""
    echo "Please install FFmpeg:"
    echo "  Linux: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
    read -p "Press Enter to continue anyway..."
else
    echo "FFmpeg is installed"
    ffmpeg -version | head -n 1
fi
echo ""

# Install Python dependencies
echo "[3/3] Installing Python packages..."
echo "This may take several minutes (downloading ~3-5 GB)..."
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install Python packages"
    exit 1
fi

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Verify installation: python3 test_installation.py"
echo "  2. Read the guide: QUICKSTART.md"
echo "  3. Try an example: python3 audio_dubbing.py --help"
echo ""
