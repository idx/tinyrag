import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32


class Database:
    def __init__(self,db: str):
        self.db = sqlite3.connect(db, check_same_thread=False) # db.db is the database file.
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db) # load sqlite-vec
        self.db.enable_load_extension(False)

    def create_db(self, embedding_dim=1024):
        self.db.execute(f"""CREATE virtual table vec_documents using vec0(
               document_id INTEGER PRIMARY KEY AUTOINCREMENT,
               contents TEXT,
               contents_embedding FLOAT[{embedding_dim}]
        );""") # Table vec_documents
        self.db.commit()

    def insert(self, content,embedding):
       with self.db:
        self.db.execute(
            "INSERT INTO vec_documents(contents,contents_embedding) VALUES(?, ?)",
            [content, serialize_float32(embedding)],
        )
        self.db.commit()

    def get_query(self, query_embedding, k:int=5):
       results = self.db.execute(
          f"""
        SELECT contents, distance FROM vec_documents
      WHERE contents_embedding MATCH ?
        AND k = {k}
      ORDER BY distance
       """,
       [serialize_float32(query_embedding)],
       ).fetchall()
       return results
