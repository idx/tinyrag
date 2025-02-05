from datasets import load_dataset
from database import Database
from embedding import get_embedding
from tqdm.auto import tqdm

ds = load_dataset("euirim/goodwiki",split="train").select(500) # first 500

list_law=list(ds["markdown"]) # list of texts

# Create database
db=Database("wiki.db") # thailaw.db
db.create_db()

# insert data to database
for text in tqdm(list_law):
    db.insert(text, get_embedding(text)["data"][0]['embedding'])
