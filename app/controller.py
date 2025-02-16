from app.llm_utils import generate_embedding, complete_chat
from app.vectordb import store_embedding, get_rel_docs
from app.utils import get_current_doc_id, chunk_text, store_current_doc_id, ssmclient


async def ingest_document_from_file(file):
    import uuid
    doc_id = str(uuid.uuid4())

    chunk_size = 200
    counter = 0

    while True:
        content = await file.read(1024)  # Await the read operation
        if not content:
            break

        text = content.decode("utf-8")  # Decode the bytes to string
        counter, current_chunks = chunk_text(
            text=text, counter=counter, chunk_size=chunk_size
        )

        for ind, txt in current_chunks.items():
            store_embedding(doc_id=str(doc_id), ind=str(counter) + str(ind), text=txt)

    store_current_doc_id(doc_id)
    return {"message": "Document ingested successfully", "doc_id": str(doc_id)}


def handle_question(query: str):
    # query = query
    query_embedding = generate_embedding(query)
    current_doc_id = get_current_doc_id()

    relevant_text_documents = get_rel_docs(query_embedding, current_doc_id)

    return complete_chat(rel_docs=relevant_text_documents, question=query)


def select_document(doc_id: str):
    response = ssmclient.put_parameter(
        Name="CURRENT_DOCUMENT_ID",
        Value=doc_id,
        Type="SecureString",
        Overwrite=True,
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {"response": f"document updated successfully with doc_id{doc_id}"}
    else:
        return {"response": "unable to update "}


def list_all_document_ids():
    currentdoid = get_current_doc_id()

    allids = ssmclient.get_parameter(Name="ALL_DOC_IDS", WithDecryption=True)
    document_ids = allids["Parameter"]["Value"].split(",")

    return {"cur_doc_id": currentdoid, "all_doc_ids": document_ids}
