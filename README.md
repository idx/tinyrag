# TinyRAG

Simple RAG system, powered by llama-cpp-python and sqlite-vec only.


> Are you bored to setting RAG system?

> Are you want to run local RAG with just llama-cpp-python and sqlite-vec?

> Are you want to do research about RAG prompt or RAG system?

Here is the repository for you!

- Simple RAG system and can DIY by yourself!
- Using llama-cpp-python and sqlite-vec (database). Not using PyTorch or other deep learning framework.
- Working with Linux, macOS and Windows.
- Support Ranking, Query and LLM answer.
- Apache License Version 2.0

Resource:

- llama-cpp-python: [https://github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- sqlite-vec: [https://github.com/asg017/sqlite-vec](https://github.com/asg017/sqlite-vec)

## Install

> pip install -r requirements.txt

## Files

- llm.py: All of LLM
- database.py: All of database
- embedding.py: All of embedding model
- reranker.py: All of Reranking
- search.py: Simple RAG system

## Demo

### Thai RAG law system

For the demo, we create Thai RAG law system.

Create the database by

> python thailaw_create-db.py

Run webdemo:

> python thailaw_app.py

![](https://i.imgur.com/mJxmemo.png)

### Goodwiki

For the demo, we create English Wikipedia RAG system.

Create the database by (get first 500 texts from [goodwiki](https://huggingface.co/datasets/euirim/goodwiki))

> python wiki_create-db.py

Run webdemo:

> python wiki_app.py

![](https://i.imgur.com/TSaHbUi.png)

## Sponsors

GitHub Sponsors: [![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=https://github.com/sponsors/wannaphong/)](https://github.com/sponsors/wannaphong/)