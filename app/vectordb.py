from pinecone import Pinecone
import numpy as np
from app.llm_utils import generate_embedding
from app.config import PINECONE_API_KEY, PINECONE_INDEX


PineconeClient = Pinecone(api_key=PINECONE_API_KEY)


def store_embedding(doc_id:str, ind:str, text:str):
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

    index = PineconeClient.Index(PINECONE_INDEX)

    response = index.query(
        vector=query_embedding.tolist(), 
        top_k=2,
        # namespace=PINECONE_NAMESPACE,
        include_metadata=True, 
        filter={"doc_id":current_doc_id}
    )

    relevant_docs = [match["metadata"]["text"] for match in response["matches"]]
    return relevant_docs

