<script lang="ts">
  import { onMount } from "svelte";
  import AllValues from "./AllValues.svelte";
  import CaseBar from "./CaseBar.svelte";
  import NmrRows from "./NmrRows.svelte";
  import Sources from "./Sources.svelte";
  import Spectrum from "./Spectrum.svelte";
  import { CAT_TH, CAT_TONE, api, type Analyte, type Assessment, type Case, type Finding, type Med, type Profile } from "../lib/api";
  import { listCases, loadAll, readQuery, runAssess, saveEdits, writeQuery } from "../lib/case";

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
  let pgx = $state<Record<string, string>>({});
  let meds = $state<Med[]>([]);
  let r = $state<Assessment | null>(null);
  let busy = $state(false);
  let error = $state("");
  let announce = $state("");
  let decisions = $state<Record<string, string>>({});
  let formSheet = $state<HTMLDialogElement>();
  let valuesSheet = $state<HTMLDialogElement>();
  let fileInput = $state<HTMLInputElement>();

  const byId = $derived(Object.fromEntries(catalog.map((a) => [a.id, a])));
  const visit = $derived(data?.visits[visitIdx]);
  const story = $derived(cases.find((c) => c.id === caseId)?.story ?? "");
  const review = $derived(r ? r.findings.filter((f) => f.severity === "stop" || f.severity === "action") : []);
  const others = $derived(r ? r.findings.filter((f) => f.severity === "monitor" || f.severity === "info") : []);
  const q = $derived(`?case=${caseId}&visit=${visitIdx + 1}`);

  const patientLine = $derived.by(() => {
    const bits: string[] = [];
    if (meds.length) bits.push(meds.map((x) => `${x.drug}${x.dose_mg ? ` ${x.dose_mg} mg` : ""}`).join(", "));
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
  const drugTouched = $derived(r ? r.nmr_summary.filter((d) => d.drugs.length).length : 0);

  async function load(id: string, v: number) {
    busy = true; error = "";
    try {
      const all = await loadAll(id, v);
      caseId = id; data = all.c; visitIdx = all.visitIdx; profile = all.profile; pgx = all.pgx; meds = all.meds; r = all.r;
      decisions = {};
      writeQuery(caseId, visitIdx);
      announce = `อัปเดตผลแล้ว: ${headline.join(" ")}`;
    } catch (e) { error = `โหลดไม่สำเร็จ: ${(e as Error).message}`; } finally { busy = false; }
  }

  async function reassess() {
    if (!data || !profile) return;
    busy = true;
    try { r = await runAssess(data, visitIdx, meds, profile, pgx); } catch (e) { error = (e as Error).message; } finally { busy = false; }
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
      visitIdx = data.visits.length - 1;
      await reassess();
    } catch (err) { error = `อ่านไฟล์ไม่สำเร็จ: ${(err as Error).message}`; }
    input.value = "";
  }

  async function saveForm(e: SubmitEvent) {
    e.preventDefault();
    formSheet?.close();
    if (profile) saveEdits(caseId, { profile: $state.snapshot(profile), pgx: $state.snapshot(pgx) });
    await reassess();
  }

  onMount(async () => {
    const [cat, list] = await Promise.all([api<{ analytes: Analyte[] }>("/api/catalog"), listCases()]);
    catalog = cat.analytes; cases = list;
    const { caseId: qc, visit } = readQuery();
    await load(list.some((c) => c.id === qc) ? qc! : list[0].id, visit ? visit - 1 : 99);
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

{#if data}
  <CaseBar {cases} {caseId} visits={data.visits} {visitIdx} onselect={(c, v) => load(c, v)} />
{/if}

<section class="top">
  <div class="who">
    {#if profile}<p class="name">{profile.sex === "female" ? "ผู้ป่วยหญิง" : "ผู้ป่วยชาย"} {profile.age} ปี</p>{/if}
    <p class="line">{patientLine}</p>
    {#if story}<p class="story">{story}</p>{/if}
  </div>
  <div class="actions">
    <button type="button" class="btn btn-sm" onclick={() => formSheet?.showModal()}>แก้ไขข้อมูลผู้ป่วย</button>
    <button type="button" class="btn btn-sm" onclick={() => fileInput?.click()}>เพิ่มผลตรวจ</button>
    <input bind:this={fileInput} type="file" accept=".csv,text/csv" class="sr-only" tabindex="-1" aria-hidden="true" onchange={onUpload} />
  </div>
</section>

{#if error}<p class="error" role="alert">{error}</p>{/if}

{#if r && visit}
  <div class="report" aria-busy={busy}>
    <section class="summary" aria-labelledby="h-sum">
      <h2 id="h-sum">สรุป</h2>
      <p class="lead">{headline[0]}</p>
      <p class="lead second">{headline[1]}</p>
      <dl class="figures">
        <div><dt>โรคหัวใจและหลอดเลือด 10 ปี</dt><dd class="num">{r.risks[0].value == null ? "–" : r.risks[0].display}</dd><dd><span class="status {CAT_TONE[r.risks[0].category]}">{CAT_TH[r.risks[0].category]}</span></dd></div>
        <div><dt>เรื่องยาที่ต้องทบทวน</dt><dd class="num">{review.length}</dd><dd class="muted small">รายการ</dd></div>
        <div><dt>หัวข้อที่ยาเปลี่ยนค่า</dt><dd class="num">{drugTouched}</dd><dd class="muted small">จาก {r.nmr_summary.length} หัวข้อ</dd></div>
        <div><dt>เทียบครั้งก่อน</dt>
          {#if visitIdx > 0}
            <dd class="num">{r.trend.filter((t) => t.verdict === "improved").length}<span class="muted"> / {r.trend.filter((t) => t.verdict === "worsened").length}</span></dd><dd class="muted small">ดีขึ้นจริง / แย่ลงจริง</dd>
          {:else}<dd class="num muted">–</dd><dd class="muted small">ตรวจครั้งแรก</dd>{/if}
        </div>
      </dl>
      <p class="next"><a href={`/care/${q}`}>ดูความเสี่ยงและวิธีดูแลตัวเอง →</a></p>
    </section>

    <section class="section" aria-labelledby="h-nmr">
      <div class="section-head">
        <h2 id="h-nmr">ผลตรวจ NMR · {visit.date}</h2>
        <button type="button" class="link-btn" onclick={() => valuesSheet?.showModal()}>ดูค่าทั้งหมด {Object.keys(visit.values).length} สาร</button>
      </div>
      <Spectrum values={visit.values} {byId} height={84} />
      <NmrRows domains={r.nmr_summary} />
      {#if drugTouched}
        <p class="drug-hint">บางค่าถูกยาที่กินประจำเปลี่ยนไป — <a href={`/medications/${q}`}>ดูว่ายาแต่ละตัวมีผลกับค่าไหน</a></p>
      {/if}
    </section>

    <section class="section" aria-labelledby="h-meds">
      <div class="section-head"><h2 id="h-meds">เรื่องยา</h2><a class="small" href={`/medications/${q}`}>ยาที่ใช้ประจำ {meds.length} รายการ →</a></div>
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
  </div>
{:else}
  <p class="muted loading">กำลังโหลด…</p>
{/if}

<dialog bind:this={valuesSheet} class="sheet" aria-labelledby="h-all" onclick={(e) => e.target === valuesSheet && valuesSheet?.close()}>
  <div class="sheet-head"><h2 id="h-all">ค่า NMR ทั้งหมด</h2><button type="button" class="btn btn-sm" onclick={() => valuesSheet?.close()}>ปิด</button></div>
  <div class="sheet-body">{#if visit && r}<AllValues {catalog} values={visit.values} trend={r.trend} />{/if}</div>
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
      <p class="hint sep">รายการยาดึงจากประวัติรับยาของโรงพยาบาลอัตโนมัติ — ดูได้ที่หน้า <a href={`/medications/${q}`}>ยาที่ใช้ประจำ</a></p>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">บันทึกและประเมินใหม่</button>
        <a class="link-btn" href="/sample_panel.csv" download>ไฟล์ตัวอย่างผลตรวจ (CSV)</a>
      </div>
    </form>
  {/if}
</dialog>

<style>
  .top { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px 40px; flex-wrap: wrap; padding: 16px 0 32px; }
  .who { max-width: 680px; min-width: 0; flex: 1 1 320px; overflow-wrap: anywhere; }
  .name { font-size: clamp(28px, 3.4vw, 38px); font-weight: 600; letter-spacing: -0.015em; line-height: 1.25; }
  .line { color: var(--ink-2); margin-top: 6px; }
  .story { color: var(--ink-3); font-size: 14.5px; margin-top: 4px; }
  .actions { display: flex; gap: 8px; flex-wrap: wrap; }
  .error { color: var(--critical); margin-bottom: 16px; }
  .loading { padding: 40px 0; }
  .report { transition: opacity .2s; }
  .report[aria-busy="true"] { opacity: .55; }
  .summary { padding: 40px 0 36px; border-top: 1px solid var(--line); }
  .lead { font-size: clamp(22px, 2.6vw, 30px); line-height: 1.45; font-weight: 400; letter-spacing: -0.01em; margin-top: 14px; max-width: 34ch; }
  .lead.second { color: var(--ink-3); margin-top: 4px; }
  .figures { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 36px 0 0; }
  .figures div { padding: 4px 24px 4px 0; border-right: 1px solid var(--line); display: grid; gap: 2px; align-content: start; }
  .figures div + div { padding-left: 24px; }
  .figures div:last-child { border-right: 0; }
  .figures dt { font-size: 13.5px; color: var(--ink-3); }
  .figures dd { margin: 0; }
  .figures dd.num { font-size: 34px; font-weight: 500; letter-spacing: -0.02em; line-height: 1.2; }
  .next { margin-top: 28px; font-weight: 500; }
  .drug-hint { margin-top: 16px; font-size: 14.5px; color: var(--ink-2); }
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
  .form fieldset { margin-bottom: 8px; }
  .sep { border-top: 1px solid var(--line); padding-top: 24px; margin-top: 24px; }
  .g2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-bottom: 14px; }
  .checks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2px 16px; margin: 8px 0 16px; }
  .hint { font-size: 14px; color: var(--ink-3); }
  .form-actions { display: flex; align-items: center; gap: 20px; margin-top: 32px; flex-wrap: wrap; }
  @media (max-width: 860px) {
    .figures { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 24px; }
    .figures div:nth-child(2) { border-right: 0; }
    .figures div:nth-child(3) { padding-left: 0; }
  }
  @media (max-width: 520px) {
    .g2, .checks { grid-template-columns: 1fr; }
    .finding { grid-template-columns: 1fr; }
    .idx { display: none; }
    .f-top { flex-direction: column; gap: 4px; }
  }
</style>
