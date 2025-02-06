from typing import List
from llama_cpp import Dict, Llama

# Can change the model by huggingface hub
llm_model = Llama.from_pretrained(
    repo_id="bartowski/Llama-3.2-1B-Instruct-GGUF",
    filename="Llama-3.2-1B-Instruct-Q4_K_S.gguf",
    n_ctx=4096,
    verbose=False,
    n_gpu_layers=-1 # Using all GPU. If you don't have gpu, use n_gpu_layers=0.
)


def get_llm_output(message):
    return llm_model.create_chat_completion(messages=message)

