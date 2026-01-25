from typing import List, Dict, Any
from ..utils import get_logger

logger = get_logger(__name__)

class Translator:
    """Handle multilingual text translation."""
    
    def __init__(self, method: str = 'm2m100'):
        # Lazy imports for heavy libraries
        import torch
        from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer, MarianMTModel, MarianTokenizer
        self.M2M100ForConditionalGeneration = M2M100ForConditionalGeneration
        self.M2M100Tokenizer = M2M100Tokenizer
        
        self.method = method
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.tokenizers = {}
        logger.info(f"Translator initialized with method: {method}")

    def _get_m2m100(self):
        model_name = "facebook/m2m100_418M"
        if model_name not in self.models:
            self.tokenizers[model_name] = self.M2M100Tokenizer.from_pretrained(model_name)
            self.models[model_name] = self.M2M100ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        return self.models[model_name], self.tokenizers[model_name]

    def translate_text(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translate a single string."""
        if not text.strip(): return ""
        if src_lang == tgt_lang: return text
        
        model, tokenizer = self._get_m2m100()
        tokenizer.src_lang = src_lang
        encoded = tokenizer(text, return_tensors="pt").to(self.device)
        
        # Improved generation parameters to prevent repetition and improve quality
        generated = model.generate(
            **encoded, 
            forced_bos_token_id=tokenizer.get_lang_id(tgt_lang),
            max_length=256,
            num_beams=5,
            no_repeat_ngram_size=3,
            early_stopping=True,
            do_sample=False  # Keep it deterministic for translation
        )
        return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

    def translate_segments(self, segments: List[Dict[str, Any]], src_lang: str, tgt_lang: str) -> List[Dict[str, Any]]:
        """Translate multiple segments in batch or loop."""
        logger.info(f"Translating {len(segments)} segments from {src_lang} to {tgt_lang}")
        translated = []
        for i, seg in enumerate(segments):
            orig_text = seg.get('text', '')
            trans_text = self.translate_text(orig_text, src_lang, tgt_lang)
            new_seg = seg.copy()
            new_seg['original_text'] = orig_text
            new_seg['translated_text'] = trans_text
            translated.append(new_seg)
            if (i+1) % 10 == 0: logger.info(f"Translated {i+1}/{len(segments)} segments")
        return translated
