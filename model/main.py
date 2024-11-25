""" 
This python file is for experimenting with models using transformers
package from hugging face
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch 
# I need to down version torch for unsloth (fine tuning)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_id = "meta-llama/Llama-3.2-1B-Instruct" # meta-llama/Llama-3.2-3B-Instruct

tokenizer = AutoTokenizer.from_pretrained(model_id, device=device)

""" bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_config
) """

generator = pipeline(
    "text-generation",
    model=model_id,
    truncation=True,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

tokenizer.chat_template

prompt = "Create a function that takes 2 integer parameters and returns the sum in Python."
better_prompt = [
    {"role": "system", "content": "You are a Python programmer that teaches Python at an introductory level"},
    {"role": "user", "content": prompt}
]

tokenizer.apply_chat_template(better_prompt, tokenize=True, add_generation_prompt=False)

outputs = generator(
    better_prompt,
    max_new_tokens=256,
    )

# response = generator(better_prompt)
gen_text = outputs[0]["generated_text"][-1]
print(gen_text)

