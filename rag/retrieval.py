"""retrieval.py — Retrieve relevant chunks and generate grounded answers.
Implements the core anti-hallucination RAG prompt and attaches page-level citations + retrieval relevance scores to every answer.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = os.getenv("GOOGLE_API_KEY")

SYSTEM_PROMPT = 
"""You are a Financial Document Assistant analyzing invoices.
RULES (follow strictly):
1. Answer ONLY using the CONTEXT below. Never use outside knowledge.
2. If the answer is not present in the context, reply exactly: "Not found in document."
3. Do not guess, infer, or estimate missing numbers or dates.
4. Be concise — one or two sentences.
5. Quote the exact supporting line from the context as your source.

CONTEXT:
{context}

QUESTION: {question}

RESPONSE FORMAT (always follow this):
Answer: <your answer>
Source: <exact quote from context>"""

def retrieve_chunks(db, query: str, k: int = 4):
    """
    Run similarity search and return chunks with relevance scores.
    FAISS returns L2 distance — lower means more similar. We convert it to a 0-100 'relevance' score so it's readable in the UI, but we label it honestly as a retrieval-similarity score, not a calibrated confidence probability.
    """
    results = db.similarity_search_with_score(query, k=k)
    chunks = []
    for doc, distance in results:
        relevance = max(0, round(100 - distance * 20))  # heuristic scaling
        chunks.append({"doc": doc, "relevance": relevance})
    return chunks

def answer_query(db, query: str, k: int = 4) -> dict:
    """Full RAG answer pipeline: retrieve → prompt → generate → cite."""
    retrieved = retrieve_chunks(db, query, k=k)
    if not retrieved:
        return {"answer": "Not found in document.", "citations": []}
    context = "\n\n".join(r["doc"].page_content for r in retrieved)
    prompt = SYSTEM_PROMPT.format(context=context, question=query)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)
    answer_text = llm.invoke(prompt).content
    citations = [
        {
            "source_file": r["doc"].metadata.get("source_file", "document"),
            "page": r["doc"].metadata.get("page_display", "?"),
            "relevance": r["relevance"],
            "excerpt": r["doc"].page_content[:300],
        }
        for r in retrieved[:3]
    ]
    return {"answer": answer_text, "citations": citations}
