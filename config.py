"""
Configuration for TinyRAG system
"""
import os

class EmbeddingConfig:
    """埋め込みモデルの設定"""
    # 使用可能なモデルタイプ
    AVAILABLE_TYPES = ["llama-cpp", "sentence-transformers"]
    
    # 各タイプで使用可能なモデル
    AVAILABLE_MODELS = {
        "llama-cpp": ["bge-m3"],
        "sentence-transformers": ["ruri-v3-310m", "intfloat/multilingual-e5-base", "BAAI/bge-m3"]
    }
    
    @classmethod
    def get_model_info(cls):
        """現在の埋め込みモデル設定を取得"""
        model_type = os.getenv("EMBEDDING_MODEL_TYPE", "sentence-transformers")
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "ruri-v3-310m")
        return {
            "type": model_type,
            "name": model_name
        }
    
    @classmethod
    def set_model(cls, model_type: str, model_name: str):
        """埋め込みモデルを設定（環境変数を設定）"""
        if model_type not in cls.AVAILABLE_TYPES:
            raise ValueError(f"Invalid model type: {model_type}. Available: {cls.AVAILABLE_TYPES}")
        
        if model_name not in cls.AVAILABLE_MODELS.get(model_type, []):
            raise ValueError(f"Invalid model name: {model_name} for type {model_type}")
        
        os.environ["EMBEDDING_MODEL_TYPE"] = model_type
        os.environ["EMBEDDING_MODEL_NAME"] = model_name


class LanguageConfig:
    # Set default language to English
    DEFAULT_LANGUAGE = "en"
    
    # Language-specific messages
    MESSAGES = {
        "en": {
            "no_results_error": "Sorry, I cannot answer this question from the database. No relevant documents found.",
            "rag_prompt": """
DOCUMENT:
{documents}

QUESTION: {query}

INSTRUCTIONS:
Answer the user's QUESTION using the DOCUMENT text above.
Keep your answer grounded in the facts of the DOCUMENT.
If the DOCUMENT doesn't contain the facts to answer the QUESTION, return "I cannot find relevant information in the documents."
"""
        },
        "th": {
            "no_results_error": "ขออภัย ไม่สามารถตอบคำถามนี้จากฐานข้อมูลได้",
            "rag_prompt": """คำถาม: {query}
จงตอบคำถามกับกำกับมาตราที่อ้างอิงด้วยข้อมูลต่อไปนี้ ห้ามตอบนอกเหนือจากข้อมูล:
{documents}"""
        },
        "ja": {
            "no_results_error": "申し訳ございません。データベースからこの質問に答えることができません。",
            "rag_prompt": """
ドキュメント:
{documents}

質問: {query}

指示:
上記のドキュメントを使用して、ユーザーの質問に答えてください。
ドキュメントの事実に基づいて回答してください。
ドキュメントに関連する情報がない場合は、「ドキュメントに関連する情報が見つかりません」と返してください。
"""
        }
    }
    
    @classmethod
    def get_message(cls, key, language=None):
        """Get message in specified language or default language"""
        lang = language or cls.DEFAULT_LANGUAGE
        if lang not in cls.MESSAGES:
            lang = cls.DEFAULT_LANGUAGE
        return cls.MESSAGES[lang].get(key, cls.MESSAGES[cls.DEFAULT_LANGUAGE].get(key, ""))
    
    @classmethod
    def set_default_language(cls, language):
        """Set the default language for the system"""
        if language in cls.MESSAGES:
            cls.DEFAULT_LANGUAGE = language
        else:
            raise ValueError(f"Unsupported language: {language}. Supported languages: {list(cls.MESSAGES.keys())}")