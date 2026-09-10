import os
from typing import List, Dict, Any

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter


try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
except ImportError:
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.schema import Document


# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

_embedding_model = None


def get_embedding_model():
    """
    Load HuggingFace embedding model only when required.
    """

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


# ---------------------------------------------------------
# TEXT CHUNKING
# ---------------------------------------------------------

def split_text(text: str) -> List[str]:
    """
    Split normal text into smaller overlapping chunks.
    """

    if not text or not text.strip():
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    return text_splitter.split_text(text)


# ---------------------------------------------------------
# PAGE-AWARE CHUNKING
# ---------------------------------------------------------

def create_documents_from_pages(
    pages: List[Dict[str, Any]]
) -> List[Document]:
    """
    Convert page-wise PDF data into LangChain Documents.

    Each chunk keeps:
        - source filename
        - page number
    """

    if not pages:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    documents = []

    for page_data in pages:

        source = page_data.get("source", "Unknown Document")
        page_number = page_data.get("page", "Unknown")
        text = page_data.get("text", "")

        if not text or not text.strip():
            continue

        chunks = text_splitter.split_text(text)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source,
                        "page": page_number
                    }
                )
            )

    return documents


# ---------------------------------------------------------
# CREATE VECTOR STORE FROM PAGE DATA
# ---------------------------------------------------------

def create_vectorstore_from_pages(
    pages: List[Dict[str, Any]]
):
    """
    Create FAISS vector database while preserving
    document filename and page number metadata.
    """

    if not pages:
        raise ValueError("No PDF pages available for vectorization.")

    documents = create_documents_from_pages(pages)

    if not documents:
        raise ValueError("No text chunks were created from PDF pages.")

    embeddings = get_embedding_model()

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vectorstore


# ---------------------------------------------------------
# OLD / BACKWARD-COMPATIBLE VECTOR STORE
# ---------------------------------------------------------

def create_vectorstore(text: str):
    """
    Backward-compatible function.

    This version does not contain source/page metadata.
    Prefer create_vectorstore_from_pages() for the final app.
    """

    if not text or not text.strip():
        raise ValueError("No text available for vectorization.")

    chunks = split_text(text)

    if not chunks:
        raise ValueError("No text chunks were created.")

    embeddings = get_embedding_model()

    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vectorstore


# ---------------------------------------------------------
# RETRIEVE DOCUMENTS
# ---------------------------------------------------------

def get_relevant_documents(
    vectorstore,
    query: str,
    k: int = 5
):
    """
    Retrieve relevant documents from FAISS.

    Returned documents contain:
        page_content
        metadata[source]
        metadata[page]
    """

    if vectorstore is None:
        return []

    if not query or not query.strip():
        return []

    return vectorstore.similarity_search(
        query,
        k=k
    )


# ---------------------------------------------------------
# RETRIEVE CONTEXT WITH SOURCE + PAGE
# ---------------------------------------------------------

def get_relevant_context(
    vectorstore,
    query: str,
    k: int = 5
) -> str:
    """
    Retrieve relevant context and include source document
    and page number for Gemini.
    """

    documents = get_relevant_documents(
        vectorstore,
        query,
        k=k
    )

    if not documents:
        return ""

    context_parts = []

    for i, doc in enumerate(documents, start=1):

        source = doc.metadata.get(
            "source",
            "Unknown Document"
        )

        page = doc.metadata.get(
            "page",
            "Unknown Page"
        )

        context_parts.append(
            f"""
[Relevant Evidence {i}]
Source Document: {source}
Page: {page}

Content:
{doc.page_content}
""".strip()
        )

    return "\n\n".join(context_parts)


# ---------------------------------------------------------
# SAVE FAISS DATABASE
# ---------------------------------------------------------

def save_vectorstore(
    vectorstore,
    folder_path="data/vectorstore"
):
    """
    Save FAISS vector database locally.
    """

    if vectorstore is None:
        raise ValueError("Vectorstore is empty.")

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    vectorstore.save_local(folder_path)

    return folder_path


# ---------------------------------------------------------
# LOAD FAISS DATABASE
# ---------------------------------------------------------

def load_vectorstore(
    folder_path="data/vectorstore"
):
    """
    Load previously saved FAISS vector database.
    """

    if not os.path.exists(folder_path):
        return None

    embeddings = get_embedding_model()

    vectorstore = FAISS.load_local(
        folder_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore