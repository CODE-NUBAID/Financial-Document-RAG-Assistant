"""ingestion.py — Load PDFs, attach source metadata, build FAISS index.

Supports multiple PDFs in one vector store. Each chunk keeps track of
which file and page it came from, so answers can cite their source.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env")


def load_pdf(path: str, source_name: str = None):
    """Load a single PDF. Tags every page with its filename for citations."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")

    docs = PyPDFLoader(path).load()
    label = source_name or os.path.basename(path)
    for d in docs:
        d.metadata["source_file"] = label
        # PyPDFLoader pages are 0-indexed internally; show 1-indexed to users
        d.metadata["page_display"] = d.metadata.get("page", 0) + 1
    return docs


def split_documents(docs):
    """Split into overlapping chunks, preserving source/page metadata."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)


def build_vector_db(chunks):
    """Embed chunks and store in a fresh FAISS index."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=API_KEY,
    )
    return FAISS.from_documents(chunks, embeddings)


def add_documents(db, chunks):
    """Add more chunks to an existing FAISS index (multi-PDF support)."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=API_KEY,
    )
    new_db = FAISS.from_documents(chunks, embeddings)
    db.merge_from(new_db)
    return db


def chunk_stats(chunks):
    """Quick stats used in the UI — shows retrieval engineering awareness."""
    sizes = [len(c.page_content) for c in chunks]
    return {
        "count": len(chunks),
        "avg_size": round(sum(sizes) / len(sizes)) if sizes else 0,
        "min_size": min(sizes) if sizes else 0,
        "max_size": max(sizes) if sizes else 0,
    }
