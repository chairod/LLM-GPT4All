##
# ก่อนจะรันทดสอบ Script ไฟล์นี้ให้รัน test.chromadb.ipynb ก่อน
# เพื่อสร้างข้อมูลเก็บใน AI DB
#

# import chromadb
# from chromadb.config import Settings
# from chromadb.utils import embedding_functions

# chroma_db = chromadb.Client(settings=Settings(
#     persist_directory='ai_db_x',
#     chroma_db_impl='duckdb+parquet',
#     allow_reset=False
# ))


# embbing = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-mpnet-base-v2')
# collection = chroma_db.get_collection(name='freewill', embedding_function=embbing)

# query_str = 'What does the Account Status Lock(buy) option indicate? '
# ret = collection.query(
#     query_texts=[query_str],
#     where_document={
#         '$contains': query_str
#     }
# )

# print(ret['documents'])





## อ่านเอกสารจาก pdf file
# and HALTED.
# What happens
# from langchain.document_loaders import PDFMinerLoader
# import os
# import re
# pdfDoc = PDFMinerLoader(file_path=f'{os.getcwd()}/source_documents-single/GS_QA.pdf')
# doc = pdfDoc.load()


# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import re
# text_spliter = RecursiveCharacterTextSplitter(
#     #separators = ['\n', '\n\n'],
#     chunk_size = 500,
#     chunk_overlap = 10
# )
# texts = re.split('\n{1,}', doc[0].page_content)
# clean_texts = [re.sub('\s{2,}', ' ', text.strip()) for text in texts if len(text.strip()) > 0]
# #print(clean_texts)

# plain_text = ' '.join(clean_texts)
# #chunks = [plain_text[i:i+500] for i in range(0, len(plain_text), 500)]
# #print(chunks)
# chunks = text_spliter.split_text(plain_text)
# clean_chunks = [re.sub('\.', '.\n', chunk) for chunk in chunks]
# print(clean_chunks)




### ทดสอบ ฟังชันก์ ของ constant.py
# import unicodedata
# from constants import (
#     transform_special_character_to_encoded,
#     decode_special_character_to_str
# )

# text_encoder = 'Cześć'.encode('utf-8', 'ignore')
# print(f'text_encoder: {text_encoder}')

# text_decoded = text_encoder.decode('utf-8', 'ignore')
# print(f'text_decoded: {text_decoded}')

# plainText = 'Cześć'
# encoder = plainText.encode('utf-8', 'ignore')
# print(f"encoder: {encoder}, byte_to_string: {encoder.decode('utf-8', 'ignore')}")


# #decoder = b'Cze\xc5\x9b\xc4\x87'
# decoder = bytes('Feature: Deposit cash balance Conditions: Users can\\xe2\\x80\\x99t', 'utf-8')
# print(decoder.split(b'\\'))





# ทดสอบ Script "helper/finetuneHelper.py"
from helper.finetuneHelper import FinetuneQuery
from constants import (
    get_default_ai_db_collection_name,
    get_default_embedding,
    load_chroma_database,
    is_exists_collection_name,
    AI_DB_SEARCH_RESULT_RECORD,
    AI_DB_METADATA_DOCUMENT_SOURCE_NAME,
    AI_DB_METADATA_INTERNAL_IDX_NAME
)

db = load_chroma_database()
collection = db.get_collection(name=get_default_ai_db_collection_name(), embedding_function=get_default_embedding())

out = FinetuneQuery.query_from_funetune(query_str='What is the bank field used for?', db=db)
print(f'query result: {out}')