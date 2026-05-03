# 📄 Invoice RAG Assistant  
### 🔍 AI-Powered Financial Document Q&A System using RAG

> Transform static invoices into intelligent, queryable data using Retrieval Augmented Generation (RAG)

---

## 🚀 Overview

The **Invoice RAG Assistant** is an AI-powered system that allows users to interact with invoice PDFs using natural language. 

Instead of manually scanning documents, users can simply ask:
*   💰 *"What is the total amount?"*  
*   📅 *"What is the due date?"*  
*   👤 *"Who is the client?"*  

...and get **accurate, context-based answers directly from the document**.

---

## 🧠 How It Works (RAG Pipeline)

1.  **PDF** → Text Extraction
2.  **Chunking** → Breaking text into manageable pieces
3.  **Embeddings** → Converting text to numerical vectors
4.  **FAISS Vector DB** → Storing and indexing data
5.  **Query** → User asks a question
6.  **Retrieval** → Finding relevant document sections
7.  **Gemini LLM** → Generating the final answer based on context

---

## ✨ Features

*   📄 **Upload & Process:** Seamlessly handle invoice PDFs.
*   🔍 **Natural Language:** Query documents using plain English.
*   🎯 **Grounded Answers:** Responses are strictly based on document context.
*   🚫 **No Hallucinations:** Returns *"Not found in document"* if data is missing.
*   📌 **Transparency:** Shows source text used to generate the answer.
*   💻 **CLI & UI:** Supports both terminal and Streamlit interfaces.

---

## 🛠 Tech Stack

| Component | Tool |
| :--- | :--- |
| **Language** | Python |
| **RAG Framework** | LangChain |
| **Vector Database** | FAISS |
| **LLM** | Gemini (Google Generative AI) |
| **PDF Processing** | PyPDF |
| **UI** | Streamlit |

---

## 📂 Project Structure

```text
invoice-rag-system/
│
├── app.py              # CLI application
├── rag_utils.py        # Core RAG logic (Embeddings, FAISS, LLM)
├── app_ui.py           # Streamlit UI (optional)
├── .env                # API key (Keep this private!)
├── requirements.txt    # Dependencies
└── invoice.pdf         # Sample invoice for testing

```
