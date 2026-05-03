import streamlit as st
from rag_utils import load_pdf, split_documents, create_vector_db, answer_query

st.title("📄 Invoice RAG Assistant")

uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    docs = load_pdf("temp.pdf")
    split_docs = split_documents(docs)
    db = create_vector_db(split_docs)

    query = st.text_input("Ask a question:")

    if query:
        answer, source_docs = answer_query(db, query)

        st.subheader("🤖 Answer")
        st.write(answer)

        st.subheader("📌 Retrieved Context")
        for doc in source_docs[:2]:
            st.write(doc.page_content[:300])