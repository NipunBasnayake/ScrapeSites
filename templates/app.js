let jobId = null;
let latestFiles = null;
let table = null;

function toast(msg, type = "info") {
  const container = document.getElementById("toast-container");
  const id = "t" + Date.now();
  const el = document.createElement("div");
  el.className = `toast align-items-center text-bg-${type} border-0 show mb-2`;
  el.role = "alert";
  el.ariaLive = "assertive";
  el.ariaAtomic = "true";
  el.id = id;
  el.innerHTML = `<div class="d-flex">
    <div class="toast-body">${msg}</div>
    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
  </div>`;
  container.appendChild(el);
  setTimeout(() => {
    if (document.getElementById(id)) container.removeChild(el);
  }, 6000);
}

function setStatus(s) {
  document.getElementById("status").textContent = "Status: " + s;
}

function enableDownload(files) {
  latestFiles = files;
  const btn = document.getElementById("downloadBtn");
  btn.disabled = false;
  btn.onclick = () => {
    const path = files.csv;
    window.open(`/api/download?path=${encodeURIComponent(path)}`, "_blank");
  };
}

function fillTable(data) {
  const tbody = document.querySelector("#resultsTable tbody");
  tbody.innerHTML = "";
  (data || []).forEach((v, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${i + 1}</td><td>${v}</td>`;
    tbody.appendChild(tr);
  });
  if (!table) {
    table = $("#resultsTable").DataTable({ pageLength: 10 });
  } else {
    table.clear();
    table.rows.add(
      $("#resultsTable tbody tr")
        .toArray()
        .map((r) => [r.cells[0].innerText, r.cells[1].innerText])
    );
    table.draw();
  }
}

function savePresets() {
  const presets = JSON.parse(localStorage.getItem("scraper_presets") || "{}");
  const name = prompt("Preset name:");
  if (!name) return;
  const p = readForm();
  presets[name] = p;
  localStorage.setItem("scraper_presets", JSON.stringify(presets));
  refreshPresetList();
}

function refreshPresetList() {
  const select = document.getElementById("presetSelect");
  const presets = JSON.parse(localStorage.getItem("scraper_presets") || "{}");
  select.innerHTML = '<option value="">— select preset —</option>';
  Object.keys(presets).forEach((k) => {
    const opt = document.createElement("option");
    opt.value = k;
    opt.text = k;
    select.appendChild(opt);
  });
}

function removePreset() {
  const sel = document.getElementById("presetSelect");
  const name = sel.value;
  if (!name) return alert("Select a preset");
  const presets = JSON.parse(localStorage.getItem("scraper_presets") || "{}");
  delete presets[name];
  localStorage.setItem("scraper_presets", JSON.stringify(presets));
  refreshPresetList();
}

function loadPreset() {
  const sel = document.getElementById("presetSelect");
  const name = sel.value;
  if (!name) return;
  const presets = JSON.parse(localStorage.getItem("scraper_presets") || "{}");
  const p = presets[name];
  if (p) {
    setForm(p);
  }
}

function readForm() {
  return {
    url: document.getElementById("url").value,
    selector_type: document.getElementById("selector_type").value,
    selector_value: document.getElementById("selector_value").value,
    attr: document.getElementById("attr").value,
    pagination: {
      pattern: document.getElementById("pag_pattern").value || null,
      start: parseInt(document.getElementById("pag_start").value || 1),
      count: parseInt(document.getElementById("pag_count").value || 1),
      delay: parseFloat(document.getElementById("pag_delay").value || 1),
    },
    timeout: parseInt(document.getElementById("timeout").value || 10),
  };
}

function setForm(p) {
  document.getElementById("url").value = p.url || "";
  document.getElementById("selector_type").value = p.selector_type || "class";
  document.getElementById("selector_value").value = p.selector_value || "";
  document.getElementById("attr").value = p.attr || "";
  document.getElementById("pag_pattern").value =
    (p.pagination && p.pagination.pattern) || "";
  document.getElementById("pag_start").value =
    (p.pagination && p.pagination.start) || 1;
  document.getElementById("pag_count").value =
    (p.pagination && p.pagination.count) || 1;
  document.getElementById("pag_delay").value =
    (p.pagination && p.pagination.delay) || 1;
  document.getElementById("timeout").value = p.timeout || 10;
}

async function startScrape() {
  const btn = document.getElementById("scrapeBtn");
  btn.disabled = true;
  setStatus("Starting job...");
  const payload = readForm();
  if (!payload.pagination.pattern) payload.pagination = null;
  try {
    const res = await fetch("/api/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const j = await res.json();
    if (!j.ok) {
      toast("Start failed: " + (j.error || "unknown"), "danger");
      setStatus("Idle");
      btn.disabled = false;
      return;
    }
    jobId = j.job_id;
    setStatus(`Job ${jobId} started`);
    pollStatus();
  } catch (e) {
    toast("Network error: " + e.message, "danger");
    setStatus("Idle");
    btn.disabled = false;
  }
}

async function pollStatus() {
  if (!jobId) return;
  setStatus("Running...");
  try {
    const r = await fetch(`/api/status/${jobId}`);
    const j = await r.json();
    if (!j.ok) {
      toast("Status fetch failed", "danger");
      return;
    }
    const job = j.job;
    if (job.status === "running" || job.status === "pending") {
      setTimeout(pollStatus, 1200);
      return;
    } else if (job.status === "done") {
      setStatus("Done");
      const data = job.result.data || [];
      fillTable(data);
      if (job.result.files) enableDownload(job.result.files);
      if ((job.result.errors || []).length)
        document.getElementById("errors").textContent =
          job.result.errors.join("\n");
      toast("Scrape completed", "success");
      document.getElementById("scrapeBtn").disabled = false;
      jobId = null;
    } else if (job.status === "error") {
      setStatus("Error");
      toast("Scrape error: " + (job.error || "unknown"), "danger");
      document.getElementById("scrapeBtn").disabled = false;
      jobId = null;
    } else {
      setStatus(job.status);
      document.getElementById("scrapeBtn").disabled = false;
      jobId = null;
    }
  } catch (e) {
    toast("Status polling error: " + e.message, "danger");
    setTimeout(pollStatus, 2000);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  refreshPresetList();
  document.getElementById("savePreset").addEventListener("click", savePresets);
  document
    .getElementById("removePreset")
    .addEventListener("click", removePreset);
  document
    .getElementById("presetSelect")
    .addEventListener("change", loadPreset);
  document.getElementById("scrapeBtn").addEventListener("click", startScrape);

  const dm = localStorage.getItem("dark") === "true";
  if (dm) document.body.classList.add("dark");
  document.getElementById("darkToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark");
    localStorage.setItem("dark", document.body.classList.contains("dark"));
  });

  table = $("#resultsTable").DataTable({
    pageLength: 10,
    searching: true,
    info: false,
  });
});
