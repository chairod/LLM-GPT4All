# LLM-GPT4All
GPT4all ในการถามตอบข้อมูลผ่านเอกสาร

Project นี้พัฒนาด้วยภาษา Python ร่วมกับ GPT4All เพื่อใช้เป็นเครื่องมื่อในการถามตอบข้อมูลในเอกสารต่างๆ ที่เรามีไว้อยู่แล้ว
และต้องการให้ AI อ่านข้อมูลเอกสารที่เรามี แล้ว พิมพ์ถาม AI ได้เลยโดยไม่ต้องอ่านเอกสารเอง

ซึ่งขึ้นอยู่กับว่าเรามีข้อมูลมาน้อยเพียงใด ที่จะส่งให้กับ AI เข้าไปอ่านเอกสารนั้นๆ ซึ่ง AI จะทำการอ่านข้อมูลในเอกสาร เก็บลงใน AI DB 
เมื่อมีการถามจะนำข้อมูลที่ได้นั้นมาวิเคราะห์คำถาม และ ตอบออกมาเป็นคำตอบ ตามเนื้อหาในไฟล์ ที่ส่งให้กับ AI


### เตรียมสภาพแวดล้อมก่อน
+ ให้ลง git เพื่อทำการ Clone project นี้ไปไว้ที่เครื่อง (ดาวน์โหลดได้จาก https://git-scm.com/downloads)
+ ใช้ Command นี้ในการ clone project  ` git clone https://github.com/chairod/LLM-GPT4All.git `
+ ให้ลง Python Version ` Python 3.10.11 ` และลง pip ` pip 23.1.2 ` ลิ้งดาวน์โหลด Python https://www.python.org/getit/
+ Window  
ให้ลง `Microsoft Visual C++` ได้จาก Folder `require-package`  
**"vs_BuildTools.exe"** และให้เลือก Package ที่จะลงในเครื่องตามภาพ **"ภาพแสดงการ install Microsoft Visual C++.png"**  
เนื่องจากในขั้นตอน `pip install -r requirements.txt` จะมี Package _ChromaDb_ ที่จำเป็นจะต้องใช้ MSV C++ Version 14 ขึ้นไปในการ Build & Install




### ขั้นตอนการใช้งาน
หลังจากที่ Clone Project มาแล้วให้เข้าไปยัง Folder ของ Project  
แล้วดำเนินการตามขั้นตอนดังต่อไปนี้

**_กำหนดค่าก่อนใช้งาน_ การตั้งค่าต่างๆสามารถกำหนดได้จากไฟล์ _.env_ ซึ่งเนื้อหาในไฟล์ตามที่แสดงในรายละเอียด้านล่างต่อไปนี้**  
```
# พาร์ทที่เก็บ LLM Model File เอาไว้
# *** ไม่ต้องระบุ \ ต่อท้าย
LLM_MODEL_PATH=models

# ชื่อ LLM Model (Deep Trained) ที่ต้องการโหลดมาใช้ในการถามตอบ
# ให้ระบุเฉพาะชื่อ เช่น ggml-gpt4all-j-v1.3-groovy.bin
# สามารถดาวน์โหลดได้จาก https://gpt4all.io/index.html ไปยังหัวข้อ Model Explorer 
# และเลือกดาวน์โหลด Model ที่ต้องการใช้มา
LLM_MODEL_NAME=ggml-gpt4all-j-v1.3-groovy.bin
#LLM_MODEL_NAME=ggml-mpt-7b-instruct.bin

# ค่าอยู่ระหว่าง 0 - 1
# เป็นค่าความคิดสร้างสรรค์ ในการตอบคำถามของ LLM
# ข้อความระวัง:
#  ค่ายิ่งใกล้กับ 1 มากเท่าไหร่คำถามเดียวกัน คำตอบจะได้ไม่เหมือนกัน ในการถามแต่ละครั้ง แต่เนื้อหาของคำตอบจะไปในทางเดียวกัน
#  ค่ายิ่งใกล้กับ 1 ทำให้ได้คำตอบที่สร้างสรรค์มากขึ้นเท่านั้น
LLM_MODEL_TEMPORATURE=0.8


# พาร์ทที่เก็บไฟล์ของ AI Database ซึ่งในโครงการนี้จะใช้ ChromaDB
# ในการเก็บ และ อ่านเอกสาร และ ถามคำexiถามเพื่อให้จัดลำดับข้อความที่ใกล้เคียงกับคำตอบมากที่สุด
AI_DB_PERSIST_DIR=ai_db\

# จำนวนรายการ ที่ได้จากการค้นหาของ AI DB
# ซึ่งการค้นหาของ AI DB จะเป็นการจัดลำดับข้อความ ที่มีความสัมพันธ์กับคำถามมากที่สุดเรียงมาเป็น
# ลำดับที่ 1, 2, 3, 4, ...
# ซึ่งผลลัพธ์ทั้งหมดที่ได้จะถูกผ่านส่งให้กับ LLM เพื่อใช้เป็นข้อมูลในการสร้างคำตอบให้กับผู้ถาม
AI_DB_SEARCH_RESULT_RECORD=3

# ชื่อ Model ของ Embeding ชึ่งใช้ HuggingFaceEmbedding
# สามารถค้นหาชื่อ Model ได้จากเว็บไซด์  https://huggingface.co/
# https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L12-v2


# พาร์ทที่เก็บรายชื่อเอกสารทั้งหมด ที่โปรแกรมจะอ่านเนื้อหาในไฟล์
# และเก็บลงไปใน AI DB
# ไม่ต้องระบุ \ ต่อท้าย
SOURCE_DOCUMENT_PATH=source_documents\
```
+ ให้รันคำสั่ง `pip install -r requirements.txt`  
เพื่อ Install package python ที่จำเป็นสำหรับโครงการนี้
+ ไฟล์เอกสารที่รองรับในปัจจุบัน ประกอบด้วย *.csv, *.doc, *.docx, *.enex, *.eml, *.epub, *.html, *.md, *.dot, *.pdf, *.ppt, *.pptx, *.txt โดยนำเอกสารที่ต้องการให้ AI อ่านไปเก็บไว้ใน Folder **source_documents** หลังจากนั้น  
สั่งให้ AI อ่านข้อมูลเอกสารโดยรันคำสั่ง `python ingre.py` หรือ `py ingre.py`  ตัว AI จะอ่านเอกสารเฉพาะที่ยังไม่เคยเก็บไว้ใน AI DB พร้อมกับแสดงสถานะระหว่างการอ่านไฟล์  
+ เปิดใช้งาน AI โดยรันคำสั่ง `python runner.py` หรือ `py runner.py`  
  **_ระหว่างการรัน_**  
  * หากยังไม่มี Model ที่กำหนดไว้ใน .env **LLM_MODEL_NAME** จะทำการดาวน์โหลดจากเว็บไซด์ของ GPT4all และเก็บลงไปในพาร์ทที่ระบุใน .env **LLM_MODEL_PATH**



### คำนิยามที่ควรทราบ
+ Token ข้อความที่ถูกเก็บอยู่ใน .bin จะถูกเก็บแยกออกเป็นแต่ล่ะ Token ซึ่งในแต่ละ Token ก็จะประกอบไปด้วยข้อความที่อยู่ภายในนั้น  
ยกตัวอย่างเช่น  
ให้มองภาพเป็นลักษณะของ Table ซึ่งใน Table ก็จะประกอบไปด้วย Cell ในแต่ละ Cell ก็คือ Token และในแต่ละ Cell ก็จะประกอบไปด้วย ข้อความที่ถูกเก็บเอาไว้ซึ่งจะมี Id กำกับเอาไว้นั่นก็คือ TokenId


### นัยความหมายของ Parameter ที่จะส่งให้กับ LLM (GPT4All)  
รายชื่อ Parameter ทั้งหมดที่ผ่านให้กับ LLM ที่ใช้ในการรันเพื่อหาคำตอบจากสิ่งที่เราถาม
```
# struct llmodel_prompt_context {
    #     float *logits;          // logits of current context
    #     size_t logits_size;     // the size of the raw logits vector
    #     int32_t *tokens;        // current tokens in the context window
    #     size_t tokens_size;     // the size of the raw tokens vector
    #     int32_t n_past;         // number of tokens in past conversation
    #     int32_t n_ctx;          // number of tokens possible in context window
    #     int32_t n_predict;      // number of tokens to predict
    #     int32_t top_k;          // จำนวน Token ที่บอกให้ LLM หยิบมาวิเคราะห์เพื่อใช้ในการตอบคำถามจากรายการที่มีคำตอบที่เป็นไปได้มากที่สุดไปหาน้อย
เช่น ถามว่า "นี่คือประเทศอะไร" ซึ่งถูกจัดลำดับรายการคำตอบที่เป็นไปได้คือ Thailand, Loa, Malasia, ... ค่าที่จะถูกหยิบมาจาก k คือ Loa, Malasia, ... เป็นต้น
ระบุค่าเป็นจำนวนเต็ม เช่น 10,20,12,6,7, ... เป็นต้น
    #     float top_p;            // เปอร์เซ็นต์ผลรวมของค่า top_k (สมมุติ กำหนดค่า top_k = 10) ผลรวมค่าความเป็นไปได้ของทั้ง 10 รายการจะต้องได้ >= top_p
เช่น
กำหนด top_p = 0.75 หรือ 75%, top_k = 10  ผลรวม % ความน่าจะเป็นของ top_k ทั้ง 10 รายการจะต้อง >= top_p (75%)
    #     float temp;             // ค่าความคิดสร้างสรรค์ ในการสร้างรูปแบบประโยค
สำหรับตอบคำถาม ค่าจะอยู่ระหว่าง 0 - 1 เช่น 0, 0.1, 0.2, 0.3, ..., 1
    #     int32_t n_batch;        // number of predictions to generate in parallel
    #     float repeat_penalty;   // penalty factor for repeated tokens
    #     int32_t repeat_last_n;  // last n tokens to penalize
    #     float context_erase;    // percent of context to erase if we exceed the context window
    # };
```

### Development Change Log
+ 13/06/2023
  + จูนค่าการค้นหาของ AI DB (score) ปัจจุบันใช้ค่าอยู่ที่ไม่เกิน 1.2 เนื่องจากผลลัพธ์จากการค้นหาของ AI DB จะมีค่า Distancing หรือ ค่าความสัมพันธ์ระหว่าคำถาม กับ เนื้อหาในเอกสารภายใน AI DB ซึ่งยิ่งค่าน้อยความสัมพันธ์ของคำถามกับผลการค้นหาก็ยิ่งใกล้เคียงมาก  
  จะมีผลต่อข้อมูลที่มีประสิทธิภาพ ที่จะส่งให้กับ LLM วิเคราะห์เพื่อเรียบเรียงประโยคเป็นคำตอบ  
  + หาค่า Temperature หรือ ค่าความคิดสร้างสรรในการตอบคำถามของ LLM ปัจจุบันใช้ค่าอยู่ที่ 0.1 ซึ่งค่านี้จำเป็นต้องปรับจูนให้เหมาะสมกับบริบทของเอกสารที่นำเข้าไปใน AI DB  

