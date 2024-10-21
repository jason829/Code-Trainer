""" 
This python file is for experimenting with models using transformers
package from hugging face
"""
from transformers import pipeline
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipe = pipeline(
    "text-generation", 
    model="meta-llama/Llama-3.2-1B",
    device=device,
    max_length=20
    )

print(pipe('hello world'))
