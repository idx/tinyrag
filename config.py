"""
Configuration for TinyRAG system
"""
import os

class EmbeddingConfig:
    """Embedding model configuration"""
    # Available model types
    AVAILABLE_TYPES = ["llama-cpp", "sentence-transformers"]
    
    # Available models for each type
    AVAILABLE_MODELS = {
        "llama-cpp": ["bge-m3"],
        "sentence-transformers": ["ruri-v3-310m", "intfloat/multilingual-e5-base", "BAAI/bge-m3"]
    }
    
    @classmethod
    def get_model_info(cls):
        """Get current embedding model configuration"""
        model_type = os.getenv("EMBEDDING_MODEL_TYPE", "sentence-transformers")
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "ruri-v3-310m")
        return {
            "type": model_type,
            "name": model_name
        }
    
    @classmethod
    def set_model(cls, model_type: str, model_name: str):
        """Set embedding model (set environment variables)"""
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
            "no_results_error": "I apologize. I cannot answer this question from the database.",
            "rag_prompt": """
Documents:
{documents}

Question: {query}

Instructions:
Use the documents above to answer the user's question.
Answer based on the facts in the documents.
If there is no relevant information in the documents, return "No relevant information found in the documents."
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