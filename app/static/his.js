"use strict";

const $ = (s, el = document) => el.querySelector(s);
const SERVICE = "precisionrx-pgx";
const DRUGS = ["carbamazepine", "oxcarbazepine", "allopurinol", "simvastatin", "atorvastatin", "rosuvastatin",
  "clopidogrel", "omeprazole", "esomeprazole", "pantoprazole", "amlodipine", "losartan", "metformin", "aspirin"];
const IND_TH = { critical: "HARD STOP", warning: "WARNING", info: "INFO" };
const state = { patients: [], p: null, cards: [], labOrders: [], selectTimer: 0 };

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function md(text) {
  // tiny markdown: **bold**, `code`, _italic_, "- " lists, blank-line paragraphs
  const inline = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`(.+?)`/g, "<code>$1</code>").replace(/_(.+?)_/g, "<i>$1</i>");
  let html = "", list = false;
  for (const line of text.split("\n")) {
    if (line.startsWith("- ")) { if (!list) { html += "<ul>"; list = true; } html += `<li>${inline(line.slice(2))}</li>`; continue; }
    if (list) { html += "</ul>"; list = false; }
    if (line.trim()) html += `<p>${inline(line)}</p>`;
  }
  return html + (list ? "</ul>" : "");
}
function toast(msg, bad = false) {
  const t = $("#toast"); t.textContent = msg; t.className = `toast${bad ? " bad" : ""}`; t.hidden = false;
  clearTimeout(toast.t); toast.t = setTimeout(() => { t.hidden = true; }, 3500);
}

// ---------- FHIR builders ----------
const medReq = (id, m, status = "active") => ({
  resourceType: "MedicationRequest", id, status, intent: "order", subject: { reference: `Patient/${state.p.id}` },
  medicationCodeableConcept: { text: m.drug },
  dosageInstruction: [{ text: m.sig || "", doseAndRate: m.dose_mg ? [{ doseQuantity: { value: m.dose_mg, unit: "mg" } }] : [] }],
});
const bundle = (rs) => ({ resourceType: "Bundle", type: "collection", entry: rs.map((resource) => ({ resource })) });
function draftOrder() {
  const f = $("#orderForm");
  const drug = f.elements.drug.value.trim().toLowerCase();
  if (!drug) return null;
  return medReq("draft-1", { drug, dose_mg: f.elements.dose.value ? Number(f.elements.dose.value) : null, sig: f.elements.sig.value }, "draft");
}
function hookBody(hook, draft) {
  const active = state.p.active.filter((m) => m.status !== "stopped").map((m) => medReq(m.id, m));
  const pgx = state.p.pgx.map((g) => ({
    resourceType: "Observation", status: "final", category: [{ text: "laboratory" }],
    code: { text: g.gene }, valueCodeableConcept: { text: g.result },
  }));
  return {
    hook, hookInstance: crypto.randomUUID(), fhirServer: location.origin + "/fhir-mock",
    context: { userId: "Practitioner/demo", patientId: state.p.id, draftOrders: bundle([draft]) },
    prefetch: { patient: { resourceType: "Patient", id: state.p.id }, activeMedications: bundle(active), pgxResults: bundle(pgx) },
  };
}
async function callHook(hook) {
  const draft = draftOrder();
  if (!draft) return [];
  const svc = hook === "order-sign" ? `${SERVICE}-sign` : SERVICE;
  const t0 = performance.now();
  const r = await fetch(`/cds-services/${svc}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(hookBody(hook, draft)) });
  const { cards } = await r.json();
  $("#hookStatus").textContent = `POST /cds-services/${svc} · hook=${hook} · ${cards.length} card(s) · ${(performance.now() - t0).toFixed(0)} ms`;
  return cards;
}
async function sendFeedback(card, outcome, extra = {}) {
  await fetch(`/cds-services/${SERVICE}/feedback`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feedback: [{ card: card.uuid, outcome, outcomeTimestamp: new Date().toISOString(), ...extra }] }),
  });
}

// ---------- render ----------
function renderPatients() {
  const ul = $("#patientList"); ul.innerHTML = "";
  for (const p of state.patients) {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.innerHTML = `${esc(p.id)} · ${esc(p.name)}<small>${p.age} ปี ${esc(p.sex)} · ${esc(p.dx)}</small>`;
    b.setAttribute("aria-current", String(state.p?.id === p.id));
    b.onclick = () => selectPatient(p.id);
    li.append(b); ul.append(li);
  }
}
function renderPatient() {
  const p = state.p;
  const chips = p.pgx.length
    ? p.pgx.map((g) => `<span class="pgx-chip ${/positive|poor|decreased|ultrarapid/.test(g.result) ? "hot" : ""}">${esc(g.gene)}: ${esc(g.result)} <span class="muted">· ${esc(g.source)} ${esc(g.date)}</span></span>`).join("")
    : `<span class="pgx-none">ไม่มีผล PGx ในระบบ</span>`;
  $("#banner").innerHTML = `<span class="who">${esc(p.name)}</span>
    <span class="kv">HN <b>${esc(p.id)}</b></span><span class="kv">อายุ <b>${p.age}</b> · <b>${esc(p.sex)}</b></span>
    <span class="kv">Dx <b>${esc(p.dx)}</b></span><span class="kv">แพ้ยา <b>${esc(p.allergy)}</b></span>
    <div class="pgx-chips">${chips}</div>`;
  const tb = $("#activeRows"); tb.innerHTML = "";
  for (const m of p.active) {
    const tr = document.createElement("tr");
    if (m.isNew) tr.className = "new";
    const st = m.status === "stopped" ? "หยุดแล้ว" : m.isNew ? "ใหม่" : "ใช้อยู่";
    tr.innerHTML = `<td>${m.status === "stopped" ? `<s>${esc(m.drug)}</s>` : esc(m.drug)}</td><td>${m.dose_mg ?? "–"} mg</td><td>${esc(m.sig || "")}</td><td>${st}</td>`;
    tb.append(tr);
  }
  if (!p.active.length) tb.innerHTML = `<tr><td colspan="4" class="muted">ไม่มียาที่ใช้อยู่</td></tr>`;
  $("#activeCount").textContent = `${p.active.filter((m) => m.status !== "stopped").length} รายการ`;
  $("#labOrders").innerHTML = state.labOrders.length ? `<b>สั่งตรวจ:</b> ${state.labOrders.map(esc).join(", ")}` : "";
  $("#tryHint").textContent = `ลองทำ: ${p.try}`;
}

function renderCards() {
  const box = $("#cards"); box.innerHTML = "";
  if (state.cards === null) return;
  if (!state.cards.length) {
    box.innerHTML = `<div class="no-cards">✓ PrecisionRx: ไม่มีประเด็น PGx/ยาตีกันจากคำสั่งนี้ (ไม่เด้ง alert)</div>`;
    return;
  }
  for (const entry of state.cards) {
    const { card } = entry;
    const div = document.createElement("div");
    div.className = `cds-card ${card.indicator}${entry.state !== "pending" ? " resolved" : ""}`;
    div.innerHTML = `<div class="sum"><span>${esc(card.summary)}</span><span class="ind">${IND_TH[card.indicator]}</span></div>
      <div class="det">${md(card.detail)}</div>
      <div class="src">แหล่ง: <a href="${esc(card.source.url)}" target="_blank" rel="noopener">${esc(card.source.label)}</a></div>`;
    if (entry.state === "pending") {
      const row = document.createElement("div"); row.className = "row";
      for (const s of card.suggestions) {
        const b = document.createElement("button"); b.className = "sugg"; b.textContent = s.label;
        b.onclick = () => acceptSuggestion(entry, s);
        row.append(b);
      }
      const sel = document.createElement("select");
      sel.innerHTML = `<option value="">— เหตุผลที่ override —</option>` + card.overrideReasons.map((r) => `<option value="${esc(r.code)}">${esc(r.display)}</option>`).join("");
      const note = document.createElement("input"); note.placeholder = "หมายเหตุถึงเภสัชกร";
      const ob = document.createElement("button"); ob.textContent = "Override → แจ้งเภสัชกร";
      ob.onclick = () => override(entry, sel, note);
      row.append(sel, note, ob);
      div.append(row);
    } else {
      const st = document.createElement("div"); st.className = "state";
      st.textContent = entry.state === "accepted" ? `✓ ทำตามคำแนะนำ: ${entry.detail}` : `↪ Override (${entry.detail}) — ส่งเข้าคิวเภสัชกรแล้ว`;
      div.append(st);
    }
    box.append(div);
  }
}

// ---------- actions ----------
async function orderSelect() {
  const cards = await callHook("order-select");
  state.cards = cards.map((card) => ({ card, state: "pending" }));
  renderCards();
}
function clearOrder() {
  $("#orderForm").reset(); state.cards = null; renderCards(); $("#hookStatus").textContent = "";
}
async function acceptSuggestion(entry, s) {
  for (const a of s.actions) {
    if (a.type === "delete") {
      for (const ref of a.resourceId || []) {
        const id = ref.split("/")[1];
        if (id === "draft-1") { $("#orderForm").reset(); continue; }
        const m = state.p.active.find((x) => x.id === id); if (m) m.status = "stopped";
      }
    } else if (a.type === "create" && a.resource.resourceType === "MedicationRequest") {
      const dq = a.resource.dosageInstruction?.[0]?.doseAndRate?.[0]?.doseQuantity?.value;
      state.p.active.push({ id: `n${Date.now()}`, drug: a.resource.medicationCodeableConcept.text, dose_mg: dq, sig: a.resource.dosageInstruction?.[0]?.text, isNew: true });
    } else if (a.type === "create" && a.resource.resourceType === "ServiceRequest") {
      state.labOrders.push(a.resource.code.text);
    }
  }
  entry.state = "accepted"; entry.detail = s.label;
  await sendFeedback(entry.card, "accepted", { acceptedSuggestions: [{ id: s.uuid }] });
  renderPatient(); renderCards();
  toast(`ทำตามคำแนะนำ: ${s.label}`);
}
async function override(entry, sel, note) {
  if (!sel.value) { toast("ต้องเลือกเหตุผลก่อน override", true); sel.focus(); return; }
  const reason = entry.card.overrideReasons.find((r) => r.code === sel.value);
  entry.state = "overridden"; entry.detail = reason.display;
  await sendFeedback(entry.card, "overridden", { overrideReason: { reason, userComment: note.value } });
  renderCards();
  toast("Override แล้ว — เภสัชกรจะเห็นในคิว");
}
async function sign(e) {
  e.preventDefault();
  const draft = draftOrder();
  if (!draft) return;
  const cards = await callHook("order-sign");
  // keep decisions already made on the same finding during order-select
  const prior = Object.fromEntries((state.cards || []).map((x) => [x.card.extension.precisionrx.finding_id, x]));
  state.cards = cards.map((card) => {
    const p = prior[card.extension.precisionrx.finding_id];
    return p && p.state !== "pending" ? { ...p, card: { ...card, uuid: p.card.uuid } } : { card, state: "pending" };
  });
  const blocking = state.cards.filter((x) => x.card.indicator === "critical" && x.state === "pending");
  const pendingWarn = state.cards.filter((x) => x.card.indicator === "warning" && x.state === "pending");
  if (blocking.length || pendingWarn.length) {
    renderCards();
    toast(blocking.length ? "⛔ บันทึกไม่ได้: มี HARD STOP — เลือกทำตามคำแนะนำ หรือ override พร้อมเหตุผล"
      : "ยังมีคำเตือนที่ยังไม่ได้ตอบ — ทำตามคำแนะนำ หรือ override พร้อมเหตุผล", true);
    return;
  }
  if (!draftOrder()) { clearOrder(); return; } // draft was cancelled via suggestion
  const f = $("#orderForm");
  state.p.active.push({ id: `n${Date.now()}`, drug: f.elements.drug.value.trim().toLowerCase(), dose_mg: f.elements.dose.value ? Number(f.elements.dose.value) : null, sig: f.elements.sig.value, isNew: true });
  toast("✓ บันทึกคำสั่งยาแล้ว");
  clearOrder(); renderPatient();
}

function selectPatient(id) {
  const p = state.patients.find((x) => x.id === id);
  state.p = structuredClone(p);
  state.p.active = state.p.active.map((m, i) => ({ ...m, id: `a${i + 1}` }));
  state.labOrders = [];
  clearOrder(); renderPatients(); renderPatient();
}

async function init() {
  for (const d of DRUGS) { const o = document.createElement("option"); o.value = d; $("#drugList").append(o); }
  const f = $("#orderForm");
  const trigger = () => { clearTimeout(state.selectTimer); state.selectTimer = setTimeout(() => { if (f.elements.drug.value.trim()) orderSelect(); }, 250); };
  f.elements.drug.addEventListener("change", trigger);
  f.elements.dose.addEventListener("change", trigger);
  f.onsubmit = sign;
  state.patients = await (await fetch("/api/his/patients")).json();
  const q = new URLSearchParams(location.search);
  selectPatient(state.patients.some((p) => p.id === q.get("hn")) ? q.get("hn") : state.patients[0].id);
  if (q.get("drug")) {
    f.elements.drug.value = q.get("drug"); f.elements.dose.value = q.get("dose") || "";
    orderSelect();
  }
}
init();
