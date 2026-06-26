// upload.js — handles multi-PDF drag-drop, file select, upload + indexing

const uploadZone   = document.getElementById("upload-zone");
const fileInput    = document.getElementById("pdf-input");
const uploadProg   = document.getElementById("upload-progress");
const uploadBar    = document.getElementById("upload-bar");
const uploadStatus = document.getElementById("upload-status");

// Drag-and-drop (accepts multiple files)
["dragover", "dragenter"].forEach(e =>
  uploadZone.addEventListener(e, ev => { ev.preventDefault(); uploadZone.classList.add("drag-over"); })
);
["dragleave", "drop"].forEach(e =>
  uploadZone.addEventListener(e, ev => { ev.preventDefault(); uploadZone.classList.remove("drag-over"); })
);
uploadZone.addEventListener("drop", ev => handleFiles([...ev.dataTransfer.files]));
fileInput.addEventListener("change", () => handleFiles([...fileInput.files]));

async function handleFiles(files) {
  const pdfs = files.filter(f => f.name.endsWith(".pdf"));
  if (!pdfs.length) { window.showError("Please upload PDF file(s)."); return; }

  for (const file of pdfs) {
    await uploadOne(file);
  }
}

async function uploadOne(file) {
  uploadProg.style.display = "block";
  uploadStatus.style.display = "block";
  uploadStatus.textContent = `Indexing ${file.name}…`;
  uploadBar.style.width = "40%";

  const fd = new FormData();
  fd.append("pdf", file);

  try {
    const res  = await fetch("/upload", { method: "POST", body: fd });
    const data = await res.json();
    uploadBar.style.width = "100%";

    if (data.error) { window.showError(data.error); resetProgress(); return; }

    uploadStatus.textContent = `✓ ${file.name} indexed`;
    setTimeout(() => { uploadProg.style.display = "none"; uploadStatus.style.display = "none"; }, 1200);

    renderStats(data);
    document.getElementById("qa-section").style.display = "block";
    window.docReady = true;

  } catch { window.showError("Upload failed. Try again."); resetProgress(); }
}

function renderStats(data) {
  document.getElementById("doc-stats").innerHTML = `
    <span class="stat-badge">📄 ${data.pages} pages</span>
    <span class="stat-badge">🔖 ${data.chunks} chunks</span>
    <span class="stat-badge">📏 avg ${data.avg_chunk_size} chars/chunk</span>
    <span class="stat-badge">📚 ${data.total_files} file${data.total_files > 1 ? "s" : ""}</span>`;
  document.getElementById("doc-stats").style.display = "flex";

  document.getElementById("file-pills").innerHTML = data.all_files
    .map(name => `<span class="file-pill">📄 ${name}</span>`).join("");

  document.getElementById("reset-btn").style.display = "inline-block";
}

function resetProgress() {
  uploadBar.style.width = "0%";
  setTimeout(() => { uploadProg.style.display = "none"; uploadStatus.style.display = "none"; }, 600);
}
