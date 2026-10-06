from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_PATH = "/home/workspace/learning/AI_Support_Eng/data/chroma_db"

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to the existing Chroma database
vectorstore = Chroma(
    collection_name="acmecloud_support_handbook",
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings,
)

# Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)