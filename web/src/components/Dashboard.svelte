<script lang="ts">
  import { onMount } from "svelte";
  import AllValues from "./AllValues.svelte";
  import NmrRows from "./NmrRows.svelte";
  import Sources from "./Sources.svelte";
  import Spectrum from "./Spectrum.svelte";
  import { CAT_TH, CAT_TONE, api, postJson, type Analyte, type Assessment, type Case, type Finding, type Med, type Profile } from "../lib/api";

  const DRUGS = ["atorvastatin", "rosuvastatin", "simvastatin", "pitavastatin", "pravastatin", "fluvastatin", "metformin",
    "clopidogrel", "omeprazole", "esomeprazole", "pantoprazole", "amlodipine", "losartan", "enalapril", "carbamazepine",
    "allopurinol", "semaglutide", "fenofibrate", "aspirin"];
  const PGX: Record<string, string[]> = {
    "HLA-B*15:02": ["positive", "negative"],
    "HLA-B*58:01": ["positive", "negative"],
    CYP2C19: ["normal metabolizer", "intermediate metabolizer", "poor metabolizer", "rapid metabolizer", "ultrarapid metabolizer"],
    SLCO1B1: ["normal function", "decreased function", "poor function"],
  };
  const SEV = { stop: ["critical", "ห้ามใช้"], action: ["serious", "ต้องทบทวน"], monitor: ["info", "ติดตาม"], info: ["good", "ตามคาด"] } as const;

  let catalog = $state<Analyte[]>([]);
  let cases = $state<{ id: string; label: string; story: string }[]>([]);
  let caseId = $state("");
  let data = $state<Case | null>(null);
  let visitIdx = $state(0);
  let profile = $state<Profile | null>(null);
  let meds = $state<(Med & { key: number })[]>([]);
  let pgx = $state<Record<string, string>>({});
  let r = $state<Assessment | null>(null);
  let busy = $state(false);
  let error = $state("");
  let announce = $state("");
  let decisions = $state<Record<string, string>>({});
  let formSheet = $state<HTMLDialogElement>();
  let valuesSheet = $state<HTMLDialogElement>();
  let fileInput = $state<HTMLInputElement>();
  let medKey = 0;

  const byId = $derived(Object.fromEntries(catalog.map((a) => [a.id, a])));
  const visit = $derived(data?.visits[visitIdx]);
  const story = $derived(cases.find((c) => c.id === caseId)?.story ?? "");
  const review = $derived(r ? r.findings.filter((f) => f.severity === "stop" || f.severity === "action") : []);
  const others = $derived(r ? r.findings.filter((f) => f.severity === "monitor" || f.severity === "info") : []);

  const patientLine = $derived.by(() => {
    if (!profile) return "";
    const bits: string[] = [];
    const m = meds.filter((x) => x.drug.trim()).map((x) => `${x.drug}${x.dose_mg ? ` ${x.dose_mg} mg` : ""}`);
    if (m.length) bits.push(m.join(", "));
    const g = Object.entries(pgx).filter(([, v]) => v).map(([k, v]) => `${k} ${v}`);
    if (g.length) bits.push(g.join(", "));
    return bits.join(" · ");
  });

  // Two plain sentences built from the engine output (no free text generation).
  const headline = $derived.by(() => {
    if (!r) return ["", ""];
    const ath = r.nmr_summary.find((d) => d.id === "atherogenic");
    let first = "";
    if (ath?.key) {
      const above = ath.key.target != null && ath.key.value >= ath.key.target;
      const v = ath.key.verdict;
      if (v === "improved") first = `ไขมันที่ทำให้หลอดเลือดแข็งลดลงจริง ${Math.abs(ath.key.pct_change ?? 0).toFixed(0)}%${above ? " แต่ยังสูงกว่าเป้า" : " และอยู่ในเป้าหมาย"}`;
      else if (v === "worsened") first = `ไขมันที่ทำให้หลอดเลือดแข็งเพิ่มขึ้นจริงจากครั้งก่อน${above ? " และสูงกว่าเป้า" : ""}`;
      else first = above ? "ไขมันที่ทำให้หลอดเลือดแข็งยังสูงกว่าเป้า" : "ไขมันที่ทำให้หลอดเลือดแข็งอยู่ในเป้าหมาย";
    }
    const watch = r.nmr_summary.filter((d) => d.id !== "atherogenic" && (d.status === "warning" || d.status === "serious")).length;
    if (watch) first += ` · ควรติดตามอีก ${watch} เรื่อง`;
    const stops = r.findings.filter((f) => f.severity === "stop").length;
    const second = stops ? `มีคำสั่งห้ามใช้ยา ${stops} รายการ และเรื่องยาที่ต้องทบทวนรวม ${review.length} รายการ`
      : review.length ? `มี ${review.length} เรื่องยาที่เภสัชกรควรทบทวน` : "ไม่มีเรื่องยาที่ต้องทบทวน";
    return [first, second];
  });

  async function loadCase(id: string, v = 0) {
    caseId = id;
    const c = await api<Case>(`/api/cases/${id}`);
    data = c; profile = { ...c.profile }; pgx = { ...c.pgx }; decisions = {};
    meds = c.meds.map((m) => ({ ...m, key: medKey++ }));
    visitIdx = Math.min(v, c.visits.length - 1);
    await assess();
    syncUrl();
  }
  function syncUrl() {
    const u = new URL(location.href); u.searchParams.set("case", caseId); u.searchParams.set("visit", String(visitIdx + 1));
    history.replaceState(null, "", u);
  }
  async function selectVisit(i: number) { visitIdx = i; syncUrl(); await assess(); }

  async function assess() {
    if (!data || !profile) return;
    busy = true; error = "";
    try {
      const n = (x: unknown) => (x === "" || x == null ? null : Number(x));
      r = await postJson<Assessment>("/api/assess", {
        profile: { ...profile, age: n(profile.age), sbp: n(profile.sbp), weight_kg: n(profile.weight_kg), height_cm: n(profile.height_cm), waist_cm: n(profile.waist_cm) },
        meds: meds.filter((m) => m.drug.trim()).map(({ key, ...m }) => ({ ...m, dose_mg: n(m.dose_mg), pdc_pct: n(m.pdc_pct) })),
        pgx: Object.fromEntries(Object.entries(pgx).filter(([, v]) => v)),
        alcohol_drinks_per_day: n(profile.alcohol_drinks_per_day) ?? 0,
        activity_min_week: n(profile.activity_min_week),
        visits: data.visits.slice(0, visitIdx + 1),
      });
      announce = `อัปเดตผลแล้ว: ${headline.join(" ")}`;
    } catch (e) {
      error = `ประเมินไม่สำเร็จ: ${(e as Error).message}`;
    } finally { busy = false; }
  }

  async function onUpload(e: Event) {
    const input = e.currentTarget as HTMLInputElement;
    const file = input.files?.[0];
    if (!file || !data) return;
    const fd = new FormData(); fd.append("file", file);
    try {
      const res = await api<{ values: Record<string, number>; unknown: string[]; date: string | null }>("/api/panel/parse", { method: "POST", body: fd });
      data.visits.push({ date: res.date ?? new Date().toISOString().slice(0, 10), label: file.name, values: res.values });
      if (res.unknown.length) error = `ข้ามสารที่ไม่รู้จัก: ${res.unknown.join(", ")}`;
      await selectVisit(data.visits.length - 1);
    } catch (err) { error = `อ่านไฟล์ไม่สำเร็จ: ${(err as Error).message}`; }
    input.value = "";
  }

  const addMed = () => (meds = [...meds, { drug: "", dose_mg: null, pdc_pct: null, start_visit: null, key: medKey++ }]);
  const removeMed = (k: number) => (meds = meds.filter((m) => m.key !== k));
  async function saveForm(e: SubmitEvent) { e.preventDefault(); formSheet?.close(); await assess(); }
  const riskValue = (k: Assessment["risks"][number]) => (k.value == null ? "–" : k.id === "dm" ? `${k.value}/17` : k.display);

  onMount(async () => {
    const [cat, list] = await Promise.all([api<{ analytes: Analyte[] }>("/api/catalog"), api<typeof cases>("/api/cases")]);
    catalog = cat.analytes; cases = list;
    const q = new URLSearchParams(location.search);
    await loadCase(list.some((c) => c.id === q.get("case")) ? q.get("case")! : list[0].id, Math.max(0, Number(q.get("visit") ?? 1) - 1));
  });
</script>

{#snippet finding(f: Finding, i: number)}
  <li class="finding" class:stop={f.severity === "stop"}>
    <span class="idx num" aria-hidden="true">{String(i + 1).padStart(2, "0")}</span>
    <div class="body">
      <div class="f-top"><h3>{f.title}</h3><span class="status {SEV[f.severity][0]}">{SEV[f.severity][1]}</span></div>
      <p>{f.detail}</p>
      <div class="meta">
        <Sources ids={f.fact_ids} facts={r!.facts} />
        <details class="why"><summary class="link-btn">เหตุผล</summary><ol>{#each f.trace as t}<li>{t}</li>{/each}</ol></details>
      </div>
      {#if f.severity === "stop" || f.severity === "action"}
        <div class="segmented decide" role="group" aria-label={`การตัดสินใจของเภสัชกร: ${f.title}`}>
          {#each [["accept", "ยอมรับ"], ["modify", "แก้ไข"], ["reject", "ไม่ยอมรับ"]] as [k, label]}
            <button type="button" aria-pressed={decisions[f.id] === k} onclick={() => (decisions[f.id] = k)}>{label}</button>
          {/each}
        </div>
      {/if}
    </div>
  </li>
{/snippet}

<div class="sr-only" role="status" aria-live="polite">{announce}</div>

<!-- ─── Patient + controls ─── -->
<section class="top">
  <div class="who">
    <label class="case-pick">
      <span>เคสตัวอย่าง</span>
      <select value={caseId} onchange={(e) => loadCase((e.currentTarget as HTMLSelectElement).value)}>
        {#each cases as c (c.id)}<option value={c.id}>{c.label}</option>{/each}
      </select>
    </label>
    {#if profile}<p class="name">{profile.sex === "female" ? "ผู้ป่วยหญิง" : "ผู้ป่วยชาย"} {profile.age} ปี</p>{/if}
    <p class="line">{patientLine}</p>
    {#if story}<p class="story">{story}</p>{/if}
  </div>
  <div class="controls">
    {#if data}
      <fieldset class="segmented">
        <legend class="sr-only">ผลตรวจครั้งที่</legend>
        {#each data.visits as v, i (i)}
          <label><input type="radio" name="visit" checked={i === visitIdx} onchange={() => selectVisit(i)} />ครั้งที่ {i + 1}<span class="date">{v.date}</span></label>
        {/each}
      </fieldset>
    {/if}
    <div class="actions">
      <button type="button" class="btn btn-sm" onclick={() => formSheet?.showModal()}>แก้ไขข้อมูลผู้ป่วย</button>
      <button type="button" class="btn btn-sm" onclick={() => fileInput?.click()}>เพิ่มผลตรวจ</button>
      <input bind:this={fileInput} type="file" accept=".csv,text/csv" class="sr-only" tabindex="-1" aria-hidden="true" onchange={onUpload} />
    </div>
  </div>
</section>

{#if error}<p class="error" role="alert">{error}</p>{/if}

{#if r && visit}
  <div class="report" aria-busy={busy}>
    <!-- ─── Summary ─── -->
    <section class="summary" aria-labelledby="h-sum">
      <h2 id="h-sum">สรุป</h2>
      <p class="lead">{headline[0]}</p>
      <p class="lead second">{headline[1]}</p>
      <dl class="figures">
        <div><dt>โรคหัวใจและหลอดเลือด 10 ปี</dt><dd class="num">{riskValue(r.risks[0])}</dd><dd><span class="status {CAT_TONE[r.risks[0].category]}">{CAT_TH[r.risks[0].category]}</span></dd></div>
        <div><dt>ความเสี่ยงเบาหวาน</dt><dd class="num">{r.risks[1].value == null ? "–" : `${r.risks[1].value}/17`}</dd><dd><span class="status {CAT_TONE[r.risks[1].category]}">{r.risks[1].category === "not_assessable" ? "เป็นเบาหวานแล้ว" : CAT_TH[r.risks[1].category]}</span></dd></div>
        <div><dt>เรื่องยาที่ต้องทบทวน</dt><dd class="num">{review.length}</dd><dd class="muted small">รายการ</dd></div>
        <div><dt>เทียบครั้งก่อน</dt>
          {#if visitIdx > 0}
            <dd class="num">{r.trend.filter((t) => t.verdict === "improved").length}<span class="muted"> / {r.trend.filter((t) => t.verdict === "worsened").length}</span></dd><dd class="muted small">ดีขึ้นจริง / แย่ลงจริง</dd>
          {:else}<dd class="num muted">–</dd><dd class="muted small">ตรวจครั้งแรก</dd>{/if}
        </div>
      </dl>
    </section>

    <!-- ─── NMR ─── -->
    <section class="section" aria-labelledby="h-nmr">
      <div class="section-head">
        <h2 id="h-nmr">ผลตรวจ NMR · {visit.date}</h2>
        <button type="button" class="link-btn" onclick={() => valuesSheet?.showModal()}>ดูค่าทั้งหมด {Object.keys(visit.values).length} สาร</button>
      </div>
      <Spectrum values={visit.values} {byId} height={84} />
      <NmrRows domains={r.nmr_summary} />
    </section>

    <!-- ─── Medication ─── -->
    <section class="section" aria-labelledby="h-meds">
      <div class="section-head"><h2 id="h-meds">เรื่องยา</h2><span class="muted small">สำหรับเภสัชกรทบทวนก่อนถึงแพทย์</span></div>
      {#if review.length}
        <ol class="findings">{#each review as f, i (f.id)}{@render finding(f, i)}{/each}</ol>
      {:else}
        <p class="empty">ไม่มีเรื่องยาที่ต้องทบทวน</p>
      {/if}
      {#if others.length}
        <h3 class="subhead">ติดตามต่อ</h3>
        <ol class="findings quiet">{#each others as f, i (f.id)}{@render finding(f, review.length + i)}{/each}</ol>
      {/if}
    </section>

    <!-- ─── Lifestyle ─── -->
    <section class="section" aria-labelledby="h-life">
      <div class="section-head"><h2 id="h-life">การดูแลตัวเอง</h2></div>
      {#if r.advice.length}
        <ul class="advice">
          {#each r.advice as a (a.id)}
            <li><h3>{a.topic}</h3><p>{a.advice}</p><p class="why-line">เพราะ{a.reason} · <Sources ids={a.fact_ids} facts={r.facts} /></p></li>
          {/each}
        </ul>
      {:else}<p class="empty">พฤติกรรมตอนนี้อยู่ในเกณฑ์ ไม่มีคำแนะนำเพิ่มเติม</p>{/if}
    </section>

    <!-- ─── Risk detail ─── -->
    <section class="section" aria-labelledby="h-risk">
      <div class="section-head"><h2 id="h-risk">ที่มาของความเสี่ยง</h2></div>
      <ul class="plain">
        {#each r.risks as k (k.id)}
          <li>
            <div><h3>{k.disease}</h3><p class="muted small">{k.score_name}{k.method !== "-" ? ` · ${k.method}` : ""}{k.notes.length ? ` · ${k.notes.join(" · ")}` : ""}</p></div>
            <p class="num val">{riskValue(k)}</p>
            <Sources ids={k.fact_ids} facts={r.facts} />
          </li>
        {/each}
        {#each r.nmr_factors as x (x.id)}
          <li>
            <div><h3>{x.title}</h3><p class="muted small">{x.detail}</p></div>
            <p class="tag">{x.level === "emerging" ? "หลักฐานเบื้องต้น" : "ตาม guideline"}</p>
            <Sources ids={x.fact_ids} facts={r.facts} />
          </li>
        {/each}
      </ul>
      <p class="muted small foot">สัญญาณจาก NMR แสดงแยกจากคะแนนความเสี่ยง ไม่ได้นำไปคำนวณรวม</p>
    </section>
  </div>
{:else}
  <p class="muted loading">กำลังโหลด…</p>
{/if}

<!-- ─── Sheets ─── -->
<dialog bind:this={valuesSheet} class="sheet" aria-labelledby="h-all" onclick={(e) => e.target === valuesSheet && valuesSheet?.close()}>
  <div class="sheet-head"><h2 id="h-all">ค่า NMR ทั้งหมด</h2><button type="button" class="btn btn-sm" onclick={() => valuesSheet?.close()}>ปิด</button></div>
  <div class="sheet-body">
    {#if visit && r}<AllValues {catalog} values={visit.values} trend={r.trend} />{/if}
  </div>
</dialog>

<dialog bind:this={formSheet} class="sheet" aria-labelledby="h-form" onclick={(e) => e.target === formSheet && formSheet?.close()}>
  <div class="sheet-head"><h2 id="h-form">ข้อมูลผู้ป่วย</h2><button type="button" class="btn btn-sm" onclick={() => formSheet?.close()}>ปิด</button></div>
  {#if profile}
    <form class="sheet-body form" onsubmit={saveForm}>
      <fieldset>
        <legend>ประวัติ</legend>
        <div class="g2">
          <label class="field">อายุ (ปี)<input class="input" type="number" min="18" max="100" required bind:value={profile.age} /></label>
          <label class="field">เพศ<select class="select" bind:value={profile.sex}><option value="female">หญิง</option><option value="male">ชาย</option></select></label>
          <label class="field">ความดันตัวบน (mmHg)<input class="input" type="number" min="70" max="250" bind:value={profile.sbp} /></label>
          <label class="field">รอบเอว (ซม.)<input class="input" type="number" step="0.1" bind:value={profile.waist_cm} /></label>
          <label class="field">น้ำหนัก (กก.)<input class="input" type="number" step="0.1" bind:value={profile.weight_kg} /></label>
          <label class="field">ส่วนสูง (ซม.)<input class="input" type="number" step="0.1" bind:value={profile.height_cm} /></label>
        </div>
        <div class="checks">
          <label class="check"><input type="checkbox" bind:checked={profile.smoker} />สูบบุหรี่</label>
          <label class="check"><input type="checkbox" bind:checked={profile.diabetes} />เป็นเบาหวาน</label>
          <label class="check"><input type="checkbox" bind:checked={profile.hypertension} />ความดันโลหิตสูง</label>
          <label class="check"><input type="checkbox" bind:checked={profile.family_history_dm} />ครอบครัวเป็นเบาหวาน</label>
        </div>
        <div class="g2">
          <label class="field">แอลกอฮอล์ (ดื่มมาตรฐาน/วัน)<input class="input" type="number" step="0.5" min="0" bind:value={profile.alcohol_drinks_per_day} /></label>
          <label class="field">ออกกำลังกาย (นาที/สัปดาห์)<input class="input" type="number" min="0" bind:value={profile.activity_min_week} /></label>
        </div>
      </fieldset>

      <fieldset class="sep">
        <legend>ยาที่ใช้</legend>
        <ul class="meds">
          {#each meds as m, i (m.key)}
            <li>
              <label class="field drug">ยา<input class="input" list="drug-list" bind:value={m.drug} /></label>
              <label class="field">mg/วัน<input class="input" type="number" step="any" bind:value={m.dose_mg} /></label>
              <label class="field">PDC %<input class="input" type="number" min="0" max="100" bind:value={m.pdc_pct} aria-describedby="pdc-hint" /></label>
              <label class="field start">เริ่มใช้
                <select class="select" bind:value={m.start_visit}>
                  <option value={null}>ก่อนตรวจครั้งแรก</option>
                  {#each (data?.visits ?? []).slice(1) as _, j}<option value={j + 1}>ก่อนตรวจครั้งที่ {j + 2}</option>{/each}
                </select>
              </label>
              <button type="button" class="link-btn remove" onclick={() => removeMed(m.key)} aria-label={`ลบยา ${m.drug || `แถวที่ ${i + 1}`}`}>ลบ</button>
            </li>
          {/each}
        </ul>
        <button type="button" class="btn btn-sm" onclick={addMed}>เพิ่มยา</button>
        <p class="hint" id="pdc-hint">PDC คือสัดส่วนวันที่มียากินจากประวัติรับยา ตั้งแต่ 80% ขึ้นไปถือว่าสม่ำเสมอ</p>
        <datalist id="drug-list">{#each DRUGS as d}<option value={d}></option>{/each}</datalist>
      </fieldset>

      <fieldset class="sep">
        <legend>ผลตรวจยีน (PGx)</legend>
        <div class="g2">
          {#each Object.entries(PGX) as [gene, opts] (gene)}
            <label class="field">{gene}
              <select class="select" bind:value={pgx[gene]}>
                <option value="">ไม่ได้ตรวจ</option>
                {#each opts as o}<option value={o}>{o}</option>{/each}
              </select>
            </label>
          {/each}
        </div>
      </fieldset>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">บันทึกและประเมินใหม่</button>
        <a class="link-btn" href="/sample_panel.csv" download>ไฟล์ตัวอย่างผลตรวจ (CSV)</a>
      </div>
    </form>
  {/if}
</dialog>

<style>
  .top { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px 40px; flex-wrap: wrap; padding-bottom: 32px; }
  .who { max-width: 640px; min-width: 0; flex: 1 1 320px; overflow-wrap: anywhere; }
  .case-pick { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--ink-3); max-width: 100%; }
  .case-pick > span { white-space: nowrap; }
  .case-pick select { min-width: 0; text-overflow: ellipsis; }
  .case-pick select {
    appearance: none; border: 0; color: var(--ink-2); cursor: pointer; padding: 4px 22px 4px 0; max-width: 100%;
    font: 500 14px/1.3 var(--font); background: none;
    background-image: linear-gradient(45deg, transparent 50%, var(--ink-3) 50%), linear-gradient(135deg, var(--ink-3) 50%, transparent 50%);
    background-position: right 7px center, right 2px center; background-size: 5px 5px; background-repeat: no-repeat;
  }
  .name { font-size: clamp(28px, 3.4vw, 38px); font-weight: 600; letter-spacing: -0.015em; line-height: 1.25; margin-top: 10px; }
  .line { color: var(--ink-2); margin-top: 6px; }
  .story { color: var(--ink-3); font-size: 14.5px; margin-top: 4px; }
  .controls { display: grid; justify-items: end; gap: 12px; }
  .segmented .date { font-size: 12px; color: var(--ink-3); margin-left: 8px; }
  .actions { display: flex; gap: 8px; flex-wrap: wrap; }
  .error { color: var(--critical); margin-bottom: 16px; }
  .loading { padding: 40px 0; }
  .report { transition: opacity .2s; }
  .report[aria-busy="true"] { opacity: .55; }

  .summary { padding: 40px 0 44px; border-top: 1px solid var(--line); }
  .lead { font-size: clamp(22px, 2.6vw, 30px); line-height: 1.45; font-weight: 400; letter-spacing: -0.01em; margin-top: 14px; max-width: 34ch; }
  .lead.second { color: var(--ink-3); margin-top: 4px; }
  .figures { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 36px 0 0; }
  .figures div { padding: 4px 24px 4px 0; border-right: 1px solid var(--line); display: grid; gap: 2px; align-content: start; }
  .figures div + div { padding-left: 24px; }
  .figures div:last-child { border-right: 0; }
  .figures dt { font-size: 13.5px; color: var(--ink-3); }
  .figures dd { margin: 0; }
  .figures dd.num { font-size: 34px; font-weight: 500; letter-spacing: -0.02em; line-height: 1.2; }

  .findings { list-style: none; margin: 0; padding: 0; }
  .finding { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 8px; padding: 20px 0; border-top: 1px solid var(--line); }
  .finding.stop { background: var(--critical-soft); border-radius: var(--radius); padding: 20px; border-top: 0; margin-bottom: 8px; }
  .idx { font-size: 14px; color: var(--ink-3); padding-top: 2px; }
  .f-top { display: flex; justify-content: space-between; gap: 16px; align-items: baseline; }
  .body > p { color: var(--ink-2); margin-top: 4px; max-width: 70ch; }
  .meta { display: flex; gap: 20px; align-items: baseline; margin-top: 10px; font-size: 13.5px; flex-wrap: wrap; }
  .why summary { list-style: none; font-size: 13.5px; }
  .why summary::-webkit-details-marker { display: none; }
  .why ol { margin: 8px 0 0; padding-left: 20px; color: var(--ink-2); font-size: 14px; }
  .decide { margin-top: 14px; }
  .subhead { font-size: 14px; color: var(--ink-3); font-weight: 500; margin: 28px 0 4px; }
  .quiet h3 { font-weight: 500; }
  .empty { color: var(--ink-3); }

  .advice { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 48px; }
  .advice p { color: var(--ink-2); margin-top: 4px; }
  .why-line { font-size: 13.5px; color: var(--ink-3) !important; }

  .plain { list-style: none; margin: 0; padding: 0; }
  .plain li { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 24px; align-items: baseline; padding: 16px 0; border-top: 1px solid var(--line); }
  .val { font-size: 20px; font-weight: 500; }
  .tag { font-size: 13px; color: var(--ink-3); white-space: nowrap; }
  .foot { margin-top: 14px; }

  .form fieldset { margin-bottom: 8px; }
  .sep { border-top: 1px solid var(--line); padding-top: 24px; margin-top: 24px; }
  .g2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-bottom: 14px; }
  .checks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2px 16px; margin: 8px 0 16px; }
  .meds { list-style: none; margin: 0 0 14px; padding: 0; }
  .meds li { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr) minmax(0, .8fr); gap: 10px; padding: 14px 0; border-bottom: 1px solid var(--line); }
  .meds .start { grid-column: 1 / 3; }
  .remove { align-self: center; justify-self: end; font-size: 14px; margin-top: 20px; }
  .hint { font-size: 13px; color: var(--ink-3); margin-top: 12px; }
  .form-actions { display: flex; align-items: center; gap: 20px; margin-top: 32px; flex-wrap: wrap; }

  @media (max-width: 860px) {
    .controls { justify-items: start; }
    .figures { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 24px; }
    .figures div:nth-child(2) { border-right: 0; }
    .figures div:nth-child(3) { padding-left: 0; }
    .advice { grid-template-columns: 1fr; }
    .plain li { grid-template-columns: minmax(0, 1fr) auto; }
  }
  @media (max-width: 520px) {
    .g2, .checks { grid-template-columns: 1fr; }
    .finding { grid-template-columns: 1fr; }
    .idx { display: none; }
    .f-top { flex-direction: column; gap: 4px; }
  }
</style>
