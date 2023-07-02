#!/usr/bin/env python3
import os
import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
import re

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from chromadb.api import Collection

from constants import (
    #CHROMA_SETTINGS, 
    AI_DB_PERSIST_DIR, 
    SOURCE_DOCUMENT_PATH, 
    #EMBEDDING_INSTANCE,
    AI_DB_STORE_DOCUMENT_SIZE_PER_CHUNK,
    AI_DB_METADATA_INTERNAL_IDX_NAME,
    AI_DB_METADATA_DOCUMENT_SOURCE_NAME,
    get_default_ai_db_collection_name,
    load_chroma_database,
    get_default_embedding
)


# Load environment variables
persist_directory = AI_DB_PERSIST_DIR
source_directory = SOURCE_DOCUMENT_PATH
#embeddings_model_name = EMBEDDING_MODEL_NAME
chunk_size = AI_DB_STORE_DOCUMENT_SIZE_PER_CHUNK
chunk_overlap = 50


# Custom document loaders
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> Document:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{ext}'")


def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, doc in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.append(doc)
                pbar.update()

    return results

def process_documents(collection: Collection, ignored_files: List[str] = []) -> List[Document]:
    """
    นำเอกสารแต่ละไฟล์ที่โหลดเนื้อหาเสร็จ มาสร้าง เป็น Document
    ทำความสะอาดเนื้อหาจากไฟล์เอกสาร เพื่อให้ลดขนาดพื้นที่ของ AI DB ไม่ต้องเก็บส่วน บรรทัดที่ไม่มีข้อความอยู่
    
    1. ตัดข้อความออกเป็นส่วนๆ โดยใช้เงื่อนไข "\ n|\ n\ n|\ r\ n"
    2. trim พื้นที่ว่างซ้ายขวา และ ใส่ "\ n" ในประโยคที่ลงท้ายด้วย .  จะได้ ".\ n"  เพื่อเป็น Markpoint ให้ LLM หยุดสร้างประโยคคำตอบ
    3. นำเนื้อความที่ได้จาก ข้อ 2 ไปสร้างเป็นเอกสาร และ เก็บลง ChromaDB (AI DB)
    """
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents from {source_directory}")


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # นำเอกสารแต่ละไฟล์ที่โหลดเนื้อหาเสร็จ มาสร้าง เป็น Document
    # ทำความสะอาดเนื้อหาจากไฟล์เอกสาร เพื่อให้ลดขนาดพื้นที่ของ AI DB ไม่ต้องเก็บส่วน บรรทัดที่ไม่มีข้อความอยู่
    #
    # 1. ตัดข้อความออกเป็นส่วนๆ โดยใช้เงื่อนไข \n|\n\n|\r\n
    # 2. trim พื้นที่ว่างซ้ายขวา และ ใส่ \n ในประโยคที่ลงท้ายด้วย .  จะได้ .\n  เพื่อเป็น Markpoint ให้ LLM หยุดสร้างประโยคคำตอบ
    # 3. นำเนื้อความที่ได้จาก ข้อ 2 ไปสร้างเป็นเอกสาร และ เก็บลง ChromaDB (AI DB)
    ret_new_document = []
    for doc in documents:
        split_texts = re.split(pattern="\n|\n\n|\r\n", string=doc.page_content)
        split_texts = [f'{text.strip()}\n' if text.strip().endswith('.') else text.strip() for text in split_texts if len(text.strip()) > 0]
        cleaned_texts = '\n'.join(split_texts)

        # ตัดข้อความแยกออกเป็นแต่ล่ะ Chunk (แยกออกเป็นก้อนๆ)
        prepare_texts = text_splitter.split_text(text=cleaned_texts)
        id_count = 1
        for prepare_text in prepare_texts:
            new_idx = f'idx_{id_count}'
            id_count += 1

            # เก็บข้อมูลในแต่ล่ะ Chunk ลง AI DB
            collection.add(
                ids = [f"{doc.metadata['source']}-{new_idx}"],
                documents=[prepare_text],
                metadatas=[{AI_DB_METADATA_INTERNAL_IDX_NAME: new_idx, AI_DB_METADATA_DOCUMENT_SOURCE_NAME: doc.metadata['source']}]
            )
            ret_new_document.append(prepare_text)

    return ret_new_document

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # split_documents = text_splitter.split_documents(documents)
    # print(f"Split into {len(split_documents)} chunks of text (max. {chunk_size} tokens each)")
    # return split_documents

def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False

def main():
    # Create embeddings
    #embeddings = EMBEDDING_INSTANCE #HuggingFaceEmbeddings(model_name=embeddings_model_name)
    #embeddings = HuggingFaceEmbeddings()

    # if does_vectorstore_exist(persist_directory):
    #     # Update and store locally vectorstore
    #     print(f"Appending to existing vectorstore at {persist_directory}")
    #     db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    #     collection = db.get()
    #     texts = process_documents([metadata['source'] for metadata in collection['metadatas']])
    #     print(f"Creating embeddings. May take some minutes...")
    #     db.add_documents(texts)
    # else:
    #     # Create and store locally vectorstore
    #     print("Creating new vectorstore")
    #     texts = process_documents()
    #     print(f"Creating embeddings. May take some minutes...")
    #     db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)

    db = load_chroma_database()
    collection = None if get_default_ai_db_collection_name() not in [coll.name for coll in db.list_collections()] else db.get_collection(name=get_default_ai_db_collection_name(), embedding_function=get_default_embedding())
    if collection == None:
        # สร้าง Vectorstore ใหม่
        # create_collection also takes an optional metadata argument which can be used to customize the distance 
        # method of the embedding space by setting the value of hnsw:space. 
        # Valid options for hnsw:space are "l2", "ip, "or "cosine"
        print('Creating new vectorstore ...')
        collection = db.create_collection(
            name=get_default_ai_db_collection_name(),
            embedding_function=get_default_embedding(),
            metadata={"hnsw:space": "cosine"}
        )
    else:
        print("Finding document there aren't exists in vectorstore and will update ...")

    # ค้นหารายการเอกสารทั้งหมดที่เก็บใน Collection
    # เพื่อนำข้อมูลใน metadatatas มาตรวจสอบ มีไฟล์ใดบ้างแล้วที่ถูก เก็บไว้
    documents = collection.get()
    process_documents(collection, [metadata['source'] for metadata in documents["metadatas"]])
    db.persist()
    db = None

    print(f"Ingestion complete! You can now run runner.py to query your documents")


if __name__ == "__main__":
    main()