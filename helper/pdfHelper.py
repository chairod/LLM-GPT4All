"""
อ่านเนื้อหาจากไฟล์ PDF ซึ่ง Helper class นี้
จะต้อง install package PyPDf2==3.0.1
"""
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from typing import List
from PyPDF2 import PdfReader

class customPdfLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        r = PdfReader(stream=self.file_path)
        page_contents = ' '.join([p.extract_text() for p in r.pages])

        #print(f'\n\nPage Content: {page_contents}, From: {self.file_path}\n\n')
        return [Document(page_content=page_contents, metadata={ 'source': self.file_path })]