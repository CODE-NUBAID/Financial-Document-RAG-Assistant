"""evaluation.py — RAG eval harness: retrieval hit rate, answer accuracy, latency.

Two separate failure modes are tracked: did FAISS retrieve the right chunk at all (retrieval_hit), and did the final LLM answer contain the right value (answer_correct).
A wrong final answer with a retrieval hit means the LLM misread good context; a miss means retrieval itself failed.

Usage: python evaluation.py path/to/invoice.pdf
"""

import sys
import json
import time
from rag.ingestion import load_pdf, split_documents, build_vector_db
from rag.retrieval import answer_query, retrieve_chunks

# Replace these with the REAL values from YOUR invoice — open the PDF
# and type the true answer. Without real values this only checks
# "did it answer," not "was the answer correct."
TEST_CASES = [
    {"question": "What is the invoice number?",   "expect_contains": "POD-26-148579648 or IN-613"},
    {"question": "What is the total amount due?", "expect_contains": "241"},
    {"question": "Who is the vendor?",             "expect_contains": "KOMAL CHAWLA"},
    {"question": "What is the due date?",          "expect_contains": "Not found"},
    {"question": "What is the capital of France?", "expect_contains": "Not found"},
]


def run_evaluation(pdf_path: str):
    print(f"Loading and indexing: {pdf_path}\n")
    docs = load_pdf(pdf_path)
    chunks = split_documents(docs)
    db = build_vector_db(chunks)

    results = []
    retrieval_hits = 0
    answer_correct = 0
    total_latency = 0.0

    for case in TEST_CASES:
        question = case["question"]
        expected = case["expect_contains"]

        start = time.time()
        retrieved = retrieve_chunks(db, question, k=4)
        result = answer_query(db, question)
        latency = round(time.time() - start, 2)
        total_latency += latency

        answer = result["answer"]
        hit, correct = _retrieval_hit(retrieved, expected), _answer_correct(answer, expected)
        retrieval_hits += int(hit)
        answer_correct += int(correct)

        results.append({
            "question": question,
            "answer": answer,
            "retrieval_hit": hit,
            "answer_correct": correct,
            "latency_sec": latency,
        })

        status = "✅" if correct else "❌"
        r_status = "✅" if hit else "❌"
        print(f"{status} Answer | {r_status} Retrieval | {latency}s  — {question}")
        print(f"        → {answer[:120]}")
        print()

    total = len(TEST_CASES)
    retrieval_rate = round(retrieval_hits / total * 100, 1)
    answer_rate = round(answer_correct / total * 100, 1)
    avg_latency = round(total_latency / total, 2)

    print("=" * 55)
    print(f"Retrieval Hit Rate : {retrieval_hits}/{total} ({retrieval_rate}%)")
    print(f"Answer Accuracy    : {answer_correct}/{total} ({answer_rate}%)")
    print(f"Avg Latency        : {avg_latency}s/question")
    print("=" * 55)
    _save_report(results, retrieval_rate, answer_rate, avg_latency)


def _retrieval_hit(retrieved: list, expected: str) -> bool:
    """Expected text found in ANY retrieved chunk's raw content?"""
    if not expected or expected.lower() == "not found":
        return True
    combined = " ".join(r["doc"].page_content for r in retrieved).lower()
    return expected.lower() in combined


def _answer_correct(answer: str, expected: str) -> bool:
    """Did the final answer contain the expected value (or refuse)?"""
    return expected.lower() in answer.lower()


def _save_report(results, retrieval_rate, answer_rate, avg_latency):
    report = {
        "retrieval_hit_rate_percent": retrieval_rate,
        "answer_accuracy_percent": answer_rate,
        "avg_latency_sec": avg_latency,
        "results": results,
    }
    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Saved detailed report to eval_report.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluation.py path/to/invoice.pdf")
        sys.exit(1)
    run_evaluation(sys.argv[1])
