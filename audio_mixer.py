"""
Audio Mixing Module
Combines all speaker audio tracks into final dubbed audio
"""
import os
from typing import List, Dict, Any, Optional
from pydub import AudioSegment
import config
from utils import get_logger, ensure_dir

# Configure FFmpeg path for PyDub
# Configure FFmpeg path for PyDub
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-essentials_build', 'bin')
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
AudioSegment.converter = FFMPEG_EXE
AudioSegment.ffmpeg = FFMPEG_EXE
AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, 'ffprobe.exe')

logger = get_logger(__name__)


class AudioMixer:
    """Handle combining multiple audio segments into final output"""
    
    def __init__(self):
        """Initialize audio mixer"""
        self.sample_rate = config.AUDIO_SETTINGS['sample_rate']
    
    def create_silence(self, duration_seconds: float) -> AudioSegment:
        """
        Create a silent audio segment
        
        Args:
            duration_seconds: Duration in seconds
            
        Returns:
            AudioSegment with silence
        """
        duration_ms = int(duration_seconds * 1000)
        return AudioSegment.silent(duration=duration_ms)
    
    def load_segment_audio(self, audio_path: str) -> AudioSegment:
        """
        Load audio segment from file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            AudioSegment
        """
        try:
            return AudioSegment.from_file(audio_path)
        except Exception as e:
            logger.error(f"Failed to load audio {audio_path}: {str(e)}")
            # Return 1 second of silence as fallback
            return self.create_silence(1.0)
    
    def overlay_segments(self, segments: List[Dict[str, Any]], 
                        total_duration: float) -> AudioSegment:
        """
        Overlay all segments at their correct timestamps
        
        Args:
            segments: List of segments with 'audio_file', 'start', 'end'
            total_duration: Total duration of output audio
            
        Returns:
            Combined AudioSegment
        """
        logger.info(f"Overlaying {len(segments)} segments")
        
        # Start with silence
        output = self.create_silence(total_duration)
        
        for i, seg in enumerate(segments):
            audio_file = seg.get('audio_path') or seg.get('audio_file')
            if not audio_file or not os.path.exists(audio_file):
                logger.warning(f"Audio file not found for segment {i}: {audio_file}")
                continue
            
            # Load segment audio
            segment_audio = self.load_segment_audio(audio_file)
            
            # Calculate allocated duration for this segment
            allocated_duration_ms = int((seg['end'] - seg['start']) * 1000)
            
            # Trim audio to fit allocated duration if it's longer
            if len(segment_audio) > allocated_duration_ms:
                logger.info(f"Trimming segment {i} from {len(segment_audio)/1000:.2f}s to {allocated_duration_ms/1000:.2f}s")
                segment_audio = segment_audio[:allocated_duration_ms]
            elif len(segment_audio) < allocated_duration_ms:
                # Pad with silence if shorter (though this shouldn't happen with proper synthesis)
                padding_ms = allocated_duration_ms - len(segment_audio)
                silence = self.create_silence(padding_ms / 1000)
                segment_audio = segment_audio + silence
                logger.debug(f"Padded segment {i} with {padding_ms/1000:.2f}s silence")
            
            # Get position
            start_ms = int(seg['start'] * 1000)
            
            # Overlay at position
            output = output.overlay(segment_audio, position=start_ms)
            
            if (i + 1) % 50 == 0:
                logger.info(f"Overlaid {i + 1}/{len(segments)} segments")
        
        logger.info("Overlay complete")
        return output
    
    def mix_audio(self, segments: List[Dict[str, Any]],
                  output_path: str,
                  background_audio_path: Optional[str] = None,
                  original_audio_path: Optional[str] = None) -> str:
        """
        Mix all segments into final audio output
        
        Args:
            segments: List of segments with audio files and timing
            output_path: Path to save final mixed audio
            background_audio_path: Optional background audio to preserve
            original_audio_path: Optional original audio path to match duration
            
        Returns:
            Path to final audio file
        """
        logger.info(f"Mixing {len(segments)} segments into {output_path}")
        
        # Calculate total duration - prefer original audio duration if provided
        if original_audio_path and os.path.exists(original_audio_path):
            try:
                original_audio = AudioSegment.from_file(original_audio_path)
                total_duration = len(original_audio) / 1000
                logger.info(f"Using original audio duration: {total_duration:.2f}s")
            except Exception as e:
                logger.warning(f"Could not load original audio duration: {str(e)}")
                total_duration = max(seg['end'] for seg in segments) if segments else 1.0
        else:
            total_duration = max(seg['end'] for seg in segments) if segments else 1.0
        
        # Overlay all segments
        mixed_audio = self.overlay_segments(segments, total_duration)
        
        # Add background audio if provided
        if background_audio_path and os.path.exists(background_audio_path):
            logger.info(f"Adding background audio from {background_audio_path}")
            mixed_audio = self._add_background(mixed_audio, background_audio_path)
        
        # Export
        logger.info(f"Exporting mixed audio to {output_path}")
        mixed_audio.export(output_path, format='wav')
        
        logger.info(f"Audio mixing complete: {output_path}")
        return output_path
    
    def _add_background(self, foreground: AudioSegment, 
                       background_path: str) -> AudioSegment:
        """
        Add background audio (like music or ambient sound)
        
        Args:
            foreground: Main dubbed audio
            background_path: Path to background audio
            
        Returns:
            Mixed audio with background
        """
        try:
            background = AudioSegment.from_file(background_path)
            
            # Match length
            fg_duration = len(foreground)
            bg_duration = len(background)
            
            if bg_duration < fg_duration:
                # Loop background if too short
                repeats = (fg_duration // bg_duration) + 1
                background = background * repeats
            
            # Trim to match foreground
            background = background[:fg_duration]
            
            # Reduce background volume
            background = background - 20  # -20 dB
            
            # Overlay foreground on background
            mixed = background.overlay(foreground)
            
            return mixed
            
        except Exception as e:
            logger.error(f"Failed to add background audio: {str(e)}")
            return foreground
    
    def extract_background_audio(self, original_audio_path: str,
                                 speech_segments: List[Dict[str, Any]],
                                 output_path: str) -> str:
        """
        Extract non-speech portions (background sounds) from original audio
        
        Args:
            original_audio_path: Path to original audio
            speech_segments: List of speech segments to remove
            output_path: Path to save background audio
            
        Returns:
            Path to background audio file
        """
        try:
            logger.info("Extracting background audio")
            
            # Load original
            audio = AudioSegment.from_file(original_audio_path)
            total_duration = len(audio)
            
            # Create mask for speech regions
            background = self.create_silence(total_duration / 1000.0)
            
            # Copy non-speech regions
            last_end = 0
            
            for seg in speech_segments:
                start_ms = int(seg['start'] * 1000)
                
                # Copy background between last_end and current start
                if start_ms > last_end:
                    bg_segment = audio[last_end:start_ms]
                    background = background.overlay(bg_segment, position=last_end)
                
                last_end = int(seg['end'] * 1000)
            
            # Copy remaining background
            if last_end < total_duration:
                bg_segment = audio[last_end:]
                background = background.overlay(bg_segment, position=last_end)
            
            # Export
            background.export(output_path, format='wav')
            logger.info(f"Background audio saved to {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to extract background: {str(e)}")
            return None


def mix_dubbed_audio(segments: List[Dict[str, Any]],
                    output_path: str,
                    original_audio_path: Optional[str] = None,
                    preserve_background: bool = False) -> str:
    """
    Convenience function to mix dubbed audio
    
    Args:
        segments: Segments with synthesized audio files
        output_path: Path to save final audio
        original_audio_path: Optional original audio for background extraction
        preserve_background: Whether to preserve background sounds
        
    Returns:
        Path to final mixed audio
    """
    mixer = AudioMixer()
    
    background_path = None
    
    if preserve_background and original_audio_path:
        # Extract background from original
        background_path = output_path.replace('.wav', '_background.wav')
        mixer.extract_background_audio(original_audio_path, segments, background_path)
    
    # Mix audio
    final_audio = mixer.mix_audio(segments, output_path, background_path)
    
    return final_audio


if __name__ == "__main__":
    # Test audio mixing
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python audio_mixer.py <segments_with_audio.json> [output.wav]")
        sys.exit(1)
    
    segments_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "mixed_output.wav"
    
    # Load segments
    with open(segments_file, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    
    # Mix
    final_path = mix_dubbed_audio(segments, output_file)
    
    print(f"\nAudio mixing complete!")
    print(f"Output: {final_path}")
    print(f"Duration: {max(seg['end'] for seg in segments):.2f} seconds")
