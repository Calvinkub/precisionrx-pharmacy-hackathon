<script lang="ts">
  import { onMount, tick } from "svelte";
  import { postJson, api } from "../lib/api";

  interface HisMed { id: string; drug: string; dose_mg: number | null; sig?: string; status?: "stopped"; isNew?: boolean }
  interface HisPatient { id: string; name: string; age: number; sex: string; dx: string; allergy: string; active: HisMed[]; pgx: { gene: string; result: string; source: string; date: string }[]; try: string }
  interface Action { type: "create" | "delete"; description: string; resource?: any; resourceId?: string[] }
  interface Suggestion { label: string; uuid: string; actions: Action[] }
  interface Card {
    uuid: string; summary: string; detail: string; indicator: "critical" | "warning" | "info";
    source: { label: string; url: string }; suggestions: Suggestion[]; overrideReasons: { code: string; display: string }[];
    extension: { precisionrx: { finding_id: string; fact_ids: string[]; hard_stop: boolean } };
  }
  interface Entry { card: Card; state: "pending" | "accepted" | "overridden"; detail?: string; reason?: string; note?: string }

  const SERVICE = "precisionrx-pgx";
  const DRUGS = ["carbamazepine", "oxcarbazepine", "allopurinol", "simvastatin", "atorvastatin", "rosuvastatin", "clopidogrel",
    "omeprazole", "esomeprazole", "pantoprazole", "amlodipine", "losartan", "metformin", "aspirin"];
  const IND = {
    critical: { th: "ห้ามสั่ง", tone: "critical" },
    warning: { th: "คำเตือน", tone: "serious" },
    info: { th: "ข้อมูล", tone: "info" },
  } as const;

  let patients = $state<HisPatient[]>([]);
  let p = $state<HisPatient | null>(null);
  let drug = $state(""), dose = $state<number | null>(null), sig = $state("");
  let cards = $state<Entry[] | null>(null);
  let labOrders = $state<string[]>([]);
  let hookStatus = $state("");
  let message = $state<{ text: string; bad: boolean } | null>(null);
  let timer = 0;
  let cardsEl = $state<HTMLElement>();

  const hasCritical = $derived(!!cards?.some((c) => c.card.indicator === "critical" && c.state === "pending"));

  const bundle = (rs: unknown[]) => ({ resourceType: "Bundle", type: "collection", entry: rs.map((resource) => ({ resource })) });
  const medReq = (id: string, m: { drug: string; dose_mg: number | null; sig?: string }, status = "active") => ({
    resourceType: "MedicationRequest", id, status, intent: "order", subject: { reference: `Patient/${p!.id}` },
    medicationCodeableConcept: { text: m.drug },
    dosageInstruction: [{ text: m.sig ?? "", doseAndRate: m.dose_mg ? [{ doseQuantity: { value: m.dose_mg, unit: "mg" } }] : [] }],
  });
  const draft = () => (drug.trim() ? medReq("draft-1", { drug: drug.trim().toLowerCase(), dose_mg: dose, sig }, "draft") : null);

  async function callHook(hook: "order-select" | "order-sign"): Promise<Card[]> {
    const d = draft();
    if (!d || !p) return [];
    const svc = hook === "order-sign" ? `${SERVICE}-sign` : SERVICE;
    const t0 = performance.now();
    const res = await postJson<{ cards: Card[] }>(`/cds-services/${svc}`, {
      hook, hookInstance: crypto.randomUUID(),
      context: { userId: "Practitioner/demo", patientId: p.id, draftOrders: bundle([d]) },
      prefetch: {
        patient: { resourceType: "Patient", id: p.id },
        activeMedications: bundle(p.active.filter((m) => m.status !== "stopped").map((m) => medReq(m.id, m))),
        pgxResults: bundle(p.pgx.map((g) => ({ resourceType: "Observation", status: "final", code: { text: g.gene }, valueCodeableConcept: { text: g.result } }))),
      },
    });
    hookStatus = `POST /cds-services/${svc} · ${hook} · ${res.cards.length} card · ${(performance.now() - t0).toFixed(0)} ms`;
    return res.cards;
  }

  async function feedback(card: Card, outcome: string, extra: object = {}) {
    await postJson(`/cds-services/${SERVICE}/feedback`, { feedback: [{ card: card.uuid, outcome, outcomeTimestamp: new Date().toISOString(), ...extra }] });
  }

  function say(text: string, bad = false) { message = { text, bad }; }

  async function orderSelect() {
    if (!drug.trim()) { cards = null; return; }
    cards = (await callHook("order-select")).map((card) => ({ card, state: "pending" }));
  }
  function scheduleSelect() { clearTimeout(timer); timer = window.setTimeout(orderSelect, 300); }

  async function accept(e: Entry, s: Suggestion) {
    if (!p) return;
    for (const a of s.actions) {
      if (a.type === "delete") {
        for (const ref of a.resourceId ?? []) {
          const id = ref.split("/")[1];
          if (id === "draft-1") { drug = ""; dose = null; sig = ""; continue; }
          const m = p.active.find((x) => x.id === id); if (m) m.status = "stopped";
        }
      } else if (a.resource?.resourceType === "MedicationRequest") {
        const di = a.resource.dosageInstruction?.[0];
        p.active.push({ id: `n${Date.now()}`, drug: a.resource.medicationCodeableConcept.text, dose_mg: di?.doseAndRate?.[0]?.doseQuantity?.value ?? null, sig: di?.text, isNew: true });
      } else if (a.resource?.resourceType === "ServiceRequest") {
        labOrders.push(a.resource.code.text);
      }
    }
    e.state = "accepted"; e.detail = s.label;
    await feedback(e.card, "accepted", { acceptedSuggestions: [{ id: s.uuid }] });
    say(`ทำตามคำแนะนำแล้ว: ${s.label}`);
  }

  async function override(e: Entry) {
    const reason = e.card.overrideReasons.find((r) => r.code === e.reason);
    if (!reason) { say("ต้องเลือกเหตุผลก่อน override", true); document.getElementById(`reason-${e.card.uuid}`)?.focus(); return; }
    e.state = "overridden"; e.detail = reason.display;
    await feedback(e.card, "overridden", { overrideReason: { reason, userComment: e.note ?? "" } });
    say("Override แล้ว — ส่งเข้าคิวเภสัชกร");
  }

  async function sign(ev: SubmitEvent) {
    ev.preventDefault();
    if (!draft() || !p) return;
    const fresh = await callHook("order-sign");
    const prior = Object.fromEntries((cards ?? []).map((x) => [x.card.extension.precisionrx.finding_id, x]));
    cards = fresh.map((card) => {
      const old = prior[card.extension.precisionrx.finding_id];
      return old && old.state !== "pending" ? { ...old, card: { ...card, uuid: old.card.uuid } } : { card, state: "pending" as const };
    });
    const blocking = cards.filter((x) => x.card.indicator === "critical" && x.state === "pending").length;
    const warn = cards.filter((x) => x.card.indicator === "warning" && x.state === "pending").length;
    if (blocking || warn) {
      say(blocking ? "บันทึกไม่ได้: มีคำสั่งห้าม (HARD STOP) — ทำตามคำแนะนำ หรือ override พร้อมเหตุผล" : "ยังมีคำเตือนที่ยังไม่ได้ตอบ — ทำตามคำแนะนำ หรือ override พร้อมเหตุผล", true);
      await tick();
      cardsEl?.querySelector<HTMLElement>(".pending button, .pending select")?.focus();
      return;
    }
    if (!drug.trim()) { cards = null; return; }
    p.active.push({ id: `n${Date.now()}`, drug: drug.trim().toLowerCase(), dose_mg: dose, sig, isNew: true });
    say(`บันทึกคำสั่ง ${drug} แล้ว`);
    drug = ""; dose = null; sig = ""; cards = null; hookStatus = "";
  }

  function selectPatient(id: string) {
    const src = patients.find((x) => x.id === id)!;
    const copy: HisPatient = structuredClone($state.snapshot(src));
    copy.active = copy.active.map((m, i) => ({ ...m, id: `a${i + 1}` }));
    p = copy; labOrders = []; drug = ""; dose = null; sig = ""; cards = null; hookStatus = ""; message = null;
    const u = new URL(location.href); u.searchParams.set("hn", id); u.searchParams.delete("drug"); u.searchParams.delete("dose");
    history.replaceState(null, "", u);
  }

  // minimal markdown for card.detail: **bold**, `code`, _italic_, "- " lists — rendered as nodes, never innerHTML
  type Seg = { t: "text" | "b" | "code" | "i"; v: string };
  function inline(s: string): Seg[] {
    const out: Seg[] = [];
    const re = /\*\*(.+?)\*\*|`(.+?)`|_(.+?)_/g;
    let last = 0, m: RegExpExecArray | null;
    while ((m = re.exec(s))) {
      if (m.index > last) out.push({ t: "text", v: s.slice(last, m.index) });
      out.push(m[1] ? { t: "b", v: m[1] } : m[2] ? { t: "code", v: m[2] } : { t: "i", v: m[3] });
      last = re.lastIndex;
    }
    if (last < s.length) out.push({ t: "text", v: s.slice(last) });
    return out;
  }
  function blocks(md: string) {
    const out: ({ kind: "p"; segs: Seg[] } | { kind: "ul"; items: Seg[][] })[] = [];
    for (const line of md.split("\n")) {
      if (line.startsWith("- ")) {
        const lastB = out.at(-1);
        if (lastB?.kind === "ul") lastB.items.push(inline(line.slice(2))); else out.push({ kind: "ul", items: [inline(line.slice(2))] });
      } else if (line.trim()) out.push({ kind: "p", segs: inline(line) });
    }
    return out;
  }

  onMount(async () => {
    patients = await api<HisPatient[]>("/api/his/patients");
    const q = new URLSearchParams(location.search);
    selectPatient(patients.some((x) => x.id === q.get("hn")) ? q.get("hn")! : patients[0].id);
    if (q.get("drug")) { drug = q.get("drug")!; dose = q.get("dose") ? Number(q.get("dose")) : null; await orderSelect(); }
  });
</script>

{#snippet segs(list: Seg[])}
  {#each list as s}{#if s.t === "b"}<strong>{s.v}</strong>{:else if s.t === "code"}<span class="ref">{s.v}</span>{:else if s.t === "i"}<em>{s.v}</em>{:else}{s.v}{/if}{/each}
{/snippet}

<div class="layout">
  <nav class="patients" aria-label="รายชื่อผู้ป่วย">
    <h2>ผู้ป่วยวันนี้</h2>
    <ul>
      {#each patients as x (x.id)}
        <li>
          <button type="button" aria-current={p?.id === x.id ? "true" : undefined} onclick={() => selectPatient(x.id)}>
            <span class="pname">{x.name}</span>
            <span class="pmeta">{x.id} · {x.age} ปี · {x.dx}</span>
          </button>
        </li>
      {/each}
    </ul>
  </nav>

  {#if p}
    <div class="main">
      <header class="patient">
        <p class="muted small">{p.id} · {p.age} ปี · {p.sex} · แพ้ยา: {p.allergy}</p>
        <h2 class="pt-name">{p.name}</h2>
        <p class="dx">{p.dx}</p>
        <p class="pgx">
          <span class="muted">ผลตรวจยีน:</span>
          {#if p.pgx.length}
            {#each p.pgx as g, i}{i ? " · " : " "}<strong>{g.gene}</strong> {g.result} <span class="muted small">({g.source} {g.date})</span>{/each}
          {:else}<span class="muted"> ยังไม่มีผล</span>{/if}
        </p>
      </header>

      <section class="block" aria-labelledby="h-active">
        <h2 id="h-active">ยาที่ใช้อยู่</h2>
        <div class="table-wrap"><table>
          <thead><tr><th scope="col">ยา</th><th scope="col">ขนาด</th><th scope="col">วิธีใช้</th><th scope="col"><span class="sr-only">สถานะ</span></th></tr></thead>
          <tbody>
            {#each p.active as m (m.id)}
              <tr class:stopped={m.status === "stopped"}>
                <th scope="row">{m.drug}</th>
                <td class="num">{m.dose_mg ?? "–"} mg</td>
                <td>{m.sig ?? ""}</td>
                <td class="r">{#if m.status === "stopped"}<span class="muted small">หยุดแล้ว</span>{:else if m.isNew}<span class="status good">เพิ่มใหม่</span>{/if}</td>
              </tr>
            {:else}
              <tr><td colspan="4" class="muted">ไม่มียาที่ใช้อยู่</td></tr>
            {/each}
          </tbody>
        </table></div>
        {#if labOrders.length}<p class="small lab">สั่งตรวจแล้ว: {labOrders.join(", ")}</p>{/if}
      </section>

      <section class="block" aria-labelledby="h-order">
        <h2 id="h-order">สั่งยาใหม่</h2>
        <form class="order" onsubmit={sign} autocomplete="off">
          <label class="field drug">ชื่อยา<input class="input" list="his-drugs" bind:value={drug} oninput={scheduleSelect} placeholder="เช่น carbamazepine" required /></label>
          <label class="field">ขนาด (mg)<input class="input" type="number" step="any" bind:value={dose} onchange={orderSelect} /></label>
          <label class="field">วิธีใช้<input class="input" bind:value={sig} placeholder="วันละครั้ง หลังอาหารเช้า" /></label>
          <button type="submit" class="btn btn-primary" aria-describedby={hasCritical ? "sign-blocked" : undefined}>ยืนยันคำสั่ง</button>
          <datalist id="his-drugs">{#each DRUGS as d}<option value={d}></option>{/each}</datalist>
        </form>
        <p class="hint">ลองสั่ง: {p.try}</p>
        {#if hasCritical}<p id="sign-blocked" class="sr-only">ยังบันทึกไม่ได้ เพราะมีคำสั่งห้าม</p>{/if}
        <div role="status" aria-live="polite">
          {#if message}<p class="msg" class:bad={message.bad}>{message.text}</p>{/if}
        </div>

        <div bind:this={cardsEl} class="cards" aria-live="polite">
          {#if cards && !cards.length}
            <p class="ok"><span class="status good">ไม่มีคำเตือน</span> <span class="muted">ไม่พบประเด็นยีนหรือยาตีกันจากคำสั่งนี้</span></p>
          {/if}
          {#each cards ?? [] as e (e.card.uuid)}
            {@const ind = IND[e.card.indicator]}
            <article class="alert {ind.tone}" class:pending={e.state === "pending"} class:resolved={e.state !== "pending"} aria-labelledby={`c-${e.card.uuid}`}>
              <div class="a-top">
                <span class="status {ind.tone}">{ind.th}</span>
                <a class="small" href={e.card.source.url} target="_blank" rel="noopener">แหล่งอ้างอิง<span class="sr-only"> (แท็บใหม่)</span></a>
              </div>
              <h3 id={`c-${e.card.uuid}`}>{e.card.summary}</h3>
              {#each blocks(e.card.detail).slice(0, 1) as b}
                {#if b.kind === "p"}<p class="lead-p">{@render segs(b.segs)}</p>{/if}
              {/each}
              <details class="more">
                <summary class="link-btn">หลักฐานและเหตุผล</summary>
                {#each blocks(e.card.detail).slice(1) as b}
                  {#if b.kind === "p"}<p>{@render segs(b.segs)}</p>{:else}<ul>{#each b.items as it}<li>{@render segs(it)}</li>{/each}</ul>{/if}
                {/each}
              </details>
              {#if e.state === "pending"}
                <div class="acts">
                  {#each e.card.suggestions as s (s.uuid)}
                    <button type="button" class="btn btn-sm btn-primary" onclick={() => accept(e, s)}>{s.label}</button>
                  {/each}
                </div>
                <div class="override">
                  <label class="field">เหตุผลถ้าจะสั่งต่อ (override)
                    <select class="select" id={`reason-${e.card.uuid}`} bind:value={e.reason}>
                      <option value={undefined}>เลือกเหตุผล</option>
                      {#each e.card.overrideReasons as r}<option value={r.code}>{r.display}</option>{/each}
                    </select>
                  </label>
                  <label class="field">หมายเหตุถึงเภสัชกร<input class="input" bind:value={e.note} /></label>
                  <button type="button" class="btn btn-sm" onclick={() => override(e)}>Override และแจ้งเภสัชกร</button>
                </div>
              {:else}
                <p class="state">{e.state === "accepted" ? `ทำตามคำแนะนำแล้ว — ${e.detail}` : `Override แล้ว (${e.detail}) — ส่งให้เภสัชกรทบทวน`}</p>
              {/if}
            </article>
          {/each}
        </div>
        {#if hookStatus}<p class="hook" aria-hidden="true">{hookStatus}</p>{/if}
      </section>
    </div>
  {/if}
</div>

<style>
  .layout { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 56px; align-items: start; }
  .patients { position: sticky; top: 96px; }
  .patients h2 { margin-bottom: 12px; }
  .patients ul { list-style: none; margin: 0; padding: 0; }
  .patients button {
    width: 100%; text-align: left; font: inherit; color: var(--ink-2); cursor: pointer; display: grid; gap: 1px;
    border: 0; background: none; padding: 12px 0 12px 14px; border-left: 2px solid var(--line);
  }
  .patients button:hover { color: var(--ink); border-left-color: var(--ink-3); }
  .patients button[aria-current="true"] { color: var(--ink); border-left-color: var(--ink); }
  .pname { font-weight: 500; }
  .pmeta { font-size: 13px; color: var(--ink-3); }
  .main { min-width: 0; }
  .patient { padding-bottom: 32px; }
  .pt-name { font-size: clamp(28px, 3.4vw, 38px); font-weight: 600; letter-spacing: -0.015em; text-transform: none; color: var(--ink); margin-top: 6px; line-height: 1.25; }
  .dx { font-size: 17px; color: var(--ink-2); margin-top: 2px; }
  .pgx { margin-top: 12px; font-size: 15px; overflow-wrap: anywhere; }
  .table-wrap { overflow-x: auto; }
  .block { border-top: 1px solid var(--line); padding: 32px 0; }
  .block > h2 { margin-bottom: 16px; }
  th[scope="row"] { font-weight: 500; font-size: 15px; color: var(--ink); border-bottom: 1px solid var(--line); }
  tr.stopped th, tr.stopped td { color: var(--ink-3); text-decoration: line-through; }
  tr.stopped td:last-child { text-decoration: none; }
  .lab { margin-top: 12px; color: var(--ink-2); }
  .order { display: grid; grid-template-columns: 2fr 1fr 2fr auto; gap: 12px; align-items: end; }
  .hint { font-size: 14px; color: var(--ink-3); margin-top: 12px; }
  .msg { margin-top: 16px; font-weight: 500; color: var(--ink); }
  .msg.bad { color: var(--critical); }
  .cards { display: grid; gap: 12px; margin-top: 20px; }
  .ok { display: flex; gap: 12px; align-items: baseline; flex-wrap: wrap; }
  .alert { border-radius: var(--radius); padding: 22px 24px; background: var(--subtle); }
  .alert.critical { background: var(--critical-soft); }
  .alert.serious { background: var(--warning-soft); }
  .alert.resolved { opacity: .7; }
  .a-top { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
  .alert h3 { font-size: 18px; margin-top: 8px; }
  .lead-p { color: var(--ink-2); margin-top: 4px; max-width: 70ch; }
  .more { margin-top: 10px; font-size: 14px; color: var(--ink-2); }
  .more summary { list-style: none; font-size: 14px; }
  .more summary::-webkit-details-marker { display: none; }
  .more p, .more ul { margin-top: 8px; }
  .more ul { padding-left: 18px; }
  .ref { font-size: 13px; color: var(--ink-3); }
  .acts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
  .override { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr) auto; gap: 10px; align-items: end; margin-top: 16px; padding-top: 16px; border-top: 1px solid color-mix(in srgb, var(--ink) 10%, transparent); }
  .state { margin-top: 14px; font-weight: 500; }
  .hook { font-size: 12.5px; color: var(--ink-3); margin-top: 16px; font-variant-numeric: tabular-nums; }
  @media (max-width: 900px) {
    .layout { grid-template-columns: 1fr; gap: 24px; }
    .patients { position: static; }
    .patients ul { display: flex; gap: 0 16px; overflow-x: auto; }
    .patients button { border-left: 0; border-bottom: 2px solid var(--line); padding: 8px 0; white-space: nowrap; }
    .patients button[aria-current="true"] { border-bottom-color: var(--ink); }
  }
  @media (max-width: 640px) { .order, .override { grid-template-columns: 1fr; } }
</style>
