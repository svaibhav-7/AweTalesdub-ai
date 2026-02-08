from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-en-te"
try:
    print(f"Loading {model_name}...")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    print("Model loaded successfully.")
    
    src_text = "Hello world"
    encoded = tokenizer(src_text, return_tensors="pt")
    generated = model.generate(**encoded)
    tgt_text = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
    print(f"Translation: {tgt_text}")

except Exception as e:
    print(f"Error: {e}")
