"""
Voice Synthesis Module
Text-to-speech with speaker-specific voices and timing alignment
"""
import os
from typing import List, Dict, Any, Optional
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import numpy as np
import config
from utils import get_logger, ensure_dir, get_temp_filename

try:
    from TTS.api import TTS
except ImportError:
    TTS = None

# Configure FFmpeg path for PyDub
# Configure FFmpeg path for PyDub
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-essentials_build', 'bin')
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
AudioSegment.converter = FFMPEG_EXE
AudioSegment.ffmpeg = FFMPEG_EXE
AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, 'ffprobe.exe')

logger = get_logger(__name__)


class VoiceSynthesizer:
    """Handle text-to-speech synthesis with multiple voices"""
    
    def __init__(self, tts_engine: str = None):
        """
        Initialize voice synthesizer
        
        Args:
            tts_engine: 'gtts', 'pyttsx3', or 'coqui'
        """
        if tts_engine is None:
            tts_engine = config.TTS_ENGINE
        
        self.engine = tts_engine
        self.voice_assignments = {}  # Track which voice is assigned to each speaker
        self.tts_model = None
        
        logger.info(f"Voice synthesizer initialized with engine: {tts_engine}")
        
        if self.engine == 'coqui' and TTS is not None:
            self._load_coqui_model()
    
    def assign_voices(self, speakers: List[str], target_lang: str) -> Dict[str, Dict[str, str]]:
        """
        Assign unique voices to each speaker for target language
        
        Args:
            speakers: List of unique speaker IDs
            target_lang: Target language code
            
        Returns:
            Dictionary mapping speaker_id -> voice_config
        """
        logger.info(f"Assigning voices for {len(speakers)} speakers in {target_lang}")
        
        voice_map = {}
        
        for i, speaker in enumerate(speakers):
            # Get voice from config
            if speaker in config.VOICE_MAPPING.get(target_lang, {}):
                voice_config = config.VOICE_MAPPING[target_lang][speaker]
            else:
                # Fallback: cycle through available voices
                available = list(config.VOICE_MAPPING.get(target_lang, {}).values())
                if available:
                    voice_config = available[i % len(available)]
                else:
                    # Ultimate fallback
                    voice_config = {
                        'gender': 'male' if i % 2 == 0 else 'female',
                        'name': target_lang,
                        'variant': 'default'
                    }
            
            voice_map[speaker] = voice_config
            logger.info(f"  {speaker} → {voice_config}")
        
        self.voice_assignments = voice_map
        return voice_map
    
    def synthesize_segment(self, text: str, 
                          speaker_id: str,
                          target_lang: str,
                          output_path: str,
                          target_duration: Optional[float] = None,
                          speaker_ref: Optional[str] = None) -> str:
        """
        Synthesize speech for a single segment
        
        Args:
            text: Text to synthesize
            speaker_id: Speaker ID
            target_lang: Target language code
            output_path: Path to save audio
            target_duration: Target duration in seconds (for timing alignment)
            speaker_ref: Optional path to reference audio for voice cloning
            
        Returns:
            Path to generated audio file
        """
        if not text.strip():
            # Create silence
            silence = AudioSegment.silent(duration=int((target_duration or 0.5) * 1000))
            silence.export(output_path, format='mp3')
            return output_path
        
        # Get voice config for this speaker
        voice_config = self.voice_assignments.get(speaker_id, {
            'name': target_lang,
            'gender': 'male'
        })
        
        # Synthesize based on engine
        if self.engine == 'gtts':
            audio_path = self._synthesize_gtts(text, voice_config, target_lang, output_path)
        elif self.engine == 'pyttsx3':
            audio_path = self._synthesize_pyttsx3(text, voice_config, output_path)
        elif self.engine == 'coqui':
            audio_path = self._synthesize_coqui(text, target_lang, output_path, speaker_ref)
        else:
            raise ValueError(f"Unknown TTS engine: {self.engine}")
        
        # Apply timing alignment if target duration is specified
        if target_duration:
            audio_path = self.align_timing(audio_path, target_duration, output_path)
        
        return audio_path
    
    def _synthesize_gtts(self, text: str, voice_config: Dict[str, str],
                        target_lang: str, output_path: str) -> str:
        """
        Synthesize using Google TTS
        
        Args:
            text: Text to synthesize
            voice_config: Voice configuration
            target_lang: Target language
            output_path: Output path
            
        Returns:
            Path to generated audio
        """
        try:
            # Get TLD for voice variation
            tld_map = {
                'en-us': 'com',
                'en-uk': 'co.uk',
                'en-au': 'com.au',
                'en-in': 'co.in',
                'hi-in': 'co.in',
                'te-in': 'co.in'
            }
            
            voice_name = voice_config.get('name', target_lang)
            tld = tld_map.get(voice_name, 'com')
            
            # Create TTS
            tts = gTTS(text=text, lang=target_lang, tld=tld, slow=False)
            
            # Save
            tts.save(output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"gTTS synthesis failed: {str(e)}")
            # Create silence as fallback
            silence = AudioSegment.silent(duration=1000)
            silence.export(output_path, format='mp3')
            return output_path
    
    def _synthesize_pyttsx3(self, text: str, voice_config: Dict[str, str],
                           output_path: str) -> str:
        """
        Synthesize using pyttsx3 (offline TTS)
        
        Args:
            text: Text to synthesize
            voice_config: Voice configuration
            output_path: Output path
            
        Returns:
            Path to generated audio
        """
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Configure voice
            voices = engine.getProperty('voices')
            
            # Try to match gender
            gender = voice_config.get('gender', 'male').lower()
            for voice in voices:
                if gender in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Set rate and volume
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 0.9)
            
            # Save
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            return output_path
            
        except Exception as e:
            logger.error(f"pyttsx3 synthesis failed: {str(e)}")
            # Fallback to gTTS
            return self._synthesize_gtts(text, voice_config, 'en', output_path)
    
    def _load_coqui_model(self):
        """Load Coqui XTTS model using the improved CoquiVoiceSynthesizer"""
        try:
            from voice_cloning import CoquiVoiceSynthesizer
            logger.info("Loading improved CoquiVoiceSynthesizer...")
            self.tts_model = CoquiVoiceSynthesizer()
            logger.info("Coqui XTTS model loaded successfully via CoquiVoiceSynthesizer")
        except Exception as e:
            logger.error(f"Failed to load Coqui model: {str(e)}")
            self.engine = 'gtts'  # Fallback
    
    def _synthesize_coqui(self, text: str, target_lang: str, 
                          output_path: str, speaker_ref: Optional[str] = None) -> str:
        """
        Synthesize using Coqui TTS (XTTS-v2) via the improved CoquiVoiceSynthesizer
        """
        if self.tts_model is None:
            logger.warning("Coqui TTS not available, falling back to gTTS")
            return self._synthesize_gtts(text, {}, target_lang, output_path)
            
        try:
            # The improved synthesizer handles reference audio and language internally
            self.tts_model.language = target_lang
            self.tts_model.synthesize_text(text, output_path, speaker_wav=speaker_ref)
            return output_path
            
        except Exception as e:
            logger.error(f"Coqui synthesis failed: {str(e)}")
            # Fallback to gTTS
            return self._synthesize_gtts(text, {}, target_lang, output_path)
    
    def align_timing(self, audio_path: str, target_duration: float,
                    output_path: str) -> str:
        """
        Adjust audio to match target duration
        
        Args:
            audio_path: Path to input audio
            target_duration: Target duration in seconds
            output_path: Path to save adjusted audio
            
        Returns:
            Path to time-aligned audio
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            current_duration = len(audio) / 1000.0  # Convert to seconds
            
            if abs(current_duration - target_duration) < 0.1:
                # Close enough, no adjustment needed
                if audio_path != output_path:
                    audio.export(output_path, format='mp3')
                return output_path
            
            # Calculate speed factor
            speed_factor = current_duration / target_duration
            
            # Limit speed changes to reasonable range
            min_speed, max_speed = config.PROSODY_SETTINGS['speed_range']
            speed_factor = max(min_speed, min(max_speed, speed_factor))
            
            if speed_factor > 1.0:
                # Speed up
                audio = speedup(audio, playback_speed=speed_factor)
            else:
                # Slow down (by changing frame rate)
                new_sample_rate = int(audio.frame_rate * speed_factor)
                audio = audio._spawn(audio.raw_data, overrides={
                    'frame_rate': new_sample_rate
                }).set_frame_rate(audio.frame_rate)
            
            # Adjust to exact duration with silence padding or trimming
            current_ms = len(audio)
            target_ms = int(target_duration * 1000)
            
            if current_ms < target_ms:
                # Add silence padding
                silence_needed = target_ms - current_ms
                silence = AudioSegment.silent(duration=silence_needed)
                audio = audio + silence
            elif current_ms > target_ms:
                # Trim
                audio = audio[:target_ms]
            
            # Export
            audio.export(output_path, format='mp3')
            
            logger.debug(f"Aligned audio: {current_duration:.2f}s → {target_duration:.2f}s")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Timing alignment failed: {str(e)}")
            # Return original
            if audio_path != output_path:
                import shutil
                shutil.copy(audio_path, output_path)
            return output_path
    
    def synthesize_all_segments(self, segments: List[Dict[str, Any]],
                               target_lang: str,
                               output_dir: str,
                               speaker_refs: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Synthesize TTS for all segments
        
        Args:
            segments: List of segments with 'translated_text'
            target_lang: Target language code
            output_dir: Directory to save audio files
            speaker_refs: Optional mapping of speaker_id to reference audio file
            
        Returns:
            Segments with 'audio_file' field added
        """
        ensure_dir(output_dir)
        
        # Get unique speakers
        speakers = list(set(seg['speaker'] for seg in segments))
        
        # Assign voices
        self.assign_voices(speakers, target_lang)
        
        logger.info(f"Synthesizing {len(segments)} segments")
        
        synthesized = []
        
        for i, seg in enumerate(segments):
            # Get text and duration
            text = seg.get('translated_text', seg.get('text', ''))
            duration = seg['end'] - seg['start']
            speaker = seg['speaker']
            
            # Generate filename
            audio_file = os.path.join(output_dir, f"seg_{i:04d}_{speaker}.mp3")
            
            # Synthesize
            self.synthesize_segment(
                text=text,
                speaker_id=speaker,
                target_lang=target_lang,
                output_path=audio_file,
                target_duration=duration,
                speaker_ref=speaker_refs.get(speaker) if speaker_refs else None
            )
            
            # Add to segment
            new_seg = seg.copy()
            new_seg['audio_file'] = audio_file
            synthesized.append(new_seg)
            
            # Log progress
            if (i + 1) % 10 == 0:
                logger.info(f"Synthesized {i + 1}/{len(segments)} segments")
        
        logger.info(f"Voice synthesis complete: {len(synthesized)} segments")
        return synthesized


if __name__ == "__main__":
    # Test voice synthesis
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("Usage: python voice_synthesis.py <segments.json> <target_lang>")
        print("Example: python voice_synthesis.py translated_segments.json hi")
        sys.exit(1)
    
    segments_file = sys.argv[1]
    target_lang = sys.argv[2]
    
    # Load segments
    with open(segments_file, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    
    # Synthesize
    synthesizer = VoiceSynthesizer()
    output_dir = os.path.join(config.TEMP_DIR, 'tts_output')
    
    synthesized = synthesizer.synthesize_all_segments(segments, target_lang, output_dir)
    
    # Show results
    print(f"\nVoice Synthesis Results:\n")
    for i, seg in enumerate(synthesized[:5]):  # Show first 5
        print(f"{i+1}. [{seg['speaker']}] {seg['audio_file']}")
        print(f"   Duration: {seg['end']-seg['start']:.2f}s")
        print(f"   Text: {seg.get('translated_text', seg.get('text', ''))}\n")
    
    # Save
    output_file = segments_file.replace('.json', '_synthesized.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(synthesized, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to {output_file}")
