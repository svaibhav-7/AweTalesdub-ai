"""
Final End-to-End Test Script
Covers the entire pipeline: Preprocessing -> Transcription -> Translation -> Synthesis -> Mixing
"""
import os
import sys
import argparse
from audio_dubbing import AudioDubber
import config
from utils import get_logger

logger = get_logger(__name__)

def run_final_test(input_file, target_lang):
    print("\n" + "="*80)
    print("      FINAL END-TO-END DUBBING PIPELINE TEST")
    print("="*80)
    print(f"Input File:      {input_file}")
    print(f"Target Language: {target_lang}")
    print("="*80)
    
    # 1. Initialize Dubber
    # We'll use the enhanced logic implemented in voice_cloning.py
    dubber = AudioDubber(use_pyannote=False) # Use default diarization for speed in test
    
    output_file = f"output/dubbed_final_{target_lang}.wav"
    
    # 2. Run Complete Pipeline
    # This internally executes:
    # - Audio Extraction (handled in process_audio_pipeline)
    # - Noise Suppression (handled in process_audio_pipeline)
    # - VAD (handled in process_audio_pipeline)
    # - Speaker Diarization
    # - STT (Whisper)
    # - Text Segmentation / Alignment
    # - Translation
    # - Voice Selection
    # - Voice Synthesis (TTS)
    # - Timing Alignment
    # - Audio Mixing
    
    results = dubber.dub_audio(
        input_file=input_file,
        target_language=target_lang,
        output_file=output_file,
        preserve_background=True,
        save_intermediates=True
    )
    
    print("\n" + "="*80)
    print("                  FINAL RESULTS")
    print("="*80)
    
    if results['status'] == 'success':
        print(f"✓ STATUS:             SUCCESS")
        print(f"✓ DETECTED LANGUAGE:  {results.get('detected_language_name')}")
        print(f"✓ NUMBER OF SPEAKERS: {results.get('num_speakers')}")
        print(f"✓ TOTAL DURATION:     {results.get('duration_seconds', 0):.2f}s")
        print(f"✓ OUTPUT FILE:        {results.get('output_file')}")
        print("\nPipeline execution complete. You can find intermediate files in the 'temp' directory.")
    else:
        print(f"✗ STATUS:             FAILED")
        print(f"✗ ERROR:              {results.get('error')}")
    
    print("="*80)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("      INTERACTIVE DUBBING PIPELINE TEST")
    print("="*80)
    
    # Check if input file exists
    default_input = "test_audio/English.wav"
    if not os.path.exists(default_input):
        print(f"Error: Default input file {default_input} not found.")
        sys.exit(1)
        
    print(f"Default input: {default_input}")
    
    # Prompt user for language choice
    print("\nAvailable target languages:")
    print("1. Telugu (te)")
    print("2. Hindi (hi)")
    print("3. Spanish (es)")
    print("4. English (en)")
    
    choice = input("\nSelect target language (enter 'te', 'hi', 'es' or 'en'): ").strip().lower()
    
    if choice not in ['te', 'hi', 'es', 'en']:
        print(f"Invalid choice '{choice}'. Defaulting to Hindi (hi).")
        choice = 'hi'
        
    run_final_test(default_input, choice)
