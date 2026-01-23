#!/usr/bin/env python3
"""
Voice Synthesis Test - Generate Hindi audio from translated segments
Tests Coqui XTTS-v2 voice synthesis without speaker cloning
"""

import json
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import voice synthesis module
try:
    from voice_cloning import CoquiVoiceSynthesizer
except ImportError as e:
    logger.error(f"Failed to import voice_cloning: {e}")
    logger.info("Please ensure TTS>=0.22.0 is installed")
    exit(1)

def main():
    logger.info("=" * 70)
    logger.info("VOICE SYNTHESIS TEST - HINDI AUDIO GENERATION")
    logger.info("=" * 70)
    
    # Paths
    translation_file = "temp/hindi_dubbing/translation.json"
    output_dir = "temp/hindi_dubbing/synthesized_audio"
    
    # Check translation file exists
    if not os.path.exists(translation_file):
        logger.error(f"❌ Translation file not found: {translation_file}")
        logger.info("Please run test_dubbing_hindi_pipeline.py first")
        return False
    
    logger.info(f"✓ Translation file found")
    
    # Load translations
    with open(translation_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    logger.info(f"✓ Loaded {len(translations)} segments for synthesis")
    
    try:
        # Initialize synthesizer
        logger.info("\n[STEP 1] Initializing Coqui XTTS-v2...")
        synthesizer = CoquiVoiceSynthesizer(language='hi')
        logger.info("✓ Voice synthesizer initialized")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Synthesize first 3 segments as test
        logger.info("\n[STEP 2] Synthesizing audio (first 3 segments)...")
        test_segments = translations[:3]
        
        synthesized = []
        for i, segment in enumerate(test_segments, 1):
            hindi_text = segment.get('translated_text', '')
            if not hindi_text:
                logger.warning(f"  Segment {i}: Empty text, skipping")
                continue
            
            try:
                logger.info(f"  Synthesizing segment {i}...")
                # Synthesize without speaker cloning
                audio_file = os.path.join(output_dir, f"segment_{i:03d}.wav")
                audio_path = synthesizer.synthesize_text(hindi_text, audio_file)
                
                synthesized.append({
                    'segment': i,
                    'text': hindi_text[:50] + "...",
                    'audio_file': audio_path
                })
                logger.info(f"    ✓ Saved: {audio_path}")
                
            except Exception as e:
                logger.error(f"  ❌ Segment {i} failed: {e}")
                continue
        
        if not synthesized:
            logger.error("❌ No segments synthesized successfully")
            return False
        
        # Report results
        logger.info("\n" + "=" * 70)
        logger.info(f"✅ VOICE SYNTHESIS TEST SUCCESSFUL!")
        logger.info("=" * 70)
        logger.info(f"Synthesized: {len(synthesized)}/{len(test_segments)} segments")
        logger.info(f"Output directory: {output_dir}")
        logger.info("\nSynthesized segments:")
        for result in synthesized:
            logger.info(f"  {result['segment']}. {result['text']}")
            logger.info(f"     Audio: {result['audio_file']}")
        
        logger.info("\n" + "=" * 70)
        logger.info("Next steps:")
        logger.info("  1. Run full synthesis on all 14 segments")
        logger.info("  2. Mix with original audio timings")
        logger.info("  3. Generate final dubbed output")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
