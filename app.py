from flask import Flask, render_template, request, jsonify
from rag_utils import (
    load_pdf,
    split_documents,
    create_vector_db,
    answer_query
)

import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    global db

    file = request.files.get("pdf")

    if not file:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        })

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(pdf_path)

    docs = load_pdf(pdf_path)

    split_docs = split_documents(docs)

    db = create_vector_db(split_docs)

    return jsonify({
        "success": True,
        "message": "Document processed successfully"
    })


@app.route("/ask", methods=["POST"])
def ask_question():

    global db

    if db is None:
        return jsonify({
            "answer": "Please upload a document first.",
            "sources": []
        })

    data = request.get_json()

    query = data.get("question")

    if not query:
        return jsonify({
            "answer": "Please enter a question.",
            "sources": []
        })

    try:

        answer, source_docs = answer_query(
            db,
            query
        )

        sources = [
            doc.page_content[:400]
            for doc in source_docs[:3]
        ]

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:

        return jsonify({
            "answer": f"Error: {str(e)}",
            "sources": []
        })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )