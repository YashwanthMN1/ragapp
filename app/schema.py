from pydantic import BaseModel
from fastapi import File, UploadFile


class Document(BaseModel):
    doc_id: str
    content: str


class Query(BaseModel):
    question: str


class DocumentSelection(BaseModel):
    selected_doc_id: str


class DocumentIngestionRequest(BaseModel):
    doc_id: str
    file: UploadFile = File(...)


class DocumentIngestionResponse(BaseModel):
    message: str
    doc_id: str
