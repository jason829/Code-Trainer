""" 
This python file is for experimenting with models using transformers
package from hugging face
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_id = "meta-llama/Llama-3.2-1B"

bnb_config = BitsAndBytesConfig(
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
)

generator = pipeline(
    "text-generation", 
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
    truncation=True,
)

def get_response(prompt):
    response = generator(prompt)
    gen_text = response[0]['generated_text']
    return gen_text

prompt = "What is Python"
llama_response = get_response(prompt)
print(llama_response)
