import chromadb
from constants import (
    AI_DB_SEARCH_RESULT_RECORD,
    AI_DB_METADATA_INTERNAL_IDX_NAME,
    AI_DB_METADATA_DOCUMENT_SOURCE_NAME,
    load_chroma_database,
    get_default_ai_db_collection_name,
    get_default_embedding,
    is_exists_collection_name
)

class FinetuneQuery:

    @staticmethod
    def query_from_funetune(query_str: str, db: chromadb.API) -> str:
        """
        ค้นหาเนื้อหาภายในเอกสาร ที่เก็บภายใน AI DB มีรูปประโยคใดบ้าง ที่ใกล้เคียงกับ query_str
        """
        ret_str = ''
        if is_exists_collection_name(collection_name=get_default_ai_db_collection_name(), db=db) == False:
            return ret_str
        
        collection = db.get_collection(
            name=get_default_ai_db_collection_name(), 
            embedding_function=get_default_embedding()
        )
        

        # Trim space ซ้าย/ขวา ก่อนใช้เป็นเงื่อนไขในการค้นหา เพราะทุกตัวอักษรถูกนำไปคิดเป็น เงื่อนไขทั้งหมด
        query_str = query_str.strip()
        query_str = query_str.replace("'", "\x027")

        # ค้นหารูปแบบประโยคที่เฉพาะเจาะจง
        parent_out = collection.query(
            query_texts=[query_str],
            n_results=AI_DB_SEARCH_RESULT_RECORD,
            where_document={
                '$contains': query_str
            }
        )
        if len(parent_out['documents'][0]) == 0:

            # ถ้าค้นหาด้วยเงื่อนไข รูปแบบประโยคที่เฉพาะเจาะจงไม่เจอ ให้ค้นหาแบบ distancing
            # คือ ให้ AI DB จัดลำดับข้อความที่มีความน่าจะเป็น ที่ใกล้เคียงกับ ประโยคคำถามมากที่สุด ไปหาน้อย (Distancing)
            # โดยใช้ ผลลัพธ์จากรายการแรก ไปค้นหาผลลัพธ์อื่นๆ
            # เนื่องจาก กรณีมีเอกสารเก็บมากกว่า 1 รายการจะทำให้ได้ผลลัพธ์จาก เอกสารอื่นๆ ติดมาด้วย ซึ่งถือว่า 
            # ไม่ใช่ข้อมูลส่วนที่ต้องการนำไปหาคำตอบ
            out = collection.query(
                query_texts=[query_str],
                n_results=1
            )
            if len(out['documents'][0]) == 0:
                return ret_str

            # ค้นหาเนื้อหาเอกสาร รายการอื่นๆ จากเอกสารเดียวกัน โดยอ้างอิงจาก source ของผลลัพธ์แรก
            source_path = out['metadatas'][0][0]['source']
            out = collection.query(
                query_texts=[query_str],
                where={
                    'source':{ '$eq': source_path }
                },
                n_results=AI_DB_SEARCH_RESULT_RECORD
            )
            
            ### ควรเพิ่ม Logic ตรวจสอบ Distaincing เท่าไหร่ถึงจะไม่นำมาควบรวม เป็นเนื้อหาให้กับ LLM
            ### ซึ่งในปัจจุบันเชื่อเฉพาะรายการแรก
            ## โดยมีความเป็นไปได้ ว่า เนื้อหาของข้อความ อาจจะไปอยู่ในเล่มอื่นๆ หรือ source เอกสารอื่นๆ
            ## ดังนั้น เนื้อหาของคำตอบเพื่อส่งให้กับ LLM อาจจะต้องใช้ 2 เล่มประกอบกัน


            ret_str = ''.join([f'{document_content} ' if document_content.endswith('.\n') else document_content for document_content in out['documents'][0]]) if len(out['documents'][0]) > 0 else ''
            return ret_str
        

        ret_str = parent_out['documents'][0][0]

        # ค้นหา Chunk ในลำดับถัดไปจาก parent_out
        # เนื่องจาก Chunk เป็นการตัดชุดของข้อความออกเป็นส่วนๆ มีโอกาสที่ คำตอบ ของคำถามจะไปอยู่ใช้ Chunk ลำดับถัดไป
        doc_source = parent_out['metadatas'][0][0][AI_DB_METADATA_DOCUMENT_SOURCE_NAME]
        doc_internal_idx = parent_out['metadatas'][0][0][AI_DB_METADATA_INTERNAL_IDX_NAME]
        doc_internal_idx = f"idx_{int(doc_internal_idx.replace('idx_', '')) + 1}"
        out = collection.query(
            query_texts=[query_str],
            n_results=1,
            where={
                '$and':[
                    {
                        AI_DB_METADATA_DOCUMENT_SOURCE_NAME: {
                            '$eq': doc_source
                        }
                    },
                    {
                        AI_DB_METADATA_INTERNAL_IDX_NAME: {
                            '$eq': doc_internal_idx
                        }
                    }
                ]
            }
        )


        ret_str = f'{ret_str} ' if ret_str.endswith('.\n') else ret_str
        ret_str = f"{ret_str}{out['documents'][0][0]}" if len(out['documents'][0]) > 0 else ret_str

        return ret_str