// reset.js — clears server session, history, and UI state

document.getElementById("reset-btn").addEventListener("click", async () => {
  if (!confirm("Delete the uploaded document(s) and all Q&A history?")) return;

  try {
    await fetch("/reset", { method: "POST" });
  } catch {}

  localStorage.removeItem("invoiceai_history");
  window.docReady = false;

  document.getElementById("doc-stats").style.display = "none";
  document.getElementById("file-pills").innerHTML = "";
  document.getElementById("qa-section").style.display = "none";
  document.getElementById("extract-section").style.display = "none";
  document.getElementById("extract-area").innerHTML = "";
  document.getElementById("results-area").innerHTML = "";
  document.getElementById("history-section").style.display = "none";
  document.getElementById("history-list").innerHTML = "";
  document.getElementById("upload-filename").textContent = "";
  document.getElementById("reset-btn").style.display = "none";
});