from constants import (
    #EMBEDDING_MODEL_NAME, 
    AI_DB_PERSIST_DIR, 
    SOURCE_DOCUMENT_PATH,
    EMBEDDING_INSTANCE,
    CHROMA_SETTINGS, 
    LLM_MODEL_PATH,
    LLM_MODEL_NAME,
    LLM_MODEL_TEMPORATURE,
    AI_DB_SEARCH_RESULT_RECORD
)
from langchain.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings

# โหลด AI Database เพื่อสร้าง Instance สำหรับการสร้างคำถาม
embedding = EMBEDDING_INSTANCE #HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
ai_db = Chroma(
    persist_directory=AI_DB_PERSIST_DIR,
    embedding_function=embedding,
    client_settings=CHROMA_SETTINGS
)
collection = ai_db.get()
metadatas = [meta['source'] for meta in collection['metadatas']]
is_ai_db = len(metadatas) > 0
if is_ai_db == False:
    print()
    print('Warning: \nIf you want to ask any question from document')
    print('before run this script please run "python ingre.py" to create AI database and query any question')
    print()
# else:
#     # ถ้ามีการสร้าง AI Database แล้ว
#     # ตรวจสอบรายการไฟล์ ที่อยู่ใน "SOURCE_DOCUMENT_PATH" 
#     # หากมีไฟล์ที่ยังไม่ถูกเก็บลงใน AI DB เรียก ingre.py เพื่อทำงาน
#     import os
#     files = os.listdir(SOURCE_DOCUMENT_PATH)
#     files = [f'{SOURCE_DOCUMENT_PATH}\\{f}' for f in files]
    
#     for file in files:


    




# ผ่านข้อมูลที่ได้จาก AI DB ให้กับ LLM (GPT4All) เพื่อเรียบเรียงคำตอบ
from langchain.prompts import PromptTemplate
from gpt4all import pyllmodel, gpt4all
import os
prompt=PromptTemplate(
    template= """
{personnel_info}

question: {question}
""",
    input_variables=['personnel_info', 'question']
)
llm = pyllmodel.LLModel()
model_path = f'{LLM_MODEL_PATH}\\{LLM_MODEL_NAME}'
if os.path.exists(model_path) == False:
    print(f"Please wait a moment for download model {LLM_MODEL_NAME} from website and save to local path {LLM_MODEL_PATH}")
    gpt4all_cls = gpt4all.GPT4All(
        model_name=LLM_MODEL_NAME,
        model_path=LLM_MODEL_PATH
    )
    gpt4all_cls.download_model(
        model_filename=LLM_MODEL_NAME, 
        model_path=LLM_MODEL_PATH,
        verbose=True
    )
llm.load_model(model_path=model_path)
# os.cpu_count() เป็นการนับจำนวน Logical Processors
# กำหนดจำนวน Thread ในการทำงานของ LLM ซึ่งในที่นี้จะใช้ Logical Processors ทั้งหมดของ CPU
llm.set_thread_count(os.cpu_count())



print()
while True:
    question=input('Input question here (Enter "exit" to end): ')
    if question.strip() == '':
        continue
    if question.lower() == 'exit':
        break



    # ทดสอบถาม AI DB
    personnel_info = ''
    if is_ai_db:
        result_docs = ai_db.similarity_search(query=question, k=AI_DB_SEARCH_RESULT_RECORD)
        personnel_info = ''.join([doc.page_content for doc in result_docs])
        #print(result_docs)

    query_str = prompt.format(personnel_info=personnel_info, question=question)
    print(f'Prompt: {query_str}')
    print()
    llm.generate(
        prompt=query_str,
        streaming=True,
        temp=LLM_MODEL_TEMPORATURE
    )
    print() # เว้นช่องว่างระหว่างคำตอบที่ได้จาก LLM และแสดง Prompt เพื่อรอคำถามใหม่