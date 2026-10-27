const input = document.querySelector("#inputText");
const count = document.querySelector("#charCount");
const button = document.querySelector("#analyzeBtn");
const errorBox = document.querySelector("#error");
input.addEventListener("input", () => count.textContent = `${input.value.length} / 10000`);
button.addEventListener("click", analyze);
document.querySelector("#refreshHistory").addEventListener("click", loadHistory);

async function analyze() {
  errorBox.classList.add("hidden");
  const text = input.value.trim();
  if (!text) { showError("Enter a message or URL first."); return; }
  button.disabled = true; button.textContent = "Investigating…";
  try {
    const response = await fetch("/api/analyze", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");
    renderResult(data); await loadHistory();
  } catch (e) { showError(e.message || "Could not contact the local server."); }
  finally { button.disabled = false; button.innerHTML = 'Analyze input <span>→</span>'; }
}
function showError(message) { errorBox.textContent = message; errorBox.classList.remove("hidden"); }
function renderResult(data) {
  const section = document.querySelector("#results");
  section.classList.remove("hidden");
  const risk = data.risk;
  document.querySelector("#score").textContent = risk.score;
  document.querySelector("#advice").textContent = risk.advice;
  const badge = document.querySelector("#levelBadge");
  badge.textContent = `${risk.level} risk`; badge.className = `risk-badge ${risk.level.toLowerCase()}`;
  const findings = [];
  const ml = data.ml_analysis;
if (ml) {
  findings.push({
    title: "Machine Learning Classifier",
    detail: ml.available
      ? `Prediction: ${ml.prediction.toUpperCase()} | Spam probability: ${(ml.spam_probability * 100).toFixed(1)}%`
      : `Unavailable: ${ml.note}`
  });
}
  for (const [category, terms] of Object.entries(data.message_analysis.signals)) findings.push({title:category.replaceAll("_"," "), detail:`Matched wording: ${terms.join(", ")}`});
  for (const url of data.url_analysis.urls) {
    findings.push({title:`URL: ${url.host}`,detail:url.flags.length ? url.flags.join(" · ") : "No URL heuristic flags detected."});
    findings.push({title:"URL limitation",detail:url.note});
  }
  document.querySelector("#findings").innerHTML = findings.map(f=>`<div class="finding"><strong>${escapeHtml(f.title)}</strong>${escapeHtml(f.detail)}</div>`).join("");
  document.querySelector("#trace").innerHTML = data.agent_trace.map(t=>`<div class="trace-item"><b>${escapeHtml(t.agent)}</b><span>${escapeHtml(t.detail)}</span></div>`).join("");
  section.scrollIntoView({behavior:"smooth",block:"start"});
}
function escapeHtml(value) { return String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
async function loadHistory() {
  const container = document.querySelector("#history");
  try {
    const response = await fetch("/api/history"); const data = await response.json();
    if (!data.items.length) { container.innerHTML='<p class="muted">No scans yet. Your completed investigations will appear here.</p>'; return; }
    container.innerHTML = data.items.map(item=>`<div class="history-item"><div class="sample">${escapeHtml(item.input_text)}<small>${escapeHtml(item.created_at)}</small></div><strong>${escapeHtml(item.risk_level)} · ${item.risk_score}/100</strong></div>`).join("");
  } catch { container.innerHTML='<p class="muted">History could not be loaded.</p>'; }
}
loadHistory();
