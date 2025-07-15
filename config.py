"""
Language configuration for TinyRAG system
"""

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