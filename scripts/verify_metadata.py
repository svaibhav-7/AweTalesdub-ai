import os
import shutil
import json
from unittest.mock import MagicMock
from src.dubsmart.modules.transcription import Transcriber
from src.dubsmart.modules.translation import Translator
from src.dubsmart.modules.cloning import VoiceCloner
from src.dubsmart.processor.mixer import AudioMixer
from src.dubsmart.core.pipeline import DubbingPipeline

def verify_pipeline():
    print("🚀 Starting Pipeline Verification (Metadata Check)...")

    # Setup paths
    audio_file = "test_audio/short_test.wav"
    output_dir = "output/verification"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Verification: Metadata Return
    print("\n[1/1] Verifying Pipeline Metadata...")
    try:
        # We need to run the full pipeline process method to check the return value
        # But we want to mock the heavy components to save time

        pipeline = DubbingPipeline(src_lang=None, tgt_lang='es', model_size="tiny")

        # Mock Translation
        pipeline.translator.translate_segments = MagicMock(return_value=[
            {'text': 'Hello world', 'translated_text': 'Hola mundo', 'start': 0.0, 'end': 2.0, 'speaker': 'S1'}
        ])

        # Mock Diarization (to avoid PyAnnote issues if any, though verify_pipeline passed before)
        # But let's use the real transcriber as it's fast enough with tiny

        output_path = os.path.join(output_dir, "metadata_test.wav")
        result = pipeline.process(audio_file, output_path)

        print(f"   ✅ Pipeline finished.")
        print(f"   🔍 Result keys: {result.keys()}")

        metadata = result.get('metadata', {})
        print(f"   🔍 Metadata: {metadata}")

        if 'detected_gender' in metadata and 'selected_voice' in metadata:
            print(f"   ✅ Metadata fields present.")
            print(f"   - Gender: {metadata['detected_gender']}")
            print(f"   - Voice: {metadata['selected_voice']}")
        else:
            print(f"   ❌ Metadata missing required fields!")

    except Exception as e:
        print(f"   ❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n✨ PIPELINE METADATA VERIFICATION COMPLETE ✨")

if __name__ == "__main__":
    verify_pipeline()
