#!/usr/bin/env python3
"""
DubSmart AI - Complete End-to-End Multilingual Dubbing Pipeline
English.wav → Transcribe → Translate → Voice Clone → Mix Audio → Final Dubbed Output

Usage:
    python dub_complete.py --lang es  # Dub to Spanish
    python dub_complete.py --lang fr  # Dub to French
    python dub_complete.py --lang hi  # Dub to Hindi
"""

import argparse
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dubsmart.core.pipeline import DubbingPipeline

def main():
    parser = argparse.ArgumentParser(description="Complete End-to-End Audio Dubbing")
    parser.add_argument("--input", default="test_audio/English.wav", help="Input audio file")
    parser.add_argument("--lang", required=True, help="Target language code (es, fr, hi, ta, etc.)")
    parser.add_argument("--output", help="Output dubbed audio file")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode (disable GPU)")

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return False

    # Set default output
    if not args.output:
        args.output = f"output/dubbed_{args.lang}_complete.wav"

    # Ensure output directory exists
    Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

    print("🎬 DUBSMART AI - COMPLETE MULTILINGUAL DUBBING")
    print("=" * 60)
    print(f"Input: {args.input}")
    print(f"Target Language: {args.lang.upper()}")
    print(f"Output: {args.output}")
    print(f"Mode: {'CPU' if args.cpu else 'GPU (if available)'}")
    print()

    try:
        # Initialize pipeline
        print("🚀 Initializing dubbing pipeline...")
        pipeline = DubbingPipeline(
            src_lang='en',
            tgt_lang=args.lang,
            use_gpu=not args.cpu
        )

        # Execute complete pipeline
        print("⚡ Processing complete end-to-end pipeline...")
        print("   1. Transcribing audio →")
        print("   2. Translating to target language →")
        print("   3. Voice cloning all segments →")
        print("   4. Mixing with original timing →")
        print("   5. Generating final dubbed audio")
        print()

        result_path = pipeline.process(args.input, args.output)

        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path) / 1024  # KB
            print()
            print("🎉 SUCCESS! Complete end-to-end dubbing delivered!")
            print("=" * 60)
            print(f"✅ Final dubbed audio: {result_path}")
            print(f"   File size: {file_size:.1f} KB")
            print()
            print("🎯 Pipeline completed successfully:")
            print("   • Transcription ✓")
            print("   • Translation ✓")
            print("   • Voice Cloning ✓")
            print("   • Audio Mixing ✓")
            print("   • Final Output ✓")
            return True
        else:
            print("❌ Pipeline completed but output file not found")
            return False

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)