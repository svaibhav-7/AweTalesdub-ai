#!/usr/bin/env python3
"""
Multi-Language Translation Demo
Shows how to translate English audio to any M2M100 supported language
"""

import json
import logging
from translation_optimized import M2M100Translator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 60)
    logger.info("MULTI-LANGUAGE TRANSLATION DEMO")
    logger.info("=" * 60)

    # Sample English text from the audio
    sample_texts = [
        "Look at the world today and feel both under and under chance.",
        "Because every voice we hear carries emotion, intention and identity.",
        "Yet for a long time, ecology only captured sound without understanding."
    ]

    # Languages to demonstrate (subset of M2M100's 100 languages)
    languages = {
        'hi': 'Hindi',
        'ta': 'Tamil',
        'ml': 'Malayalam',
        'kn': 'Kannada',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ar': 'Arabic'
    }

    try:
        # Initialize translator
        logger.info("Initializing M2M100 translator...")
        translator = M2M100Translator(model_size='418M', use_gpu=False)
        logger.info("✓ Translator ready")

        # Translate to each language
        for lang_code, lang_name in languages.items():
            logger.info(f"\n🌍 Translating to {lang_name} ({lang_code}):")

            translations = translator.translate_batch(sample_texts, 'en', lang_code)

            for i, (original, translated) in enumerate(zip(sample_texts, translations), 1):
                logger.info(f"  {i}. EN: {original[:50]}...")
                logger.info(f"     {lang_code.upper()}: {translated}")
                logger.info("")

        logger.info("=" * 60)
        logger.info("✅ MULTI-LANGUAGE TRANSLATION DEMO COMPLETE!")
        logger.info("=" * 60)
        logger.info("Your system can translate English audio to ANY of M2M100's 100 languages")
        logger.info("Just change the target language code in the translation call")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
