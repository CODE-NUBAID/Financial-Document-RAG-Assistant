import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# ---------- LOAD PDF ----------
def load_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ PDF file not found")

    loader = PyPDFLoader(file_path)
    return loader.load()


# ---------- SPLIT TEXT ----------
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


# ---------- CREATE VECTOR DB ----------
def create_vector_db(docs):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    return FAISS.from_documents(docs, embeddings)


# ---------- CREATE LLM ----------
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key
    )


# ---------- PROMPT ----------
def build_prompt(context, question):
    return f"""
You are a highly accurate invoice analysis assistant.

STRICT RULES:
- Answer ONLY from the provided context
- Do NOT guess
- If not found, say: "Not found in document"

CONTEXT:
{context}

QUESTION:
{question}

OUTPUT FORMAT:
Answer: <answer>
Source: <exact line from context>
"""


# ---------- QUERY FUNCTION ----------
def answer_query(db, query):
    retriever = db.as_retriever()

    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant data found."

    context = "\n".join([doc.page_content for doc in docs])

    llm = get_llm()
    prompt = build_prompt(context, query)

    response = llm.invoke(prompt)

    return response.content, docs