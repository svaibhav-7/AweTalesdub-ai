import os
from typing import Optional, List, Dict, Any
from pydub import AudioSegment
from ..utils import get_logger, get_temp_filename, ensure_dir

logger = get_logger(__name__)

class VoiceCloner:
    """Advanced voice cloning using Coqui XTTS-v2."""
    
    def __init__(self, use_gpu: bool = True):
        import torch
        self.use_gpu = use_gpu
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.model = None
        
    def _load_model(self):
        if self.model is not None:
            return
        try:
            from TTS.api import TTS
        except ImportError:
            logger.warning("TTS library not installed. Using fallback.")
            return

        try:
            logger.info("Loading Coqui XTTS-v2 model (Lazy Load)...")
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=self.device=="cuda")
        except Exception as e:
            logger.error(f"Failed to load Coqui model: {e}")

    def clone_voice(self, text: str, ref_wav: str, lang: str, output_path: str, speed: float = 1.0) -> str:
        """Synthesize text with voice cloning."""
        self._load_model()
        if self.model is None:
            # Fallback logic could go here
            return None
        
        self.model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=ref_wav,
            language=lang,
            speed=speed
        )
        return output_path

    def batch_clone_voices(self, segments: List[Dict[str, Any]], 
                           ref_map: Dict[str, str], lang: str, output_dir: str) -> List[Dict[str, Any]]:
        """Process multiple segments."""
        ensure_dir(output_dir)
        for i, seg in enumerate(segments):
            speaker_id = seg.get('speaker', 'default')
            text = seg.get('translated_text', seg.get('text', ''))
            ref_wav = ref_map.get(speaker_id)
            
            if not text or not ref_wav: continue
            
            out_path = os.path.join(output_dir, f"seg_{i:03d}_{speaker_id}.wav")
            seg['audio_path'] = self.clone_voice(text, ref_wav, lang, out_path)
            seg['audio_synthesized'] = True if seg['audio_path'] else False
        return segments

    def extract_rich_embedding(self, audio_paths: List[str]) -> str:
        """Concatenate references for a richer profile (cloned from advanced)."""
        import numpy as np
        import librosa
        import soundfile as sf
        
        combined = []
        target_sr = 22050
        for path in audio_paths:
            if not os.path.exists(path): continue
            audio, sr = librosa.load(path, sr=None)
            if sr != target_sr: audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
            combined.append(librosa.effects.trim(audio)[0])
            combined.append(np.zeros(int(target_sr * 0.2)))
            
        if not combined: return None
        final_path = get_temp_filename(suffix='_rich_ref.wav')
        sf.write(final_path, np.concatenate(combined), target_sr)
        return final_path
