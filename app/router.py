from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from app.controller import (
    ingest_document_from_file,
    handle_question,
    list_all_document_ids,
    select_document,
)


router = APIRouter()


@router.post("/add_document")
async def ingest_document_route(file: UploadFile = File(...)) -> dict:
    return await ingest_document_from_file(file)


@router.get("/ask")
def qa(query: str) ->dict:
    # tell me something about karna"
    return handle_question(query)


@router.get("/list_doc_ids")
def list_doc_ids() -> dict:
    return list_all_document_ids()


@router.post("/select_document")
def select_documents_route(selected_doc_id: str) -> dict:
    return select_document(selected_doc_id)
