from transformers import M2M100Tokenizer

try:
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    candidates = ["te", "tel", "te_IN", "te-IN", "ta", "hi", "en"]
    print("Checking candidates:")
    for code in candidates:
        try:
            lid = tokenizer.get_lang_id(code)
            print(f"  {code}: {lid}")
        except:
            print(f"  {code}: Not supported")
            
    # Also print first 20 keys to see format
    keys = list(tokenizer.lang_code_to_id.keys())
    print("\nFirst 20 keys:")
    print(keys[:20])

except Exception as e:
    print(f"Fatal Error: {e}")
