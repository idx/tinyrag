from database import Database # for query database
from llm import get_llm_output # get llm output
from embedding import get_embedding # covert text to embedding
from reranker import get_reranker # ranking embedding

db=Database("thailaw.db")

while True:
    query=input("Question: ")
    query_embedding = get_embedding(query)["data"][0]['embedding']
    results_query = db.get_query(query_embedding)
    list_txt=[]
    for row in results_query:
        list_txt.append(row[0])
    list_txt_rank=get_reranker(query,list_txt) # [float, ...] that match list_txt
    list_txt=[i for i,j in zip(list_txt,list_txt_rank) if j>=0]
    str_txt='\n'.join(['- '+i.strip() for i in list_txt])
    temp=f"""คำถาม: {query}\nจงตอบคำถามกับกำกับมาตราที่อ้างอิงด้วยข้อมูลต่อไปนี้ ห้ามตอบนอกเหนือจากข้อมูล:\n{str_txt}"""
    llm_out=get_llm_output([{"role": "user","content": temp}])
    print(temp)
    print("====================")
    print(llm_out["choices"][0]['message']["content"])
    print()
    print()