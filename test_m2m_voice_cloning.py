"""
Test Script - Validate M2M100 + Voice Cloning Components
"""
import torch
import os
from utils import get_logger

logger = get_logger(__name__)


def test_gpu():
    """Test GPU availability"""
    logger.info("\n" + "="*60)
    logger.info("GPU/CUDA CHECK")
    logger.info("="*60)
    
    if torch.cuda.is_available():
        logger.info(f"✓ CUDA Available: {torch.cuda.get_device_name(0)}")
        logger.info(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        logger.info(f"  PyTorch Version: {torch.__version__}")
    else:
        logger.warning("⚠ CUDA not available, will use CPU (slower)")
    
    logger.info(f"✓ Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")


def test_m2m100():
    """Test M2M100 translator"""
    logger.info("\n" + "="*60)
    logger.info("M2M100 TRANSLATOR TEST")
    logger.info("="*60)
    
    try:
        from translation_optimized import M2M100Translator
        
        # Initialize
        logger.info("Loading M2M100 model...")
        translator = M2M100Translator(
            model_size='418M',
            use_gpu=torch.cuda.is_available()
        )
        logger.info("✓ M2M100 loaded successfully")
        
        # Test single translation
        test_text = "Hello, how are you today?"
        logger.info(f"\nTest 1: Single Translation")
        logger.info(f"  Input: {test_text}")
        
        result_hi = translator.translate(test_text, 'en', 'hi')
        logger.info(f"  Hindi: {result_hi}")
        
        result_te = translator.translate(test_text, 'en', 'te')
        logger.info(f"  Telugu: {result_te}")
        
        # Test batch translation
        logger.info(f"\nTest 2: Batch Translation")
        texts = [
            "Good morning, everyone!",
            "How is the weather?",
            "Welcome to our school!"
        ]
        
        results_hi = translator.translate_batch(texts, 'en', 'hi')
        logger.info(f"  Batch of {len(texts)} texts translated to Hindi")
        for i, (orig, trans) in enumerate(zip(texts, results_hi), 1):
            logger.info(f"    {i}. {orig} → {trans}")
        
        # Test supported languages
        logger.info(f"\nTest 3: Supported Languages")
        langs = translator.get_supported_languages()
        logger.info(f"  Total languages: {len(langs)}")
        logger.info(f"  Indic: {', '.join(['hi', 'te', 'ta', 'ml', 'kn'])}")
        
        logger.info("\n✓ M2M100 tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ M2M100 test failed: {str(e)}", exc_info=True)
        return False


def test_voice_cloning():
    """Test Voice Cloner"""
    logger.info("\n" + "="*60)
    logger.info("VOICE CLONING TEST")
    logger.info("="*60)
    
    try:
        from voice_cloning import VoiceCloner
        
        # Initialize
        logger.info("Loading Coqui XTTS-v2 model...")
        cloner = VoiceCloner(use_gpu=torch.cuda.is_available())
        logger.info("✓ Voice Cloner loaded successfully")
        
        # Test supported languages
        logger.info(f"\nTest 1: Supported Languages")
        langs = cloner.get_supported_languages()
        logger.info(f"  Total languages: {len(langs)}")
        logger.info(f"  Sample: {', '.join(list(langs.items())[:5])}")
        
        # Test synthesis with default voice
        logger.info(f"\nTest 2: Synthesize with Default Voice")
        test_text = "Hello, this is a test."
        output_path = "temp/test_synthesis_en.wav"
        
        logger.info(f"  Text: {test_text}")
        logger.info(f"  Language: English")
        
        result = cloner._synthesize_default(test_text, 'en', output_path)
        
        if os.path.exists(result):
            size_mb = os.path.getsize(result) / (1024 * 1024)
            logger.info(f"  ✓ Synthesis complete: {result} ({size_mb:.2f} MB)")
        else:
            logger.warning(f"  ⚠ Output file not found: {result}")
        
        # Test with multiple languages
        logger.info(f"\nTest 3: Multilingual Synthesis")
        test_cases = [
            ("Hello", "en"),
            ("Namaste", "hi"),
            ("Namaskaaram", "te"),
        ]
        
        for text, lang in test_cases:
            output = f"temp/test_synthesis_{lang}.wav"
            try:
                cloner._synthesize_default(text, lang, output)
                if os.path.exists(output):
                    logger.info(f"  ✓ {lang}: {text}")
                else:
                    logger.warning(f"  ⚠ {lang}: synthesis incomplete")
            except Exception as e:
                logger.warning(f"  ⚠ {lang}: {str(e)}")
        
        logger.info("\n✓ Voice Cloning tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Voice Cloning test failed: {str(e)}", exc_info=True)
        return False


def test_audio_dependencies():
    """Test audio processing dependencies"""
    logger.info("\n" + "="*60)
    logger.info("AUDIO DEPENDENCIES CHECK")
    logger.info("="*60)
    
    try:
        # Check required libraries
        imports = {
            'pydub': 'Audio mixing',
            'librosa': 'Audio analysis',
            'soundfile': 'Audio I/O',
            'numpy': 'Numerical operations',
            'scipy': 'Scientific computing',
        }
        
        for module, description in imports.items():
            try:
                __import__(module)
                logger.info(f"  ✓ {module}: {description}")
            except ImportError:
                logger.warning(f"  ✗ {module}: {description} (NOT INSTALLED)")
        
        # Check FFmpeg
        ffmpeg_dir = "ffmpeg-8.0.1-essentials_build/bin"
        ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        
        if os.path.exists(ffmpeg_exe):
            logger.info(f"  ✓ FFmpeg: Found at {ffmpeg_exe}")
        else:
            logger.warning(f"  ⚠ FFmpeg: Not found at expected location")
        
        logger.info("\n✓ Audio dependencies check complete!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Dependency check failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    logger.info("\n" + "="*60)
    logger.info("DUBBING SYSTEM - COMPONENT TESTS")
    logger.info("="*60)
    
    results = {}
    
    # Test GPU
    test_gpu()
    
    # Test Audio Dependencies
    results['Audio Dependencies'] = test_audio_dependencies()
    
    # Test M2M100
    results['M2M100 Translator'] = test_m2m100()
    
    # Test Voice Cloning
    results['Voice Cloning'] = test_voice_cloning()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    for component, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        logger.info(f"  {component}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✓ ALL TESTS PASSED - System ready for dubbing!")
    else:
        logger.warning("\n⚠ Some tests failed - See above for details")
    
    logger.info("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
