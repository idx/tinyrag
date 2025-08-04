from typing import List
from llama_cpp import Dict, Llama

# Can change the model by huggingface hub
llm_model = Llama.from_pretrained(
    repo_id="bartowski/Llama-3.2-1B-Instruct-GGUF",
    filename="Llama-3.2-1B-Instruct-Q4_K_S.gguf",
    n_ctx=16384,
    verbose=False,
    n_gpu_layers=-1 # Using all GPU. If you don't have gpu, use n_gpu_layers=0.
)


def get_llm_output(message, stream=False):
    """
    Get LLM output from messages
    
    Args:
        message: List of message dictionaries with 'role' and 'content'
        stream: If True, returns streaming response generator
    
    Returns:
        If stream=False: Complete response dictionary
        If stream=True: Generator yielding response chunks
    """
    return llm_model.create_chat_completion(messages=message, stream=stream)


def get_llm_stream(message):
    """
    Get streaming LLM output from messages
    
    Args:
        message: List of message dictionaries with 'role' and 'content'
        
    Yields:
        String chunks of the response content
    """
    for chunk in llm_model.create_chat_completion(messages=message, stream=True):
        if chunk['choices'][0]['delta'].get('content'):
            yield chunk['choices'][0]['delta']['content']

