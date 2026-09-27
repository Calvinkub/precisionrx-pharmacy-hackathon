"use strict";

const $ = (s, el = document) => el.querySelector(s);
const state = { catalog: [], byId: {}, facts: {}, cases: [], caseData: null, visitIdx: 0, lastResult: null };

const DRUGS = ["atorvastatin", "rosuvastatin", "simvastatin", "pitavastatin", "pravastatin", "fluvastatin",
  "metformin", "clopidogrel", "omeprazole", "esomeprazole", "pantoprazole", "amlodipine", "losartan",
  "enalapril", "carbamazepine", "allopurinol", "semaglutide", "fenofibrate", "aspirin"];
const PGX = {
  "HLA-B*15:02": ["positive", "negative"],
  "HLA-B*58:01": ["positive", "negative"],
  "CYP2C19": ["normal metabolizer", "intermediate metabolizer", "poor metabolizer", "rapid metabolizer", "ultrarapid metabolizer"],
  "SLCO1B1": ["normal function", "decreased function", "poor function"],
};
const VERDICT_TH = {
  improved: "ดีขึ้นจริง", worsened: "แย่ลงจริง", within_variation: "ยังอยู่ในความแปรปรวนปกติ",
  changed: "เปลี่ยนจริง", not_assessable: "ประเมินไม่ได้ (ไม่มีข้อมูล CVi)",
};
const CAT_TH = { low: "ต่ำ", moderate: "ปานกลาง", high: "สูง", very_high: "สูงมาก", not_assessable: "ประเมินไม่ได้" };
const SEV_TH = { stop: "STOP", action: "ACTION NEEDED", monitor: "MONITOR", info: "OK" };

// ---------- helpers ----------
async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error(`${path}: ${r.status} ${await r.text()}`);
  return r.json();
}
const el = (tag, attrs = {}, ...kids) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v; else if (k === "html") e.innerHTML = v; else e.setAttribute(k, v);
  }
  for (const k of kids) e.append(k);
  return e;
};
const fmt = (v) => v == null ? "–" : Math.abs(v) >= 100 ? v.toFixed(0) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toFixed(2);
const cssVar = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
function status(a, v) {
  if (v == null) return "none";
  if (a.ref_high != null && v > a.ref_high) return "high";
  if (a.ref_low != null && v < a.ref_low) return "low";
  return "normal";
}

// ---------- spectrum (illustrative only) ----------
// peaks: [ppm, half-width, height]; heights are scaled by the analyte value / reference midpoint
const PEAKS = {
  tg: [[0.87, 0.05, 1.3], [1.27, 0.06, 2.4], [2.02, 0.035, 0.35], [5.30, 0.04, 0.35]],
  total_c: [[0.70, 0.03, 0.35], [0.87, 0.04, 0.5], [1.20, 0.05, 0.6]],
  glyca: [[2.03, 0.012, 0.9]],
  lactate: [[1.32, 0.005, 1.0], [1.34, 0.005, 1.0], [4.11, 0.008, 0.25]],
  glucose: [[3.24, 0.008, 0.45], [3.41, 0.01, 0.55], [3.47, 0.01, 0.6], [3.53, 0.008, 0.45], [3.72, 0.012, 0.65], [3.84, 0.012, 0.6], [3.89, 0.01, 0.5], [5.23, 0.006, 0.3]],
  creatinine: [[3.04, 0.006, 0.55], [4.05, 0.006, 0.4]],
  citrate: [[2.53, 0.006, 0.35], [2.67, 0.006, 0.35]],
  valine: [[0.99, 0.005, 0.4], [1.04, 0.005, 0.4]],
  leucine: [[0.96, 0.006, 0.45]],
  isoleucine: [[0.94, 0.005, 0.25], [1.01, 0.005, 0.3]],
  alanine: [[1.48, 0.005, 0.55]],
  bohb: [[1.20, 0.006, 0.3]],
  acetone: [[2.23, 0.005, 0.25]],
};
const PEAK_LABELS = [["tg", 1.27, "–CH₂– (lipids)"], ["glyca", 2.03, "GlycA"], ["glucose", 3.72, "Glc"], ["creatinine", 3.04, "Crea"], ["alanine", 1.48, "Ala"], ["valine", 0.99, "BCAA"]];
const PPM_MAX = 5.6, PPM_MIN = 0.5;
let specAnim = 0;

function spectrumSignal(values) {
  const peaks = [];
  for (const [id, list] of Object.entries(PEAKS)) {
    const a = state.byId[id]; const v = values[id];
    if (!a || v == null) continue;
    const mid = a.ref_low != null && a.ref_high != null ? (a.ref_low + a.ref_high) / 2 : (a.ref_high || a.ref_low || v);
    const s = Math.max(0.25, Math.min(2.5, v / mid));
    for (const [ppm, w, h] of list) peaks.push([ppm, w, h * s]);
  }
  return (ppm) => {
    let y = 0;
    for (const [p, w, h] of peaks) y += h / (1 + ((ppm - p) / w) ** 2);
    return y + 0.015 * Math.sin(ppm * 97) * Math.cos(ppm * 31); // tiny deterministic "noise"
  };
}

function drawSpectrum(values, animate = true) {
  const cv = $("#spectrum"); const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = 190;
  cv.width = W * dpr; cv.height = H * dpr;
  const ctx = cv.getContext("2d"); ctx.scale(dpr, dpr);
  const pad = { l: 8, r: 8, t: 16, b: 22 };
  const f = spectrumSignal(values);
  const N = Math.max(400, Math.floor(W * 2));
  const pts = [];
  let ymax = 0;
  for (let i = 0; i <= N; i++) {
    const ppm = PPM_MAX - (PPM_MAX - PPM_MIN) * i / N;
    const y = Math.abs(ppm - 4.75) < 0.12 ? 0 : f(ppm); // water region suppressed
    pts.push([ppm, y]); ymax = Math.max(ymax, y);
  }
  const x = (ppm) => pad.l + (PPM_MAX - ppm) / (PPM_MAX - PPM_MIN) * (W - pad.l - pad.r);
  const y = (v) => H - pad.b - v / (ymax * 1.08) * (H - pad.t - pad.b);
  const color = cssVar("--spectrum"), grid = cssVar("--grid"), muted = cssVar("--muted");

  cancelAnimationFrame(specAnim);
  const dur = animate && !REDUCED ? 1600 : 0;
  let t0 = null;
  const frame = (now) => {
    t0 ??= now;
    const k = dur ? Math.min(1, Math.max(0, (now - t0) / dur)) : 1;
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = grid; ctx.fillStyle = muted; ctx.lineWidth = 1;
    ctx.font = "10px IBM Plex Mono, monospace"; ctx.textAlign = "center";
    for (let p = 5; p >= 1; p--) {
      ctx.beginPath(); ctx.moveTo(x(p), pad.t); ctx.lineTo(x(p), H - pad.b); ctx.stroke();
      ctx.fillText(`${p}.0`, x(p), H - 6);
    }
    ctx.textAlign = "right"; ctx.fillText("ppm", W - pad.r, H - 6);
    const upto = Math.floor(pts.length * k);
    ctx.beginPath(); ctx.strokeStyle = color; ctx.lineWidth = 1.3;
    for (let i = 0; i < upto; i++) { const [p, v] = pts[i]; i ? ctx.lineTo(x(p), y(v)) : ctx.moveTo(x(p), y(v)); }
    ctx.stroke();
    if (k < 1) {
      const sx = x(pts[upto]?.[0] ?? PPM_MIN);
      ctx.strokeStyle = color; ctx.globalAlpha = 0.35; ctx.lineWidth = 8;
      ctx.beginPath(); ctx.moveTo(sx, pad.t); ctx.lineTo(sx, H - pad.b); ctx.stroke(); ctx.globalAlpha = 1;
      $("#scanStatus").textContent = `acquiring… ${(pts[upto]?.[0] ?? PPM_MIN).toFixed(2)} ppm`;
      specAnim = requestAnimationFrame(frame);
    } else {
      ctx.fillStyle = muted; ctx.textAlign = "center"; ctx.font = "10.5px IBM Plex Sans Thai, sans-serif";
      for (const [id, ppm, label] of PEAK_LABELS) {
        if (values[id] == null) continue;
        ctx.fillText(label, x(ppm), Math.max(11, y(f(ppm)) - 5));
      }
      $("#scanStatus").textContent = `quantified ${Object.keys(values).length} analytes ✓`;
    }
  };
  specAnim = requestAnimationFrame(frame);
  return dur;
}

// ---------- panel ----------
function renderPanel(values, prev, delay) {
  const box = $("#panel"); box.innerHTML = "";
  const rows = [];
  let group = null;
  for (const a of state.catalog) {
    const v = values[a.id];
    if (v == null) continue;
    if (a.group !== group) { group = a.group; box.append(el("div", { class: "group-title" }, group)); }
    // fixed domain per analyte so a higher value really sits further right
    const hi = Math.max((a.ref_high ?? v) * 1.6, v * 1.08, (prev?.[a.id] ?? 0) * 1.08) || 1;
    const pos = (val) => `${Math.min(100, Math.max(0, val / hi * 100))}%`;
    const st = status(a, v);
    const track = el("div", { class: "track" });
    if (a.ref_low != null || a.ref_high != null) {
      const lo = a.ref_low ?? 0, up = a.ref_high ?? hi;
      track.append(el("div", { class: "range", style: `left:${pos(lo)};width:calc(${pos(up)} - ${pos(lo)})` }));
    }
    const bar = el("div", { class: "bar", style: `background:var(--${st === "normal" ? "normal" : st})` });
    const marker = el("div", { class: "marker", style: `left:0;background:var(--${st === "normal" ? "normal" : st})` });
    track.append(bar, marker);
    if (prev?.[a.id] != null) track.append(el("div", { class: "prev", style: `left:${pos(prev[a.id])}`, title: `ครั้งก่อน ${fmt(prev[a.id])}` }));
    const ref = a.ref_low != null && a.ref_high != null ? `${fmt(a.ref_low)}–${fmt(a.ref_high)}`
      : a.ref_high != null ? `< ${fmt(a.ref_high)}` : a.ref_low != null ? `> ${fmt(a.ref_low)}` : "ไม่มีช่วงอ้างอิง";
    const flag = st === "high" ? "▲" : st === "low" ? "▼" : "";
    const valEl = el("div", { class: "an-val" });
    valEl.innerHTML = `<span class="num" data-v="${v}">0</span> <small>${a.unit}</small><span class="flag" style="color:var(--${st})">${flag}</span><br><small>ref ${ref}</small>`;
    const row = el("div", { class: "an-row", title: a.note || "" },
      el("div", { class: "an-name", html: `${a.abbr}<small>${a.name}</small>` }), track, valEl);
    box.append(row);
    rows.push([row, bar, marker, pos(v), valEl.querySelector(".num"), v]);
  }
  const stagger = REDUCED ? 0 : 70;
  if (REDUCED) delay = 0;
  rows.forEach(([row, bar, marker, p, num, v], i) => {
    setTimeout(() => {
      row.classList.add("show"); bar.style.width = p; marker.style.left = p;
      countUp(num, v);
    }, delay + i * stagger);
  });
  return delay + rows.length * stagger;
}
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
function countUp(node, target) {
  if (REDUCED) { node.textContent = fmt(target); return; }
  let t0 = null;
  const step = (now) => {
    t0 ??= now;
    const k = Math.min(1, Math.max(0, (now - t0) / 600));
    node.textContent = fmt(target * (1 - (1 - k) ** 3));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// ---------- visits ----------
function renderVisitTabs() {
  const box = $("#visitTabs"); box.innerHTML = "";
  state.caseData.visits.forEach((v, i) => {
    const b = el("button", { role: "tab", "aria-selected": String(i === state.visitIdx) }, `ครั้งที่ ${i + 1} · ${v.date}`);
    b.onclick = () => selectVisit(i);
    box.append(b);
  });
  renderStartVisitOptions();
}
function selectVisit(i) {
  state.visitIdx = i;
  renderVisitTabs();
  const v = state.caseData.visits[i];
  const prev = i > 0 ? state.caseData.visits[i - 1].values : null;
  $("#visitMeta").textContent = `${v.label || ""} · ${v.date}`;
  const d = drawSpectrum(v.values);
  const end = renderPanel(v.values, prev, d);
  setTimeout(assess, Math.min(end, d + 400));
}

// ---------- form ----------
function medRow(m = {}) {
  const tr = el("tr");
  const drug = el("input", { list: "drugList", value: m.drug || "", placeholder: "ชื่อยา", "data-k": "drug" });
  const dose = el("input", { type: "number", step: "any", value: m.dose_mg ?? "", "data-k": "dose_mg" });
  const pdc = el("input", { type: "number", min: "0", max: "100", value: m.pdc_pct ?? "", "data-k": "pdc_pct" });
  const start = el("select", { "data-k": "start_visit" });
  start.dataset.value = m.start_visit == null ? "" : String(m.start_visit + 1); // UI is 1-based
  const del = el("button", { type: "button", class: "del", "aria-label": "ลบ" }, "×");
  del.onclick = () => tr.remove();
  for (const c of [drug, dose, pdc, start]) tr.append(el("td", {}, c));
  tr.append(el("td", {}, del));
  return tr;
}
function renderStartVisitOptions() {
  const n = state.caseData?.visits.length || 1;
  for (const s of document.querySelectorAll('select[data-k="start_visit"]')) {
    const cur = s.value || s.dataset.value;
    s.innerHTML = "";
    s.append(el("option", { value: "" }, "ก่อนครั้งแรก"));
    for (let i = 2; i <= n; i++) s.append(el("option", { value: String(i) }, `ครั้งที่ ${i}`));
    s.value = cur || "";
  }
}
function fillForm(c) {
  const f = $("#profileForm");
  for (const [k, v] of Object.entries(c.profile)) {
    const input = f.elements[k];
    if (!input) continue;
    if (input.type === "checkbox") input.checked = !!v; else input.value = v ?? "";
  }
  const rows = $("#medRows"); rows.innerHTML = "";
  for (const m of c.meds) rows.append(medRow(m));
  renderStartVisitOptions();
  for (const g of Object.keys(PGX)) $(`select[name="pgx:${g}"]`).value = c.pgx?.[g] || "";
}
function readForm() {
  const f = $("#profileForm");
  const num = (k) => f.elements[k].value === "" ? null : Number(f.elements[k].value);
  const profile = {
    age: num("age"), sex: f.elements.sex.value, sbp: num("sbp"),
    weight_kg: num("weight_kg"), height_cm: num("height_cm"), waist_cm: num("waist_cm"),
    smoker: f.elements.smoker.checked, diabetes: f.elements.diabetes.checked,
    hypertension: f.elements.hypertension.checked, family_history_dm: f.elements.family_history_dm.checked,
  };
  const meds = [...$("#medRows").rows].map((tr) => {
    const g = (k) => tr.querySelector(`[data-k="${k}"]`).value;
    return {
      drug: g("drug"), dose_mg: g("dose_mg") === "" ? null : Number(g("dose_mg")),
      pdc_pct: g("pdc_pct") === "" ? null : Number(g("pdc_pct")),
      start_visit: g("start_visit") === "" ? null : Number(g("start_visit")) - 1,
    };
  }).filter((m) => m.drug.trim());
  const pgx = {};
  for (const g of Object.keys(PGX)) { const v = $(`select[name="pgx:${g}"]`).value; if (v) pgx[g] = v; }
  return {
    profile, meds, pgx,
    alcohol_drinks_per_day: num("alcohol_drinks_per_day") || 0,
    activity_min_week: num("activity_min_week"),
    visits: state.caseData.visits.slice(0, state.visitIdx + 1),
  };
}

// ---------- results ----------
function factChips(ids) {
  const box = el("div", { class: "facts" });
  for (const id of ids) {
    const f = state.facts[id];
    const chip = el("button", { type: "button", class: `fact${f && !f.verified ? " unverified" : ""}` }, id);
    chip.onclick = (e) => showFact(id, e);
    box.append(chip);
  }
  return box;
}
function showFact(id, e) {
  const f = state.facts[id]; const pop = $("#factPop");
  if (!f) return;
  pop.innerHTML = `<b>${id}</b> · <i>${f.level}</i>${f.verified ? "" : ' · <b style="color:var(--action)">ยังไม่ได้ตรวจถ้อยคำ</b>'}
    <p style="margin:6px 0">${f.text}</p><div class="muted">${f.source}</div><a href="${f.url}" target="_blank" rel="noopener">${f.url}</a>`;
  pop.hidden = false;
  const r = e.target.getBoundingClientRect();
  pop.style.left = `${Math.min(r.left, window.innerWidth - 380)}px`;
  pop.style.top = `${Math.min(r.bottom + 6, window.innerHeight - pop.offsetHeight - 10)}px`;
  e.stopPropagation();
}
document.addEventListener("click", () => { $("#factPop").hidden = true; });

function renderResults(r) {
  state.lastResult = r;
  Object.assign(state.facts, r.facts);
  $("#results").hidden = false;

  const risks = $("#risks"); risks.innerHTML = "";
  for (const k of r.risks) {
    const box = el("div", { class: "risk" });
    box.innerHTML = `<div class="name">${k.disease}</div><div class="val">${k.value == null ? "–" : k.id === "dm" ? `${k.value}/17` : k.display}</div>
      <div class="meta">${k.score_name}${k.method === "-" ? "" : " · " + k.method} · <span class="cat cat-${k.category}">${CAT_TH[k.category]}</span></div>`;
    const notes = [...(k.value == null ? [k.display] : k.id === "dm" ? [k.display] : []), ...k.notes];
    if (notes.length) box.append(el("div", { class: "notes" }, notes.join(" · ")));
    box.append(factChips(k.fact_ids));
    risks.append(box);
  }
  const nf = $("#nmrFactors"); nf.innerHTML = "";
  if (!r.nmr_factors.length) nf.append(el("div", { class: "empty" }, "ไม่พบปัจจัยเสริม"));
  for (const x of r.nmr_factors) {
    const it = el("div", { class: `item sev-${x.severity}` },
      el("div", { class: "title" }, x.title, el("span", { class: "sev-label" }, x.level.toUpperCase())),
      el("div", { class: "detail" }, x.detail));
    it.append(factChips(x.fact_ids));
    nf.append(it);
  }

  const fb = $("#findings"); fb.innerHTML = "";
  const needs = r.findings.filter((f) => f.severity === "stop" || f.severity === "action").length;
  $("#queueCount").textContent = needs ? `ต้องทบทวน ${needs} รายการ` : "ไม่มีรายการต้องทบทวน";
  if (!r.findings.length) fb.append(el("div", { class: "empty" }, "ไม่พบประเด็นเรื่องยา"));
  for (const f of r.findings) {
    const it = el("div", { class: `item sev-${f.severity}` },
      el("div", { class: "title" }, f.title, el("span", { class: "sev-label" }, SEV_TH[f.severity])),
      el("div", { class: "detail" }, f.detail));
    it.append(factChips(f.fact_ids));
    const acts = el("div", { class: "actions" });
    const why = el("button", { type: "button" }, "Why?");
    const trace = el("div", { class: "trace", hidden: "" });
    trace.innerHTML = `<b>Trace</b><ol>${f.trace.map((t) => `<li>${t}</li>`).join("")}<li>rule → ${f.fact_ids.join(", ")}</li></ol>`;
    why.onclick = () => { trace.hidden = !trace.hidden; };
    acts.append(why);
    if (f.severity !== "info") {
      for (const label of ["Accept", "Modify", "Reject"]) {
        const b = el("button", { type: "button" }, label);
        b.onclick = () => { acts.querySelectorAll(".chosen").forEach((x) => x.classList.remove("chosen")); b.classList.add("chosen"); };
        acts.append(b);
      }
    }
    it.append(acts, trace);
    fb.append(it);
  }

  const ad = $("#advice"); ad.innerHTML = "";
  if (!r.advice.length) ad.append(el("div", { class: "empty" }, "ไม่มีคำแนะนำเพิ่มเติม"));
  for (const a of r.advice) {
    const it = el("div", { class: "item" },
      el("div", { class: "title" }, a.topic), el("div", { class: "detail" }, a.advice),
      el("div", { class: "muted" }, `เหตุผล: ${a.reason}`));
    it.append(factChips(a.fact_ids));
    ad.append(it);
  }

  const tc = $("#trendCard");
  tc.hidden = !r.trend.length;
  if (r.trend.length) {
    const counts = {};
    for (const t of r.trend) counts[t.verdict] = (counts[t.verdict] || 0) + 1;
    const sum = $("#trendSummary"); sum.innerHTML = "";
    for (const v of ["improved", "worsened", "within_variation", "changed", "not_assessable"]) {
      if (counts[v]) sum.append(el("span", { class: `pill v-${v}` }, `${VERDICT_TH[v]} ${counts[v]}`));
    }
    const tb = $("#trendRows"); tb.innerHTML = "";
    const order = { worsened: 0, improved: 1, changed: 2, within_variation: 3, not_assessable: 4 };
    const rows = [...r.trend].sort((a, b) => order[a.verdict] - order[b.verdict]);
    const hidden = rows.filter((t) => t.verdict === "not_assessable").length;
    for (const t of rows) {
      const tr = el("tr");
      if (t.verdict === "not_assessable") { tr.className = "na-row"; tr.hidden = true; }
      tr.innerHTML = `<td>${t.abbr}</td><td class="num">${fmt(t.previous)}</td><td class="num">${fmt(t.current)} <small class="muted">${t.unit}</small></td>
        <td class="num">${t.pct_change > 0 ? "+" : ""}${t.pct_change.toFixed(0)}%</td>
        <td class="num">${t.rcv_pct == null ? "–" : "±" + t.rcv_pct.toFixed(0) + "%"}</td>
        <td><span class="pill v-${t.verdict}" style="padding:2px 8px;font-size:12px">${VERDICT_TH[t.verdict]}</span></td>`;
      tb.append(tr);
    }
    if (hidden) {
      const btn = el("button", { type: "button", class: "btn-ghost" }, `แสดงสารที่ยังไม่มีข้อมูล CVi (${hidden}) — เห็นค่าได้แต่ตัดสินไม่ได้ว่าเปลี่ยนจริง`);
      btn.onclick = () => { tb.querySelectorAll(".na-row").forEach((x) => { x.hidden = false; }); btn.remove(); };
      tb.append(el("tr", {}, el("td", { colspan: "6" }, btn)));
    }
  }
}

async function assess() {
  try {
    renderResults(await api("/api/assess", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(readForm()),
    }));
  } catch (e) { console.error(e); alert(e.message); }
}

// ---------- init ----------
async function loadCase(id, visit = 0) {
  state.caseData = await api(`/api/cases/${id}`);
  const v = Math.min(visit, state.caseData.visits.length - 1);
  state.visitIdx = v;
  fillForm(state.caseData);
  selectVisit(v);
}

async function init() {
  const saved = (() => { try { return localStorage.getItem("theme"); } catch { return null; } })();
  if (saved) document.documentElement.dataset.theme = saved;
  $("#themeBtn").onclick = () => {
    const dark = document.documentElement.dataset.theme === "dark" ||
      (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("theme", document.documentElement.dataset.theme); } catch { /* ignore */ }
    if (state.caseData) drawSpectrum(state.caseData.visits[state.visitIdx].values, false);
  };

  for (const d of DRUGS) $("#drugList").append(el("option", { value: d }));
  for (const [g, opts] of Object.entries(PGX)) {
    const s = el("select", { name: `pgx:${g}` }, el("option", { value: "" }, "ไม่ทราบ / ไม่ได้ตรวจ"));
    for (const o of opts) s.append(el("option", { value: o }, o));
    $("#pgxFields").append(el("label", {}, g, s));
  }
  $("#addMed").onclick = () => { $("#medRows").append(medRow()); renderStartVisitOptions(); };
  $("#profileForm").onsubmit = (e) => { e.preventDefault(); assess(); };

  $("#csvInput").onchange = async (e) => {
    const file = e.target.files[0]; if (!file) return;
    const fd = new FormData(); fd.append("file", file);
    try {
      const res = await api("/api/panel/parse", { method: "POST", body: fd });
      if (res.unknown.length) alert(`ไม่รู้จักสาร: ${res.unknown.join(", ")} (ข้าม)`);
      const today = new Date().toISOString().slice(0, 10);
      state.caseData.visits.push({ date: res.date || today, label: `อัปโหลด: ${file.name}`, values: res.values });
      selectVisit(state.caseData.visits.length - 1);
    } catch (err) { alert(err.message); }
    e.target.value = "";
  };

  const [catalog, cases] = await Promise.all([api("/api/catalog"), api("/api/cases")]);
  state.catalog = catalog.analytes;
  state.byId = Object.fromEntries(catalog.analytes.map((a) => [a.id, a]));
  $("#snapshot").textContent = catalog.snapshot;
  state.cases = cases;
  for (const c of cases) $("#caseSelect").append(el("option", { value: c.id }, c.label));
  $("#caseSelect").onchange = (e) => loadCase(e.target.value);
  window.addEventListener("resize", () => state.caseData && drawSpectrum(state.caseData.visits[state.visitIdx].values, false));
  const q = new URLSearchParams(location.search);
  const start = cases.some((c) => c.id === q.get("case")) ? q.get("case") : cases[0].id;
  $("#caseSelect").value = start;
  await loadCase(start, Math.max(0, Number(q.get("visit") || 1) - 1));
}
init();
