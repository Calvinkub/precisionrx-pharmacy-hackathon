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
    critical: { th: "ห้ามสั่ง (HARD STOP)", icon: "⛔", tone: "critical" },
    warning: { th: "คำเตือน", icon: "⚠", tone: "serious" },
    info: { th: "ข้อมูล", icon: "ℹ", tone: "info" },
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
  {#each list as s}{#if s.t === "b"}<strong>{s.v}</strong>{:else if s.t === "code"}<code>{s.v}</code>{:else if s.t === "i"}<em>{s.v}</em>{:else}{s.v}{/if}{/each}
{/snippet}

<div class="layout">
  <nav class="card patients" aria-label="รายชื่อผู้ป่วย">
    <h2>ผู้ป่วยวันนี้</h2>
    <ul>
      {#each patients as x (x.id)}
        <li>
          <button type="button" aria-current={p?.id === x.id ? "true" : undefined} onclick={() => selectPatient(x.id)}>
            <strong>{x.id} · {x.name}</strong>
            <small>{x.age} ปี {x.sex} · {x.dx}</small>
          </button>
        </li>
      {/each}
    </ul>
  </nav>

  {#if p}
    <div class="main">
      <section class="card banner" aria-label="ข้อมูลผู้ป่วย">
        <div class="who">
          <h2>{p.name}</h2>
          <dl>
            <div><dt>HN</dt><dd>{p.id}</dd></div>
            <div><dt>อายุ/เพศ</dt><dd>{p.age} ปี · {p.sex}</dd></div>
            <div><dt>วินิจฉัย</dt><dd>{p.dx}</dd></div>
            <div><dt>แพ้ยา</dt><dd>{p.allergy}</dd></div>
          </dl>
        </div>
        <div class="pgx">
          <h3>ผล PGx ในระบบ</h3>
          {#if p.pgx.length}
            <ul>
              {#each p.pgx as g}
                <li class="chip {/positive|poor|decreased|ultrarapid/.test(g.result) ? 'critical' : ''}"><span class="dot"></span><span class="mono">{g.gene}</span> {g.result} <span class="muted">· {g.source} {g.date}</span></li>
              {/each}
            </ul>
          {:else}
            <p class="muted">ยังไม่มีผล PGx</p>
          {/if}
        </div>
      </section>

      <section class="card" aria-labelledby="h-active">
        <div class="card-head"><h2 id="h-active">ยาที่ใช้อยู่</h2><p>{p.active.filter((m) => m.status !== "stopped").length} รายการ</p></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th scope="col">ยา</th><th scope="col">ขนาด</th><th scope="col">วิธีใช้</th><th scope="col">สถานะ</th></tr></thead>
            <tbody>
              {#each p.active as m (m.id)}
                <tr class:new={m.isNew}>
                  <th scope="row">{#if m.status === "stopped"}<s>{m.drug}</s>{:else}{m.drug}{/if}</th>
                  <td class="num">{m.dose_mg ?? "–"} mg</td>
                  <td>{m.sig ?? ""}</td>
                  <td>{#if m.status === "stopped"}<span class="chip">หยุดแล้ว</span>{:else if m.isNew}<span class="chip good"><span class="dot"></span>ใหม่</span>{:else}ใช้อยู่{/if}</td>
                </tr>
              {:else}
                <tr><td colspan="4" class="muted">ไม่มียาที่ใช้อยู่</td></tr>
              {/each}
            </tbody>
          </table>
        </div>
        {#if labOrders.length}<p class="lab"><strong>สั่งตรวจแล้ว:</strong> {labOrders.join(", ")}</p>{/if}
      </section>

      <section class="card" aria-labelledby="h-order">
        <div class="card-head"><h2 id="h-order">สั่งยาใหม่</h2><p>ลองทำ: {p.try}</p></div>
        <form class="order" onsubmit={sign} autocomplete="off">
          <label class="field drug">ชื่อยา<input class="input" list="his-drugs" bind:value={drug} oninput={scheduleSelect} placeholder="เช่น carbamazepine" required /></label>
          <label class="field">ขนาด (mg)<input class="input" type="number" step="any" bind:value={dose} onchange={orderSelect} /></label>
          <label class="field">วิธีใช้<input class="input" bind:value={sig} placeholder="วันละครั้ง หลังอาหารเช้า" /></label>
          <button type="submit" class="btn btn-primary" aria-describedby={hasCritical ? "sign-blocked" : undefined}>ยืนยันคำสั่ง</button>
          <datalist id="his-drugs">{#each DRUGS as d}<option value={d}></option>{/each}</datalist>
        </form>
        <p class="hint">พิมพ์ชื่อยาแล้วระบบส่ง <code>order-select</code> ไปที่ PrecisionRx ทันที · กดยืนยันส่ง <code>order-sign</code> ตรวจซ้ำ</p>
        {#if hasCritical}<p id="sign-blocked" class="sr-only">ยังบันทึกไม่ได้ เพราะมีคำสั่งห้าม</p>{/if}
        {#if hookStatus}<p class="hook mono" aria-hidden="true">{hookStatus}</p>{/if}
        <div role="status" aria-live="polite" class="msg-wrap">
          {#if message}<p class="msg" class:bad={message.bad}>{message.text}</p>{/if}
        </div>

        <div bind:this={cardsEl} class="cards" aria-live="polite">
          {#if cards && !cards.length}
            <p class="ok"><span class="chip good"><span class="dot"></span>ผ่าน</span> ไม่มีประเด็น PGx หรือยาตีกันจากคำสั่งนี้ — ไม่เด้งเตือน</p>
          {/if}
          {#each cards ?? [] as e (e.card.uuid)}
            {@const ind = IND[e.card.indicator]}
            <article class="cds tone-{ind.tone}" class:pending={e.state === "pending"} class:resolved={e.state !== "pending"} aria-labelledby={`c-${e.card.uuid}`}>
              <header>
                <h3 id={`c-${e.card.uuid}`}>{e.card.summary}</h3>
                <span class="chip {ind.tone}"><span aria-hidden="true">{ind.icon}</span>{ind.th}</span>
              </header>
              <div class="detail">
                {#each blocks(e.card.detail) as b}
                  {#if b.kind === "p"}<p>{@render segs(b.segs)}</p>{:else}<ul>{#each b.items as it}<li>{@render segs(it)}</li>{/each}</ul>{/if}
                {/each}
              </div>
              <p class="src">แหล่ง: <a href={e.card.source.url} target="_blank" rel="noopener">{e.card.source.label}<span class="sr-only"> (แท็บใหม่)</span></a></p>
              {#if e.state === "pending"}
                {#if e.card.suggestions.length}
                  <div class="row" role="group" aria-label="ทำตามคำแนะนำ">
                    {#each e.card.suggestions as s (s.uuid)}
                      <button type="button" class="btn btn-sm sugg" onclick={() => accept(e, s)}>{s.label}</button>
                    {/each}
                  </div>
                {/if}
                <div class="override">
                  <label class="field">เหตุผลที่ override
                    <select class="select" id={`reason-${e.card.uuid}`} bind:value={e.reason}>
                      <option value={undefined}>— เลือกเหตุผล —</option>
                      {#each e.card.overrideReasons as r}<option value={r.code}>{r.display}</option>{/each}
                    </select>
                  </label>
                  <label class="field">หมายเหตุถึงเภสัชกร<input class="input" bind:value={e.note} /></label>
                  <button type="button" class="btn btn-sm" onclick={() => override(e)}>Override → แจ้งเภสัชกร</button>
                </div>
              {:else}
                <p class="state">{e.state === "accepted" ? `✓ ทำตามคำแนะนำ: ${e.detail}` : `↪ Override (${e.detail}) — ส่งเข้าคิวเภสัชกรแล้ว`}</p>
              {/if}
            </article>
          {/each}
        </div>
      </section>
    </div>
  {/if}
</div>

<style>
  .layout { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 16px; align-items: start; }
  .main { display: grid; gap: 16px; min-width: 0; }
  .patients { position: sticky; top: 80px; }
  .patients h2 { margin-bottom: 10px; }
  .patients ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .patients button {
    width: 100%; text-align: left; font: inherit; color: var(--ink); cursor: pointer; display: grid; gap: 2px;
    border: 1px solid var(--border); background: var(--raised); border-radius: 10px; padding: 10px 12px; min-height: 48px;
  }
  .patients button:hover { border-color: var(--ink-3); }
  .patients button[aria-current="true"] { border-color: var(--accent); background: var(--accent-soft); }
  .patients strong { font-size: 14px; }
  .patients small { font-size: 12.5px; color: var(--ink-2); }
  .banner { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; }
  .who h2 { font-size: 20px; }
  dl { display: flex; flex-wrap: wrap; gap: 4px 20px; margin: 8px 0 0; }
  dl div { display: flex; gap: 6px; font-size: 14px; }
  dt { color: var(--ink-3); } dd { margin: 0; font-weight: 500; }
  .pgx h3 { font-size: 13px; color: var(--ink-2); font-weight: 500; margin-bottom: 6px; }
  .pgx ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
  .pgx .chip { white-space: normal; }
  .table-wrap { overflow-x: auto; }
  th[scope="row"] { font-size: 14px; color: var(--ink); font-weight: 500; border-bottom: 1px solid var(--border); }
  tr.new th, tr.new td { background: var(--good-soft); }
  .lab { margin-top: 10px; font-size: 14px; }
  .order { display: grid; grid-template-columns: 2fr 1fr 2fr auto; gap: 10px; align-items: end; }
  .hint { font-size: 12.5px; color: var(--ink-3); margin-top: 8px; }
  .hook { font-size: 12px; color: var(--ink-3); margin-top: 6px; }
  .msg-wrap { margin-top: 10px; }
  .msg { padding: 10px 14px; border-radius: 10px; background: var(--good-soft); border-left: 4px solid var(--good); font-weight: 500; }
  .msg.bad { background: var(--critical-soft); border-left-color: var(--critical); }
  .cards { display: grid; gap: 12px; margin-top: 12px; }
  .ok { font-size: 14px; display: flex; gap: 8px; align-items: center; }
  .cds { border-radius: 12px; padding: 14px 16px; background: var(--sunken); border-left: 5px solid var(--border-strong); }
  .cds.resolved { opacity: .75; }
  .cds header { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
  .cds h3 { font-size: 16px; }
  .detail { font-size: 14px; margin-top: 6px; }
  .detail p { margin-top: 4px; }
  .detail ul { margin: 4px 0; padding-left: 20px; }
  .detail code { font-size: 12px; }
  .src { font-size: 13px; margin-top: 8px; }
  .row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
  .sugg { border-color: var(--accent); color: var(--accent); }
  .override { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr) auto; gap: 8px; align-items: end; margin-top: 12px; padding-top: 12px; border-top: 1px dashed var(--border-strong); }
  .state { margin-top: 10px; font-weight: 600; font-size: 14px; }
  .tone-critical { background: var(--critical-soft); border-left-color: var(--critical); }
  .tone-serious { background: var(--serious-soft); border-left-color: var(--serious); }
  .tone-info { background: var(--info-soft); border-left-color: var(--series-1); }
  @media (max-width: 960px) {
    .layout { grid-template-columns: 1fr; }
    .patients { position: static; }
    .patients ul { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
    .banner { grid-template-columns: 1fr; }
  }
  @media (max-width: 640px) {
    .order, .override { grid-template-columns: 1fr; }
  }
</style>
