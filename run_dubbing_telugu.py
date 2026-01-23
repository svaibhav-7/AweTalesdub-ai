"""
Run dubbing pipeline on test audio - Telugu target
"""
from audio_dubbing import AudioDubber
import config
import os

def main():
    print("=" * 60)
    print("AUDIO DUBBING PIPELINE - English to Telugu")
    print("=" * 60)
    
    # Ensure output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Create dubber instance
    dubber = AudioDubber()
    
    # Dub audio from English to Telugu
    print("\nStarting dubbing process...")
    print("Input: test_audio/English.wav")
    print("Target: Telugu")
    print("-" * 60)
    
    results = dubber.dub_audio(
        input_file="test_audio/English.wav",
        target_language="te",  # Telugu
        output_file="output/dubbed_telugu.wav",
        save_intermediates=True
    )
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if results['status'] == 'success':
        print(f"Status: SUCCESS")
        print(f"Detected Language: {results.get('detected_language_name', 'Unknown')}")
        print(f"Target Language: Telugu")
        print(f"Output File: {results['output_file']}")
    else:
        print(f"Status: FAILED")
        print(f"Error: {results.get('error', 'Unknown error')}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
