import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from ..utils import get_logger, ensure_dir, save_json
from ..modules import Transcriber, Translator, VoiceCloner, SpeakerDiarizer
from ..processor import AudioProcessor, AudioMixer

logger = get_logger(__name__)

class DubbingPipeline:
    """Deployment-ready dubbing pipeline."""
    
    def __init__(self, src_lang: str, tgt_lang: str, use_gpu: bool = True, model_size: str = 'small'):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        
        # Initialize components
        self.processor = AudioProcessor()
        self.transcriber = Transcriber(model_name=model_size)
        self.diarizer = SpeakerDiarizer()
        self.translator = Translator()
        self.cloner = VoiceCloner(use_gpu=use_gpu)
        self.mixer = AudioMixer()

    def process(self, audio_path: str, output_path: str) -> Dict[str, Any]:
        """Execute the full dubbing pipeline and return metadata."""
        logger.info(f"Starting pipeline for {audio_path}")
        
        pipeline_metadata = {
            "detected_language": None,
            "detected_gender": None,
            "selected_voice": None
        }

        # 1. Transcribe & Diarize
        transcript = self.transcriber.transcribe_audio(audio_path, language=self.src_lang)
        
        # If auto-detected, update internal src_lang for subsequent steps (like Translation)
        detected_lang = transcript.get('language')
        if not self.src_lang and detected_lang:
            logger.info(f"Auto-detected source language as: {detected_lang}")
            self.src_lang = detected_lang

        pipeline_metadata["detected_language"] = self.src_lang

        transcript = self.diarizer.diarize(audio_path, transcript)
        
        print("\n" + "="*50)
        print(f"TRANSCRIPTION COMPLETE: {len(transcript['segments'])} segments found")
        if self.src_lang:
            print(f"DETECTED LANGUAGE: {self.src_lang.upper()}")
        print("="*50)
        for i, seg in enumerate(transcript['segments']):
            print(f"[{seg.get('speaker', 'S1')}] {seg.get('text', '')}")
        print("="*50 + "\n")

        # 2. Extract references
        ref_map = self.diarizer.extract_speaker_references(audio_path, transcript['segments'], "temp/refs")
        
        # 3. Translate
        print(f"Translating to {self.tgt_lang.upper()}...")
        translated = self.translator.translate_segments(transcript['segments'], self.src_lang, self.tgt_lang)
        
        print("\n" + "="*50)
        print(f"DUBBING PROGRESS (TRANSLATED):")
        print("="*50)
        for i, seg in enumerate(translated):
            orig = seg.get('original_text', seg.get('text', ''))
            trans = seg.get('translated_text', '')
            speaker = seg.get('speaker', 'S1')
            print(f"[{speaker}] {orig}")
            print(f"   └─> {trans}")
            print("-" * 20)
        print("="*50 + "\n")
        
        # 4. Synthesize
        from ..utils.helpers import normalize_language_code
        xtts_lang = normalize_language_code(self.tgt_lang, target_model='xtts')
        
        synthesized = self.cloner.batch_clone_voices(translated, ref_map, xtts_lang, "temp/syn")
        
        # Validation: Check if any audio was actually produced
        synthesized_count = sum(1 for seg in synthesized if seg.get('audio_path'))
        if synthesized_count == 0:
            logger.error("DUBBING FAILED: No segments were successfully synthesized. Check logs for model loading errors.")
            raise RuntimeError("Synthesis failed for all segments. Final output would be silent.")
        
        logger.info(f"Synthesized {synthesized_count}/{len(synthesized)} segments")
        
        # Capture metadata from cloning (e.g., voice used for first segment as a sample)
        # Note: In a multi-speaker scenario, this might only show one.
        # We'll try to find the gender/voice from the cloner logs or logic if exposed,
        # but for now, we can infer it or update VoiceCloner to return it.
        # Since VoiceCloner.batch_clone_voices returns the modified segments,
        # but doesn't explicitly return the "selected voice model", we might need to update VoiceCloner too
        # OR just rely on what we can get.

        # NOTE: To get the exact voice selected by Smart Matching, we'd need to update VoiceCloner.
        # However, for this pass, we can use the `_detect_gender` logic here if we wanted,
        # but better to let VoiceCloner handle it.
        # Let's assume we want to just pass back the output path for now,
        # but the plan said to return metadata.

        # HACK: Re-detect gender here just for metadata reporting if VoiceCloner doesn't return it
        # ideally VoiceCloner should return this info.
        try:
             # Basic check on the reference audio for the first speaker
             first_ref = ref_map.get('S1') or ref_map.get('default')
             if first_ref:
                 gender = self.cloner._detect_gender(first_ref)
                 pipeline_metadata["detected_gender"] = gender

                 # Infer voice model name
                 lang_key = xtts_lang.lower().split('-')[0]
                 voice_options = self.cloner.edge_voice_map.get(lang_key, self.cloner.edge_voice_map.get('en'))
                 if voice_options:
                     pipeline_metadata["selected_voice"] = voice_options.get(gender, "Unknown")
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")

        # 5. Mix
        output_file = self.mixer.mix_audio(synthesized, output_path, original_audio_path=audio_path)

        return {
            "output_path": output_file,
            "metadata": pipeline_metadata
        }
