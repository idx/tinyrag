from database import Database # for query database
from llm import get_llm_output, get_llm_stream # get llm output
from embedding import get_embedding # covert text to embedding
from reranker import get_reranker # ranking embedding
from config import LanguageConfig

db=Database("thailaw.db")

import sys

# Ask for streaming preference
print("Enable streaming output? (y/n): ", end="")
use_streaming = input().lower().startswith('y')
print()

while True:
    query = input("Question: ")
    if query.lower() in ['quit', 'exit', 'q']:
        break
        
    # Get embedding for query (is_query=True for sentence-transformers)
    if hasattr(get_embedding, '__code__') and 'is_query' in get_embedding.__code__.co_varnames:
        query_embedding = get_embedding(query, is_query=True)["data"][0]['embedding']
    else:
        query_embedding = get_embedding(query)["data"][0]['embedding']
    results_query = db.get_query(query_embedding)
    list_txt = []
    for row in results_query:
        list_txt.append(row[0])
    list_txt_rank = get_reranker(query, list_txt) # [float, ...] that match list_txt
    list_txt = [i for i, j in zip(list_txt, list_txt_rank) if j >= 0]
    
    if len(list_txt) == 0:
        print(LanguageConfig.get_message("no_results_error"))
        print()
        print()
        continue
        
    str_txt = '\n'.join(['- ' + i.strip() for i in list_txt])
    # RAG prompt
    temp = LanguageConfig.get_message("rag_prompt").format(query=query, documents=str_txt)
    
    print("RAG Prompt:")
    print(temp)
    print("====================")
    print("Response:")
    
    if use_streaming:
        # Streaming output
        for chunk in get_llm_stream([{"role": "user", "content": temp}]):
            print(chunk, end="", flush=True)
        print()  # New line after streaming
    else:
        # Non-streaming output
        llm_out = get_llm_output([{"role": "user", "content": temp}])
        print(llm_out["choices"][0]['message']["content"])
    
    print()
    print("References:")
    print(str_txt)
    print()
    print()