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

import whisper

logger = get_logger(__name__)

# supported languages from config
LANG_MAP = config.SUPPORTED_LANGUAGES

def detect_language(audio_path):
    print(f"Detecting language for: {audio_path}...")
    # Using 'base' for even faster detection if accuracy holds, sticking to user's 'small' for now
    model = whisper.load_model("small")
    
    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the spoken language
    _, probs = model.detect_language(mel)
    detected_lang = max(probs, key=probs.get)
    return detected_lang

def run_final_test(input_file, target_lang):
    print("\n" + "="*80)
    print("      FINAL END-TO-END DUBBING PIPELINE TEST")
    print("="*80)
    print(f"Input File:      {input_file}")
    print(f"Target Language: {LANG_MAP.get(target_lang, target_lang)}")
    print("="*80)
    
    # Language check
    detected_lang = detect_language(input_file)
    print(f"Detected Language : {LANG_MAP.get(detected_lang, detected_lang)}")
    print(f"Target Language   : {LANG_MAP.get(target_lang, target_lang)}")

    if detected_lang == target_lang:
        print("\n❌ ERROR: Source and target languages are the SAME")
        print("Please choose a different target language.")
        return

    print("✅ Language check passed")
    print("Proceed with translation and dubbing...")
    
    # 1. Initialize Dubber
    dubber = AudioDubber(use_pyannote=False)
    
    output_file = f"output/dubbed_final_{target_lang}.wav"
    
    # 2. Run Complete Pipeline
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
    
    # Prompt for input file
    print("Enter the path to the input audio file (e.g., test_audio/English.wav)")
    print("Common files:")
    print("1. test_audio/English.wav")
    print("2. test_audio/WAZ_hid.wav")
    
    input_choice = input("\nInput file path [test_audio/English.wav]: ").strip()
    if not input_choice:
        input_choice = "test_audio/English.wav"
        
    if not os.path.exists(input_choice):
        print(f"Error: Input file {input_choice} not found.")
        sys.exit(1)
        
    # Prompt user for language choice
    print("\nAvailable target languages:")
    for i, (code, name) in enumerate(LANG_MAP.items()):
        print(f"{i+1}. {name} ({code})")
    
    choice = input("\nSelect target language (enter 'te', 'hi', 'es' or 'en'): ").strip().lower()
    
    if choice not in LANG_MAP:
        print(f"❌ Unsupported target language: {choice}")
        sys.exit(1)
        
    run_final_test(input_choice, choice)
