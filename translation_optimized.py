"""
Optimized Translation Module
Enhanced M2M100 for script translation with batch processing and quality improvements
"""
from typing import List, Dict, Any, Optional
import os
import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import config
from utils import get_logger

logger = get_logger(__name__)


class M2M100Translator:
    """Optimized M2M100 translator for multi-language dubbing scripts"""
    
    # Language code mapping for M2M100
    # Using simpler 2-letter codes that work with get_lang_id()
    M2M100_LANG_CODES = {
        'en': 'en',
        'hi': 'hi',
        'te': 'te',
        'ta': 'ta',
        'ml': 'ml',
        'kn': 'kn',
        'mr': 'mr',
        'gu': 'gu',
        'pa': 'pa',
        'ur': 'ur',
        'bn': 'bn',
        'or': 'or',
        'as': 'as',
        'fr': 'fr',
        'es': 'es',
        'de': 'de',
        'pt': 'pt',
        'zh': 'zh',
        'ja': 'ja',
        'ko': 'ko',
        'ar': 'ar',
        'it': 'it',
        'ru': 'ru',
    }
    
    def __init__(self, model_size: str = '418M', use_gpu: bool = True):
        """
        Initialize M2M100 translator
        
        Args:
            model_size: '418M' or '1.2B' (larger is more accurate but slower)
            use_gpu: Use GPU acceleration if available
        """
        self.model_size = model_size
        self.device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        self.model_name = f"facebook/m2m100_{model_size}"
        
        self.model = None
        self.tokenizer = None
        
        logger.info(f"M2M100Translator initialized - Model: {self.model_name}, Device: {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load model and tokenizer"""
        try:
            logger.info(f"Loading M2M100 model: {self.model_name}")
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
            self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            # Enable mixed precision for faster inference
            if self.device == "cuda":
                self.model.half()  # Use float16 for faster inference
                
            logger.info("M2M100 model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load M2M100 model: {str(e)}")
            raise
    
    def _get_m2m_lang_code(self, lang_code: str) -> str:
        """
        Get M2M100 language code from standard ISO code
        
        Args:
            lang_code: Standard language code (e.g., 'en', 'hi', 'te')
            
        Returns:
            M2M100 language code that works with tokenizer
            
        Raises:
            ValueError: If language is not supported
        """
        # Direct mapping - M2M100 uses simple language codes internally
        # but the tokenizer expects the codes it has tokens for
        if lang_code not in self.M2M100_LANG_CODES:
            raise ValueError(
                f"Language '{lang_code}' not supported. "
                f"Supported: {', '.join(sorted(self.M2M100_LANG_CODES.keys()))}"
            )
        
        # Check if tokenizer has this language
        try:
            self.tokenizer.get_lang_token(lang_code)
            return lang_code
        except KeyError:
            # Fallback to a similar language
            fallbacks = {
                'te': 'hi',  # Telugu -> Hindi
                'ta': 'hi',  # Tamil -> Hindi
                'ml': 'hi',  # Malayalam -> Hindi
                'kn': 'hi',  # Kannada -> Hindi
                'mr': 'hi',  # Marathi -> Hindi
                'gu': 'hi',  # Gujarati -> Hindi
                'pa': 'hi',  # Punjabi -> Hindi
                'ur': 'hi',  # Urdu -> Hindi
                'bn': 'hi',  # Bengali -> Hindi
                'or': 'hi',  # Odia -> Hindi
                'as': 'hi',  # Assamese -> Hindi
            }
            fallback = fallbacks.get(lang_code, 'en')
            logger.warning(f"Language '{lang_code}' not supported by M2M100 tokenizer, using '{fallback}' as fallback")
            return fallback
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using M2M100
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        try:
            # Get M2M codes
            src_code = self._get_m2m_lang_code(source_lang)
            tgt_code = self._get_m2m_lang_code(target_lang)
            
            # Set source language
            self.tokenizer.src_lang = src_code
            
            # Tokenize with truncation for long texts
            encoded = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding='longest'
            ).to(self.device)
            
            # Generate translation
            with torch.no_grad():
                generated = self.model.generate(
                    **encoded,
                    forced_bos_token_id=self.tokenizer.get_lang_id(tgt_code),
                    max_length=512,
                    num_beams=4,  # Beam search for better quality
                    early_stopping=True,
                    temperature=0.7
                )
            
            # Decode
            translated = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
            
            logger.debug(f"Translated ({source_lang}→{target_lang}): {text[:50]}... → {translated[:50]}...")
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """
        Translate multiple texts in batch for efficiency
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated texts
        """
        if not texts:
            return []
        
        try:
            # Get M2M codes
            src_code = self._get_m2m_lang_code(source_lang)
            tgt_code = self._get_m2m_lang_code(target_lang)
            
            # Set source language
            self.tokenizer.src_lang = src_code
            
            # Tokenize batch
            encoded = self.tokenizer(
                texts,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding='longest'
            ).to(self.device)
            
            # Generate translations
            with torch.no_grad():
                generated = self.model.generate(
                    **encoded,
                    forced_bos_token_id=self.tokenizer.get_lang_id(tgt_code),
                    max_length=512,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode batch
            translated = self.tokenizer.batch_decode(generated, skip_special_tokens=True)
            
            logger.info(f"Translated batch of {len(texts)} texts ({source_lang}→{target_lang})")
            return translated
            
        except Exception as e:
            logger.error(f"Batch translation failed: {str(e)}")
            raise
    
    def translate_segments(self, segments: List[Dict[str, Any]], 
                          source_lang: str, target_lang: str) -> List[Dict[str, Any]]:
        """
        Translate transcription segments (with metadata preservation)
        
        Args:
            segments: List of segment dicts with 'text' key
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Segments with translated text
        """
        if not segments:
            return []
        
        # Extract texts
        texts = [seg.get('text', '') for seg in segments]
        
        # Translate batch
        translated_texts = self.translate_batch(texts, source_lang, target_lang)
        
        # Merge back with metadata
        for segment, translated_text in zip(segments, translated_texts):
            segment['text'] = translated_text
            segment['translated_text'] = translated_text
            segment['source_lang'] = source_lang
            segment['target_lang'] = target_lang
        
        return segments
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get all supported languages
        
        Returns:
            Dict mapping language codes to names
        """
        lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'or': 'Odia',
            'as': 'Assamese',
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
