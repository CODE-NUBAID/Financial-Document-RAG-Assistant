# 📄 Invoice RAG Assistant

> **AI-Powered Financial Document Question Answering using Retrieval-Augmented Generation (RAG)**

Transform static invoice PDFs into intelligent, searchable knowledge sources. Instead of manually scanning invoices, users can ask questions in natural language and receive accurate, context-aware answers grounded directly in the document.

---

## 🚀 Overview

**Invoice RAG Assistant** is a Retrieval-Augmented Generation (RAG) application that enables users to interact with invoice PDFs through conversational queries.

Simply upload an invoice and ask questions such as:

- 💰 **What is the total amount?**
- 📅 **What is the due date?**
- 👤 **Who is the client?**
- 🧾 **What is the invoice number?**

The system retrieves the most relevant information from the invoice and generates responses strictly based on the document content, reducing hallucinations and improving reliability.

---

## 🧠 RAG Workflow

```text
Invoice PDF
     │
     ▼
Text Extraction
     │
     ▼
Chunking
     │
     ▼
Embeddings Generation
     │
     ▼
FAISS Vector Database
     │
     ▼
User Query
     │
     ▼
Relevant Context Retrieval
     │
     ▼
Gemini LLM
     │
     ▼
Final Answer + Source Context
```

---

## ✨ Features

- 📄 Upload and process invoice PDFs
- 🔍 Ask questions in natural language
- 🎯 Context-aware answers grounded in invoice data
- 🚫 Hallucination-resistant responses
- 📌 Source text displayed for transparency
- ⚡ Fast semantic search using FAISS
- 💻 Command Line Interface (CLI)
- 🌐 Optional Streamlit Web Interface
- 🛡️ Error handling for common failures

---

## 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| RAG Framework | LangChain |
| Vector Database | FAISS |
| LLM | Gemini (Google Generative AI) |
| Embeddings | Google Generative AI Embeddings |
| PDF Processing | PyPDF |
| Environment Variables | python-dotenv |
| User Interface | Flask |

---

## 📂 Project Structure

```text
invoice-rag-system/
│
├── app.py                # CLI application
├── app_ui.py             # Streamlit UI (optional)
├── rag_utils.py          # Core RAG pipeline logic
├── invoice.pdf           # Sample invoice document
├── requirements.txt      # Project dependencies
├── .env                  # API key configuration
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CODE-NUBAID/Financial-Document-RAG-Assistant
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from:

https://aistudio.google.com/

### 5. Add an Invoice PDF

Place your invoice file in the root directory:

```text
invoice.pdf
```

---

## ▶️ Running the Application

### CLI Mode

```bash
python app.py
```

### Streamlit Web Interface

```bash
streamlit run app_ui.py
```

---

## 💬 Example Queries

Try asking:

```text
What is the invoice number?
What is the total amount?
What is the due date?
Who is the client?
What services were billed?
When was the invoice issued?
```

---

## 📌 Example Response

```text
Question:
What is the total amount?

Answer:
The total amount is ₹15,000.

Source:
"Total Amount: ₹15,000"
```

---

## ⚠️ Error Handling

The application gracefully handles:

- ❌ Missing API key
- ❌ Missing PDF file
- ❌ Invalid document format
- ❌ Empty user queries
- ❌ No relevant context found
- ❌ API request failures

If information is not available in the document, the system returns:

```text
Not found in document.
```

---

## 🧩 Core Components

| Component | Purpose |
|------------|----------|
| PyPDFLoader | Extracts text from PDF invoices |
| Text Splitter | Divides text into manageable chunks |
| Embeddings Model | Converts text into vector representations |
| FAISS | Stores and retrieves document embeddings |
| Retriever | Finds the most relevant chunks for a query |
| Gemini LLM | Generates answers using retrieved context |

---

## 🎯 Key Learning Outcomes

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Semantic Search and Vector Databases
- Document Question Answering Systems
- LangChain Integration
- FAISS Vector Store Usage
- Gemini API Integration
- Prompt Engineering Techniques
- Building AI-Powered Business Applications

---

## 🔮 Future Enhancements

- 📊 Multi-invoice support
- 🧾 Structured invoice extraction (JSON format)
- 🔗 n8n workflow integration
- 📈 Analytics dashboard
- 🤖 Automatic document classification
- 📤 Bulk invoice processing
- 🌍 Multi-language support
- 🏢 Vendor and customer insights

---
