from pinecone import Pinecone
import numpy as np
from app.llm_utils import generate_embedding
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "")


PineconeClient = Pinecone(api_key=PINECONE_API_KEY)


def store_embedding(doc_id:str, ind:str, text:str):
    """
    stores the given text's LLM embedding in the Pinecone index. The 
    document id is stored as metadata in the index.

    args:
        doc_id (str): The id of the document to store the embedding for
        ind (str): The index to store the embedding in
        text (str): The text to generate an embedding for and store in the index
    """
    embedding = generate_embedding(text)
    index = PineconeClient.Index(PINECONE_INDEX)

    index.upsert(
        vectors=[
            (
                ind,
                embedding.tolist(),
                {"text": text, "doc_id": doc_id},
            )
        ],  
    )

    print(f"Stored embedding for ID: {id}")


def get_rel_docs(query_embedding:np.ndarray,current_doc_id:str):
    """
    given a query embedding, returns the two most relevant documents from the Pinecone index that do not match the given document id.

    args:
        query_embedding (np.ndarray): The query embedding to search the index with
        current_doc_id (str): The id of the document to exclude from the search results

    returns:
        List[str]: The text of the two most relevant documents, excluding the one with the given id
    """
    index = PineconeClient.Index(PINECONE_INDEX)

    response = index.query(
        vector=query_embedding.tolist(), 
        top_k=2,
        # namespace=PINECONE_NAMESPACE,  #because using default namespace
        include_metadata=True, 
        filter={"doc_id":current_doc_id}
    )

    relevant_docs = [match["metadata"]["text"] for match in response["matches"]]
    return relevant_docs

