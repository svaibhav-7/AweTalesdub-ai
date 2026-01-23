"""
Voice Cloning Module
Effective voice cloning using Coqui XTTS-v2 for natural dubbing
"""
import os
import torch
import numpy as np
from typing import Optional, List, Dict, Any
from pydub import AudioSegment
import librosa
import soundfile as sf

try:
    from TTS.api import TTS
except ImportError:
    TTS = None

import config
from utils import get_logger, ensure_dir, get_temp_filename

logger = get_logger(__name__)

# Configure FFmpeg
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-essentials_build', 'bin')
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
if os.path.exists(FFMPEG_EXE):
    AudioSegment.converter = FFMPEG_EXE
    AudioSegment.ffmpeg = FFMPEG_EXE
    AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, 'ffprobe.exe')


class CoquiVoiceSynthesizer:
    """Enhanced TTS Synthesizer using Coqui XTTS-v2 with advanced voice cloning features"""
    
    def __init__(self, language: str = 'en', use_gpu: bool = True):
        self.language = language
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.cloner = VoiceCloner(use_gpu=use_gpu)
        logger.info(f"CoquiVoiceSynthesizer initialized for language: {language}")

    def synthesize_text(self, text: str, output_path: str, speaker_wav: Optional[str] = None) -> str:
        """Synthesize text using voice cloning if speaker_wav is provided"""
        if not speaker_wav:
            # If no speaker_wav, use a default speaker from XTTS if cloner supports it, 
            # or fallback to default synthesis.
            return self.cloner.clone_voice(text, None, self.language, output_path)
            
        return self.cloner.clone_voice(text, speaker_wav, self.language, output_path)


class VoiceCloner:
    """Advanced voice cloning using Coqui XTTS-v2"""
    
    LANGUAGE_CODES = {
        'en': 'en',
        'hi': 'hi',
        'te': 'te',
        'ta': 'ta',
        'ml': 'ml',
        'kn': 'kn',
        'fr': 'fr',
        'es': 'es',
        'de': 'de',
        'pt': 'pt',
        'zh': 'zh-cn',
        'ja': 'ja',
        'ko': 'ko',
        'ar': 'ar',
        'it': 'it',
        'ru': 'ru',
    }
    
    def __init__(self, use_gpu: bool = True):
        """
        Initialize Voice Cloner
        
        Args:
            use_gpu: Use GPU acceleration if available
        """
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.tts_model = None
        self.speaker_cache = {}  # Cache speaker embeddings
        
        logger.info(f"Voice Cloner initialized - Device: {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load Coqui XTTS-v2 model"""
        if TTS is None:
            logger.warning("TTS library not installed. Voice cloning will use fallback TTS.")
            logger.info("To enable voice cloning, install TTS with: pip install TTS")
            self.tts_model = None
            return
        
        try:
            logger.info("Loading Coqui XTTS-v2 model (this may take 1-2 minutes)...")
            
            # XTTS-v2 is the best multilingual model with speaker cloning
            self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=self.device=="cuda")
            
            logger.info("Coqui XTTS-v2 model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load Coqui model: {str(e)}")
            logger.warning("Voice cloning disabled. Using fallback TTS.")
            self.tts_model = None
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages"""
        lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'pt': 'Portuguese',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'it': 'Italian',
            'ru': 'Russian',
        }
        return lang_names
    
    def validate_speaker_audio(self, audio_path: str, min_duration: float = 2.0) -> bool:
        """
        Validate speaker reference audio
        
        Args:
            audio_path: Path to speaker reference audio
            min_duration: Minimum duration in seconds
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if not os.path.exists(audio_path):
                logger.warning(f"Speaker audio not found: {audio_path}")
                return False
            
            # Load audio
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            
            if duration < min_duration:
                logger.warning(f"Speaker audio too short: {duration:.2f}s (min {min_duration}s)")
                return False
            
            logger.debug(f"Speaker audio valid: {duration:.2f}s at {sr}Hz")
            return True
            
        except Exception as e:
            logger.error(f"Error validating speaker audio: {str(e)}")
            return False
    
    def prepare_speaker_audio(self, audio_path: str, target_sample_rate: int = 22050) -> str:
        """
        Prepare speaker reference audio for best cloning results.
        Includes trimming silence and normalization to improve embedding quality.
        
        Args:
            audio_path: Path to original speaker audio
            target_sample_rate: Target sample rate (default 22050Hz for XTTS)
            
        Returns:
            Path to processed speaker audio
        """
        try:
            logger.info(f"Preparing speaker audio: {audio_path}")
            
            # Load audio
            audio, sr = librosa.load(audio_path, sr=None)
            
            # Trim silence from both ends
            audio, _ = librosa.effects.trim(audio, top_db=20)
            
            # Resample if necessary
            if sr != target_sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sample_rate)
                sr = target_sample_rate
            
            # Normalize audio (loudness normalization)
            max_val = np.abs(audio).max()
            if max_val > 0:
                audio = audio / max_val * 0.9
            
            # Save processed audio
            processed_path = get_temp_filename(suffix='.wav')
            sf.write(processed_path, audio, sr)
            
            logger.debug(f"Speaker audio prepared: {processed_path}")
            return processed_path
            
        except Exception as e:
            logger.error(f"Error preparing speaker audio: {str(e)}")
            return audio_path # Fallback to original
    
    def clone_voice(self, text: str, speaker_audio_path: str, target_lang: str,
                   output_path: str, speed: float = 1.0) -> str:
        """
        Clone voice and synthesize speech
        
        Args:
            text: Text to synthesize
            speaker_audio_path: Path to speaker reference audio
            target_lang: Target language code
            output_path: Path to save output audio
            speed: Speech speed (0.5-2.0)
            
        Returns:
            Path to synthesized audio
        """
        if self.tts_model is None:
            logger.warning("TTS model not available, using fallback synthesis")
            return self._synthesize_fallback(text, target_lang, output_path, speed)
        
        if not text or not text.strip():
            logger.warning("Empty text provided for synthesis")
            return None
        
        try:
            # Validate language
            if target_lang not in self.LANGUAGE_CODES:
                logger.warning(f"Language {target_lang} not supported, falling back to English")
                target_lang = 'en'
            
            tts_lang = self.LANGUAGE_CODES[target_lang]
            
            # Validate and prepare speaker audio
            if not self.validate_speaker_audio(speaker_audio_path):
                logger.warning(f"Invalid speaker audio, using default voice")
                return self._synthesize_default(text, target_lang, output_path, speed)
            
            speaker_audio = self.prepare_speaker_audio(speaker_audio_path)
            
            logger.info(f"Cloning voice for language: {target_lang}")
            
            # Synthesize with speaker cloning and optimized parameters
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=speaker_audio,
                language=tts_lang,
                split_sentences=True,
                verbose=False,
                # Advanced parameters for better quality
                # Note: these depend on the specific XTTS-v2 implementation version
                repetition_penalty=2.0,
                temperature=0.75,
                speed=speed
            )
            
            logger.info(f"Voice cloning complete: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Voice cloning failed: {str(e)}")
            # Fallback to default synthesis
            return self._synthesize_default(text, target_lang, output_path, speed)
    
    def _synthesize_fallback(self, text: str, target_lang: str, 
                           output_path: str, speed: float = 1.0) -> str:
        """
        Fallback synthesis when TTS is not available
        
        Args:
            text: Text to synthesize
            target_lang: Target language code
            output_path: Path to save output audio
            speed: Speech speed
            
        Returns:
            Path to synthesized audio
        """
        logger.info(f"Using fallback TTS for {target_lang}")
        
        try:
            from gtts import gTTS
            
            # Map language codes
            gtts_lang_map = {
                'en': 'en',
                'hi': 'hi',
                'te': 'te',
                'ta': 'ta',
                'ml': 'ml',
                'kn': 'kn',
                'fr': 'fr',
                'es': 'es',
                'de': 'de',
                'pt': 'pt',
                'zh': 'zh-cn',
                'ja': 'ja',
                'ko': 'ko',
                'ar': 'ar',
                'it': 'it',
                'ru': 'ru',
            }
            
            lang = gtts_lang_map.get(target_lang, 'en')
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=False)
            temp_mp3 = output_path.replace('.wav', '.mp3')
            tts.save(temp_mp3)
            
            # Convert to WAV
            audio = AudioSegment.from_mp3(temp_mp3)
            audio.export(output_path, format="wav")
            
            # Clean up
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            
            # Apply speed adjustment if needed
            if speed != 1.0:
                output_path = self._adjust_speed(output_path, speed)
            
            logger.info(f"Fallback synthesis complete: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Fallback synthesis failed: {str(e)}")
            return self._synthesize_default(text, target_lang, output_path, speed)
    
    def _synthesize_default(self, text: str, target_lang: str, 
                           output_path: str, speed: float = 1.0) -> str:
        """
        Fallback: synthesize with default voice
        
        Args:
            text: Text to synthesize
            target_lang: Target language code
            output_path: Path to save output audio
            speed: Speech speed
            
        Returns:
            Path to synthesized audio
        """
        try:
            if target_lang not in self.LANGUAGE_CODES:
                target_lang = 'en'
            
            tts_lang = self.LANGUAGE_CODES[target_lang]
            
            logger.info(f"Using default voice for {target_lang}")
            
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                language=tts_lang,
                split_sentences=True,
                verbose=False
            )
            
            if speed != 1.0:
                output_path = self._adjust_speed(output_path, speed)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Default synthesis failed: {str(e)}")
            raise
    
    def _adjust_speed(self, audio_path: str, speed: float) -> str:
        """
        Adjust audio playback speed
        
        Args:
            audio_path: Path to audio file
            speed: Speed multiplier (0.5-2.0)
            
        Returns:
            Path to speed-adjusted audio (same as input if speed == 1.0)
        """
        if speed == 1.0:
            return audio_path
        
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=None)
            
            # Change speed using pitch-preserving algorithm
            y_stretched = librosa.effects.time_stretch(audio, rate=speed)
            
            # Save
            sf.write(audio_path, y_stretched, sr)
            logger.debug(f"Speed adjusted: {speed}x")
            
            return audio_path
            
        except Exception as e:
            logger.error(f"Speed adjustment failed: {str(e)}")
            return audio_path
    
    def batch_clone_voices(self, segments: List[Dict[str, Any]], 
                          speaker_audio_map: Dict[str, str],
                          target_lang: str,
                          output_dir: str) -> List[Dict[str, Any]]:
        """
        Clone voices for multiple segments
        
        Args:
            segments: List of segments with 'text' and 'speaker' keys
            speaker_audio_map: Mapping of speaker_id to audio file path
            target_lang: Target language code
            output_dir: Directory to save synthesized audio
            
        Returns:
            Segments with 'audio_path' added
        """
        ensure_dir(output_dir)
        
        for i, segment in enumerate(segments):
            try:
                speaker_id = segment.get('speaker', 'default')
                text = segment.get('text', '')
                
                if not text:
                    logger.warning(f"Segment {i} has no text")
                    continue
                
                # Get speaker audio
                speaker_audio = speaker_audio_map.get(speaker_id)
                if not speaker_audio:
                    logger.warning(f"No speaker audio for {speaker_id}, using default")
                    speaker_audio = list(speaker_audio_map.values())[0] if speaker_audio_map else None
                
                if not speaker_audio:
                    logger.error(f"No speaker audio available for segment {i}")
                    continue
                
                # Synthesize
                output_path = os.path.join(output_dir, f"segment_{i:04d}.wav")
                
                segment['audio_path'] = self.clone_voice(
                    text=text,
                    speaker_audio_path=speaker_audio,
                    target_lang=target_lang,
                    output_path=output_path
                )
                
                segment['audio_synthesized'] = True
                
            except Exception as e:
                logger.error(f"Failed to synthesize segment {i}: {str(e)}")
                segment['audio_synthesized'] = False
        
        logger.info(f"Batch voice cloning complete: {len(segments)} segments")
        return segments
