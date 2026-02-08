from transformers import M2M100Tokenizer

tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
# Print all keys in lang_code_to_id
print(list(tokenizer.lang_code_to_id.keys()))
