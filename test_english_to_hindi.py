"""
Test Script - English to Hindi Translation
Translates English sentences to Hindi using M2M100
"""
from translation_optimized import M2M100Translator
from utils import get_logger

logger = get_logger(__name__)


def main():
    """Test English to Hindi translation"""
    
    logger.info("=" * 70)
    logger.info("ENGLISH TO HINDI TRANSLATION TEST")
    logger.info("=" * 70)
    
    try:
        # Initialize translator
        logger.info("\n[1/3] Loading M2M100 Translator...")
        translator = M2M100Translator(model_size='418M', use_gpu=False)
        logger.info("✓ M2M100 Translator loaded successfully")
        
        # Test translations
        logger.info("\n[2/3] Testing translations...")
        
        test_sentences = [
            "Hello, how are you?",
            "Welcome to our school!",
            "Good morning, everyone!",
            "What is your name?",
            "I am learning Hindi language."
        ]
        
        logger.info(f"\n📝 Translating {len(test_sentences)} sentences from English to Hindi:\n")
        
        translations = translator.translate_batch(test_sentences, 'en', 'hi')
        
        for i, (eng, hin) in enumerate(zip(test_sentences, translations), 1):
            logger.info(f"{i}. EN: {eng}")
            logger.info(f"   HI: {hin}\n")
        
        logger.info("[3/3] Test Summary")
        logger.info(f"✓ Successfully translated {len(translations)} sentences")
        logger.info(f"✓ Source: English (en)")
        logger.info(f"✓ Target: Hindi (hi)")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ TRANSLATION TEST SUCCESSFUL!")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Test failed with error:")
        logger.error(f"   {str(e)}", exc_info=True)
        logger.info("\n" + "=" * 70)
        logger.info("❌ TRANSLATION TEST FAILED")
        logger.info("=" * 70)
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
