import hashlib
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.documents import Document
load_dotenv()


# ----------------------------------
# Embedding model (HuggingFace endpoint)
# ----------------------------------
embeddings = HuggingFaceEndpointEmbeddings(
    repo_id="sentence-transformers/all-MiniLM-L6-v2"
)

# ----------------------------------
# Hash article URL → consistent collection name
# ----------------------------------
def get_collection_name(article_url: str) -> str:
    return hashlib.sha256(article_url.encode()).hexdigest()[:32]


# ----------------------------------
# Check if collection exists
# ----------------------------------
def collection_exists(persist_dir: str, collection_name: str) -> bool:
    if not os.path.exists(persist_dir):
        return False

    # Chroma stores collections inside the persist directory
    # We can check if collection manifest exists
    try:
        existing = Chroma(
            persist_directory=persist_dir,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        count = existing._collection.count()
        return count > 0
    except Exception:
        return False



# ----------------------------------
# Store embeddings for the article
# ----------------------------------
def store_article_embeddings(article_url: str, chunks: list[Document]):

    persist_dir = "chroma_vector_db"
    collection_name = get_collection_name(article_url)

    # 1. If collection exists → return vectordb (skip embedding)
    if collection_exists(persist_dir, collection_name):
        print(f"🔵 Collection '{collection_name}' already exists. Skipping embedding.")
        vectordb = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
            collection_name=collection_name,
        )
        return vectordb

    # 2. Create new Chroma collection
    print(f"🟢 Creating new Chroma collection: {collection_name}")

    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    # 3. Add documents to vector store
    vectordb.add_documents(chunks)

    print(f"🔶 Stored {len(chunks)} chunks in Chroma collection '{collection_name}'")

    return vectordb
