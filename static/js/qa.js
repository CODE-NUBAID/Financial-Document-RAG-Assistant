// qa.js — handles question asking, answer + citation rendering, history

const queryInput     = document.getElementById("query-input");
const askBtn         = document.getElementById("ask-btn");
const resultsArea    = document.getElementById("results-area");
const historySection = document.getElementById("history-section");
const historyList    = document.getElementById("history-list");

let qaHistory = JSON.parse(localStorage.getItem("invoiceai_history") || "[]");

askBtn.addEventListener("click", askQuestion);
queryInput.addEventListener("keydown", e => { if (e.key === "Enter") askQuestion(); });

if (qaHistory.length) renderHistory();

async function askQuestion() {
  const query = queryInput.value.trim();
  if (!query || !window.docReady) return;

  askBtn.classList.add("loading");
  askBtn.disabled = true;
  resultsArea.innerHTML = "";

  try {
    const res  = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    data.error ? window.showError(data.error) : renderAnswer(query, data.answer, data.citations);
  } catch { window.showError("Something went wrong. Please try again."); }
  finally { askBtn.classList.remove("loading"); askBtn.disabled = false; }
}

// ── Render answer + citations ───────────────────────────────────────────────────
function renderAnswer(query, answer, citations) {
  let html = `
    <div class="answer-card">
      <div class="a-label">✦ Answer</div>
      <div class="a-body">${esc(answer)}</div>
    </div>`;

  if (citations?.length) {
    html += `<div class="citation-list">` + citations.map(c => `
      <div class="citation">
        <div class="citation-meta">
          📄 ${esc(c.source_file)} · Page ${c.page}
          <span class="relevance-bar"><span class="relevance-fill" style="width:${c.relevance}%"></span></span>
          ${c.relevance}% match
        </div>
        <div class="citation-excerpt">${esc(c.excerpt)}</div>
      </div>`).join("") + `</div>`;
  }

  resultsArea.innerHTML = html;
  addHistory(query, answer);
}

// ── History (persisted in localStorage) ─────────────────────────────────────────
function addHistory(q, a) {
  qaHistory.unshift({ q, a, ts: new Date().toLocaleString() });
  if (qaHistory.length > 10) qaHistory.pop();
  localStorage.setItem("invoiceai_history", JSON.stringify(qaHistory));
  renderHistory();
}

function renderHistory() {
  if (qaHistory.length < 1) return;
  historySection.style.display = "block";
  historyList.innerHTML = qaHistory.map(item => `
    <div class="history-item">
      <div class="history-q">Q: ${esc(item.q)} <small style="color:var(--ink-3)">· ${item.ts || ""}</small></div>
      <div class="history-a">${esc(item.a.substring(0, 200))}${item.a.length > 200 ? "…" : ""}</div>
    </div>`).join("");
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function esc(str) {
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
