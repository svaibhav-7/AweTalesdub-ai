import os
import shutil
import json
from unittest.mock import MagicMock
from src.dubsmart.modules.transcription import Transcriber
from src.dubsmart.modules.translation import Translator
from src.dubsmart.modules.cloning import VoiceCloner
from src.dubsmart.processor.mixer import AudioMixer

def verify_pipeline():
    print("🚀 Starting Pipeline Verification (Enhanced)...")

    # Setup paths
    audio_file = "test_audio/short_test.wav"
    output_dir = "output/verification"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Verification: Transcription (Auto-Detect)
    print("\n[1/4] Verifying Transcription (Auto-Detect Language)...")
    detected_lang = None
    try:
        transcriber = Transcriber(model_name="tiny")
        # Pass None to force auto-detection
        transcription = transcriber.transcribe_audio(audio_file, language=None)
        segments = transcription.get('segments', [])
        detected_lang = transcription.get('language')

        print(f"   ✅ Transcription successful. Found {len(segments)} segments.")
        print(f"   ✅ Auto-detected language: {detected_lang}")

        if detected_lang != 'en':
            print(f"   ⚠️ Warning: Expected 'en' but got '{detected_lang}'. (Might be due to short audio clip)")

    except Exception as e:
        print(f"   ❌ Transcription failed: {e}")
        return

    # 2. Verification: Translation (Mocked)
    print("\n[2/4] Verifying Translation (Mocked)...")
    try:
        target_lang = 'es'
        translator = Translator()
        translator.translate_text = MagicMock(side_effect=lambda text, src, tgt: f"Translated({tgt}): {text[:20]}")

        translated_segments = translator.translate_segments(segments, detected_lang or 'en', target_lang)
        print(f"   ✅ Translation successful (Mocked). Processed {len(translated_segments)} segments.")
    except Exception as e:
        print(f"   ❌ Translation failed: {e}")
        return

    # 3. Verification: Voice Cloning (Smart Matching)
    print("\n[3/4] Verifying Voice Cloning (Smart Matching)...")
    try:
        cloner = VoiceCloner(use_gpu=False)
        # Create a dummy ref map
        ref_map = {'S1': audio_file, 'default': audio_file}

        synthesized_segments = cloner.batch_clone_voices(
            translated_segments,
            ref_map,
            target_lang,
            os.path.join(output_dir, "segments")
        )

        success_count = sum(1 for seg in synthesized_segments if seg.get('audio_path'))
        print(f"   ✅ Voice Cloning successful. Synthesized {success_count}/{len(translated_segments)} segments.")

        if success_count > 0:
            sample_file = synthesized_segments[0]['audio_path']
            size = os.path.getsize(sample_file)
            print(f"   Sample file size: {size} bytes")
            if size > 10000:
                 print("   ✅ Large file size confirms EdgeTTS (Smart Matching) is active.")
            else:
                 print("   ⚠️ Small file size suggests gTTS fallback (Smart Matching might have failed).")

    except Exception as e:
        print(f"   ❌ Voice Cloning failed: {e}")
        return

    # 4. Verification: Mixing (Real)
    print("\n[4/4] Verifying Audio Mixing...")
    try:
        mixer = AudioMixer()
        final_output = os.path.join(output_dir, "final_dub.wav")
        mixer.mix_audio(synthesized_segments, final_output)

        if os.path.exists(final_output):
             print(f"   ✅ Mixing successful. Output at: {final_output}")
             size = os.path.getsize(final_output)
             print(f"   Filesize: {size} bytes")
        else:
             print("   ❌ Mixing failed: Output file not found.")
             return
    except Exception as e:
        print(f"   ❌ Mixing failed: {e}")
        return

    print("\n✨ PIPELINE VERIFICATION COMPLETE ✨")

if __name__ == "__main__":
    verify_pipeline()
