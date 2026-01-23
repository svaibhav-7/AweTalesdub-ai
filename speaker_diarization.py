"""
Speaker Diarization Module
Identifies different speakers in audio and assigns speaker IDs
"""
import os
import numpy as np
from typing import List, Dict, Any, Optional
import torch
from pydub import AudioSegment
import config
from utils import get_logger, merge_overlapping_segments

logger = get_logger(__name__)


class SpeakerDiarizer:
    """Handle speaker diarization (identifying who speaks when)"""
    
    def __init__(self, use_pyannote: bool = True):
        """
        Initialize diarizer
        
        Args:
            use_pyannote: Whether to try using PyAnnote (requires HF token)
        """
        self.use_pyannote = use_pyannote and config.DIARIZATION_SETTINGS['use_pyannote']
        self.pipeline = None
        
        if self.use_pyannote:
            try:
                self._load_pyannote()
            except Exception as e:
                logger.warning(f"Failed to load PyAnnote: {str(e)}")
                logger.info("Falling back to simple diarization")
                self.use_pyannote = False
    
    def _load_pyannote(self):
        """Load PyAnnote diarization pipeline"""
        try:
            from pyannote.audio import Pipeline
            
            # Check for HuggingFace token
            token = config.HUGGINGFACE_TOKEN
            if not token:
                logger.warning("No HuggingFace token found - PyAnnote may not work")
                logger.info("Set HUGGINGFACE_TOKEN environment variable to use PyAnnote")
                self.use_pyannote = False
                return
            
            # Load pipeline
            logger.info("Loading PyAnnote diarization pipeline...")
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=token
            )
            
            # Use GPU if available
            if torch.cuda.is_available():
                self.pipeline.to(torch.device("cuda"))
            
            logger.info("PyAnnote pipeline loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load PyAnnote: {str(e)}")
            self.use_pyannote = False
    
    def diarize_audio(self, audio_path: str, 
                     min_speakers: Optional[int] = None,
                     max_speakers: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform speaker diarization on audio file
        
        Args:
            audio_path: Path to audio file
            min_speakers: Minimum number of speakers (None for auto)
            max_speakers: Maximum number of speakers (None for auto)
            
        Returns:
            List of segments with speaker IDs and timestamps
            Format: [{"speaker": "S1", "start": 0.0, "end": 2.5}, ...]
        """
        logger.info(f"Performing speaker diarization on {audio_path}")
        
        if self.use_pyannote and self.pipeline:
            segments = self._diarize_with_pyannote(audio_path, min_speakers, max_speakers)
        else:
            segments = self._diarize_simple(audio_path)
        
        logger.info(f"Diarization complete: {len(segments)} segments found")
        
        # Log speaker statistics
        speakers = set(seg['speaker'] for seg in segments)
        logger.info(f"Number of unique speakers: {len(speakers)}")
        
        return segments
    
    def _diarize_with_pyannote(self, audio_path: str,
                               min_speakers: Optional[int] = None,
                               max_speakers: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Diarize using PyAnnote pipeline
        
        Args:
            audio_path: Path to audio file
            min_speakers: Minimum number of speakers
            max_speakers: Maximum number of speakers
            
        Returns:
            List of speaker segments
        """
        logger.info("Using PyAnnote for diarization")
        
        # Set defaults from config
        if min_speakers is None:
            min_speakers = config.DIARIZATION_SETTINGS['min_speakers']
        if max_speakers is None:
            max_speakers = config.DIARIZATION_SETTINGS['max_speakers']
        
        # Run diarization
        diarization = self.pipeline(
            audio_path,
            min_speakers=min_speakers,
            max_speakers=max_speakers
        )
        
        # Convert to our format
        segments = []
        speaker_mapping = {}
        speaker_counter = 1
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # Map speaker labels to S1, S2, etc.
            if speaker not in speaker_mapping:
                speaker_mapping[speaker] = f"S{speaker_counter}"
                speaker_counter += 1
            
            segments.append({
                "speaker": speaker_mapping[speaker],
                "start": turn.start,
                "end": turn.end
            })
        
        # Sort by start time
        segments.sort(key=lambda x: x['start'])
        
        return segments
    
    def _diarize_simple(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Simple fallback diarization using energy-based segmentation
        This is a simplified approach suitable for demos
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of speaker segments
        """
        logger.info("Using simple energy-based diarization (fallback)")
        
        # Load audio
        audio = AudioSegment.from_file(audio_path)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        
        # Normalize
        if len(samples) > 0:
            samples = samples / np.max(np.abs(samples))
        
        sample_rate = audio.frame_rate
        
        # Calculate energy in windows
        window_size = int(0.5 * sample_rate)  # 500ms windows
        hop_size = int(0.25 * sample_rate)    # 250ms hop
        
        energies = []
        times = []
        
        for i in range(0, len(samples) - window_size, hop_size):
            window = samples[i:i+window_size]
            energy = np.sqrt(np.mean(window**2))  # RMS energy
            energies.append(energy)
            times.append(i / sample_rate)
        
        energies = np.array(energies)
        
        # Threshold for speech detection
        threshold = np.mean(energies) * 0.3
        
        # Find speech segments
        is_speech = energies > threshold
        
        # Find transitions
        segments = []
        in_speech = False
        start_time = 0
        
        for i, (time, speech) in enumerate(zip(times, is_speech)):
            if speech and not in_speech:
                # Start of speech
                start_time = time
                in_speech = True
            elif not speech and in_speech:
                # End of speech
                if time - start_time > 0.5:  # Min 0.5s segments
                    segments.append({
                        "speaker": "S1",  # Default to single speaker
                        "start": start_time,
                        "end": time
                    })
                in_speech = False
        
        # Add final segment if still in speech
        if in_speech and times:
            segments.append({
                "speaker": "S1",
                "start": start_time,
                "end": times[-1]
            })
        
        # For multi-speaker detection (very simple heuristic)
        # Alternate speakers based on pauses
        if len(segments) > 1:
            for i, seg in enumerate(segments):
                # Alternate between S1 and S2 if there's a long pause
                if i > 0:
                    pause = seg['start'] - segments[i-1]['end']
                    if pause > 1.0:  # If pause > 1 second, assume speaker change
                        seg['speaker'] = 'S2' if segments[i-1]['speaker'] == 'S1' else 'S1'
        
        logger.info(f"Simple diarization found {len(segments)} segments")
        return segments
    
    def merge_consecutive_segments(self, segments: List[Dict[str, Any]], 
                                   max_gap: float = 0.5) -> List[Dict[str, Any]]:
        """
        Merge consecutive segments from the same speaker
        
        Args:
            segments: List of speaker segments
            max_gap: Maximum gap to merge (seconds)
            
        Returns:
            Merged segments
        """
        if not segments:
            return []
        
        merged = [segments[0].copy()]
        
        for seg in segments[1:]:
            last = merged[-1]
            
            # Check if same speaker and close enough
            if (seg['speaker'] == last['speaker'] and 
                seg['start'] - last['end'] <= max_gap):
                # Merge
                last['end'] = seg['end']
            else:
                merged.append(seg.copy())
        
        return merged
    
    def diarize(self, audio_path: str, transcription: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform speaker diarization and merge with transcription
        
        Args:
            audio_path: Path to audio file
            transcription: Transcription dict with segments
            
        Returns:
            Transcription with speaker information added to segments
        """
        # Perform diarization
        speaker_segments = self.diarize_audio(audio_path)
        
        # Merge speaker information with transcription segments
        if 'segments' in transcription:
            transcription_segments = transcription['segments']
            
            # For each transcription segment, find the overlapping speaker
            for trans_seg in transcription_segments:
                trans_start = trans_seg.get('start', 0)
                trans_end = trans_seg.get('end', 0)
                
                # Find speaker segments that overlap with this transcription segment
                overlapping_speakers = []
                for speaker_seg in speaker_segments:
                    speaker_start = speaker_seg['start']
                    speaker_end = speaker_seg['end']
                    
                    # Check for overlap
                    if (speaker_start < trans_end and speaker_end > trans_start):
                        overlap_start = max(speaker_start, trans_start)
                        overlap_end = min(speaker_end, trans_end)
                        overlap_duration = overlap_end - overlap_start
                        
                        overlapping_speakers.append({
                            'speaker': speaker_seg['speaker'],
                            'overlap': overlap_duration
                        })
                
                # Assign the speaker with the most overlap
                if overlapping_speakers:
                    best_speaker = max(overlapping_speakers, key=lambda x: x['overlap'])
                    trans_seg['speaker'] = best_speaker['speaker']
                else:
                    # Fallback to first speaker
                    trans_seg['speaker'] = speaker_segments[0]['speaker'] if speaker_segments else 'S1'
        
        return transcription
    
    def extract_speaker_references(self, audio_path: str, segments: List[Dict[str, Any]], 
                                  output_dir: str, min_duration: float = 3.0) -> Dict[str, str]:
        """
        Extract reference audio clips for each speaker for voice cloning
        
        Args:
            audio_path: Path to source audio file
            segments: List of speaker segments from diarization
            output_dir: Directory to save reference audio files
            min_duration: Minimum duration for reference clips (seconds)
            
        Returns:
            Dictionary mapping speaker_id -> path_to_reference_audio
        """
        from utils import ensure_dir
        ensure_dir(output_dir)
        
        speaker_refs = {}
        unique_speakers = list(set(seg['speaker'] for seg in segments))
        
        logger.info(f"Extracting reference audio for {len(unique_speakers)} speakers...")
        
        # Load audio
        try:
            audio = AudioSegment.from_file(audio_path)
        except Exception as e:
            logger.error(f"Failed to load audio file {audio_path}: {str(e)}")
            return speaker_refs
        
        for speaker in unique_speakers:
            # Find all segments for this speaker
            speaker_segs = [s for s in segments if s['speaker'] == speaker]
            if not speaker_segs:
                continue
            
            # Sort by duration (longest first)
            speaker_segs.sort(key=lambda x: x['end'] - x['start'], reverse=True)
            
            # Try to find a segment that's long enough
            ref_segment = None
            for seg in speaker_segs:
                duration = seg['end'] - seg['start']
                if duration >= min_duration:
                    ref_segment = seg
                    break
            
            # If no segment is long enough, take the longest one
            if ref_segment is None and speaker_segs:
                ref_segment = speaker_segs[0]
            
            if ref_segment is None:
                logger.warning(f"No suitable segment found for speaker {speaker}")
                continue
            
            # Extract up to 10 seconds from the start of the segment
            start_time = ref_segment['start'] * 1000  # Convert to milliseconds
            duration = min(ref_segment['end'] - ref_segment['start'], 10.0)  # Max 10 seconds
            end_time = start_time + (duration * 1000)
            
            # Extract segment
            try:
                ref_audio = audio[start_time:end_time]
                ref_path = os.path.join(output_dir, f"{speaker}_reference.wav")
                ref_audio.export(ref_path, format="wav")
                
                speaker_refs[speaker] = ref_path
                logger.info(f"✓ Extracted {duration:.2f}s reference for {speaker}: {ref_path}")
                
            except Exception as e:
                logger.error(f"Failed to extract reference for {speaker}: {str(e)}")
        
        logger.info(f"Extracted references for {len(speaker_refs)} speakers")
        return speaker_refs


def diarize_audio_file(audio_path: str, use_pyannote: bool = True) -> List[Dict[str, Any]]:
    """
    Convenience function to diarize an audio file
    
    Args:
        audio_path: Path to audio file
        use_pyannote: Whether to try using PyAnnote
        
    Returns:
        List of speaker segments
    """
    diarizer = SpeakerDiarizer(use_pyannote=use_pyannote)
    segments = diarizer.diarize_audio(audio_path)
    
    # Merge consecutive segments from same speaker
    segments = diarizer.merge_consecutive_segments(segments)
    
    return segments


if __name__ == "__main__":
    # Test diarization
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python speaker_diarization.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    segments = diarize_audio_file(audio_file)
    
    print(f"\nDiarization Results:")
    print(f"Total segments: {len(segments)}")
    print("\nSegments:")
    
    for i, seg in enumerate(segments[:10]):  # Show first 10
        print(f"{i+1}. {seg['speaker']}: {seg['start']:.2f}s - {seg['end']:.2f}s "
              f"(duration: {seg['end']-seg['start']:.2f}s)")
