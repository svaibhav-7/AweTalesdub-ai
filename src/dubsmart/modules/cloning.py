import os
import asyncio
from typing import Optional, List, Dict, Any
from pydub import AudioSegment
from ..utils import get_logger, get_temp_filename, ensure_dir

logger = get_logger(__name__)

class VoiceCloner:
    """Advanced voice cloning using Coqui XTTS-v2 with EdgeTTS and gTTS fallbacks."""
    
    def __init__(self, use_gpu: bool = True):
        import torch
        self.use_gpu = use_gpu
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.model = None
        self.edge_voices = {
            'en': 'en-US-ChristopherNeural',
            'es': 'es-ES-AlvaroNeural',
            'fr': 'fr-FR-HenriNeural',
            'de': 'de-DE-KillianNeural',
            'it': 'it-IT-DiegoNeural',
            'pt': 'pt-BR-AntonioNeural',
            'hi': 'hi-IN-MadhurNeural',
            'te': 'te-IN-MohanNeural',
            # Add more defaults as needed
        }
        
    def _load_model(self):
        if self.model is not None:
            return
        try:
            import os
            # Work around PyTorch 2.6 weights_only issue
            os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'

            from TTS.api import TTS
        except ImportError:
            logger.warning("TTS library not installed. Using EdgeTTS/gTTS fallback.")
            return

        try:
            logger.info("Loading Coqui XTTS-v2 model (Lazy Load)...")
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=self.device=="cuda")
        except Exception as e:
            logger.error(f"Failed to load Coqui model: {e}")
            logger.info("Model loading failed, will use fallback synthesis")

    async def _generate_edge_tts(self, text: str, voice: str, output_path: str):
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    def clone_voice(self, text: str, ref_wav: str, lang: str, output_path: str, speed: float = 1.0) -> str:
        """Synthesize text with voice cloning."""
        self._load_model()
        
        # Primary: Coqui XTTS-v2
        if self.model is not None:
            try:
                self.model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=ref_wav,
                    language=lang,
                    speed=speed
                )
                return output_path
            except Exception as e:
                logger.error(f"XTTS synthesis failed: {e}. Switching to EdgeTTS fallback.")

        # Secondary: EdgeTTS (Microsoft Edge Online TTS) - High Quality, Free
        try:
            logger.info(f"Using EdgeTTS fallback for {lang}...")
            # Normalize lang code (e.g., 'es' -> 'es')
            lang_key = lang.lower().split('-')[0]
            voice = self.edge_voices.get(lang_key, 'en-US-ChristopherNeural')

            # Run async function in synchronous context
            asyncio.run(self._generate_edge_tts(text, voice, output_path))

            # Verify file exists
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
            else:
                raise RuntimeError("EdgeTTS produced empty file")

        except Exception as e_edge:
            logger.error(f"EdgeTTS fallback failed: {e_edge}. Switching to gTTS.")

        # Tertiary: gTTS (Google Text-to-Speech) - Basic Quality
        try:
            from gtts import gTTS
            logger.info("Using gTTS fallback...")
            tts = gTTS(text=text, lang=lang)
            tts.save(output_path)
            return output_path
        except Exception as e_fallback:
            logger.error(f"gTTS fallback failed: {e_fallback}")
            return None

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
