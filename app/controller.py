from app.llm_utils import generate_embedding, complete_chat
from app.vectordb import store_embedding, get_rel_docs
from app.utils import get_current_doc_id, chunk_text, store_current_doc_id, ssmclient


async def ingest_document_from_file(file):
    """
    asynchronously ingests a document from a file by reading its content, 
    chunking the text, storing embeddings for each chunk, and updating 
    the current document ID.

    args:
        file (uploadFile): An uploaded file object containing the document content.

    returns:
        dict: A message indicating successful ingestion and the generated document id.
    """

    import uuid
    doc_id = str(uuid.uuid4())

    chunk_size = 200
    counter = 0

    while True:
        content = await file.read(1024)  
        if not content:
            break

        text = content.decode("utf-8") 
        counter, current_chunks = chunk_text(
            text=text, counter=counter, chunk_size=chunk_size
        )

        for ind, txt in current_chunks.items():
            store_embedding(doc_id=str(doc_id), ind=str(counter) + str(ind), text=txt)

    store_current_doc_id(doc_id)
    return {"message": "Document ingested successfully", "doc_id": str(doc_id)}


def handle_question(query: str):
    """
    processes a query by generating its embedding, fetching relevant documents,
    and completing the chat interaction with those documents.

    args:
        query (str): The user question or query.

    returns:
        dict: The response from the chat completion, potentially including
              the answer to the user's query.
    """

    query_embedding = generate_embedding(query)
    current_doc_id = get_current_doc_id()

    relevant_text_documents = get_rel_docs(query_embedding, current_doc_id)

    return complete_chat(rel_docs=relevant_text_documents, question=query)


def select_document(doc_id: str):
    """
    updates the current document id in the system's secure parameter store.

    args:
        doc_id (str): The new document id to set as the current document.

    returns:
        dict: A dictionary containing a response message indicating whether 
              the document id was updated successfully or not.
    """

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
    """
    retrieves all document IDs from the system's secure parameter store and returns a json object 
    containing the current document id and all document ids.

    returns:
        dict: A dictionary containing the current document id and all document ids.
    """
    currentdoid = get_current_doc_id()

    allids = ssmclient.get_parameter(Name="ALL_DOC_IDS", WithDecryption=True)
    document_ids = allids["Parameter"]["Value"].split(",")

    return {"cur_doc_id": currentdoid, "all_doc_ids": document_ids}
