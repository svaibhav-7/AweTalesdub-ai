from typing import List, Dict, Any, Optional
from ..utils import get_logger

logger = get_logger(__name__)

class AudioMixer:
    """Combine synthesized segments into a final master track."""

    def mix_audio(self, segments: List[Dict[str, Any]], output_path: str, 
                  original_audio_path: Optional[str] = None) -> str:
        """Mix all segments based on timestamps."""
        from pydub import AudioSegment
        if not segments: return None
        
        total_duration = max(seg['end'] for seg in segments)
        master = AudioSegment.silent(duration=int(total_duration * 1000))
        
        for seg in segments:
            if not seg.get('audio_path'): continue
            audio = AudioSegment.from_file(seg['audio_path'])
            start_ms = int(seg['start'] * 1000)
            master = master.overlay(audio, position=start_ms)
            
        master.export(output_path, format='wav')
        logger.info(f"Mixed audio saved to: {output_path}")
        return output_path
