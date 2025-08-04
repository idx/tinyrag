import gradio as gr
from database import Database # for query database
from llm import get_llm_output, get_llm_stream # get llm output
from embedding import get_embedding # covert text to embedding
from reranker import get_reranker # ranking embedding
from config import LanguageConfig
db=Database("thailaw.db") # thailaw.db


def search(query, history, k=5, stream=True):
    """
    Search and generate response with optional streaming for Thai Law
    
    Args:
        query: User query string
        history: Conversation history
        k: Number of documents to retrieve
        stream: If True, yields streaming response; if False, returns complete response
    
    Returns/Yields:
        If stream=True: Generator yielding response chunks
        If stream=False: Complete response string
    """
    query_embedding = get_embedding(query)["data"][0]['embedding']
    results_query = db.get_query(query_embedding, k=k)
    list_txt = [i[0] for i in results_query]
    list_txt_rank = get_reranker(query, list_txt) # [float, ...] that match list_txt
    list_txt = [i for i, j in zip(list_txt, list_txt_rank) if j >= 0]
    
    if len(list_txt) == 0:
        error_msg = LanguageConfig.get_message("no_results_error", "th")
        if stream:
            yield error_msg
            return
        else:
            return error_msg
    
    str_txt = '\n'.join(['- ' + i.strip() for i in list_txt])
    # RAG prompt with Thai language
    temp = LanguageConfig.get_message("rag_prompt", "th").format(query=query, documents=str_txt)
    # Create a copy of history and add the RAG prompt
    llm_messages = history.copy()
    llm_messages.append({"role": "user", "content": temp})
    
    if stream:
        # Stream the response
        response_text = ""
        for chunk in get_llm_stream(llm_messages):
            response_text += chunk
            yield response_text
        # Add references at the end
        yield response_text + "\n\nReferences:\n" + str_txt
    else:
        # Non-streaming response (backward compatibility)
        response = get_llm_output(llm_messages)["choices"][0]['message']["content"]
        return response + "\n\nReferences:\n" + str_txt


def respond(
    message,
    history: list[tuple[str, str]],
    k
):
    """
    Handle streaming response for Thai Law Gradio ChatInterface
    
    Args:
        message: Current user message
        history: List of (user, assistant) message tuples
        k: Number of documents to retrieve for RAG
        
    Yields:
        Streaming response chunks
    """
    messages = []

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    # Show initial processing message
    yield "กำลังค้นหา..."
    
    # Perform RAG search
    query_embedding = get_embedding(message)["data"][0]['embedding']
    
    yield "กำลังค้นหาเอกสาร..."
    results_query = db.get_query(query_embedding, k=k)
    list_txt = [i[0] for i in results_query]
    
    yield "กำลังจัดอันดับเอกสารที่เกี่ยวข้อง..."
    list_txt_rank = get_reranker(message, list_txt) # [float, ...] that match list_txt
    list_txt = [i for i, j in zip(list_txt, list_txt_rank) if j >= 0]
    
    if len(list_txt) == 0:
        yield LanguageConfig.get_message("no_results_error", "th")
        return
    
    str_txt = '\n'.join(['- ' + i.strip() for i in list_txt])
    # RAG prompt with Thai language
    temp = LanguageConfig.get_message("rag_prompt", "th").format(query=message, documents=str_txt)
    # Create a copy of history and add the RAG prompt
    llm_messages = messages.copy()
    llm_messages.append({"role": "user", "content": temp})
    
    yield "กำลังสร้างคำตอบ..."
    
    # Stream the actual LLM response
    response_text = ""
    first_chunk = True
    for chunk in get_llm_stream(llm_messages):
        response_text += chunk
        # After the first chunk arrives, start showing the actual response
        if first_chunk:
            first_chunk = False
        yield response_text
    
    # Add references at the end
    yield response_text + "\n\nReferences:\n" + str_txt


demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Slider(minimum=3, maximum=10, value=5, step=1, label="k")
    ]
)


if __name__ == "__main__":
    demo.launch()
