from datasets import load_dataset
from database import Database
from embedding import get_embedding, get_embedding_dimension
from tqdm.auto import tqdm

ds = load_dataset("euirim/goodwiki",split="train").select(range(500)) # first 500

list_law=list(ds["markdown"]) # list of texts

# Create database
db=Database("wiki.db") # thailaw.db
# 埋め込みモデルの次元数を取得してデータベースを作成
embedding_dim = get_embedding_dimension()
print(f"Creating database with embedding dimension: {embedding_dim}")
db.create_db(embedding_dim=embedding_dim)

# insert data to database
for text in tqdm(list_law):
    db.insert(text, get_embedding(text)["data"][0]['embedding'])
