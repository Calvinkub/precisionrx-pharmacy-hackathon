<script lang="ts">
  import { onMount, tick } from "svelte";
  import AnalytePanel from "./AnalytePanel.svelte";
  import NmrSummary from "./NmrSummary.svelte";
  import Results from "./Results.svelte";
  import Spectrum from "./Spectrum.svelte";
  import { api, postJson, type Analyte, type Assessment, type Case, type Med, type Profile } from "../lib/api";

  const DRUGS = ["atorvastatin", "rosuvastatin", "simvastatin", "pitavastatin", "pravastatin", "fluvastatin", "metformin",
    "clopidogrel", "omeprazole", "esomeprazole", "pantoprazole", "amlodipine", "losartan", "enalapril", "carbamazepine",
    "allopurinol", "semaglutide", "fenofibrate", "aspirin"];
  const PGX: Record<string, string[]> = {
    "HLA-B*15:02": ["positive", "negative"],
    "HLA-B*58:01": ["positive", "negative"],
    CYP2C19: ["normal metabolizer", "intermediate metabolizer", "poor metabolizer", "rapid metabolizer", "ultrarapid metabolizer"],
    SLCO1B1: ["normal function", "decreased function", "poor function"],
  };

  let catalog = $state<Analyte[]>([]);
  let cases = $state<{ id: string; label: string; story: string }[]>([]);
  let caseId = $state("");
  let data = $state<Case | null>(null);
  let visitIdx = $state(0);
  let profile = $state<Profile | null>(null);
  let meds = $state<(Med & { key: number })[]>([]);
  let pgx = $state<Record<string, string>>({});
  let result = $state<Assessment | null>(null);
  let busy = $state(false);
  let error = $state("");
  let announce = $state("");
  let medKey = 0;

  const byId = $derived(Object.fromEntries(catalog.map((a) => [a.id, a])));
  const visit = $derived(data?.visits[visitIdx]);
  const prev = $derived(visitIdx > 0 && data ? data.visits[visitIdx - 1].values : null);
  const story = $derived(cases.find((c) => c.id === caseId)?.story ?? "");

  async function loadCase(id: string, v = 0) {
    caseId = id;
    const c = await api<Case>(`/api/cases/${id}`);
    data = c;
    profile = { ...c.profile };
    meds = c.meds.map((m) => ({ ...m, key: medKey++ }));
    pgx = { ...c.pgx };
    visitIdx = Math.min(v, c.visits.length - 1);
    await assess();
    const u = new URL(location.href); u.searchParams.set("case", id); u.searchParams.set("visit", String(visitIdx + 1));
    history.replaceState(null, "", u);
  }

  async function selectVisit(i: number) {
    visitIdx = i;
    const u = new URL(location.href); u.searchParams.set("visit", String(i + 1)); history.replaceState(null, "", u);
    await assess();
  }

  async function assess() {
    if (!data || !profile) return;
    busy = true; error = "";
    try {
      const n = (x: unknown) => (x === "" || x == null ? null : Number(x));
      result = await postJson<Assessment>("/api/assess", {
        profile: { ...profile, age: n(profile.age), sbp: n(profile.sbp), weight_kg: n(profile.weight_kg), height_cm: n(profile.height_cm), waist_cm: n(profile.waist_cm) },
        meds: meds.filter((m) => m.drug.trim()).map(({ key, ...m }) => ({ ...m, dose_mg: n(m.dose_mg), pdc_pct: n(m.pdc_pct) })),
        pgx: Object.fromEntries(Object.entries(pgx).filter(([, v]) => v)),
        alcohol_drinks_per_day: n(profile.alcohol_drinks_per_day) ?? 0,
        activity_min_week: n(profile.activity_min_week),
        visits: data.visits.slice(0, visitIdx + 1),
      });
      const review = result.findings.filter((f) => f.severity === "stop" || f.severity === "action").length;
      announce = `ประเมินแล้ว: เรื่องยาที่ต้องทบทวน ${review} รายการ, ปัจจัยเสริมจาก NMR ${result.nmr_factors.length} รายการ`;
    } catch (e) {
      error = `ประเมินไม่สำเร็จ: ${(e as Error).message}`;
    } finally {
      busy = false;
    }
  }

  async function onUpload(e: Event) {
    const input = e.currentTarget as HTMLInputElement;
    const file = input.files?.[0];
    if (!file || !data) return;
    const fd = new FormData(); fd.append("file", file);
    try {
      const res = await api<{ values: Record<string, number>; unknown: string[]; date: string | null }>("/api/panel/parse", { method: "POST", body: fd });
      data.visits.push({ date: res.date ?? new Date().toISOString().slice(0, 10), label: `อัปโหลด: ${file.name}`, values: res.values });
      if (res.unknown.length) error = `ข้ามสารที่ไม่รู้จัก: ${res.unknown.join(", ")}`;
      await selectVisit(data.visits.length - 1);
      await tick();
      document.getElementById(`visit-${data.visits.length - 1}`)?.focus();
    } catch (err) {
      error = `อ่านไฟล์ไม่สำเร็จ: ${(err as Error).message}`;
    }
    input.value = "";
  }

  const addMed = () => (meds = [...meds, { drug: "", dose_mg: null, pdc_pct: null, start_visit: null, key: medKey++ }]);
  const removeMed = (k: number) => (meds = meds.filter((m) => m.key !== k));

  onMount(async () => {
    const [cat, list] = await Promise.all([api<{ analytes: Analyte[] }>("/api/catalog"), api<typeof cases>("/api/cases")]);
    catalog = cat.analytes;
    cases = list;
    const q = new URLSearchParams(location.search);
    const start = list.some((c) => c.id === q.get("case")) ? q.get("case")! : list[0].id;
    await loadCase(start, Math.max(0, Number(q.get("visit") ?? 1) - 1));
  });
</script>

<div class="sr-only" role="status" aria-live="polite">{announce}</div>

<section class="toolbar card" aria-label="เลือกข้อมูล">
  <label class="field case-field">
    เคสตัวอย่าง
    <select class="select" value={caseId} onchange={(e) => loadCase((e.currentTarget as HTMLSelectElement).value)}>
      {#each cases as c (c.id)}<option value={c.id}>{c.label}</option>{/each}
    </select>
  </label>
  {#if data}
    <fieldset class="visits">
      <legend class="field-label">ผลตรวจครั้งที่</legend>
      <div class="seg">
        {#each data.visits as v, i (i)}
          <label class="seg-item">
            <input type="radio" name="visit" id={`visit-${i}`} checked={i === visitIdx} onchange={() => selectVisit(i)} />
            <span><strong>ครั้งที่ {i + 1}</strong><small>{v.date}</small></span>
          </label>
        {/each}
      </div>
    </fieldset>
  {/if}
  <div class="upload">
    <label class="btn btn-ghost">
      <input type="file" accept=".csv,text/csv" class="sr-only" onchange={onUpload} />
      <span aria-hidden="true">＋</span> เพิ่มผลตรวจใหม่ (CSV)
    </label>
    <a class="small-link" href="/sample_panel.csv" download>ดาวน์โหลดไฟล์ตัวอย่าง</a>
  </div>
  {#if story}<p class="story"><span class="chip info"><span class="dot"></span>เรื่องของเคส</span> {story}</p>{/if}
</section>

{#if error}<p class="error" role="alert">{error}</p>{/if}

<div class="grid">
  <section class="card" aria-labelledby="h-nmr">
    <div class="card-head">
      <h2 id="h-nmr"><span class="step">1</span>ผล NMR</h2>
      {#if visit}<p>{visit.label ? `${visit.label} · ` : ""}{visit.date}</p>{/if}
    </div>
    {#if visit && catalog.length}
      <Spectrum values={visit.values} {byId} height={120} />
      {#if result?.nmr_summary}
        <NmrSummary domains={result.nmr_summary} />
      {:else}
        <p class="muted">กำลังสรุปผล…</p>
      {/if}
      <details class="all-values">
        <summary>ดูค่าทั้งหมด {Object.keys(visit.values).length} สาร <span class="muted">(สำหรับเภสัชกร)</span></summary>
        <AnalytePanel {catalog} values={visit.values} {prev} />
      </details>
    {:else}
      <p class="muted">กำลังโหลด…</p>
    {/if}
  </section>

  <section class="card form-card" aria-labelledby="h-form">
    <div class="card-head"><h2 id="h-form"><span class="step">2</span>ข้อมูลผู้ป่วย</h2><p>แก้ไขแล้วกด "ประเมินใหม่"</p></div>
    {#if profile}
      <form onsubmit={(e) => { e.preventDefault(); assess(); }}>
        <fieldset>
          <legend>ประวัติส่วนตัว</legend>
          <div class="g3">
            <label class="field">อายุ (ปี)<input class="input" type="number" min="18" max="100" required bind:value={profile.age} /></label>
            <label class="field">เพศ
              <select class="select" bind:value={profile.sex}><option value="female">หญิง</option><option value="male">ชาย</option></select>
            </label>
            <label class="field">ความดันตัวบน (mmHg)<input class="input" type="number" min="70" max="250" bind:value={profile.sbp} /></label>
            <label class="field">น้ำหนัก (กก.)<input class="input" type="number" step="0.1" bind:value={profile.weight_kg} /></label>
            <label class="field">ส่วนสูง (ซม.)<input class="input" type="number" step="0.1" bind:value={profile.height_cm} /></label>
            <label class="field">รอบเอว (ซม.)<input class="input" type="number" step="0.1" bind:value={profile.waist_cm} /></label>
          </div>
          <div class="checks">
            <label class="check"><input type="checkbox" bind:checked={profile.smoker} /> สูบบุหรี่</label>
            <label class="check"><input type="checkbox" bind:checked={profile.diabetes} /> เป็นเบาหวาน</label>
            <label class="check"><input type="checkbox" bind:checked={profile.hypertension} /> ความดันโลหิตสูง</label>
            <label class="check"><input type="checkbox" bind:checked={profile.family_history_dm} /> พ่อแม่/พี่น้องเป็นเบาหวาน</label>
          </div>
          <div class="g2">
            <label class="field">แอลกอฮอล์ (ดื่มมาตรฐาน/วัน)<input class="input" type="number" step="0.5" min="0" bind:value={profile.alcohol_drinks_per_day} /></label>
            <label class="field">ออกกำลังกาย (นาที/สัปดาห์)<input class="input" type="number" min="0" bind:value={profile.activity_min_week} /></label>
          </div>
        </fieldset>

        <fieldset class="sep">
          <legend>ยาที่ใช้</legend>
          <p class="hint" id="pdc-hint">PDC = สัดส่วนวันที่มียากิน จากประวัติรับยา · ≥ 80% ถือว่าสม่ำเสมอ</p>
          <ul class="meds">
            {#each meds as m, i (m.key)}
              <li class="med">
                <label class="field drug">ยา<input class="input" list="drug-list" bind:value={m.drug} placeholder="ชื่อยา" /></label>
                <label class="field">ขนาด (mg/วัน)<input class="input" type="number" step="any" bind:value={m.dose_mg} /></label>
                <label class="field">PDC %<input class="input" type="number" min="0" max="100" aria-describedby="pdc-hint" bind:value={m.pdc_pct} /></label>
                <label class="field start">เริ่มใช้
                  <select class="select" bind:value={m.start_visit}>
                    <option value={null}>ก่อนตรวจครั้งแรก</option>
                    {#each (data?.visits ?? []).slice(1) as _, j}<option value={j + 1}>ก่อนตรวจครั้งที่ {j + 2}</option>{/each}
                  </select>
                </label>
                <button type="button" class="btn btn-sm remove" onclick={() => removeMed(m.key)} aria-label={`ลบยา ${m.drug || `แถวที่ ${i + 1}`}`}>ลบ</button>
              </li>
            {/each}
          </ul>
          <button type="button" class="btn btn-ghost btn-sm" onclick={addMed}>＋ เพิ่มยา</button>
          <datalist id="drug-list">{#each DRUGS as d}<option value={d}></option>{/each}</datalist>
        </fieldset>

        <fieldset class="sep">
          <legend>ผล PGx (ถ้ามี)</legend>
          <div class="g2">
            {#each Object.entries(PGX) as [gene, opts] (gene)}
              <label class="field">{gene}
                <select class="select" bind:value={pgx[gene]}>
                  <option value="">ไม่ทราบ / ไม่ได้ตรวจ</option>
                  {#each opts as o}<option value={o}>{o}</option>{/each}
                </select>
              </label>
            {/each}
          </div>
        </fieldset>

        <button type="submit" class="btn btn-primary submit" disabled={busy}>{busy ? "กำลังประเมิน…" : "ประเมินใหม่ →"}</button>
      </form>
    {/if}
  </section>
</div>

{#if result}
  <div class="results" aria-busy={busy}>
    <Results r={result} hasPrev={visitIdx > 0} />
  </div>
{/if}

<style>
  .toolbar { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 14px 24px; margin-bottom: 16px; }
  .case-field { min-width: min(340px, 100%); }
  .field-label { font-size: 13px; color: var(--ink-2); font-weight: 500; margin-bottom: 5px; }
  .seg { display: flex; gap: 4px; background: var(--sunken); padding: 4px; border-radius: 11px; flex-wrap: wrap; }
  .seg-item { position: relative; cursor: pointer; }
  .seg-item input { position: absolute; opacity: 0; inset: 0; cursor: pointer; }
  .seg-item span { display: grid; padding: 6px 14px; border-radius: 8px; line-height: 1.25; color: var(--ink-2); min-height: 40px; }
  .seg-item small { font-size: 11.5px; font-family: var(--mono); }
  .seg-item input:checked + span { background: var(--raised); color: var(--ink); box-shadow: 0 1px 3px rgba(0, 0, 0, .12); }
  .seg-item input:focus-visible + span { outline: 3px solid var(--focus); outline-offset: 1px; }
  .upload { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .upload label { cursor: pointer; }
  .upload label:focus-within { outline: 3px solid var(--focus); outline-offset: 2px; }
  .small-link { font-size: 13px; }
  .story { flex-basis: 100%; font-size: 14px; color: var(--ink-2); display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .error { background: var(--critical-soft); border-left: 4px solid var(--critical); padding: 10px 14px; border-radius: 10px; margin-bottom: 16px; }

  .all-values { margin-top: 16px; border-top: 1px solid var(--border); padding-top: 12px; }
  .all-values summary {
    cursor: pointer; font-weight: 600; min-height: 44px; display: flex; align-items: center; gap: 8px; list-style: none;
    padding: 0 12px; border-radius: 10px; background: var(--sunken);
  }
  .all-values summary::-webkit-details-marker { display: none; }
  .all-values summary::before { content: "▸"; transition: transform .15s; }
  .all-values[open] summary::before { transform: rotate(90deg); }
  .grid { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 16px; align-items: start; }
  .form-card { position: sticky; top: 80px; max-height: calc(100vh - 96px); overflow-y: auto; }
  .g2, .g3 { display: grid; gap: 10px; margin-bottom: 10px; }
  .g2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .g3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .checks { display: flex; flex-wrap: wrap; gap: 2px 18px; margin: 4px 0 10px; }
  .sep { background: linear-gradient(var(--border), var(--border)) top / 100% 1px no-repeat; padding-top: 16px; margin-top: 8px; }
  .hint { font-size: 12.5px; color: var(--ink-3); margin: -4px 0 10px; }
  .meds { list-style: none; margin: 0 0 10px; padding: 0; display: grid; gap: 10px; }
  .med {
    display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr) minmax(0, .8fr); gap: 8px 10px; align-items: end;
    padding: 12px; background: var(--sunken); border-radius: 12px;
  }
  .med .start { grid-column: 1 / 3; }
  .remove { align-self: end; justify-self: end; }
  .submit { width: 100%; margin-top: 16px; min-height: 48px; font-size: 16px; }
  .submit:disabled { opacity: .6; cursor: progress; }
  .results { margin-top: 16px; transition: opacity .2s; }
  .results[aria-busy="true"] { opacity: .6; }

  @media (max-width: 1080px) {
    .grid { grid-template-columns: 1fr; }
    .form-card { position: static; max-height: none; }
  }
  @media (max-width: 560px) {
    .g3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .med { grid-template-columns: 1fr 1fr; }
    .med .drug, .med .start { grid-column: 1 / -1; }
  }
</style>
