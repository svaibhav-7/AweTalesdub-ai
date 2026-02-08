from transformers import M2M100Tokenizer

try:
    print("Loading tokenizer...")
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    print(f"Tokenizer loaded. Vocab size: {tokenizer.vocab_size}")
    
    lang_id = tokenizer.get_lang_id("te")
    print(f"Language ID for 'te': {lang_id}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error Type: {type(e).__name__}")
