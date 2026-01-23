"""
Run dubbing pipeline on test audio
"""
from audio_dubbing import AudioDubber
import config

def main():
    print("=" * 60)
    print("AUDIO DUBBING PIPELINE - English to Hindi")
    print("=" * 60)
    
    # Create dubber instance
    dubber = AudioDubber()
    
    # Dub audio from English to Hindi
    print("\nStarting dubbing process...")
    print("Input: test_audio/English.wav")
    print("Target: Hindi")
    print("-" * 60)
    
    results = dubber.dub_audio(
        input_file="test_audio/English.wav",
        target_language="hi",  # Hindi
        output_file="output/dubbed_hindi.wav",
        save_intermediates=True  # Save intermediate files for debugging
    )
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if results['status'] == 'success':
        print(f"✓ Status: SUCCESS")
        print(f"✓ Detected Language: {results.get('detected_language_name', 'Unknown')}")
        print(f"✓ Number of Speakers: {results.get('num_speakers', 'Unknown')}")
        print(f"✓ Number of Segments: {results.get('num_segments', 'Unknown')}")
        print(f"✓ Output File: {results['output_file']}")
        print("\nDubbing completed successfully!")
    else:
        print(f"✗ Status: FAILED")
        print(f"✗ Error: {results.get('error', 'Unknown error')}")
        
        # Print more details if available
        if 'traceback' in results:
            print("\nTraceback:")
            print(results['traceback'])
    
    print("=" * 60)
    return results

if __name__ == "__main__":
    main()
