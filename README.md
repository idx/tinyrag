# TinyRAG

A lightweight Retrieval-Augmented Generation (RAG) system with flexible embedding model support.

## 🎯 Features

- **Lightweight & Fast**: Optimized for minimal dependencies and maximum performance
- **Flexible Embedding Models**: Support for both sentence-transformers and llama-cpp backends
- **Japanese Language Optimized**: Default Japanese model (ruri-v3-310m) with specialized prefixes
- **Multi-language Support**: English, Japanese, and Thai language configurations
- **Modern Python**: Built with Python 3.13+ and uv package manager
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Web UI**: Interactive Gradio interface for easy testing
- **Complete RAG Pipeline**: Ranking, query processing, and LLM answer generation

## 🔧 Technical Stack

### Core Technologies
- **LLM**: Llama-3.2-1B-Instruct (Q4_K_S quantized)
- **Vector Database**: sqlite-vec for efficient similarity search
- **Web Framework**: Gradio for interactive UI
- **Package Management**: uv (recommended) or pip

### Embedding Models
- **Default**: `cl-nagoya/ruri-v3-310m` (Japanese-optimized, 310M parameters)
- **Alternative**: `bge-m3` (Multilingual, GGUF quantized)

### Key Dependencies
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - GGUF model execution
- [sqlite-vec](https://github.com/asg017/sqlite-vec) - Vector search extension
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) - Embedding models
- [gradio](https://github.com/gradio-app/gradio) - Web interface

## 🚀 Quick Start

### Installation

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### Project Structure

```
tinyrag/
├── pyproject.toml       # Project configuration & dependencies
├── llm.py              # LLM model management (Llama-3.2-1B)
├── database.py         # SQLite vector database operations
├── embedding.py        # Embedding models (switchable backends)
├── reranker.py         # Document reranking (bge-reranker-v2-m3)
├── search.py           # RAG system implementation
├── config.py           # Multi-language configuration
├── wiki_app.py         # Wikipedia demo (Gradio UI)
├── wiki_create-db.py   # Wikipedia database creation
├── thailaw_app.py      # Thai law demo
└── thailaw_create-db.py # Thai law database creation
```

## 🔄 Embedding Model Configuration

Switch between embedding models using environment variables:

```bash
# Japanese-optimized (default)
export EMBEDDING_MODEL_TYPE=sentence-transformers
export EMBEDDING_MODEL_NAME=ruri-v3-310m

# Multilingual alternative
export EMBEDDING_MODEL_TYPE=llama-cpp
export EMBEDDING_MODEL_NAME=bge-m3
```

## 📊 Demo Applications

### 1. Wikipedia RAG System

English Wikipedia RAG with interactive Gradio interface.

**Dataset**: [euirim/goodwiki](https://huggingface.co/datasets/euirim/goodwiki) (first 500 texts)

```bash
# Create database (default: ruri-v3-310m)
python wiki_create-db.py

# Alternative: Use bge-m3 model
EMBEDDING_MODEL_TYPE=llama-cpp EMBEDDING_MODEL_NAME=bge-m3 python wiki_create-db.py

# Launch web interface
python wiki_app.py
```

**Features**:
- Interactive Gradio chat interface
- Adjustable k parameter for retrieval
- Real-time document ranking and filtering
- Reference display with retrieved documents

![](https://i.imgur.com/TSaHbUi.png)

### 2. Thai Legal RAG System

Thai law document retrieval system for legal research.

**Dataset**: [airesearch/WangchanX-Legal-ThaiCCL-RAG](https://huggingface.co/datasets/airesearch/WangchanX-Legal-ThaiCCL-RAG)

```bash
# Create Thai law database
python thailaw_create-db.py

# Launch Thai law interface
python thailaw_app.py
```

**Features**:
- Thai language support with proper tokenization
- Legal document-specific ranking
- Specialized prompts for legal queries

![](https://i.imgur.com/mJxmemo.png)

## ⚠️ Important Notes

### Embedding Model Switching
- **Database Recreation Required**: When changing embedding models, you must recreate the database as vector dimensions may differ
- **ruri-v3-310m**: Requires Japanese prefixes ("検索文書: " for documents, "検索クエリ: " for queries)
- **bge-m3**: Works without prefixes and supports multiple languages

### Performance Considerations
- **Memory Usage**: Models require several GB of RAM during initialization
- **GPU Support**: Use `n_gpu_layers=-1` for full GPU acceleration, `0` for CPU-only
- **First Run**: Initial model downloads may take time depending on internet speed

## 🔧 Development

### Running Tests
```bash
# Individual module testing
python -c "from embedding import get_embedding; print('Embedding OK')"
python -c "from database import Database; print('Database OK')"

# End-to-end testing
python search.py
```

### Adding New Models
1. Update `embedding.py` with new model configuration
2. Add appropriate prefixes if required
3. Update environment variable handling
4. Test with small dataset before full deployment

## 📄 License

Apache License Version 2.0

## 🙏 Acknowledgments

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - GGUF model execution
- [sqlite-vec](https://github.com/asg017/sqlite-vec) - Vector search capabilities  
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) - Embedding model framework
- [cl-nagoya/ruri-v3-310m](https://huggingface.co/cl-nagoya/ruri-v3-310m) - Japanese-optimized embeddings

## 💝 Support

GitHub Sponsors: [![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=https://github.com/sponsors/wannaphong/)](https://github.com/sponsors/wannaphong/)