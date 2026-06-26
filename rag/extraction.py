"""extraction.py — Structured field extraction from invoice text.
Demonstrates the 'structured output' pattern: instead of free-text RAG answers, we ask the LLM to return strict JSON matching a known schema.
This is a common real-world AI engineering technique (function-calling / JSON mode) for turning unstructured documents into structured records.
"""

import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = os.getenv("GOOGLE_API_KEY")

EXTRACTION_PROMPT = """Extract invoice fields from the text below.
Return ONLY valid JSON — no markdown, no explanation, no code fences.
Schema:
{{
  "vendor": string or null,
  "client": string or null,
  "invoice_number": string or null,
  "invoice_date": string or null,
  "due_date": string or null,
  "total_amount": string or null,
  "currency": string or null
}}
If a field is not present in the text, use null. Do not guess.
TEXT:
{text}
"""

def extract_invoice_fields(full_text: str) -> dict:
    """Call the LLM once with a JSON-only instruction and parse the result."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)
    prompt = EXTRACTION_PROMPT.format(text=full_text[:6000])  # keep prompt small
    raw = llm.invoke(prompt).content.strip()
    cleaned = _strip_code_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "Could not parse structured fields from this document."}

def _strip_code_fences(text: str) -> str:
    """LLMs sometimes wrap JSON in ```json fences even when told not to."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text
