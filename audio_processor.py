"""
Audio Processing Module
Handles audio extraction, conversion, noise suppression, and VAD
"""
import os
import subprocess
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import soundfile as sf
import torch
from typing import List, Tuple, Optional
import config
from utils import get_logger, ensure_dir

# Configure FFmpeg path for PyDub (using local installation)
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-essentials_build', 'bin')
FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
AudioSegment.converter = FFMPEG_EXE
AudioSegment.ffmpeg = FFMPEG_EXE
AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, 'ffprobe.exe')

logger = get_logger(__name__)


class AudioProcessor:
    """Handle all audio preprocessing operations"""
    
    def __init__(self):
        self.sample_rate = config.AUDIO_SETTINGS['sample_rate']
        self.channels = config.AUDIO_SETTINGS['channels']
        
    def extract_audio(self, video_path: str, output_path: str) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to input video file
            output_path: Path to save extracted audio
            
        Returns:
            Path to extracted audio file
        """
        logger.info(f"Extracting audio from {video_path}")
        
        cmd = [
            FFMPEG_EXE, '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM codec
            '-ar', str(self.sample_rate),  # Sample rate
            '-ac', str(self.channels),  # Mono
            '-y',  # Overwrite
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Audio extracted to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract audio: {e.stderr.decode()}")
            raise
    
    def convert_audio(self, input_path: str, output_path: str) -> str:
        """
        Convert audio to required format (mono, 16kHz)
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save converted audio
            
        Returns:
            Path to converted audio file
        """
        logger.info(f"Converting audio: {input_path}")
        
        # Load audio using pydub
        audio = AudioSegment.from_file(input_path)
        
        # Convert to mono
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Set sample rate
        if audio.frame_rate != self.sample_rate:
            audio = audio.set_frame_rate(self.sample_rate)
        
        # Export
        audio.export(output_path, format='wav')
        logger.info(f"Audio converted to {output_path}")
        
        return output_path
    
    def suppress_noise(self, input_path: str, output_path: str) -> str:
        """
        Apply noise suppression using ffmpeg afftdn filter
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save cleaned audio
            
        Returns:
            Path to noise-suppressed audio file
        """
        logger.info(f"Applying noise suppression to {input_path}")
        
        # Using ffmpeg's afftdn (FFT denoiser) filter
        cmd = [
            FFMPEG_EXE, '-i', input_path,
            '-af', f'afftdn=nf={config.NOISE_REDUCTION["noise_floor"]}',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Noise suppression applied, saved to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to suppress noise: {e.stderr.decode()}")
            # If noise suppression fails, copy original file
            logger.warning("Continuing without noise suppression")
            import shutil
            shutil.copy(input_path, output_path)
            return output_path
    
    def apply_vad(self, audio_path: str, return_speech_segments: bool = True) -> List[Tuple[float, float]]:
        """
        Apply Voice Activity Detection using Silero VAD
        
        Args:
            audio_path: Path to audio file
            return_speech_segments: If True, return list of (start, end) tuples
            
        Returns:
            List of speech segments as (start_time, end_time) in seconds
        """
        logger.info(f"Applying VAD to {audio_path}")
        
        try:
            # Load Silero VAD model
            model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=False
            )
            
            (get_speech_timestamps, _, read_audio, *_) = utils
            
            # Read audio
            wav = read_audio(audio_path, sampling_rate=self.sample_rate)
            
            # Get speech timestamps
            speech_timestamps = get_speech_timestamps(
                wav,
                model,
                sampling_rate=self.sample_rate,
                threshold=config.VAD_SETTINGS['threshold'],
                min_speech_duration_ms=int(config.VAD_SETTINGS['min_speech_duration'] * 1000),
                min_silence_duration_ms=int(config.VAD_SETTINGS['min_silence_duration'] * 1000)
            )
            
            # Convert to seconds
            segments = [
                (ts['start'] / self.sample_rate, ts['end'] / self.sample_rate)
                for ts in speech_timestamps
            ]
            
            logger.info(f"Found {len(segments)} speech segments")
            return segments
            
        except Exception as e:
            logger.error(f"VAD failed: {str(e)}")
            logger.warning("Continuing without VAD - assuming entire audio is speech")
            # Fallback: return entire audio duration
            audio = AudioSegment.from_file(audio_path)
            duration = len(audio) / 1000.0  # Convert to seconds
            return [(0.0, duration)]
    
    def extract_segment(self, input_path: str, output_path: str, 
                       start_time: float, end_time: float) -> str:
        """
        Extract a specific time segment from audio
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save segment
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            Path to extracted segment
        """
        audio = AudioSegment.from_file(input_path)
        
        # Convert to milliseconds
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        
        # Export
        segment.export(output_path, format='wav')
        
        return output_path
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0


def process_audio_pipeline(input_file: str, output_dir: str = config.TEMP_DIR) -> Tuple[str, List[Tuple[float, float]]]:
    """
    Complete audio preprocessing pipeline
    
    Args:
        input_file: Path to input audio/video file
        output_dir: Directory to save processed files
        
    Returns:
        Tuple of (processed_audio_path, speech_segments)
    """
    ensure_dir(output_dir)
    processor = AudioProcessor()
    
    # Determine file type
    _, ext = os.path.splitext(input_file)
    is_video = ext.lower() in ['.mp4', '.avi', '.mov', '.mkv']
    
    # Step 1: Extract audio if video
    if is_video:
        audio_raw = os.path.join(output_dir, 'audio_raw.wav')
        processor.extract_audio(input_file, audio_raw)
    else:
        audio_raw = input_file
    
    # Step 2: Convert to required format
    audio_converted = os.path.join(output_dir, 'audio_converted.wav')
    processor.convert_audio(audio_raw, audio_converted)
    
    # Step 3: Noise suppression
    audio_clean = os.path.join(output_dir, 'audio_clean.wav')
    processor.suppress_noise(audio_converted, audio_clean)
    
    # Step 4: Voice Activity Detection
    speech_segments = processor.apply_vad(audio_clean)
    
    logger.info(f"Audio preprocessing complete: {audio_clean}")
    logger.info(f"Found {len(speech_segments)} speech segments")
    
    return audio_clean, speech_segments


if __name__ == "__main__":
    # Test the audio processor
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_processor.py <input_audio_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    processed_audio, segments = process_audio_pipeline(input_file)
    
    print(f"\nProcessed audio: {processed_audio}")
    print(f"Speech segments: {len(segments)}")
    for i, (start, end) in enumerate(segments[:5]):  # Show first 5
        print(f"  Segment {i+1}: {start:.2f}s - {end:.2f}s")
