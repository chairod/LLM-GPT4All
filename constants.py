import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
#from langchain.embeddings import HuggingFaceEmbeddings

# มองหาไฟล์ .env และโหลดขึ้นมาใช้งาน
# os.environ.get('key')
load_dotenv()



def load_chroma_database() -> chromadb.API:
    """
    โหลด AI Database โดยในโครงการนี้จะใช้ ChromaDB ซึ่งจะไม่ผ่าน langchain
    """
    return chromadb.Client(settings=CHROMA_SETTINGS)

def get_default_ai_db_collection_name() -> str:
    """
    ชื่อ Collection name ในการเก็บข้อมูลเอกสารใน AI DB
    """
    return 'freewill-company'

def is_exists_collection_name(collection_name: str, db: chromadb.API | None = None) -> bool:
    """
    ชื่อ collection name มีอยู่ภายใน AI DB หรือไม่
    True = มีอยู่แล้ว, False = ยังไม่มี
    """
    ai_db = load_chroma_database() if db == None else db
    return collection_name in [collection.name for collection in ai_db.list_collections()]


def get_default_embedding() -> embedding_functions.SentenceTransformerEmbeddingFunction:
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)





# ค่าคงที่ ที่เกี่ยวข้องกับ AI DB
AI_DB_PERSIST_DIR = os.environ.get('AI_DB_PERSIST_DIR')
AI_DB_SEARCH_RESULT_RECORD=int(os.environ.get('AI_DB_SEARCH_RESULT_RECORD', 4))
AI_DB_STORE_DOCUMENT_SIZE_PER_CHUNK = int(os.environ.get('AI_DB_STORE_DOCUMENT_SIZE_PER_CHUNK', 500))
AI_DB_METADATA_INTERNAL_IDX_NAME = 'internal_idx' # ชื่อ internal_idx สำหรับเก็บลำดับรายการ Chunk ในเอกสารแต่ล่ะฉบับ จะถูกนำไปอ้างอิงใน metadatas ซึ่งเป็นข้อมูลเพิ่มเติมของเอกสารในแต่ละ Chunk (แต่ล่ะก้อนข้อมูล) ที่ถูกบรรจุภายใน AI DB - สามารถตั้งชื่ออะไรก็ได้ และมีประโยชน์สำหรับใช้ในการ query
AI_DB_METADATA_DOCUMENT_SOURCE_NAME = 'source' # ชื่อ source เพื่อเก็บแหล่งที่มาของเอกสาร จะถูกนำไปอ้างอิงใน metadatas ซึ่งเป็นข้อมูลเพิ่มเติมของเอกสารในแต่ละ Chunk (แต่ล่ะก้อนข้อมูล) ที่ถูกบรรจุภายใน AI DB - สามารถตั้งชื่ออะไรก็ได้ และมีประโยชน์สำหรับใช้ในการ query


LLM_RUNNING_MODE = os.environ.get('LLM_RUNNING_MODE', 'DEBUG') 
LLM_MODEL_PATH = os.environ.get('LLM_MODEL_PATH')
LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME')
LLM_MODEL_TEMPORATURE = float(os.environ.get('LLM_MODEL_TEMPORATURE', '0.4'))

SOURCE_DOCUMENT_PATH = os.environ.get('SOURCE_DOCUMENT_PATH')

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=AI_DB_PERSIST_DIR,
        #anonymized_telemetry=False,
        allow_reset=False # True = ทุกครั้งที่มีการเรียก chromadb.Client(settings=CHROMA_SETTINGS) ข้อมูลใน db จะถูกลบทั้งทั้งหมด
)


EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME')
EMBEDDING_INSTANCE = get_default_embedding() #embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
#EMBEDDING_INSTANCE = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
