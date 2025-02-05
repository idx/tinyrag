import gradio as gr
from database import Database # for query database
from llm import get_llm_output # get llm output
from embedding import get_embedding # covert text to embedding
from reranker import get_reranker # ranking embedding
db=Database("wiki.db") # wiki.db


def search(query,history,k=5):
    query_embedding = get_embedding(query)["data"][0]['embedding']
    results_query = db.get_query(query_embedding,k=k)
    list_txt=[i[0] for i in results_query]
    list_txt_rank=get_reranker(query,list_txt) # [float, ...] that match list_txt
    list_txt=[i for i,j in zip(list_txt,list_txt_rank) if j>=0]
    if len(list_txt) == 0 :
        return "Sorry, I can answer from Database. I don't found any docs." # Can't answer
    str_txt='\n'.join(['- '+i.strip() for i in list_txt])
    # RAG prompt
    temp=f"""
    DOCUMENT:
{str_txt}

QUESTION: {query}

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return 'Sorry, I can answer from Database. I don't found any docs.'"""
    history.append({"role": "user","content": temp})
    return get_llm_output(history)["choices"][0]['message']["content"]+"\n\nDocument:\n"+str_txt


def respond(
    message,
    history: list[tuple[str, str]],
    k
):
    messages = []

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    yield search(message, history=messages,k=k)


demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Slider(minimum=3, maximum=10, value=5, step=1, label="k")
    ]
)


if __name__ == "__main__":
    demo.launch()
