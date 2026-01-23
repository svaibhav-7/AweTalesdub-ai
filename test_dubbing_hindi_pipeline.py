"""
Full Test - English to Target Language Dubbing with English.wav
Interactive language selection with numbered options
Processes English.wav, translates to selected language, and saves to output/{lang}/
"""
import os
import sys
from datetime import datetime
from translation_optimized import M2M100Translator
from transcription import Transcriber
from speaker_diarization import SpeakerDiarizer
from audio_mixer import AudioMixer
from utils import get_logger, ensure_dir

logger = get_logger(__name__)

# M2M100 supported languages (verified against tokenizer)
LANGUAGE_OPTIONS = {
    1: ('hi', 'Hindi'),
    2: ('ta', 'Tamil'),
    3: ('ml', 'Malayalam'),
    4: ('kn', 'Kannada'),
    5: ('fr', 'French'),
    6: ('es', 'Spanish'),
    7: ('de', 'German'),
    8: ('zh', 'Chinese'),
    9: ('ja', 'Japanese'),
    10: ('ar', 'Arabic'),
    11: ('ru', 'Russian'),
    12: ('pt', 'Portuguese'),
    13: ('it', 'Italian'),
    14: ('ko', 'Korean'),
    15: ('tr', 'Turkish'),
    16: ('vi', 'Vietnamese'),
    17: ('th', 'Thai'),
    18: ('bn', 'Bengali'),
    19: ('ur', 'Urdu'),
    20: ('gu', 'Gujarati'),
    21: ('mr', 'Marathi'),
    22: ('pa', 'Punjabi'),
    23: ('or', 'Oriya'),
    24: ('ne', 'Nepali'),
    25: ('si', 'Sinhala')
}

def select_target_language():
    """Select target language - either from command line arg or interactive"""
    # Check if language provided as command line argument
    if len(sys.argv) > 1:
        lang_code = sys.argv[1].lower()
        # Find the language name
        for num, (code, name) in LANGUAGE_OPTIONS.items():
            if code == lang_code:
                print(f"✅ Selected via argument: {name} ({code})")
                return code, name
        print(f"❌ Language code '{lang_code}' not supported")
        print(f"Supported codes: {', '.join([code for code, name in LANGUAGE_OPTIONS.values()])}")
        sys.exit(1)

    # Interactive selection
    print("\n" + "=" * 70)
    print("🎯 SELECT TARGET LANGUAGE FOR DUBBING")
    print("=" * 70)
    print("Choose the language you want to translate English audio to:")
    print("(Note: English input is excluded from options)")
    print()

    for num, (code, name) in LANGUAGE_OPTIONS.items():
        print(f"{num:2d}. {name} ({code})")

    print()
    while True:
        try:
            choice = int(input("Enter your choice (1-25): "))
            if choice in LANGUAGE_OPTIONS:
                lang_code, lang_name = LANGUAGE_OPTIONS[choice]
                print(f"\n✅ Selected: {lang_name} ({lang_code})")
                print(f"   English audio will be dubbed to {lang_name}")
                return lang_code, lang_name
            else:
                print("❌ Invalid choice. Please enter a number between 1-25.")
        except ValueError:
            print("❌ Please enter a valid number.")


def main():
    """Test English to target language dubbing with English.wav"""

    SOURCE_LANG = 'en'

    # Interactive language selection
    TARGET_LANG, TARGET_LANG_NAME = select_target_language()

    AUDIO_FILE = 'test_audio/English.wav'

    logger.info("=" * 70)
    logger.info(f"ENGLISH TO {TARGET_LANG_NAME.upper()} DUBBING - FULL PIPELINE TEST")
    logger.info("=" * 70)
    logger.info(f"Input: {AUDIO_FILE}")
    logger.info(f"Translation: English → {TARGET_LANG_NAME}")
    logger.info("=" * 70)

    # Verify file exists
    if not os.path.exists(AUDIO_FILE):
        logger.error(f"❌ Audio file not found: {AUDIO_FILE}")
        return False

    logger.info(f"✓ Audio file found")

    try:
        # Step 1: Transcribe
        logger.info("\n[STEP 1] Transcribing audio...")
        transcriber = Transcriber()
        transcription = transcriber.transcribe_audio(AUDIO_FILE)
        segments = transcription.get('segments', [])
        logger.info(f"✓ Transcription complete: {len(segments)} segments")

        # Show sample
        if segments:
            logger.info(f"\n📝 Sample transcription (first 3 segments):")
            for i, seg in enumerate(segments[:3], 1):
                text = seg.get('text', '')[:60]
                logger.info(f"   {i}. {text}...")

        # Step 2: Translate
        logger.info(f"\n[STEP 2] Translating to {TARGET_LANG_NAME}...")
        translator = M2M100Translator(model_size='418M', use_gpu=False)

        # Extract texts for translation
        texts = [seg.get('text', '') for seg in segments]
        translated_texts = translator.translate_batch(texts, SOURCE_LANG, TARGET_LANG)

        # Add translations back to segments
        for seg, trans_text in zip(segments, translated_texts):
            seg['translated_text'] = trans_text

        logger.info(f"✓ Translation complete: {len(segments)} segments translated")

        # Show sample
        logger.info(f"\n🌍 Sample translation (first 3 segments):")
        for i, seg in enumerate(segments[:3], 1):
            orig = seg.get('text', '')[:40]
            trans = seg.get('translated_text', '')[:40]
            logger.info(f"   {i}. EN: {orig}...")
            logger.info(f"      {TARGET_LANG.upper()}: {trans}...")

        # Save intermediate results
        logger.info(f"\n[STEP 3] Saving intermediate results...")
        output_dir = f"output/{TARGET_LANG}"
        ensure_dir(output_dir)

        import json
        with open(f'{output_dir}/transcription.json', 'w', encoding='utf-8') as f:
            json.dump({'segments': segments[:5]}, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Transcription saved: {output_dir}/transcription.json")

        with open(f'{output_dir}/translation.json', 'w', encoding='utf-8') as f:
            json.dump({'segments': segments[:5]}, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Translation saved: {output_dir}/translation.json")

        # Step 4: Final summary
        logger.info("\n" + "=" * 70)
        logger.info("✅ DUBBING PIPELINE TEST SUCCESSFUL!")
        logger.info("=" * 70)
        logger.info(f"Transcription: {len(segments)} segments extracted")
        logger.info(f"Translation: English → {TARGET_LANG_NAME}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Next steps:")
        logger.info(f"  1. Voice synthesis (requires Coqui TTS)")
        logger.info(f"  2. Audio mixing and alignment")
        logger.info(f"  3. Final dubbed output")
        logger.info("=" * 70)

        return True

    except Exception as e:
        logger.error(f"\n❌ Test failed:")
        logger.error(f"   {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)