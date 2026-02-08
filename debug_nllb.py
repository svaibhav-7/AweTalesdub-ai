import os
print(f"HF_TOKEN: {os.environ.get('HF_TOKEN')}")
print(f"HUGGINGFACE_TOKEN: {os.environ.get('HUGGINGFACE_TOKEN')}")

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"
try:
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("Model loaded successfully.")
    
    src_text = "Hello world"
    # NLLB uses BCP-47 codes. English is 'eng_Latn', Telugu is 'tel_Telu'
    inputs = tokenizer(src_text, return_tensors="pt")
    
    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id["tel_Telu"],
        max_length=30
    )
    tgt_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    print(f"Translation (tel_Telu): {tgt_text}")

except Exception as e:
    print(f"Error: {e}")
