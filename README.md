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



