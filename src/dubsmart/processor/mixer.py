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
        
        # Sort segments by start time to ensures we process them in the correct order
        segments.sort(key=lambda x: x['start'])
        
        master = AudioSegment.empty()
        
        for i, seg in enumerate(segments):
            if not seg.get('audio_path'): continue
            
            # Load the synthesized audio for this segment
            audio_segment = AudioSegment.from_file(seg['audio_path'])
            
            # Smart Shift Logic:
            # 1. We want to start at the original timestamp: int(seg['start'] * 1000)
            # 2. BUT, we must not overlap with where the 'master' track currently ends.
            # 3. We also add a tiny 50ms buffer so words don't run into each other.
            
            original_start_ms = int(seg['start'] * 1000)
            min_allowed_start_ms = len(master) + 50  # 50ms buffer after previous segment
            
            # If it's the very first segment, we can allow it to start at 0 if needed
            if i == 0:
                min_allowed_start_ms = 0

            # The actual start time is the later of the two
            target_start_ms = max(original_start_ms, min_allowed_start_ms)
            
            # Calculate how much silence we need to add to reach that target start time
            silence_gap_ms = target_start_ms - len(master)
            
            # Append silence if needed (this "moves the cursor" to the target start time)
            if silence_gap_ms > 0:
                master += AudioSegment.silent(duration=silence_gap_ms)
            
            # Append the audio segment
            master += audio_segment
            
        master.export(output_path, format='wav')
        logger.info(f"Mixed audio saved to: {output_path}")
        return output_path
