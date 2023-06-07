from constants import (
    EMBEDDING_MODEL_NAME, 
    AI_DB_PERSIST_DIR, 
    CHROMA_SETTINGS, 
    LLM_MODEL_PATH,
    LLM_MODEL_NAME,
    LLM_MODEL_TEMPORATURE
)
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# โหลด AI Database เพื่อสร้าง Instance สำหรับการสร้างคำถาม
embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
ai_db = Chroma(
    persist_directory=AI_DB_PERSIST_DIR,
    embedding_function=embedding,
    client_settings=CHROMA_SETTINGS
)


# ผ่านข้อมูลที่ได้จาก AI DB ให้กับ LLM (GPT4All) เพื่อเรียบเรียงคำตอบ
from langchain.prompts import PromptTemplate
from gpt4all import pyllmodel
prompt=PromptTemplate(
    template=
"""
information: {personnel_info}
question: {question}
""",
    input_variables=['personnel_info', 'question']
)
llm = pyllmodel.LLModel()
llm.load_model(model_path=f'{LLM_MODEL_PATH}\\{LLM_MODEL_NAME}')



print()
while True:
    question=input('Input question here: ')
    if question == 'exit':
        break
    if question.strip() == '':
        continue



    # ทดสอบถาม AI DB
    result_docs = ai_db.similarity_search(query=question, )
    #print(result_docs)

    query_str = prompt.format(personnel_info=''.join([doc.page_content for doc in result_docs]), question=question)
    print(f'Prompt: {query_str}')
    print()
    llm.generate(
        prompt=query_str,
        streaming=True,
        temp=LLM_MODEL_TEMPORATURE
    )
    print() # เว้นช่องว่างระหว่างคำตอบที่ได้จาก LLM และ Prompt เพื่อรอคำถามใหม่