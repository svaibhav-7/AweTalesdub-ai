import torch
from translation import Translator
import config

def test_translation():
    print("Initializing Translator...")
    translator = Translator(translation_method='m2m100')
    
    test_text = "Hello, how are you today?"
    source = 'en'
    target = 'te'
    
    print(f"Translating: '{test_text}' from {source} to {target}...")
    try:
        result = translator.translate_text(test_text, source, target)
        print(f"Result: '{result}'")
        
        if result == test_text:
            print("FAILURE: Translation returned original text (silent fallback).")
        else:
            print("SUCCESS: Translation worked.")
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_translation()
