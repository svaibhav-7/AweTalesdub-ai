import os
import asyncio
import librosa
import numpy as np
from typing import Optional, List, Dict, Any
from pydub import AudioSegment
from ..utils import get_logger, get_temp_filename, ensure_dir

# SET EARLY: Disable weights_only for PyTorch 2.6+ compatibility with TTS models
os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'

logger = get_logger(__name__)

class VoiceCloner:
    """Advanced voice cloning using Coqui XTTS-v2 with Smart EdgeTTS fallback."""
    
    def __init__(self, use_gpu: bool = True):
        import torch
        self.use_gpu = use_gpu
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.model = None

        # Fix PyTorch 2.6+ weights_only issue for Coqui XTTS
        try:
            # Try to import and register the config class as a safe global
            from TTS.tts.configs.xtts_config import XttsConfig
            if hasattr(torch.serialization, 'add_safe_globals'):
                torch.serialization.add_safe_globals([XttsConfig])
                logger.info("Added XttsConfig to PyTorch safe globals.")
        except Exception as err:
            logger.warning(f"Could not auto-register XttsConfig: {err}. Will attempt weights_only=False on load.")
        
        # EdgeTTS Voice Database (Gender-mapped)
        self.edge_voice_map = {
            'en': {'male': 'en-US-ChristopherNeural', 'female': 'en-US-JennyNeural'},
            'es': {'male': 'es-ES-AlvaroNeural', 'female': 'es-ES-ElviraNeural'},
            'fr': {'male': 'fr-FR-HenriNeural', 'female': 'fr-FR-DeniseNeural'},
            'de': {'male': 'de-DE-KillianNeural', 'female': 'de-DE-KatjaNeural'},
            'it': {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
            'pt': {'male': 'pt-BR-AntonioNeural', 'female': 'pt-BR-FranciscaNeural'},
            'hi': {'male': 'hi-IN-MadhurNeural', 'female': 'hi-IN-SwaraNeural'},
            'te': {'male': 'te-IN-MohanNeural', 'female': 'te-IN-ShrutiNeural'},
        }

    def _load_model(self):
        if self.model is not None:
            return
        try:
            import os
            # Ensure weights_only is disabled via environment as a double safety
            os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'

            from TTS.api import TTS
        except ImportError:
            logger.warning("TTS library not installed. Using Smart EdgeTTS fallback.")
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

    def _detect_gender(self, audio_path: str) -> str:
        """Crude pitch-based gender detection (Fallback estimation)."""
        try:
            y, sr = librosa.load(audio_path, sr=None, duration=10.0)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

            # Extract pitch from high-magnitude bins
            threshold = np.max(magnitudes) * 0.1
            pitches = pitches[magnitudes > threshold]

            if len(pitches) == 0:
                return 'male' # Default

            # Calculate average pitch (f0)
            avg_pitch = np.mean(pitches)

            # Heuristic: < 165Hz = Male, > 165Hz = Female
            # This is a simplification but works for general cases.
            logger.info(f"Detected average pitch: {avg_pitch:.2f} Hz")
            return 'female' if avg_pitch > 165 else 'male'

        except Exception as e:
            logger.warning(f"Gender detection failed: {e}. Defaulting to male.")
            return 'male'

    def clone_voice(self, text: str, ref_wav: str, lang: str, output_path: str, speed: float = 1.0) -> str:
        """Synthesize text with voice cloning or smart matching."""
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
                logger.error(f"XTTS synthesis failed: {e}. Switching to Smart EdgeTTS fallback.")

        # Secondary: Smart EdgeTTS (Voice Matching)
        try:
            logger.info(f"Using Smart EdgeTTS fallback for {lang}...")

            # Detect gender from reference audio
            gender = self._detect_gender(ref_wav)
            logger.info(f"Matched input voice to gender: {gender.upper()}")

            # Select voice
            lang_key = lang.lower().split('-')[0]
            voice_options = self.edge_voice_map.get(lang_key, self.edge_voice_map['en'])
            voice = voice_options.get(gender, voice_options['male'])

            logger.info(f"Selected EdgeTTS Voice: {voice}")

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

        # Cache gender detection per speaker to avoid re-processing
        speaker_gender_cache = {}

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
