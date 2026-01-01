from fastapi import FastAPI
from pydantic import BaseModel
from loader import medium_structure_loader
from embeddings_store import store_article_embeddings
from retrieval import retrieve_chunks
from rag_argumentation import build_rag_argumentation_inputs
from rag_generation import generate_final_answer
from langchain_core.documents import Document
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# INDEX ENDPOINT
# ================================
class IndexArticleRequest(BaseModel):
    article_url: str
    article_content: str


@app.post("/index-article")
async def index_article(payload: IndexArticleRequest):

    chunks = medium_structure_loader(
        article_text=payload.article_content,
        source_url=payload.article_url
    )

    store_article_embeddings(
        article_url=payload.article_url,
        chunks=chunks
    )

    return {
        "status": "ok",
        "chunk_count": len(chunks),
        "message": "Article indexed and embeddings stored successfully."
    }



# ================================
# RAG QUERY PIPELINE
# ================================
class RetrieveRequest(BaseModel):
    mode: str
    question: str
    article_url: str | None = None
    snippet: str | None = None


@app.post("/query")
async def query_route(req: RetrieveRequest):

    # ----------------------------
    # 1. RETRIEVAL
    # ----------------------------
    if req.mode == "ask_document":
        retrieved_docs = retrieve_chunks(
            article_url=req.article_url,
            query=req.question
        )

    elif req.mode == "ask_selected":
        retrieved_docs = [Document(page_content=req.snippet)]

    else:
        return {"error": "Invalid mode"}


    # ----------------------------
    # 2. ARGUMENTATION PREP
    # ----------------------------
    prep = build_rag_argumentation_inputs(
        query=req.question,
        retrieved_chunks=retrieved_docs
    )

    # prompt (messages list)
    prompt = prep["prompt"]

    # pydantic schema
    schema = prep["schema"]


    # ----------------------------
    # 3. GENERATION (LLM)
    # ----------------------------
    answer_object = generate_final_answer(
        prompt=prompt,
        schema=schema
    )
    
    print(answer_object)

    # ----------------------------
    # 4. FINAL RESPONSE TO FRONTEND
    # ----------------------------
    return {
        "status": "ok",
        "message": "final answer ready",
        "answer": answer_object,
        "retrieved_chunks": [d.page_content for d in retrieved_docs]
    }
