"""
Transcription Module
Multilingual speech-to-text with automatic language detection using Whisper
"""
import os
import whisper
import torch
from typing import List, Dict, Any, Optional
import config
from utils import get_logger, save_segments_json

logger = get_logger(__name__)


class Transcriber:
    """Handle speech-to-text transcription with language detection"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize transcriber with Whisper model
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large)
        """
        if model_name is None:
            model_name = config.WHISPER_MODEL
        
        self.model_name = model_name
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing Whisper model: {model_name} on {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info(f"Whisper model '{self.model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str, 
                        language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file with automatic language detection
        
        Args:
            audio_path: Path to audio file
            language: Language code (if known), or None for auto-detection
            
        Returns:
            Dictionary with transcription results including detected language
        """
        logger.info(f"Transcribing audio: {audio_path}")
        
        # Transcribe with Whisper
        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",  # Use "translate" to force English translation
            verbose=False
        )
        
        detected_lang = result.get("language", "unknown")
        logger.info(f"Detected language: {detected_lang}")
        
        # Log some stats
        num_segments = len(result.get("segments", []))
        logger.info(f"Transcription complete: {num_segments} segments")
        
        return result
    
    def detect_language(self, audio_path: str) -> str:
        """
        Detect the language of audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Language code (e.g., 'en', 'hi', 'te')
        """
        logger.info(f"Detecting language for: {audio_path}")
        
        # Load audio
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        
        # Make log-Mel spectrogram
        mel = whisper.log_mel_spectrogram(audio).to(self.device)
        
        # Detect language
        _, probs = self.model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)
        confidence = probs[detected_lang]
        
        logger.info(f"Detected language: {detected_lang} (confidence: {confidence:.2%})")
        
        return detected_lang
    
    def align_with_speakers(self, whisper_result: Dict[str, Any],
                           speaker_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Align Whisper transcription with speaker diarization
        
        Args:
            whisper_result: Result from Whisper transcription
            speaker_segments: List of speaker segments from diarization
            
        Returns:
            Aligned segments with speaker IDs and text
        """
        logger.info("Aligning transcription with speaker segments")
        
        whisper_segments = whisper_result.get("segments", [])
        aligned = []
        
        # For each Whisper segment, find overlapping speaker segment
        for wseg in whisper_segments:
            w_start = wseg['start']
            w_end = wseg['end']
            w_text = wseg['text'].strip()
            
            if not w_text:
                continue
            
            # Find best matching speaker segment
            best_speaker = "S1"  # Default
            max_overlap = 0
            
            for sseg in speaker_segments:
                s_start = sseg['start']
                s_end = sseg['end']
                
                # Calculate overlap
                overlap_start = max(w_start, s_start)
                overlap_end = min(w_end, s_end)
                overlap = max(0, overlap_end - overlap_start)
                
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_speaker = sseg['speaker']
            
            aligned.append({
                "speaker": best_speaker,
                "start": w_start,
                "end": w_end,
                "text": w_text
            })
        
        logger.info(f"Aligned {len(aligned)} segments")
        return aligned
    
    def merge_consecutive_speaker_segments(self, segments: List[Dict[str, Any]],
                                          max_gap: float = 1.0) -> List[Dict[str, Any]]:
        """
        Merge consecutive segments from same speaker
        
        Args:
            segments: List of aligned segments
            max_gap: Maximum gap between segments to merge (seconds)
            
        Returns:
            Merged segments
        """
        if not segments:
            return []
        
        merged = [segments[0].copy()]
        
        for seg in segments[1:]:
            last = merged[-1]
            
            # Check if same speaker and close enough
            gap = seg['start'] - last['end']
            if seg['speaker'] == last['speaker'] and gap <= max_gap:
                # Merge text and extend time
                last['text'] += ' ' + seg['text']
                last['end'] = seg['end']
            else:
                merged.append(seg.copy())
        
        return merged


def transcribe_with_speaker_diarization(audio_path: str,
                                        speaker_segments: List[Dict[str, Any]],
                                        language: Optional[str] = None) -> tuple[str, List[Dict[str, Any]]]:
    """
    Transcribe audio and align with speaker segments
    
    Args:
        audio_path: Path to audio file
        speaker_segments: Speaker diarization results
        language: Language code (None for auto-detection)
        
    Returns:
        Tuple of (detected_language, aligned_segments)
        aligned_segments has format: [{"speaker": "S1", "start": 0.0, "end": 2.5, "text": "..."}, ...]
    """
    transcriber = Transcriber()
    
    # Transcribe
    result = transcriber.transcribe_audio(audio_path, language=language)
    detected_lang = result.get("language", "unknown")
    
    # Align with speakers
    aligned = transcriber.align_with_speakers(result, speaker_segments)
    
    # Merge consecutive segments from same speaker
    aligned = transcriber.merge_consecutive_speaker_segments(aligned)
    
    logger.info(f"Final transcription: {len(aligned)} segments, language: {detected_lang}")
    
    return detected_lang, aligned


if __name__ == "__main__":
    # Test transcription
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python transcription.py <audio_file> [speaker_segments.json]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    # Load speaker segments if provided
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            speaker_segments = json.load(f)
    else:
        # Default: single speaker for entire audio
        from audio_processor import AudioProcessor
        processor = AudioProcessor()
        duration = processor.get_audio_duration(audio_file)
        speaker_segments = [{"speaker": "S1", "start": 0.0, "end": duration}]
    
    # Transcribe
    detected_lang, segments = transcribe_with_speaker_diarization(
        audio_file, speaker_segments
    )
    
    print(f"\nDetected Language: {detected_lang}")
    print(f"Total segments: {len(segments)}\n")
    
    # Show results
    for i, seg in enumerate(segments[:10]):  # Show first 10
        print(f"{i+1}. [{seg['speaker']}] ({seg['start']:.2f}s - {seg['end']:.2f}s)")
        print(f"   {seg['text']}\n")
    
    # Save to file
    output_file = "transcription_output.json"
    save_segments_json(segments, output_file)
    print(f"Saved to {output_file}")
