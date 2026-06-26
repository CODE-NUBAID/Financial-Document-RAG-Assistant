"""app.py — Flask entry point: upload, ask, and extract routes."""

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from rag.ingestion import load_pdf, split_documents, build_vector_db, add_documents, chunk_stats
from rag.retrieval import answer_query
from rag.extraction import extract_invoice_fields

app = Flask(__name__)
app.secret_key = os.urandom(24)
limiter = Limiter(get_remote_address, app=app, default_limits=["50 per hour"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Per-session in-memory state: db, file list, and raw text for extraction
sessions: dict = {}

def _key(req):
    return req.cookies.get("session", "default")

def _get_session(req):
    return sessions.setdefault(_key(req), {"db": None, "files": [], "all_text": ""})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
@limiter.limit("10 per hour")
def upload():
    file = request.files.get("pdf")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF."}), 400

    path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(path)
    state = _get_session(request)

    try:
        docs = load_pdf(path, source_name=file.filename)
        chunks = split_documents(docs)
        state["db"] = add_documents(state["db"], chunks) if state["db"] else build_vector_db(chunks)
        state["files"].append(file.filename)
        state["all_text"] += "\n".join(d.page_content for d in docs) + "\n"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    stats = chunk_stats(chunks)
    return jsonify({
        "success": True,
        "doc_name": file.filename,
        "pages": len(docs),
        "chunks": stats["count"],
        "avg_chunk_size": stats["avg_size"],
        "total_files": len(state["files"]),
        "all_files": state["files"],
    })

@app.route("/ask", methods=["POST"])
@limiter.limit("15 per hour")

def ask():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    state = _get_session(request)
    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400
    if not state["db"]:
        return jsonify({"error": "No document indexed. Upload a PDF first."}), 400
    try:
        result = answer_query(state["db"], query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract", methods=["POST"])
def extract():
    """Structured field extraction — returns invoice data as JSON."""
    state = _get_session(request)
    if not state["all_text"]:
        return jsonify({"error": "No document indexed. Upload a PDF first."}), 400

    try:
        fields = extract_invoice_fields(state["all_text"])
        return jsonify(fields)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/reset", methods=["POST"])
def reset():
    """Clear this session's uploaded documents, index, and extracted text."""
    key = _key(request)
    sessions.pop(key, None)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
    
