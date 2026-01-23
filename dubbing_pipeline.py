"""
Unified Dubbing Pipeline
Combines M2M100 translation + Coqui voice cloning for end-to-end dubbing
"""
import os
import json
from typing import Dict, List, Any, Optional
import torch
from datetime import datetime

from translation_optimized import M2M100Translator
from voice_cloning import VoiceCloner
from transcription import Transcriber
from speaker_diarization import SpeakerDiarizer
from audio_mixer import AudioMixer
import config
from utils import get_logger, ensure_dir, get_temp_filename

logger = get_logger(__name__)


class DubbingPipeline:
    """End-to-end dubbing pipeline with M2M100 + Coqui voice cloning"""
    
    def __init__(self, source_lang: str, target_lang: str, 
                 use_gpu: bool = True, save_intermediates: bool = True):
        """
        Initialize dubbing pipeline
        
        Args:
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'hi', 'te')
            use_gpu: Use GPU acceleration
            save_intermediates: Save intermediate results for debugging
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.use_gpu = use_gpu
        self.save_intermediates = save_intermediates
        
        # Pipeline stages
        self.transcriber = None
        self.diarizer = None
        self.translator = None
        self.voice_cloner = None
        self.mixer = None
        
        # State
        self.transcription = None
        self.translation = None
        self.synthesis = None
        self.final_audio = None
        self.speaker_references = None
        
        # Directories
        self.output_dir = config.OUTPUT_DIR
        self.temp_dir = config.TEMP_DIR
        ensure_dir(self.output_dir)
        ensure_dir(self.temp_dir)
        
        logger.info(f"DubbingPipeline initialized: {source_lang} → {target_lang}")
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize pipeline components"""
        try:
            logger.info("Initializing pipeline components...")
            
            # Translator
            self.translator = M2M100Translator(use_gpu=self.use_gpu)
            logger.info("✓ M2M100 Translator loaded")
            
            # Voice Cloner
            self.voice_cloner = VoiceCloner(use_gpu=self.use_gpu)
            logger.info("✓ Voice Cloner initialized")
            
            # Audio Mixer
            self.mixer = AudioMixer()
            logger.info("✓ Audio Mixer loaded")
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}")
            raise
    
    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Step 1: Transcribe audio
        
        Args:
            audio_path: Path to source audio file
            
        Returns:
            Transcription with segments
        """
        try:
            logger.info(f"Step 1: Transcribing audio ({self.source_lang})...")
            
            if self.transcriber is None:
                self.transcriber = Transcriber()
            
            # Transcribe
            self.transcription = self.transcriber.transcribe_audio(audio_path)
            
            # Perform speaker diarization
            if self.diarizer is None:
                self.diarizer = SpeakerDiarizer()
            
            self.transcription = self.diarizer.diarize(
                audio_path, 
                self.transcription
            )
            
            # Extract speaker reference audio for voice cloning
            speaker_ref_dir = os.path.join(self.temp_dir, 'speaker_references')
            segments = self.transcription.get('segments', [])
            self.speaker_references = self.diarizer.extract_speaker_references(
                audio_path, segments, speaker_ref_dir
            )
            
            # Save intermediates
            if self.save_intermediates:
                transcript_path = os.path.join(self.temp_dir, 'transcription.json')
                with open(transcript_path, 'w', encoding='utf-8') as f:
                    json.dump(self.transcription, f, indent=2, ensure_ascii=False)
                logger.info(f"Transcription saved: {transcript_path}")
            
            logger.info(f"✓ Transcription complete: {len(self.transcription.get('segments', []))} segments")
            return self.transcription
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise
    
    def translate(self, transcription: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Step 2: Translate transcription using M2M100
        
        Args:
            transcription: Transcription dict (uses self.transcription if None)
            
        Returns:
            Translation with segments
        """
        try:
            logger.info(f"Step 2: Translating text ({self.source_lang} → {self.target_lang})...")
            
            if transcription is None:
                transcription = self.transcription
            
            if transcription is None:
                raise ValueError("No transcription provided. Run transcribe() first.")
            
            # Extract segments
            segments = transcription.get('segments', [])
            
            # Batch translate for efficiency
            logger.info(f"Translating {len(segments)} segments with M2M100...")
            translated_segments = self.translator.translate_segments(
                segments,
                self.source_lang,
                self.target_lang
            )
            
            # Create translation result
            self.translation = {
                'source_lang': self.source_lang,
                'target_lang': self.target_lang,
                'segments': translated_segments,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save intermediates
            if self.save_intermediates:
                translation_path = os.path.join(self.temp_dir, 'translation.json')
                with open(translation_path, 'w', encoding='utf-8') as f:
                    json.dump(self.translation, f, indent=2, ensure_ascii=False)
                logger.info(f"Translation saved: {translation_path}")
            
            logger.info(f"✓ Translation complete: {len(translated_segments)} segments translated")
            return self.translation
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    def synthesize(self, translation: Optional[Dict] = None,
                  speaker_audio_map: Optional[Dict[str, str]] = None,
                  output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Step 3: Synthesize dubbed audio using voice cloning
        
        Args:
            translation: Translation dict (uses self.translation if None)
            speaker_audio_map: Mapping of speaker_id to reference audio path
            output_dir: Directory for synthesized audio
            
        Returns:
            List of synthesized segments
        """
        try:
            logger.info(f"Step 3: Synthesizing dubbed audio ({self.target_lang})...")
            
            if translation is None:
                translation = self.translation
            
            if translation is None:
                raise ValueError("No translation provided. Run translate() first.")
            
            if output_dir is None:
                output_dir = os.path.join(self.temp_dir, 'synthesized_audio')
            
            ensure_dir(output_dir)
            
            segments = translation.get('segments', [])
            
            # Create default speaker audio map if not provided
            if speaker_audio_map is None or not speaker_audio_map:
                if self.speaker_references:
                    speaker_audio_map = self.speaker_references
                    logger.info(f"Using extracted speaker references for voice cloning: {len(speaker_audio_map)} speakers")
                else:
                    logger.warning("No speaker audio provided and no references extracted, using default voices")
                    speaker_audio_map = {}
            
            # Synthesize segments
            logger.info(f"Synthesizing {len(segments)} segments with voice cloning...")
            synthesized_segments = self.voice_cloner.batch_clone_voices(
                segments,
                speaker_audio_map,
                self.target_lang,
                output_dir
            )
            
            self.synthesis = synthesized_segments
            
            # Save intermediates
            if self.save_intermediates:
                synthesis_path = os.path.join(self.temp_dir, 'synthesis.json')
                with open(synthesis_path, 'w', encoding='utf-8') as f:
                    json.dump(synthesized_segments, f, indent=2, ensure_ascii=False)
                logger.info(f"Synthesis metadata saved: {synthesis_path}")
            
            successful = sum(1 for s in synthesized_segments if s.get('audio_synthesized'))
            logger.info(f"✓ Synthesis complete: {successful}/{len(segments)} segments synthesized")
            return synthesized_segments
            
        except Exception as e:
            logger.error(f"Synthesis failed: {str(e)}")
            raise
    
    def mix(self, synthesis: Optional[List[Dict]] = None,
           original_audio: Optional[str] = None,
           output_path: Optional[str] = None) -> str:
        """
        Step 4: Mix synthesized audio into final dubbed output
        
        Args:
            synthesis: List of synthesized segments (uses self.synthesis if None)
            original_audio: Original audio (for reference)
            output_path: Path to save final dubbed audio
            
        Returns:
            Path to final dubbed audio
        """
        try:
            logger.info("Step 4: Mixing final dubbed audio...")
            
            if synthesis is None:
                synthesis = self.synthesis
            
            if synthesis is None:
                raise ValueError("No synthesis provided. Run synthesize() first.")
            
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    self.output_dir,
                    f"dubbed_{self.target_lang}_{timestamp}.wav"
                )
            
            # Mix audio
            self.final_audio = self.mixer.mix_audio(synthesis, output_path, original_audio_path=original_audio)
            
            logger.info(f"✓ Final dubbed audio: {self.final_audio}")
            return self.final_audio
            
        except Exception as e:
            logger.error(f"Mixing failed: {str(e)}")
            raise
    
    def process(self, audio_path: str, 
               speaker_audio_map: Optional[Dict[str, str]] = None,
               output_path: Optional[str] = None) -> str:
        """
        Execute complete dubbing pipeline
        
        Args:
            audio_path: Path to source audio
            speaker_audio_map: Mapping of speaker_id to reference audio
            output_path: Path for final dubbed audio
            
        Returns:
            Path to final dubbed audio
        """
        try:
            logger.info("=" * 60)
            logger.info("STARTING DUBBING PIPELINE")
            logger.info(f"Language: {self.source_lang} → {self.target_lang}")
            logger.info("=" * 60)
            
            # Step 1: Transcribe
            self.transcribe(audio_path)
            
            # Step 2: Translate
            self.translate()
            
            # Step 3: Synthesize
            self.synthesize(speaker_audio_map=speaker_audio_map)
            
            # Step 4: Mix
            final_audio = self.mix(original_audio=audio_path, output_path=output_path)
            
            logger.info("=" * 60)
            logger.info("DUBBING COMPLETE!")
            logger.info(f"Output: {final_audio}")
            logger.info("=" * 60)
            
            return final_audio
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'transcription': 'complete' if self.transcription else 'pending',
            'translation': 'complete' if self.translation else 'pending',
            'synthesis': 'complete' if self.synthesis else 'pending',
            'final_audio': self.final_audio,
        }
