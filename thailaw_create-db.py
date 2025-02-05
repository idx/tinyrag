from datasets import load_dataset
from database import Database
from embedding import get_embedding
from tqdm.auto import tqdm

ds = load_dataset("airesearch/WangchanX-Legal-ThaiCCL-RAG")

train_df=ds["train"].to_pandas()
test_df=ds["test"].to_pandas()

_temp=set()
for i in train_df["positive_contexts"]:
    for j in i:
        _temp.add(j['text'])
for i in train_df["hard_negative_contexts"]:
    for j in i:
        _temp.add(j['text'])
for i in test_df["positive_contexts"]:
    for j in i:
        _temp.add(j['text'])
for i in test_df["hard_negative_contexts"]:
    for j in i:
        _temp.add(j['text'])

list_law=list(_temp) # list of texts
del list_law[list_law.index('')] # del error from dataset

# Create database
db=Database("thailaw.db") # thailaw.db
db.create_db()

# insert data to database
for text in tqdm(list_law):
    db.insert(text, get_embedding(text)["data"][0]['embedding'])
