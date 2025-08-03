import os
from typing import List, Union
import numpy as np

# Get embedding model type from environment variable (default is sentence-transformers)
EMBEDDING_MODEL_TYPE = os.getenv("EMBEDDING_MODEL_TYPE", "sentence-transformers")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "ruri-v3-310m")

# For llama-cpp
if EMBEDDING_MODEL_TYPE == "llama-cpp":
    from llama_cpp import Llama
    
    if EMBEDDING_MODEL_NAME == "bge-m3":
        embedding_model = Llama.from_pretrained(
            repo_id="bbvch-ai/bge-m3-GGUF",
            filename="bge-m3-q4_k_m.gguf",
            n_ctx=4096,
            embedding=True,
            verbose=False,
            n_gpu_layers=-1  # Using all GPU. If you don't have gpu, use n_gpu_layers=0.
        )
    else:
        raise ValueError(f"Unknown llama-cpp embedding model: {EMBEDDING_MODEL_NAME}")
    
    def get_embedding(text: str):
        """Get embedding function for llama-cpp"""
        return embedding_model.create_embedding(text)

# For sentence-transformers
elif EMBEDDING_MODEL_TYPE == "sentence-transformers":
    from sentence_transformers import SentenceTransformer
    
    if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
        # Load ruri-v3-310m model
        embedding_model = SentenceTransformer("cl-nagoya/ruri-v3-310m")
        
        # ruri-v3-310m requires specific Japanese prefixes for optimal performance
        # These prefixes are part of the model design and must remain in Japanese
        # See: https://huggingface.co/cl-nagoya/ruri-v3-310m
        DOCUMENT_PREFIX = "検索文書: "  # Required Japanese prefix for documents
        QUERY_PREFIX = "検索クエリ: "     # Required Japanese prefix for queries
    else:
        # Other sentence-transformers models
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        DOCUMENT_PREFIX = ""
        QUERY_PREFIX = ""
    
    def get_embedding(text: str, is_query: bool = False):
        """Get embedding function for sentence-transformers
        
        Args:
            text: Text to get embedding for
            is_query: True for query, False for document (for ruri-v3-310m)
        """
        # Add prefix
        if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
            if is_query:
                text = QUERY_PREFIX + text
            else:
                text = DOCUMENT_PREFIX + text
        
        # Get embedding
        embedding = embedding_model.encode(text, normalize_embeddings=True)
        
        # Return in the same format as llama-cpp
        return {
            "data": [{
                "embedding": embedding.tolist()
            }]
        }

else:
    raise ValueError(f"Unknown embedding model type: {EMBEDDING_MODEL_TYPE}")


def get_embedding_dimension():
    """Return the dimension of embedding vectors"""
    if EMBEDDING_MODEL_TYPE == "llama-cpp":
        return 1024  # bge-m3 dimension
    elif EMBEDDING_MODEL_TYPE == "sentence-transformers":
        if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
            return 768  # ruri-v3-310m dimension is 768
        else:
            # Get dimension from model
            return embedding_model.get_sentence_embedding_dimension()
    else:
        return 1024  # Default