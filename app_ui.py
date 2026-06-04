from flask import Flask, render_template, request
from rag_utils import load_pdf, split_documents, create_vector_db, answer_query
import os

app = Flask(__name__)

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    answer, sources = None, []
    if request.method == "POST":
        pdf_file = request.files.get("pdf")
        query = request.form.get("query")

        if pdf_file:
            pdf_path = "uploaded_invoice.pdf"
            pdf_file.save(pdf_path)

            docs = load_pdf(pdf_path)
            split_docs = split_documents(docs)
            db = create_vector_db(split_docs)

            if query:
                answer, source_docs = answer_query(db, query)
                sources = [doc.page_content[:300] for doc in source_docs[:2]]

    return render_template("index.html", answer=answer, sources=sources)

if __name__ == "__main__":
    app.run(debug=True)
