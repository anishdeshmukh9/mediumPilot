from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def medium_structure_loader(article_text: str, source_url: str):
    """
    Loads and splits Medium article respecting typical structure.
    """

    # 1. Pre-clean text
    cleaned = re.sub(r'\n{3,}', '\n\n', article_text).strip()

    # 2. Medium-aware split rules
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=[
            "\n```",
            "```",
            "\n## ",
            "\n### ",
            "\n- ",
            "\n\n",
            "\n",
            " "
        ]
    )

    chunks = splitter.split_text(cleaned)

    docs = [
        Document(
            page_content=c.strip(),
            metadata={"source": source_url, "length": len(c)}
        )
        for c in chunks
    ]

    return docs


def medium_structure_loader(article_text: str, source_url: str):
    """
    Loads and splits Medium article respecting typical structure:
    - Headings (#, ##)
    - Subheadings
    - Paragraph groups
    - Code blocks (```...```)
    """

    # --------------------------------------------------
    # Step 1: Pre-clean text (remove excessive spacing)
    # --------------------------------------------------
    cleaned = re.sub(r'\n{3,}', '\n\n', article_text).strip()

    # --------------------------------------------------
    # Step 2: Custom chunking logic
    # --------------------------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=[
            "\n```",      # code block start
            "```",        # code block end
            "\n## ",      # section
            "\n### ",     # subsection
            "\n- ",       # bullet point
            "\n\n",       # paragraph break
            "\n",         # line break
            " "           # fallback
        ]
    )

    splits = splitter.split_text(cleaned)

    # --------------------------------------------------
    # Step 3: Convert chunks → LangChain Document objects
    # --------------------------------------------------
    docs = []
    for chunk in splits:
        doc = Document(
            page_content=chunk.strip(),
            metadata={
                "source": source_url,
                "length": len(chunk)
            }
        )
        docs.append(doc)

    return docs
