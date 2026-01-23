"""
Download public test audio files for testing the dubbing system
"""
import os
import urllib.request
from pathlib import Path

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"  ✓ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {str(e)}")
        return False

def main():
    """Download test audio files"""
    
    print("=" * 60)
    print("Downloading Public Test Audio Files")
    print("=" * 60)
    print()
    
    # Create test_audio directory
    test_dir = Path("test_audio")
    test_dir.mkdir(exist_ok=True)
    
    # Public domain audio files
    test_files = [
        {
            "name": "english_speech.mp3",
            "url": "https://www.soundjay.com/human/sounds/human-voice-hello-1.mp3",
            "description": "Short English greeting"
        },
        {
            "name": "sample_speech.wav",
            "url": "https://www2.cs.uic.edu/~i101/SoundFiles/taunt.wav",
            "description": "English speech sample"
        },
    ]
    
    downloaded = []
    
    for file_info in test_files:
        output_path = test_dir / file_info["name"]
        print(f"File: {file_info['name']}")
        print(f"Description: {file_info['description']}")
        
        if download_file(file_info["url"], str(output_path)):
            downloaded.append(str(output_path))
        
        print()
    
    print("=" * 60)
    print(f"Downloaded {len(downloaded)} files to test_audio/")
    print("=" * 60)
    print()
    
    if downloaded:
        print("Test these files with:")
        for file in downloaded:
            print(f"  python audio_dubbing.py \"{file}\" hi output_hindi.wav")
    else:
        print("Note: Some downloads may have failed due to network issues.")
        print("You can use your own audio files for testing instead.")
        print()
        print("Alternative: Use online text-to-speech to create test files:")
        print("  1. Go to https://ttsmp3.com/")
        print("  2. Generate English speech")
        print("  3. Download as WAV/MP3")
        print("  4. Save to test_audio/")

if __name__ == "__main__":
    main()
