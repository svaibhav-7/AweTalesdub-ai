"""
Test Script - English to Telugu Dubbing
Processes English.wav and creates Telugu dubbed version
"""
import os
import sys
from datetime import datetime
from dubbing_pipeline import DubbingPipeline
from utils import get_logger

logger = get_logger(__name__)


def main():
    """Test English to Telugu dubbing"""
    
    # Configuration
    SOURCE_LANG = 'en'
    TARGET_LANG = 'te'  # Telugu
    AUDIO_FILE = 'test_audio/English.wav'
    
    logger.info("=" * 70)
    logger.info("ENGLISH TO TELUGU DUBBING TEST")
    logger.info("=" * 70)
    logger.info(f"Source Language: English")
    logger.info(f"Target Language: Telugu")
    logger.info(f"Input Audio: {AUDIO_FILE}")
    logger.info("=" * 70)
    
    # Verify file exists
    if not os.path.exists(AUDIO_FILE):
        logger.error(f"❌ Audio file not found: {AUDIO_FILE}")
        return False
    
    logger.info(f"✓ Audio file found: {AUDIO_FILE}")
    
    try:
        # Initialize pipeline
        logger.info("\n[1/5] Initializing pipeline...")
        pipeline = DubbingPipeline(
            source_lang=SOURCE_LANG,
            target_lang=TARGET_LANG,
            use_gpu=True,
            save_intermediates=True
        )
        logger.info("✓ Pipeline initialized successfully")
        
        # Get pipeline status
        status = pipeline.get_status()
        logger.info(f"✓ Device: {status['device']}")
        
        # Run full pipeline
        logger.info("\n[2/5] Transcribing audio...")
        pipeline.transcribe(AUDIO_FILE)
        logger.info(f"✓ Transcription complete: {len(pipeline.transcription.get('segments', []))} segments")
        
        # Show sample transcription
        segments = pipeline.transcription.get('segments', [])
        if segments:
            logger.info(f"\n📝 Sample Transcription (first 3 segments):")
            for i, seg in enumerate(segments[:3], 1):
                text = seg.get('text', '')[:60]
                speaker = seg.get('speaker', 'N/A')
                logger.info(f"   {i}. [{speaker}] {text}...")
        
        logger.info("\n[3/5] Translating to Telugu...")
        pipeline.translate()
        logger.info(f"✓ Translation complete")
        
        # Show sample translation
        trans_segments = pipeline.translation.get('segments', [])
        if trans_segments:
            logger.info(f"\n🌍 Sample Translation (first 3 segments):")
            for i, seg in enumerate(trans_segments[:3], 1):
                orig = seg.get('text', '')[:40]
                trans = seg.get('translated_text', '')[:40]
                logger.info(f"   {i}. EN: {orig}...")
                logger.info(f"      TE: {trans}...")
        
        logger.info("\n[4/5] Synthesizing dubbed audio (this may take a few minutes)...")
        pipeline.synthesize(
            speaker_audio_map=None,  # Use extracted speaker references
            output_dir='temp/dubbed_audio_te'
        )
        successful = sum(1 for s in pipeline.synthesis if s.get('audio_synthesized'))
        logger.info(f"✓ Synthesis complete: {successful}/{len(pipeline.synthesis)} segments")
        
        logger.info("\n[5/5] Mixing final audio...")
        output_file = pipeline.mix(output_path='output/dubbed_english_to_telugu.wav')
        logger.info(f"✓ Mixing complete!")
        
        # Final status
        logger.info("\n" + "=" * 70)
        logger.info("✅ DUBBING COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"Input:  test_audio/English.wav (English)")
        logger.info(f"Output: {output_file} (Telugu)")
        logger.info("=" * 70)
        
        # Print file info
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            logger.info(f"✓ Output file size: {size_mb:.2f} MB")
        
        # Intermediate files
        logger.info("\n📁 Intermediate Files Saved (for debugging):")
        logger.info("   temp/transcription.json - Original transcription")
        logger.info("   temp/translation.json - Translated text")
        logger.info("   temp/synthesis.json - Synthesis metadata")
        logger.info("   temp/dubbed_audio_te/ - Individual dubbed segments")
        
        logger.info("\n" + "=" * 70)
        logger.info("Test Status: ✅ SUCCESS")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Test failed with error:")
        logger.error(f"   {str(e)}", exc_info=True)
        logger.info("\n" + "=" * 70)
        logger.info("Test Status: ❌ FAILED")
        logger.info("=" * 70)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
