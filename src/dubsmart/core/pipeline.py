import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..utils import get_logger, ensure_dir, save_json
from ..modules import Transcriber, Translator, VoiceCloner, SpeakerDiarizer
from ..processor import AudioProcessor, AudioMixer

logger = get_logger(__name__)

class DubbingPipeline:
    """Deployment-ready dubbing pipeline."""
    
    def __init__(self, src_lang: str, tgt_lang: str, use_gpu: bool = True):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        
        # Initialize components
        self.processor = AudioProcessor()
        self.transcriber = Transcriber()
        self.diarizer = SpeakerDiarizer()
        self.translator = Translator()
        self.cloner = VoiceCloner(use_gpu=use_gpu)
        self.mixer = AudioMixer()

    def process(self, audio_path: str, output_path: str) -> str:
        """Execute the full dubbing pipeline."""
        logger.info(f"Starting pipeline for {audio_path}")
        
        # 1. Transcribe & Diarize
        transcript = self.transcriber.transcribe_audio(audio_path, language=self.src_lang)
        transcript = self.diarizer.diarize(audio_path, transcript)
        
        # 2. Extract references
        ref_map = self.diarizer.extract_speaker_references(audio_path, transcript['segments'], "temp/refs")
        
        # 3. Translate
        translated = self.translator.translate_segments(transcript['segments'], self.src_lang, self.tgt_lang)
        
        # 4. Synthesize
        synthesized = self.cloner.batch_clone_voices(translated, ref_map, self.tgt_lang, "temp/syn")
        
        # 5. Mix
        return self.mixer.mix_audio(synthesized, output_path, original_audio_path=audio_path)
