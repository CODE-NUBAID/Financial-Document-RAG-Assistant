// utils.js — shared helpers loaded first by index.html

window.docReady = false;

// Global error renderer used by upload.js and qa.js
window.showError = function(msg) {
  document.getElementById("results-area").innerHTML =
    `<div class="error-card">⚠ ${msg}</div>`;
};

// Build example query pills
const EXAMPLES = [
  "What is the total amount due?",
  "Who is the client?",
  "What is the invoice due date?",
  "What is the invoice number?",
  "List all line items.",
  "What are the payment terms?",
];

document.addEventListener("DOMContentLoaded", () => {
  const wrap = document.getElementById("pills");
  EXAMPLES.forEach(ex => {
    const btn = document.createElement("button");
    btn.className = "pill";
    btn.textContent = ex;
    btn.addEventListener("click", () => {
      document.getElementById("query-input").value = ex;
      document.getElementById("query-input").focus();
    });
    wrap.appendChild(btn);
  });
});

// Theme toggle — persists choice in localStorage
const themeToggle = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("invoiceai_theme") || "dark";
document.documentElement.setAttribute("data-theme", savedTheme);
themeToggle.textContent = savedTheme === "dark" ? "☀️" : "🌙";

themeToggle.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  themeToggle.textContent = next === "dark" ? "☀️" : "🌙";
  localStorage.setItem("invoiceai_theme", next);
});