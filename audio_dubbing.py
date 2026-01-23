"""
Audio Dubbing Main Pipeline
Complete orchestrator for multilingual audio dubbing
"""
import os
import json
from typing import Optional, Dict, Any
import config
from utils import get_logger, ensure_dir, save_segments_json, load_segments_json
from audio_processor import process_audio_pipeline, AudioProcessor
from speaker_diarization import diarize_audio_file
from transcription import transcribe_with_speaker_diarization
from translation import Translator
from voice_synthesis import VoiceSynthesizer
from audio_mixer import mix_dubbed_audio

logger = get_logger(__name__)


class AudioDubber:
    """
    Complete audio dubbing pipeline
    Takes an audio file, translates it to target language, and produces dubbed audio
    """
    
    def __init__(self, use_pyannote: bool = False):
        """
        Initialize audio dubber
        
        Args:
            use_pyannote: Whether to use PyAnnote for speaker diarization
        """
        self.use_pyannote = use_pyannote
        self.processor = AudioProcessor()
        self.translator = Translator()
        self.synthesizer = VoiceSynthesizer()
        
        logger.info("AudioDubber initialized")
    
    def dub_audio(self,
                  input_file: str,
                  target_language: str,
                  output_file: str,
                  preserve_background: bool = False,
                  save_intermediates: bool = True) -> Dict[str, Any]:
        """
        Complete dubbing pipeline
        
        Args:
            input_file: Path to input audio file
            target_language: Target language code ('en', 'hi', 'te')
            output_file: Path to save dubbed audio
            preserve_background: Whether to preserve background sounds
            save_intermediates: Whether to save intermediate files
            
        Returns:
            Dictionary with pipeline results and metadata
        """
        logger.info("=" * 80)
        logger.info("AUDIO DUBBING PIPELINE STARTED")
        logger.info("=" * 80)
        logger.info(f"Input: {input_file}")
        logger.info(f"Target Language: {target_language}")
        logger.info(f"Output: {output_file}")
        
        # Create working directory
        work_dir = config.TEMP_DIR
        ensure_dir(work_dir)
        ensure_dir(config.OUTPUT_DIR)
        
        results = {
            'input_file': input_file,
            'target_language': target_language,
            'output_file': output_file
        }
        
        try:
            # STEP 1-4: Audio Preprocessing
            logger.info("\n" + "=" * 80)
            logger.info("STEP 1-4: AUDIO PREPROCESSING")
            logger.info("=" * 80)
            
            clean_audio, vad_segments = process_audio_pipeline(input_file, work_dir)
            results['clean_audio'] = clean_audio
            results['vad_segments'] = len(vad_segments)
            
            # STEP 5: Speaker Diarization
            logger.info("\n" + "=" * 80)
            logger.info("STEP 5: SPEAKER DIARIZATION")
            logger.info("=" * 80)
            
            speaker_segments = diarize_audio_file(clean_audio, use_pyannote=self.use_pyannote)
            
            if save_intermediates:
                diarization_file = os.path.join(work_dir, 'speaker_segments.json')
                save_segments_json(speaker_segments, diarization_file)
            
            unique_speakers = set(seg['speaker'] for seg in speaker_segments)
            results['num_speakers'] = len(unique_speakers)
            results['speakers'] = list(unique_speakers)
            
            logger.info(f"Found {len(unique_speakers)} unique speakers")
            
            # STEP 5.5: Extract Reference Audio for Voice Cloning
            logger.info("\n" + "=" * 80)
            logger.info("STEP 5.5: EXTRACTING SPEAKER REFERENCE AUDIO")
            logger.info("=" * 80)
            
            speaker_refs = self._extract_reference_audio(clean_audio, speaker_segments, work_dir)
            results['speaker_refs'] = speaker_refs
            
            # STEP 6-8: Transcription & Language Detection
            logger.info("\n" + "=" * 80)
            logger.info("STEP 6-8: TRANSCRIPTION & LANGUAGE DETECTION")
            logger.info("=" * 80)
            
            detected_lang, transcribed_segments = transcribe_with_speaker_diarization(
                clean_audio, speaker_segments
            )
            
            results['detected_language'] = detected_lang
            results['detected_language_name'] = config.SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            
            logger.info(f"Detected language: {results['detected_language_name']} ({detected_lang})")
            
            if save_intermediates:
                transcription_file = os.path.join(work_dir, 'transcription.json')
                save_segments_json(transcribed_segments, transcription_file)
            
            # STEP 7: Validate Languages (Source ≠ Target)
            logger.info("\n" + "=" * 80)
            logger.info("STEP 7: LANGUAGE VALIDATION")
            logger.info("=" * 80)
            
            try:
                self.translator.validate_languages(detected_lang, target_language)
                logger.info(f"✓ Language validation passed: {detected_lang} → {target_language}")
            except ValueError as e:
                logger.error(f"✗ Language validation failed: {str(e)}")
                results['error'] = str(e)
                results['status'] = 'failed'
                return results
            
            # STEP 9: Translation
            logger.info("\n" + "=" * 80)
            logger.info("STEP 9: TRANSLATION")
            logger.info("=" * 80)
            
            translated_segments = self.translator.translate_segments(
                transcribed_segments,
                detected_lang,
                target_language
            )
            
            if save_intermediates:
                translation_file = os.path.join(work_dir, 'translated_segments.json')
                save_segments_json(translated_segments, translation_file)
            
            # STEP 10-12: Voice Synthesis
            logger.info("\n" + "=" * 80)
            logger.info("STEP 10-12: VOICE SYNTHESIS")
            logger.info("=" * 80)
            
            tts_dir = os.path.join(work_dir, 'tts_audio')
            synthesized_segments = self.synthesizer.synthesize_all_segments(
                translated_segments,
                target_language,
                tts_dir,
                speaker_refs=speaker_refs
            )
            
            if save_intermediates:
                synthesized_file = os.path.join(work_dir, 'synthesized_segments.json')
                save_segments_json(synthesized_segments, synthesized_file)
            
            # STEP 13-14: Audio Mixing
            logger.info("\n" + "=" * 80)
            logger.info("STEP 13-14: AUDIO MIXING & FINAL OUTPUT")
            logger.info("=" * 80)
            
            final_audio = mix_dubbed_audio(
                synthesized_segments,
                output_file,
                original_audio_path=clean_audio if preserve_background else None,
                preserve_background=preserve_background
            )
            
            results['status'] = 'success'
            results['num_segments'] = len(synthesized_segments)
            
            # Calculate duration
            total_duration = max(seg['end'] for seg in synthesized_segments) if synthesized_segments else 0
            results['duration_seconds'] = total_duration
            
            logger.info("\n" + "=" * 80)
            logger.info("AUDIO DUBBING PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            logger.info(f"✓ Input language: {results['detected_language_name']}")
            logger.info(f"✓ Target language: {config.SUPPORTED_LANGUAGES[target_language]}")
            logger.info(f"✓ Speakers: {len(unique_speakers)}")
            logger.info(f"✓ Segments: {len(synthesized_segments)}")
            logger.info(f"✓ Duration: {total_duration:.2f}s")
            logger.info(f"✓ Output: {output_file}")
            logger.info("=" * 80)
            
            return results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            results['status'] = 'failed'
            results['error'] = str(e)
            return results

    def _extract_reference_audio(self, audio_path: str, speaker_segments: List[Dict[str, Any]], work_dir: str) -> Dict[str, str]:
        """
        Extract multiple reference audio clips for each speaker and combine them
        for a richer voice profile (mini "fine-tuning").
        """
        speaker_refs = {}
        unique_speakers = list(set(seg['speaker'] for seg in speaker_segments))
        
        ref_dir = os.path.join(work_dir, 'speaker_refs')
        ensure_dir(ref_dir)
        
        logger.info(f"Extracting rich reference audio for {len(unique_speakers)} speakers...")
        
        from pydub import AudioSegment
        
        for speaker in unique_speakers:
            # Find segments for this speaker
            speaker_segs = [s for s in speaker_segments if s['speaker'] == speaker]
            if not speaker_segs:
                continue
                
            # Pick top 3 longest segments for a better profile
            speaker_segs.sort(key=lambda x: x['end'] - x['start'], reverse=True)
            top_segs = speaker_segs[:3]
            
            combined = AudioSegment.empty()
            total_dur = 0
            
            for i, seg in enumerate(top_segs):
                start, end = seg['start'], seg['end']
                temp_ref = os.path.join(ref_dir, f"{speaker}_part_{i}.wav")
                self.processor.extract_segment(audio_path, temp_ref, start, end)
                
                part = AudioSegment.from_wav(temp_ref)
                combined += part
                total_dur += len(part) / 1000.0
                
                # Cleanup temp part
                if os.path.exists(temp_ref):
                    os.remove(temp_ref)
                
                if total_dur >= 15.0: # 15s is usually plenty for XTTS
                    break
            
            ref_path = os.path.join(ref_dir, f"{speaker}_ref_rich.wav")
            combined.export(ref_path, format="wav")
            speaker_refs[speaker] = ref_path
            logger.info(f"  ✓ {speaker}: {total_dur:.2f}s rich reference created at {ref_path}")
                
        return speaker_refs


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Multilingual Audio Dubbing System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dub English audio to Hindi
  python audio_dubbing.py input.wav hi output.wav
  
  # Dub with PyAnnote speaker diarization
  python audio_dubbing.py input.wav te output.wav --use-pyannote
  
  # Preserve background sounds
  python audio_dubbing.py input.wav en output.wav --preserve-background

Supported languages:
  en - English
  hi - Hindi
  te - Telugu
        """
    )
    
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('target_lang', choices=['en', 'hi', 'te'],
                       help='Target language code')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--use-pyannote', action='store_true',
                       help='Use PyAnnote for speaker diarization (requires HF token)')
    parser.add_argument('--preserve-background', action='store_true',
                       help='Preserve background sounds from original')
    parser.add_argument('--no-intermediates', action='store_true',
                       help='Do not save intermediate files')
    
    args = parser.parse_args()
    
    # Create dubber
    dubber = AudioDubber(use_pyannote=args.use_pyannote)
    
    # Run pipeline
    results = dubber.dub_audio(
        input_file=args.input,
        target_language=args.target_lang,
        output_file=args.output,
        preserve_background=args.preserve_background,
        save_intermediates=not args.no_intermediates
    )
    
    # Print results
    if results['status'] == 'success':
        print("\n✓ Dubbing completed successfully!")
        print(f"  Output: {results['output_file']}")
        print(f"  Duration: {results['duration_seconds']:.2f}s")
        print(f"  Detected: {results['detected_language_name']}")
        print(f"  Speakers: {results['num_speakers']}")
    else:
        print(f"\n✗ Dubbing failed: {results.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
