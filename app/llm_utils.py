from openai import OpenAI
import openai
import numpy as np
from app.config import OPENAI_API_KEY,COMPLETION_MODEL, EMBEDDING_MODEL

openai.api_key = OPENAI_API_KEY

Client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embedding(text: str) -> np.ndarray:
    response = openai.embeddings.create(input=text, model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    return np.array(embedding)


def complete_chat(rel_docs: list, question: str):
    promt_messages = [
        {
            "role": "system",
            "content": f"""
        You are JIVA an AI assistant that only answers questions based on the PROVIDED_DOCUMENTS . If the answer is not in the PROVIDED_DOCUMENTS, politely say 'I don't know' and do not make up any information.
        PROVIDED_DOCUMENTS : {rel_docs}
        """,
        }
    ]

    promt_messages.append({"role": "user", "content": question})

    try:
        response = Client.chat.completions.create(
            messages=promt_messages,
            model="gpt-3.5-turbo",
            max_tokens=200,
            stream=False,
        )
        return {"completion_response": response.choices[0].message.content}

    except openai.OpenAIError as e:
        return f"Error: {str(e)}"
