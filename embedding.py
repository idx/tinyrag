import os
from typing import List, Union
import numpy as np

# 埋め込みモデルのタイプを環境変数から取得（デフォルトはsentence-transformers）
EMBEDDING_MODEL_TYPE = os.getenv("EMBEDDING_MODEL_TYPE", "sentence-transformers")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "ruri-v3-310m")

# llama-cppの場合
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
        """llama-cpp用の埋め込み取得関数"""
        return embedding_model.create_embedding(text)

# sentence-transformersの場合
elif EMBEDDING_MODEL_TYPE == "sentence-transformers":
    from sentence_transformers import SentenceTransformer
    
    if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
        # ruri-v3-310mモデルをロード
        embedding_model = SentenceTransformer("cl-nagoya/ruri-v3-310m")
        
        # ruri-v3-310mは用途に応じてプレフィックスを使い分ける
        # ここではRAG用の検索文書プレフィックスを使用
        DOCUMENT_PREFIX = "検索文書: "
        QUERY_PREFIX = "検索クエリ: "
    else:
        # その他のsentence-transformersモデル
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        DOCUMENT_PREFIX = ""
        QUERY_PREFIX = ""
    
    def get_embedding(text: str, is_query: bool = False):
        """sentence-transformers用の埋め込み取得関数
        
        Args:
            text: 埋め込みを取得するテキスト
            is_query: クエリの場合True、文書の場合False（ruri-v3-310m用）
        """
        # プレフィックスを追加
        if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
            if is_query:
                text = QUERY_PREFIX + text
            else:
                text = DOCUMENT_PREFIX + text
        
        # 埋め込みを取得
        embedding = embedding_model.encode(text, normalize_embeddings=True)
        
        # llama-cppと同じ形式で返す
        return {
            "data": [{
                "embedding": embedding.tolist()
            }]
        }

else:
    raise ValueError(f"Unknown embedding model type: {EMBEDDING_MODEL_TYPE}")


def get_embedding_dimension():
    """埋め込みベクトルの次元数を返す"""
    if EMBEDDING_MODEL_TYPE == "llama-cpp":
        return 1024  # bge-m3の次元数
    elif EMBEDDING_MODEL_TYPE == "sentence-transformers":
        if EMBEDDING_MODEL_NAME == "ruri-v3-310m":
            return 768  # ruri-v3-310mの次元数は768
        else:
            # モデルから次元数を取得
            return embedding_model.get_sentence_embedding_dimension()
    else:
        return 1024  # デフォルト