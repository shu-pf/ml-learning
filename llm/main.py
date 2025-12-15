from transformers import AutoModelForCausalLM, AutoTokenizer

# モデルとトークナイザーの読み込み
model_name = "openlm-research/open_llama_7b"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token  # Llama has no pad token by default
model = AutoModelForCausalLM.from_pretrained(model_name)

# テキスト入力をトークン化
prompt = "A list of foods: apple, banana, orange"
model_inputs = tokenizer(prompt, return_tensors="pt")

# テキスト生成
generated_ids = model.generate(**model_inputs)

# 生成されたテキストをデコードして表示
generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(generated_text)
