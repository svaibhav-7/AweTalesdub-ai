"""
Translation Module
Translates text from source to target language with validation
"""
from typing import List, Dict, Any
import os
from transformers import MarianMTModel, MarianTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
import config
from utils import get_logger

logger = get_logger(__name__)


class Translator:
    """Handle text translation between languages"""
    
    def __init__(self, translation_method: str = None):
        """
        Initialize translator
        
        Args:
            translation_method: 'm2m100', 'marian', 'google', or 'gemini'
        """
        if translation_method is None:
            translation_method = os.getenv('TRANSLATION_METHOD', 'm2m100')
        
        self.method = translation_method
        self.models = {}  # Cache for loaded models
        self.tokenizers = {}  # Cache for tokenizers
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Translator initialized with method: {translation_method}")
    
    def validate_languages(self, source_lang: str, target_lang: str) -> bool:
        """
        Validate that source and target languages are different and supported
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        # Check if languages are supported
        if source_lang not in config.SUPPORTED_LANGUAGES:
            raise ValueError(f"Source language '{source_lang}' not supported. "
                           f"Supported: {list(config.SUPPORTED_LANGUAGES.keys())}")
        
        if target_lang not in config.SUPPORTED_LANGUAGES:
            raise ValueError(f"Target language '{target_lang}' not supported. "
                           f"Supported: {list(config.SUPPORTED_LANGUAGES.keys())}")
        
        # Check if languages are different
        if source_lang == target_lang:
            raise ValueError(f"Source and target languages must be different! "
                           f"Cannot translate {source_lang} to {source_lang}")
        
        logger.info(f"Language validation passed: {source_lang} → {target_lang}")
        return True
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if not text.strip():
            return ""
        
        if self.method == 'm2m100':
            return self._translate_m2m100(text, source_lang, target_lang)
        elif self.method == 'marian':
            return self._translate_marian(text, source_lang, target_lang)
        elif self.method == 'google':
            return self._translate_google(text, source_lang, target_lang)
        elif self.method == 'gemini':
            return self._translate_gemini(text, source_lang, target_lang)
        else:
            raise ValueError(f"Unknown translation method: {self.method}")
    
    def _get_marian_model_name(self, source_lang: str, target_lang: str) -> str:
        """
        Get the appropriate MarianMT model name for language pair
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Model name on HuggingFace
        """
        # Map language codes to MarianMT naming
        lang_map = {
            'en': 'en',
            'hi': 'hi',
            'te': 'te'
        }
        
        src = lang_map.get(source_lang, source_lang)
        tgt = lang_map.get(target_lang, target_lang)
        
        # Try direct model
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        
        # Common model mappings
        # Note: Not all language pairs have direct models
        # For Indic languages, we might need multi-language models
        if source_lang in ['hi', 'te'] and target_lang == 'en':
            # Indic to English
            model_name = f"Helsinki-NLP/opus-mt-{src}-en"
        elif source_lang == 'en' and target_lang in ['hi', 'te']:
            # English to Indic
            model_name = f"Helsinki-NLP/opus-mt-en-{tgt}"
        elif source_lang in ['hi', 'te'] and target_lang in ['hi', 'te']:
            # Indic to Indic (through English as bridge)
            logger.warning(f"No direct model for {src}-{tgt}, will use English as bridge")
            model_name = None
        
        return model_name
    
    def _translate_m2m100(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate using Facebook's M2M100 model
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        model_name = "facebook/m2m100_418M"
        
        # Load model and tokenizer (with caching)
        if model_name not in self.models:
            try:
                logger.info(f"Loading M2M100 model: {model_name}")
                self.tokenizers[model_name] = M2M100Tokenizer.from_pretrained(model_name)
                self.models[model_name] = M2M100ForConditionalGeneration.from_pretrained(model_name).to(self.device)
                logger.info(f"M2M100 model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load M2M100 model {model_name}: {str(e)}")
                # Fallback to simple passthrough
                return text
        
        tokenizer = self.tokenizers[model_name]
        model = self.models[model_name]
        
        # Translate
        try:
            # Set source language
            tokenizer.src_lang = source_lang
            
            # Tokenize
            encoded_text = tokenizer(text, return_tensors="pt").to(self.device)
            
            # Generate translation
            # For M2M100, we need the language id for the target language
            lang_id = tokenizer.get_lang_id(target_lang)
            
            generated_tokens = model.generate(
                **encoded_text, 
                forced_bos_token_id=lang_id
            )
            
            # Decode
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            
            return translated_text
            
        except Exception as e:
            logger.error(f"M2M100 Translation failed: {str(e)}")
            return text

    def _translate_marian(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate using MarianMT
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        model_name = self._get_marian_model_name(source_lang, target_lang)
        
        # Handle bridge translation for Indic-to-Indic
        if model_name is None:
            logger.info(f"Using English as bridge: {source_lang} → en → {target_lang}")
            # Translate to English first
            english_text = self._translate_marian(text, source_lang, 'en')
            # Then translate to target
            return self._translate_marian(english_text, 'en', target_lang)
        
        # Load model and tokenizer (with caching)
        if model_name not in self.models:
            try:
                logger.info(f"Loading MarianMT model: {model_name}")
                self.tokenizers[model_name] = MarianTokenizer.from_pretrained(model_name)
                self.models[model_name] = MarianMTModel.from_pretrained(model_name).to(self.device)
                logger.info(f"MarianMT model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load MarianMT model {model_name}: {str(e)}")
                # Fallback to simple passthrough
                return text
        
        tokenizer = self.tokenizers[model_name]
        model = self.models[model_name]
        
        # Translate
        try:
            # Tokenize
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate translation
            translated = model.generate(**inputs)
            
            # Decode
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            
            return translated_text
            
        except Exception as e:
            logger.error(f"MarianMT Translation failed: {str(e)}")
            return text
    
    def _translate_google(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate using Google Translate API
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        try:
            from googletrans import Translator as GoogleTranslator
            
            translator = GoogleTranslator()
            result = translator.translate(text, src=source_lang, dest=target_lang)
            return result.text
            
        except Exception as e:
            logger.error(f"Google Translate failed: {str(e)}")
            logger.warning("Returning original text")
            return text
    
    def _translate_gemini(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate using Gemini API
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        logger.warning("Gemini translation not implemented yet, using passthrough")
        # TODO: Implement Gemini API translation
        return text
    
    def translate_segments(self, segments: List[Dict[str, Any]],
                          source_lang: str,
                          target_lang: str) -> List[Dict[str, Any]]:
        """
        Translate all segments
        
        Args:
            segments: List of segments with 'text' field
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Segments with 'translated_text' field added
        """
        logger.info(f"Translating {len(segments)} segments from {source_lang} to {target_lang}")
        
        # Validate languages
        self.validate_languages(source_lang, target_lang)
        
        translated_segments = []
        
        for i, seg in enumerate(segments):
            # Translate
            original_text = seg.get('text', '')
            translated_text = self.translate_text(original_text, source_lang, target_lang)
            
            # Create new segment with translation
            new_seg = seg.copy()
            new_seg['original_text'] = original_text
            new_seg['translated_text'] = translated_text
            
            translated_segments.append(new_seg)
            
            # Log progress
            if (i + 1) % 10 == 0:
                logger.info(f"Translated {i + 1}/{len(segments)} segments")
        
        logger.info(f"Translation complete: {len(translated_segments)} segments")
        return translated_segments


if __name__ == "__main__":
    # Test translation
    import sys
    import json
    
    if len(sys.argv) < 4:
        print("Usage: python translation.py <segments.json> <source_lang> <target_lang>")
        print("Example: python translation.py segments.json en hi")
        sys.exit(1)
    
    segments_file = sys.argv[1]
    source_lang = sys.argv[2]
    target_lang = sys.argv[3]
    
    # Load segments
    with open(segments_file, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    
    # Translate
    translator = Translator()
    translated = translator.translate_segments(segments, source_lang, target_lang)
    
    # Show results
    print(f"\nTranslation Results ({source_lang} → {target_lang}):\n")
    for i, seg in enumerate(translated[:5]):  # Show first 5
        print(f"{i+1}. [{seg['speaker']}] ({seg['start']:.2f}s - {seg['end']:.2f}s)")
        print(f"   Original:   {seg['original_text']}")
        print(f"   Translated: {seg['translated_text']}\n")
    
    # Save
    output_file = segments_file.replace('.json', f'_translated_{target_lang}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to {output_file}")
