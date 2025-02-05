from typing import List
import llama_cpp
from llama_cpp import Llama as local_llama


# Use the pull request from https://github.com/abetlen/llama-cpp-python/pull/1820
class Llama(local_llama):
    def tokenize(
        self, text: bytes, add_bos: bool = True, special: bool = True
    ) -> List[int]:
        """Tokenize a string.

        Args:
            text: The utf-8 encoded string to tokenize.
            add_bos: Whether to add a beginning of sequence token.
            special: Whether to tokenize special tokens.

        Raises:
            RuntimeError: If the tokenization failed.

        Returns:
            A list of tokens.
        """
        return self.tokenizer_.tokenize(text, add_bos, special)


reranker_model = Llama.from_pretrained(
	repo_id="puppyM/bge-reranker-v2-m3-Q4_K_M-GGUF",
	filename="bge-reranker-v2-m3-q4_k_m.gguf",
    verbose=False,
    embedding=True,
    n_gpu_layers=-1, # Using all GPU. If you don't have gpu, use n_gpu_layers=0.
    pooling_type=llama_cpp.LLAMA_POOLING_TYPE_RANK
)

def get_reranker(query:str,documents:List[str])->List[float]:
    input = [f"{query}</s><s>{doc}" for doc in documents]
    embeds = reranker_model.embed(input)
    rank_scores = [embed[0] for embed in embeds]
    return rank_scores
