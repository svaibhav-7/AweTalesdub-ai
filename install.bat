@echo off
REM Installation script for Audio Dubbing System
REM Run this to install all dependencies

echo ================================================
echo Audio Dubbing System - Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version
echo.

REM Check if FFmpeg is installed
echo [2/3] Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not installed
    echo.
    echo Please install FFmpeg:
    echo   Option 1: choco install ffmpeg
    echo   Option 2: Download from https://ffmpeg.org/download.html
    echo.
    echo Press any key to continue anyway (installation will proceed)...
    pause >nul
) else (
    echo FFmpeg is installed
    ffmpeg -version | findstr "ffmpeg version"
)
echo.

REM Install Python dependencies
echo [3/3] Installing Python packages...
echo This may take several minutes (downloading ~3-5 GB)...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Verify installation: python test_installation.py
echo   2. Read the guide: QUICKSTART.md
echo   3. Try an example: python audio_dubbing.py --help
echo.
pause
