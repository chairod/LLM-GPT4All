import os
from dotenv import load_dotenv
from chromadb.config import Settings

# มองหาไฟล์ .env และโหลดขึ้นมาใช้งาน
# os.environ.get('key')
load_dotenv()

# พาร์ทที่เก็บ file ของ AI DB
AI_DB_PERSIST_DIR = os.environ.get('AI_DB_PERSIST_DIR')
EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME')

LLM_MODEL_PATH = os.environ.get('LLM_MODEL_PATH')
LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME')
LLM_MODEL_TEMPORATURE = float(os.environ.get('LLM_MODEL_TEMPORATURE', '0.4'))

SOURCE_DOCUMENT_PATH = os.environ.get('SOURCE_DOCUMENT_PATH')

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=AI_DB_PERSIST_DIR,
        anonymized_telemetry=False,   
)