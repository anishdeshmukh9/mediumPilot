
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# =====================================================
# 1. STRICT OUTPUT SCHEMA (Pydantic enforced)
# =====================================================
class RAGAnswerSchema(BaseModel):
    answer_title: str = Field(
        ...,
        description="A very short 3–6 word title summarizing the answer. "
                    "Used as bold heading in UI. No long sentences."
    )
    answer: str = Field(
        ...,
        description="The full explanation strictly based on provided context."
    )
    is_answerable: bool = Field(
        ...,
        description="True if answer exists in provided context, else False."
    )
    used_chunks: List[str] = Field(
        ...,
        description="List of text chunks used to answer the question."
    )
    message: str = Field(
        ...,
        description="Status message: 'ok' if answered, otherwise explanation why not."
    )


# =====================================================
# 2. BEST-PRACTICE RAG PROMPT (No JSON enforcement inside)
# =====================================================
RAG_PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
You are a friendly, intelligent assistant. 
your name :- mediumPilot 
purpose :- you are a integrated assistent user asks questions to you from medium article.
You are free to respond naturally, like a helpful human who has read the article text provided below.

Here’s what matters:
- Use the article text only when the question is ABOUT the article.
- If the question is general (like “What is CAGR?” or “What is AI?”), feel free to answer using your own general knowledge.
- If the user is just greeting or chatting, respond warmly and naturally.
- If the user asks something specific that is NOT in the article, be honest about that — 
  say that you don’t see that information in the article, but still respond helpfully if possible.
- Never make up facts about the article.
- Keep answer_title very short (3–6 words
- also give main aswer littel explanable manner deatiled).

-------------------------------
ARTICLE CONTENT (for reference):
{context}
-------------------------------

USER MESSAGE:
{question}

Please provide content that fills the structured output fields (answer_title, answer, is_answerable, used_chunks, message) naturally and conversationally.
""")


# =====================================================
# 3. FUNCTION TO PREPARE ARGUMENTATION INPUT
# =====================================================
def build_rag_argumentation_inputs(query: str, retrieved_chunks: list[object]):
    """
    This function prepares:
    - the merged context for the model
    - the formatted prompt
    - the enforced pydantic output schema

    This does NOT call the LLM.
    It only returns what the upstream pipeline will use later.
    """

    # merge chunk contents into a readable block
    chunk_texts = [doc.page_content for doc in retrieved_chunks]

    context_combined = "\n\n--- CHUNK SPLIT ---\n\n".join(chunk_texts)

    prompt = RAG_PROMPT_TEMPLATE.format(
        question=query,
        context=context_combined
    )

    # return both: prompt + schema
    return {
        "prompt": prompt,
        "schema": RAGAnswerSchema  # pydantic model to enforce output
    }
