import hashlib
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings


# ----------------------------------
# Reuse the SAME embedding model
# ----------------------------------
embeddings = HuggingFaceEndpointEmbeddings(
    repo_id="sentence-transformers/all-MiniLM-L6-v2"
)


# ----------------------------------
# Helper: Hash URL → collection name
# ----------------------------------
def get_collection_name(article_url: str) -> str:
    return hashlib.sha256(article_url.encode()).hexdigest()[:32]


# ----------------------------------
# Load vectordb collection for this URL
# ----------------------------------
def load_vectordb(article_url: str):
    persist_dir = "chroma_vector_db"
    collection_name = get_collection_name(article_url)

    vectordb = Chroma(
        persist_directory=persist_dir,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    return vectordb


# ----------------------------------
# RETRIEVAL LOGIC
# ----------------------------------
def retrieve_chunks(article_url: str, query: str):

    vectordb = load_vectordb(article_url)

    # MMR = Maximum Marginal Relevance
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,        # final chunks returned
            "fetch_k": 15  # candidates considered
        }
    )

    # Retrieve matching chunks
    results = retriever.invoke(query)

    # Print chunks for debugging
    print("\n================ RETRIEVED CHUNKS ================\n")
    for i, doc in enumerate(results):
        print(f"---- Retrieved Chunk {i+1} ----")
        print(doc.page_content)
        print("\n----------------------------------------------\n")
    print("==================================================\n")

    return results
