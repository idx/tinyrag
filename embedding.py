from llama_cpp import Llama

# get model
embedding_model = Llama.from_pretrained(
    repo_id="bbvch-ai/bge-m3-GGUF",
    filename="bge-m3-q4_k_m.gguf",
    n_ctx=4096,
    embedding=True,
    verbose=False,
    n_gpu_layers=-1 # Using all GPU. If you don't have gpu, use n_gpu_layers=0.
)


def get_embedding(text: str):
    return embedding_model.create_embedding(text)