// extract.js — structured invoice field extraction

const extractBtn  = document.getElementById("extract-btn");
const extractArea = document.getElementById("extract-area");

const FIELD_LABELS = {
  vendor: "Vendor", client: "Client", invoice_number: "Invoice #",
  invoice_date: "Invoice Date", due_date: "Due Date",
  total_amount: "Total Amount", currency: "Currency",
};

extractBtn.addEventListener("click", async () => {
  if (!window.docReady) return;

  extractBtn.textContent = "Extracting…";
  extractBtn.disabled = true;

  try {
    const res  = await fetch("/extract", { method: "POST" });
    const data = await res.json();

    if (data.error) { window.showError(data.error); return; }
    renderFields(data);
  } catch {
    window.showError("Extraction failed. Please try again.");
  } finally {
    extractBtn.textContent = "🧩 Extract Structured Fields";
    extractBtn.disabled = false;
  }
});

function renderFields(data) {
  const cards = Object.entries(FIELD_LABELS).map(([key, label]) => {
    const value = data[key];
    const isEmpty = value === null || value === undefined || value === "";
    return `
      <div class="field-card">
        <div class="field-label">${label}</div>
        <div class="field-value ${isEmpty ? "empty" : ""}">${isEmpty ? "Not found" : esc(value)}</div>
      </div>`;
  }).join("");

  extractArea.innerHTML = `<div class="field-grid">${cards}</div>`;
}

function esc(str) {
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
