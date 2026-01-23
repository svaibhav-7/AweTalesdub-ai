"""
Quick Start Script - M2M100 + Voice Cloning
Demonstrates the unified dubbing pipeline
"""
import os
import sys
from dubbing_pipeline import DubbingPipeline
from utils import get_logger

logger = get_logger(__name__)


def main():
    """Run dubbing pipeline with M2M100 + voice cloning"""
    
    # Configuration
    SOURCE_LANG = 'en'      # English
    TARGET_LANG = 'hi'      # Hindi (or 'te' for Telugu)
    AUDIO_FILE = 'test_audio/sample.wav'  # Your source audio
    
    # Optional: Speaker reference audio for voice cloning
    # If not provided, default voices will be used
    SPEAKER_AUDIO_MAP = {
        'S1': 'speaker_references/speaker1.wav',  # Male speaker
        'S2': 'speaker_references/speaker2.wav',  # Female speaker
    }
    
    try:
        # Initialize pipeline
        pipeline = DubbingPipeline(
            source_lang=SOURCE_LANG,
            target_lang=TARGET_LANG,
            use_gpu=True,
            save_intermediates=True
        )
        
        # Check if audio file exists
        if not os.path.exists(AUDIO_FILE):
            logger.error(f"Audio file not found: {AUDIO_FILE}")
            logger.info("Please provide a valid audio file")
            return
        
        # Optional: If speaker references don't exist, use default (pass empty dict)
        if not all(os.path.exists(path) for path in SPEAKER_AUDIO_MAP.values()):
            logger.warning("Speaker reference audio not found, using default voices")
            SPEAKER_AUDIO_MAP = {}
        
        # Execute pipeline
        output_file = pipeline.process(
            audio_path=AUDIO_FILE,
            speaker_audio_map=SPEAKER_AUDIO_MAP
        )
        
        logger.info(f"\n{'='*60}")
        logger.info("SUCCESS!")
        logger.info(f"Dubbed audio: {output_file}")
        logger.info(f"{'='*60}")
        
        # Print status
        status = pipeline.get_status()
        logger.info("\nPipeline Status:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")
        
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
    except Exception as e:
        logger.error(f"\nPipeline failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
