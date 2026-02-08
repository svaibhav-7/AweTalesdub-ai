from transformers import AutoTokenizer

model_name = "facebook/nllb-200-distilled-600M"
try:
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print(f"Tokenizer class: {type(tokenizer).__name__}")
    
    # Check for lang_code_to_id
    if hasattr(tokenizer, 'lang_code_to_id'):
        print("Has lang_code_to_id")
    else:
        print("No lang_code_to_id")
        
    # Check for alternatives
    print(f"Has vocab: {hasattr(tokenizer, 'vocab')}")
    print(f"Has get_vocab: {hasattr(tokenizer, 'get_vocab')}")
    
    # Try different ways to get lang id
    try:
        print(f"get_lang_id('tel_Telu'): {tokenizer.convert_tokens_to_ids('tel_Telu')}")
    except Exception as e:
        print(f"convert_tokens_to_ids failed: {e}")

    try:
        print(f"tokenizer.lang_code_to_id['tel_Telu']: {tokenizer.lang_code_to_id['tel_Telu']}")
    except Exception as e:
        print(f"Direct access failed: {e}")

except Exception as e:
    print(f"Error: {e}")
