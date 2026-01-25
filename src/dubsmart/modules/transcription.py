import os
from typing import List, Dict, Any, Optional, Tuple
from ..utils import get_logger, save_json

logger = get_logger(__name__)

class Transcriber:
    """Handle speech-to-text transcription with language detection."""
    
    def __init__(self, model_name: str = 'base'):
        import whisper
        import torch
        self.whisper = whisper
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing Whisper model: {model_name} on {self.device}")
        self.model = self.whisper.load_model(self.model_name, device=self.device)
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Transcribe audio file."""
        logger.info(f"Transcribing audio: {audio_path}")
        result = self.model.transcribe(audio_path, language=language, task="transcribe")
        logger.info(f"Detected language: {result.get('language', 'unknown')}")
        return result

    def align_with_speakers(self, whisper_result: Dict[str, Any],
                           speaker_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Align Whisper segments with speaker diarization results."""
        whisper_segments = whisper_result.get("segments", [])
        aligned = []
        
        for wseg in whisper_segments:
            w_start, w_end = wseg['start'], wseg['end']
            w_text = wseg['text'].strip()
            if not w_text: continue
            
            best_speaker = "S1"
            max_overlap = 0
            for sseg in speaker_segments:
                overlap = max(0, min(w_end, sseg['end']) - max(w_start, sseg['start']))
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_speaker = sseg['speaker']
            
            aligned.append({
                "speaker": best_speaker,
                "start": w_start,
                "end": w_end,
                "text": w_text
            })
        return aligned
