import os


# OLD MONGO CREDS
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# DB_NAME = "document_db"
# DOCUMENT_COLLECTION = "documents"
# DOCUMENT_MANAGER_COLLECTION = "doc_manager"


# here use your openai api key i have used mine in env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
COMPLETION_MODEL = os.getenv("COMPLETION_MODEL", "gpt-3.5-turbo")


PINECONE_ENV = os.getenv("PINECONE_ENV", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "")


S3BUCKETNAME = "documentsbucket657"
AWSREGION = "us-east-1"
