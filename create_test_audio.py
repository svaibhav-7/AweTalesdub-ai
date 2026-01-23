"""
Create simple test audio files using gTTS (once installed)
This creates test files in different languages for testing
"""

def create_test_audio_files():
    """Create test audio files using gTTS"""
    
    try:
        from gtts import gTTS
        import os
        
        print("=" * 60)
        print("Creating Test  Audio Files with gTTS")
        print("=" * 60)
        print()
        
        # Create test directory
        os.makedirs("test_audio", exist_ok=True)
        
        # Test cases
        test_cases = [
            {
                "text": "Hello, this is a test of the audio dubbing system. I am the first speaker.",
                "lang": "en",
                "filename": "test_audio/english_test.mp3",
                "description": "English test audio"
            },
            {
                "text": "नमस्ते, यह ऑडियो डबिंग सिस्टम का परीक्षण है। मैं दूसरा वक्ता हूं।",
                "lang": "hi",
                "filename": "test_audio/hindi_test.mp3",
                "description": "Hindi test audio"
            },
        ]
        
        created = []
        
        for test in test_cases:
            print(f"Creating: {test['description']}")
            print(f"  Language: {test['lang']}")
            print(f"  Text: {test['text'][:50]}...")
            
            try:
                tts = gTTS(text=test['text'], lang=test['lang'], slow=False)
                tts.save(test['filename'])
                created.append(test['filename'])
                print(f"  ✓ Saved: {test['filename']}")
            except Exception as e:
                print(f"  ✗ Failed: {str(e)}")
            
            print()
        
        print("=" * 60)
        print(f"Created {len(created)} test audio files")
        print("=" * 60)
        print()
        
        if created:
            print("Test the English audio with:")
            print(f'  python audio_dubbing.py "test_audio/english_test.mp3" hi "output/english_to_hindi.wav"')
            print()
            print("This should:")
            print("  1. Detect English language")
            print("  2. Translate to Hindi")
            print("  3. Generate Hindi speech")
        
        return created
        
    except ImportError:
        print("gTTS not installed yet. Run this after: pip install gTTS")
        return []

if __name__ == "__main__":
    create_test_audio_files()
