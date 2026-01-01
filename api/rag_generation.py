# rag_generation.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# HuggingFace Gateway Token
hf_token = os.getenv("HF_TOKEN")


# =====================================================
# CREATE LLM INSTANCE (HUGGINGFACE ROUTER)
# =====================================================
def get_llm(structured_schema):
    """
    Returns a ChatOpenAI model configured to output
    strictly matching the provided Pydantic schema.
    """

    base_model = ChatOpenAI(
        model="openai/gpt-oss-20b:groq",
        openai_api_key=hf_token,
        openai_api_base="https://router.huggingface.co/v1",
        temperature=0  # IMPORTANT for zero hallucinations in RAG
    )

    return base_model.with_structured_output(structured_schema)



# =====================================================
# GENERATION CALL
# =====================================================
def generate_final_answer(prompt, schema):
    """
    Uses HuggingFace Router LLM + Pydantic structured output
    to generate final RAG answer.
    """

    llm = get_llm(schema)

    response = llm.invoke(prompt)

    # Convert pydantic object → python dict (then > json automatic)
    return response.dict()
