##
# ก่อนจะรันทดสอบ Script ไฟล์นี้ให้รัน test.chromadb.ipynb ก่อน
# เพื่อสร้างข้อมูลเก็บใน AI DB
#

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

chroma_db = chromadb.Client(settings=Settings(
    persist_directory='ai_db_x',
    chroma_db_impl='duckdb+parquet',
    allow_reset=False
))


embbing = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-mpnet-base-v2')
collection = chroma_db.get_collection(name='freewill', embedding_function=embbing)

query_str = 'What does the Account Status Lock(buy) option indicate? '
ret = collection.query(
    query_texts=[query_str],
    where_document={
        '$contains': query_str
    }
)

print(ret['documents'])