import re
import chromadb
from helper.finetuneHelper import FinetuneQuery
from constants import (
    #EMBEDDING_MODEL_NAME, 
    #AI_DB_PERSIST_DIR, 
    #SOURCE_DOCUMENT_PATH,
    #EMBEDDING_INSTANCE,
    #CHROMA_SETTINGS, 
    LLM_RUNNING_MODE,
    LLM_MODEL_PATH,
    LLM_MODEL_NAME,
    #LLM_MODEL_TEMPORATURE,
    # AI_DB_SEARCH_RESULT_RECORD,
    # AI_DB_METADATA_INTERNAL_IDX_NAME,
    # AI_DB_METADATA_DOCUMENT_SOURCE_NAME,
    load_chroma_database,
    # get_default_ai_db_collection_name,
    # get_default_embedding,
    # is_exists_collection_name
)
#from langchain.vectorstores import Chroma
#from dotenv import load_dotenv

#from langchain.embeddings import HuggingFaceEmbeddings

# โหลด AI Database เพื่อสร้าง Instance สำหรับการสร้างคำถาม
# embedding = EMBEDDING_INSTANCE #HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
# ai_db = Chroma(
#     persist_directory=AI_DB_PERSIST_DIR,
#     embedding_function=embedding,
#     client_settings=CHROMA_SETTINGS
# )
# collection = ai_db.get()
# metadatas = [meta['source'] for meta in collection['metadatas']]
# is_ai_db = len(metadatas) > 0
# if is_ai_db == False:
#     print()
#     print('Warning: \nIf you want to ask any question from document')
#     print('before run this script please run "python ingre.py" to create AI database and query any question')
#     print()
# # else:
# #     # ถ้ามีการสร้าง AI Database แล้ว
# #     # ตรวจสอบรายการไฟล์ ที่อยู่ใน "SOURCE_DOCUMENT_PATH" 
# #     # หากมีไฟล์ที่ยังไม่ถูกเก็บลงใน AI DB เรียก ingre.py เพื่อทำงาน
# #     import os
# #     files = os.listdir(SOURCE_DOCUMENT_PATH)
# #     files = [f'{SOURCE_DOCUMENT_PATH}\\{f}' for f in files]
    
# #     for file in files:



ai_db = load_chroma_database()
if len(ai_db.list_collections()) == 0:
    print()
    print('Warning: \nIf you want to ask any question from document (FineTune)')
    print('before run this script please run "python ingre.py" to create AI database and then query any question')
    print('Hint: You can settings document source path from .env file and supports file types .xls, .pdf, .json, .txt, .doc, .docx, .html, ...')
    print()

# def query_from_funetune(query_str: str, db: chromadb.API) -> str:
#     """
#     ค้นหาเนื้อหาภายในเอกสาร ที่เก็บภายใน AI DB มีรูปประโยคใดบ้าง ที่ใกล้เคียงกับ query_str
#     """
#     ret_str = ''
#     if is_exists_collection_name(collection_name=get_default_ai_db_collection_name(), db=db) == False:
#         return ret_str
    
#     collection = db.get_collection(
#         name=get_default_ai_db_collection_name(), 
#         embedding_function=get_default_embedding()
#     )


#     # Trim space ซ้าย/ขวา ก่อนใช้เป็นเงื่อนไขในการค้นหา เพราะทุกตัวอักษรถูกนำไปคิดเป็น เงื่อนไขทั้งหมด
#     query_str = query_str.strip()
#     query_str = query_str.replace("'", "\x027")

#     # ค้นหารูปแบบประโยคที่เฉพาะเจาะจง
#     parent_out = collection.query(
#         query_texts=[query_str],
#         n_results=AI_DB_SEARCH_RESULT_RECORD,
#         where_document={
#             '$contains': query_str
#         }
#     )
#     if len(parent_out['documents'][0]) == 0:
#         # ถ้าค้นหาด้วยเงื่อนไข รูปแบบประโยคที่เฉพาะเจาะจงไม่เจอ ให้ค้นหาแบบ distancing
#         # คือ ให้ AI DB จัดลำดับข้อความที่มีความน่าจะเป็น ที่ใกล้เคียงกับ ประโยคคำถามมากที่สุด ไปหาน้อย (Distancing)
#         out = collection.query(
#             query_texts=[query_str],
#             n_results=AI_DB_SEARCH_RESULT_RECORD
#         )

#         ret_str = ''.join([f'{document_content} ' if document_content.endswith('.\n') else document_content for document_content in out['documents'][0]]) if len(out['documents'][0]) > 0 else ''
#         return ret_str
    

#     ret_str = parent_out['documents'][0][0]

#     # ค้นหา Chunk ในลำดับถัดไปจาก parent_out
#     # เนื่องจาก Chunk เป็นการตัดชุดของข้อความออกเป็นส่วนๆ มีโอกาสที่ คำตอบ ของคำถามจะไปอยู่ใช้ Chunk ลำดับถัดไป
#     doc_source = parent_out['metadatas'][0][0][AI_DB_METADATA_DOCUMENT_SOURCE_NAME]
#     doc_internal_idx = parent_out['metadatas'][0][0][AI_DB_METADATA_INTERNAL_IDX_NAME]
#     doc_internal_idx = f"idx_{int(doc_internal_idx.replace('idx_', '')) + 1}"
#     out = collection.query(
#         query_texts=[query_str],
#         n_results=1,
#         where={
#             '$and':[
#                 {
#                     AI_DB_METADATA_DOCUMENT_SOURCE_NAME: {
#                         '$eq': doc_source
#                     }
#                 },
#                 {
#                     AI_DB_METADATA_INTERNAL_IDX_NAME: {
#                         '$eq': doc_internal_idx
#                     }
#                 }
#             ]
#         }
#     )


#     ret_str = f'{ret_str} ' if ret_str.endswith('.\n') else ret_str
#     ret_str = f"{ret_str}{out['documents'][0][0]}" if len(out['documents'][0]) > 0 else ret_str

#     return ret_str





    

# ผ่านข้อมูลที่ได้จาก AI DB ให้กับ LLM (GPT4All) เพื่อเรียบเรียงคำตอบ
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering.stuff_prompt import CHAT_PROMPT
#from gpt4all import pyllmodel, gpt4all
from gpt4allV0_3 import pyllmodel, gpt4all
from helper.ProgressiveCounter import TimerCounter


import time
import os
model_path = f'{LLM_MODEL_PATH}\\{LLM_MODEL_NAME}'
if os.path.exists(model_path) == False:
    print(f"Please wait a moment for download model {LLM_MODEL_NAME} from website and save to local path {LLM_MODEL_PATH}")
    gpt4all.GPT4All.download_model(
        model_filename=LLM_MODEL_NAME, 
        model_path=LLM_MODEL_PATH
    )
    print('Please wait about 5 seconds after download LLM Model')
    time.sleep(5) # หยุดรอ 5 วินาที หลังดาวน์โหลดไฟล์เสร็จ

llm = pyllmodel.LLModel()
llm.load_model(model_path=model_path)
# os.cpu_count() เป็นการนับจำนวน Logical Processors
# กำหนดจำนวน Thread ในการทำงานของ LLM ซึ่งในที่นี้จะใช้ Logical Processors ทั้งหมดของ CPU
llm.set_thread_count(os.cpu_count())


# กำหนดรูปแบบของ Prompt
# สำหรับผ่านค่าให้กับ LLM
# {personnel_info}, {question}  ตั้งชื่อเป็นอะไรก็ได้ และ input_variables จะต้องกำหนดชื่อนั้นๆลงไปด้วย
# question: เมื่อ LLM เจอคำนี้และได้คำตอบแล้ว LLM จะแสดงข้อความว่า  Answer: ....
prompt=PromptTemplate(
    template= """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer, answer short questions without explanation, make up an answer of no more than 3 sentences, there must be no test cases out there in the answer.

{context}

Question: {question}
Helpful Answer:""",
    input_variables=['context', 'question']
)

progressive = TimerCounter()
print()
#good_distancing_qa_score = float(os.environ.get('AI_DB_SEARCH_RESULT_DISTANCING_SCORE_QA_LESS_THAN'))
llm_temperature = float(os.environ.get('LLM_MODEL_TEMPORATURE'))
while True:
    question=input('Input question here (Enter "exit" to end): ').strip()
    if '' == question or len(question) == 1:
        continue
    if 'exit' == question.lower():
        break

    # load_dotenv()
    # good_distancing_qa_score = float(os.environ.get('AI_DB_SEARCH_RESULT_DISTANCING_SCORE_QA_LESS_THAN'))
    # llm_temperature = float(os.environ.get('LLM_MODEL_TEMPORATURE'))

    # ทดสอบถาม AI DB
    # personnel_info = ''
    # if is_ai_db:
    #     result_docs = ai_db.similarity_search_with_score(
    #         query=question, 
    #         k=AI_DB_SEARCH_RESULT_RECORD,
    #         kwargs={
                
    #         }
    #     )
    #     out_info = []
    #     for doc in result_docs:
    #         document, score = doc

    #         # ค่า score ที่ได้จาก ai db ที่น่าเชื่อถือที่สุด เพราะบางครั้งสิ่งที่เข้าไป สอบถาม ใน AI DB
    #         # เนื้อหาของข้อความที่ได้จะไม่ตรงกับคำถาม เป็นผลทำให้  LLM ไม่สามารถตอบคำถามได้ จนตอบคำถามเพี้ยน
    #         if good_distancing_qa_score == -1 or score >= good_distancing_qa_score:
    #             continue
    #         out_info.append(f'{document.page_content}')
    #         #out_info.append(f'\n\nscore: {score}\n') # แสดง score เส้นระยะความใกล้เคียงของเนื้อหาใน ai db กับคำถาม

    #     # ถ้าคำถามกับเนื้อหาใน AI DB ไม่มีส่วนที่เกี่ยวข้อง บอกให้ AI ตอบไปว่า "I don\'t know"
    #     # ตัว AI DB จะจับคำ "answer" แล้วนำไปตอบให้
    #     if len(out_info) == 0: 
    #         out_info.append('Answer: "I don\'t know"')
    #     personnel_info = ' .\n '.join(out_info) + ' .\n'

    finetune_context = FinetuneQuery.query_from_funetune(query_str=question,db=ai_db)
    #finetune_context = "Answer: i don't know" if finetune_context.strip() == '' else finetune_context
    query_str = prompt.format(context=finetune_context, question=question)
    # query_template_str = """
    # {human_information}

    # Question: {question}
    # """
    # query_str = query_template_str.replace('{human_information}', personnel_info)
    # query_str = query_str.replace('{question}', question)

    if 'DEBUG' == LLM_RUNNING_MODE:
        query_str_out = query_str#.replace("\n", "[debug:new_line]")
        f = open('prompt.log', 'w')
        f.write(f'prompt message: \n{query_str_out}')
        #f.write(f'\n\n\nResult from fine-tune:\n{finetune_context}')
        f.close()

        #print(query_str_out)

    # เอกสาร อ้างอิงความหมายของ Parameter 
    # custom_gpt4all\llmodel_DO_NOT_MODIFY\llmodel_c.h -> llmodel_prompt_context
    # อ่านรายระเอียดในแต่ละ Parameter 
    #   ได้จาก llm-parameter-meaning หรือใน README.md "นัยความหมายของ Parameter ที่จะส่งให้กับ LLM (GPT4All)"
    #
    #  
    #
    # struct llmodel_prompt_context {
    #     float *logits;          // logits of current context
    #     size_t logits_size;     // the size of the raw logits vector
    #     int32_t *tokens;        // current tokens in the context window
    #     size_t tokens_size;     // the size of the raw tokens vector
    #     int32_t n_past;         // number of tokens in past conversation
    #     int32_t n_ctx;          // number of tokens possible in context window
    #     int32_t n_predict;      // number of tokens to predict
    #     int32_t top_k;          // top k logits to sample from => จำนวน Token
    #     float top_p;            // nucleus sampling probability threshold
    #     float temp;             // temperature to adjust model's output distribution
    #     int32_t n_batch;        // number of predictions to generate in parallel
    #     float repeat_penalty;   // penalty factor for repeated tokens
    #     int32_t repeat_last_n;  // last n tokens to penalize
    #     float context_erase;    // percent of context to erase if we exceed the context window
    # };

    #progressive.StartWaiting()
    llm.generate(
        prompt=query_str,
        streaming=True,

        # ค่าอยู่ระหว่าง 0 - 1 เช่น 0.1, 0.2, 0.3, 0.4, ..., 1
        # เป็นค่าความคิดสร้างสรรค์ ในการตอบคำถามของ LLM
        # นัยสำคัญของ Fine-tune:
        #   ค่า temp จะมีนัยสำคัญในการนำข้อความ ที่ผ่านให้กับ LLM ด้วย Prompt โดย LLM จะนำ Prompt นั้นมาวิเคราะห์ข้อความที่อยู่ภายใน Prompt เพื่อให้ได้ซึ่งคำตอบ
        # ตัวอย่างเช่น:
        #   Feature: Deposit cash balance Conditions: Users can't deposit cash amounts over 20,000 baht per transaction.\n 
        # Users can’t deposit cash amounts over 500,000 baht per day.\n
        # Users can deposit cash amounts between 9.00-17.00 If the user’s age is between 12- and 15 years old the fee amount charged is 0.00 baht.\n
        #
        #  Question: Can I deposit more than 500,000 baht per day?
        #  ถ้ากำหนด temp = 0.3 คำตอบที่ได้จะเป็น Yes เสมอ
        #  ถ้ากำหนด temp = 0.5 คำตอบที่ได้จะเป็น No แต่รูปแบบประโยค ยังไม่สมบูรณ์
        #  ถ้ากำหนด temp = 0.6 คำตอบที่ได้จะเป็น No แต่รูปแบบประโยค ยังไม่สมบูรณ์ แต่ทิศทางดีกว่า temp = 0.5
        #  ถ้ากำหนด temp = 0.7 คำตอบที่ได้จะเป็น No แต่รูปแบบประโยค เริ่มสมบูรณ์ขึ้น แต่ยังมีบางส่วนที่ต้องแก้ไข
        #  ถ้ากำหนด temp = 0.8 คำตอบที่ได้จะเป็น No รูปแบบประโยคเริ่มถูกต้อง และมีทิศทางทีดี (แนะนำให้ใช้ค่าประมาณนี้)
        #
        # คำแนะนำและบริษทในการปรับค่า:
        #   A. หากนำ LLM นี้ไปใช้งานในเอกสารที่เป็น ลักษณะ Q & A ซึ่งมีคำถามและคำตอบ ในเนื้อหาอยู่แล้ว แนะนำให้ใช้ค่าที่ 0.3 ก็เพียงพอแล้ว
        #   B. หากนำ LLM นี้ไปใช้งานในเอกสารที่มีเนื้อหา ที่ต้องการให้ LLM นำเนื้อหานั้นมาวิเคราะห์ข้อความ เพื่อสังเคราะห์ออกมาเป็นคำตอบให้ปรับค่าเป็น 0.8 จะถือเป็นค่าที่เหมาะสม
        temp=llm_temperature,


        # จำนวน Token (ชุดของข้อความที่มีความเป็นไปได้ ที่ใกล้งเคียงกับคำถาม) ที่บอกให้ LLM หยิบมาใช้ในการสร้างประโยคคำตอบ
        # ซึ่งรายการ Token ที่ได้จะถูกจัดลำดับ (sort) ตามความน่าจะเป็นที่ มากสุดไปน้อย สุด
        # ค่านี้จะมีผลต่อ ความยาวของประโยคคำตอบ
        # กำหนดค่านี้เป็น 1 จะได้ประโยคคำตอบที่สั้นและกระชับ
        top_k=20, 


        # ผลรวม % จากจำนวนทั้งหมดของ top_k (คือ 20 รายการ)
        # จะต้องได้ >= top_p ถึงจะออกมาเป็นคำตอบ
        # หลักๆ แล้วจะใช้ในการ กรองข้อมูล Token ที่มีความน่าจะเป็น ของคำตอบน้อย ออกไป
        top_p=0.9,

        # จำนวนคำ (Token) สูงสุด ที่นำมาสร้างเป็นรูปประโยคคำตอบ สูงสุดไม่เกินจำนวนกี่คำ
        # หากเกินจำนวนคำที่กำหนดแล้ว ถึงแม้ประโยคจะไม่สมบูรณ์ ก็จะหยุดสร้างคำตอบทันที (Stop Generate Text)
        n_predict = 128,


        # จำนวน Prediction (การคาดการณ์/การทำนาย คำถาม หรือ จำนวนคำถาม) ที่จะเกิดขึ้นระหว่างการสร้างคำตอบ (Generate text)
        # ส่วนใหญ่จะเกิดในกรณีที่ Q & A
        # เช่น
        # Q: Is it possible to buy and sell shares when the Share Status is CLOSEONLY? \
        # A: No, it is not possible to buy and sell shares when the Share Status is CLOSEONLY.
        # What are the possible values for the CanBuy and CanSell Account Status options?
        #
        # เมื่อ LLM สร้างคำตอบ สิ่งที่ได้จะเป็นส่วนของ A (Answer) และมีคำถามติดมาด้วย What are ...
        # หากกำหนดค่า n_batch 2,3,4,5, ... LLM ก็จะค้นหาคำตอบเพิ่มเติมจากคำถามที่พบ
        n_batch=1500,

        
        

        #repeat_penalty = 0,
        #repeat_last_n = 0,
    )

    #progressive.StopWaiting()
    print() # เว้นช่องว่างระหว่างคำตอบที่ได้จาก LLM และแสดง Prompt เพื่อรอคำถามใหม่



