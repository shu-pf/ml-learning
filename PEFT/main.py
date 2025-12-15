"""
🤗 PEFTアダプターを読み込んで使用するシンプルな例
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

# ベースモデルIDとPEFTアダプターモデルID
base_model_id = "facebook/opt-350m"
peft_model_id = "ybelkada/opt-350m-lora"

# トークナイザーはベースモデルから読み込む
print(f"トークナイザーを読み込み中: {base_model_id}")
tokenizer = AutoTokenizer.from_pretrained(base_model_id)

# PEFTアダプターモデルを読み込む
print(f"PEFTアダプターモデルを読み込み中: {peft_model_id}")
model = AutoModelForCausalLM.from_pretrained(peft_model_id)

# テキストを生成
text = "Hello, my name is"
inputs = tokenizer(text, return_tensors="pt")

print(f"\n入力テキスト: {text}")
print("テキストを生成中...")

outputs = model.generate(**inputs, max_new_tokens=20)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"\n生成されたテキスト: {generated_text}")
