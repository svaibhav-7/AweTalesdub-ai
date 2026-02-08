import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dubsmart.modules.translation import Translator
from dubsmart.utils.config import TRANSLATION_METHOD

print(f"Current Translation Method in Config: {TRANSLATION_METHOD}")

try:
    translator = Translator()
    print(f"Translator initialized. Method: {translator.method}")
    
    text = "Hello, how are you?"
    src = "en"
    tgt = "te"
    
    print(f"Translating '{text}' from {src} to {tgt}...")
    translated = translator.translate_text(text, src, tgt)
    print(f"Result (ascii): {ascii(translated)}")
    if "హలో" in translated or "\\u0c39\\u0c32\\u0c4b" in ascii(translated):
        print("Verification SUCCESS: Translation contains expected Telugu greeting.")
    else:
        print("Verification WARNING: Translation output might be unexpected. Validate manually.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
