<script lang="ts">
  import { onMount } from "svelte";
  import CaseBar from "./CaseBar.svelte";
  import Sources from "./Sources.svelte";
  import type { Assessment, Case } from "../lib/api";
  import { listCases, loadAll, readQuery, writeQuery, type MedRecord } from "../lib/case";

  let cases = $state<{ id: string; label: string }[]>([]);
  let caseId = $state("");
  let data = $state<Case | null>(null);
  let visitIdx = $state(0);
  let rec = $state<MedRecord | null>(null);
  let r = $state<Assessment | null>(null);
  let pulled = $state(false);
  let pulling = $state(false);
  let announce = $state("");

  const STATUS = { regular: ["good", "กินประจำ"], new: ["info", "เพิ่งเริ่ม"], stopped: ["", "หยุดแล้ว"] } as const;
  const DIR = { down: "↓ ลดลง", up: "↑ เพิ่มขึ้น", stable: "– ไม่ควรเปลี่ยน" } as const;
  const active = $derived(rec ? rec.medications.filter((m) => m.status !== "stopped") : []);
  const shifting = $derived(active.filter((m) => m.effects.some((e) => e.direction !== "stable")));
  const lowPdc = $derived(active.filter((m) => m.status !== "new" && m.pdc_pct < 80));
  const affected = $derived(r ? r.nmr_summary.filter((d) => d.drug_note) : []);
  const q = $derived(`?case=${caseId}&visit=${visitIdx + 1}`);
  const thDate = (d: string) => new Date(d).toLocaleDateString("th-TH", { day: "numeric", month: "short", year: "numeric" });

  async function load(id: string, v: number, keepPulled = false) {
    const all = await loadAll(id, v);
    caseId = id; data = all.c; visitIdx = all.visitIdx; rec = all.rec; r = all.r;
    pulled = keepPulled;
    writeQuery(caseId, visitIdx);
  }

  async function pull() {
    pulling = true;
    await new Promise((res) => setTimeout(res, matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 500));
    pulled = true; pulling = false;
    announce = `ดึงรายการยาแล้ว ${active.length} รายการ`;
  }

  onMount(async () => {
    cases = await listCases();
    const { caseId: qc, visit } = readQuery();
    await load(cases.some((c) => c.id === qc) ? qc! : cases[0].id, visit ? visit - 1 : 99);
  });
</script>

<div class="sr-only" role="status" aria-live="polite">{announce}</div>

{#if data}
  <CaseBar {cases} {caseId} visits={data.visits} {visitIdx} onselect={(c, v) => load(c, v, pulled)} />
{/if}

<section class="intro">
  <p class="lead">ยาหลายตัวเปลี่ยนระดับสารในเลือดโดยตรง เช่น ยาลดไขมันทำให้ ApoB และ LDL ต่ำลง ถ้าไม่รู้ว่าคนไข้กินยาอะไรอยู่ ผล NMR อาจดูความเสี่ยงต่ำกว่าความจริง</p>
  {#if !pulled}
    <button type="button" class="btn btn-primary pull" onclick={pull} disabled={pulling || !rec}>
      {pulling ? "กำลังดึงข้อมูล…" : "ดึงรายการยาจากระบบโรงพยาบาล"}
    </button>
    <p class="muted small">ดึงจากประวัติการรับยาที่ห้องยา (ข้อมูลจำลอง) ณ วันที่ตรวจ</p>
  {/if}
</section>

{#if pulled && rec}
  <section class="section" aria-labelledby="h-sum">
    <h2 id="h-sum">สรุป ณ วันที่ {thDate(rec.as_of)}</h2>
    <dl class="figures">
      <div><dt>ยาที่กินประจำ</dt><dd class="num">{active.length}</dd><dd class="muted small">รายการ</dd></div>
      <div><dt>ยาที่เปลี่ยนค่าในเลือด</dt><dd class="num">{shifting.length}</dd><dd class="muted small">{shifting.map((m) => m.drug).join(", ") || "ไม่มี"}</dd></div>
      <div><dt>กินไม่สม่ำเสมอ (PDC &lt; 80%)</dt><dd class="num">{lowPdc.length}</dd><dd class="muted small">{lowPdc.map((m) => m.drug).join(", ") || "ไม่มี"}</dd></div>
    </dl>
  </section>

  <section class="section" aria-labelledby="h-list">
    <div class="section-head"><h2 id="h-list">รายการยา</h2><span class="muted small">{rec.source}</span></div>
    <ul class="meds">
      {#each rec.medications as m (m.drug)}
        <li class="med" class:stopped={m.status === "stopped"}>
          <div class="m-head">
            <div>
              <h3>{m.drug} {m.dose_mg ? `${m.dose_mg} mg` : ""}</h3>
              <p class="muted small">{m.sig} · เริ่มรับยา {thDate(m.first_fill)} · รับยา {m.fills} ครั้ง</p>
            </div>
            <span class="status {STATUS[m.status][0]}">{STATUS[m.status][1]}</span>
          </div>

          {#if m.status !== "new"}
            <div class="pdc">
              <span class="pdc-label">กินสม่ำเสมอ</span>
              <span class="meter" aria-hidden="true"><span class="fill" class:low={m.pdc_pct < 80} style={`width:${Math.min(100, m.pdc_pct)}%`}></span><span class="mark"></span></span>
              <span class="num pdc-val">{m.pdc_pct.toFixed(0)}%</span>
              <span class="sr-only">PDC {m.pdc_pct.toFixed(0)} เปอร์เซ็นต์ เกณฑ์ 80</span>
            </div>
          {/if}

          <div class="effects">
            <p class="e-title">ผลต่อค่าในเลือด</p>
            {#if m.effects.length}
              <ul>
                {#each m.effects as e}
                  <li><span class="dir" class:down={e.direction === "down"}>{DIR[e.direction]}</span> <span>{e.analytes.join(", ")}</span>{#if e.note}<span class="muted small">&nbsp;— {e.note}</span>{/if}</li>
                {/each}
              </ul>
            {/if}
            <p class="interp">{m.interpretation}</p>
            {#if m.fact_ids.length}<Sources ids={m.fact_ids} facts={rec.facts} />{/if}
          </div>
        </li>
      {/each}
    </ul>
    <p class="muted small foot">PDC = สัดส่วนวันที่มียากินจากประวัติรับยา ย้อนหลังสูงสุด 180 วัน · ตั้งแต่ 80% ขึ้นไปถือว่าสม่ำเสมอ <Sources ids={["DISPENSING-PDC", "PQA-PDC80"]} facts={rec.facts} /></p>
  </section>

  <section class="section" aria-labelledby="h-nmr">
    <div class="section-head"><h2 id="h-nmr">ผลต่อการอ่านผล NMR ครั้งนี้</h2><a class="small" href={`/dashboard/${q}`}>ไปหน้าผลตรวจ →</a></div>
    {#if affected.length}
      <ul class="affected">
        {#each affected as d (d.id)}
          <li><h3>{d.title}</h3><p>{d.drug_note}</p></li>
        {/each}
      </ul>
    {:else}
      <p class="muted">ยาที่กินอยู่ไม่มีผลต่อค่า NMR ที่ใช้ในรายงานนี้ตามหลักฐานที่มี</p>
    {/if}
    <p class="muted small foot">รายการยานี้ถูกนำไปใช้ในหน้าผลตรวจและหน้าความเสี่ยงโดยอัตโนมัติ</p>
  </section>
{/if}

<style>
  .intro { padding: 32px 0 40px; }
  .lead { font-size: clamp(19px, 2vw, 23px); line-height: 1.55; color: var(--ink-2); max-width: 46ch; }
  .pull { margin: 28px 0 10px; min-height: 50px; padding: 12px 28px; font-size: 16px; }
  .pull:disabled { opacity: .6; cursor: progress; }
  .figures { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 20px 0 0; }
  .figures div { padding: 4px 24px 4px 0; border-right: 1px solid var(--line); display: grid; gap: 2px; align-content: start; }
  .figures div + div { padding-left: 24px; }
  .figures div:last-child { border-right: 0; }
  .figures dt { font-size: 13.5px; color: var(--ink-3); }
  .figures dd { margin: 0; }
  .figures dd.num { font-size: 34px; font-weight: 500; line-height: 1.2; }
  .meds { list-style: none; margin: 0; padding: 0; }
  .med { padding: 28px 0; border-top: 1px solid var(--line); display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr); gap: 16px 48px; align-items: start; grid-template-rows: auto 1fr; animation: rise .4s var(--ease) both; }
  .med:nth-child(2) { animation-delay: .06s; } .med:nth-child(3) { animation-delay: .12s; } .med:nth-child(4) { animation-delay: .18s; }
  @keyframes rise { from { opacity: 0; transform: translateY(6px); } }
  .med.stopped { opacity: .55; }
  .m-head { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; grid-column: 1; }
  .m-head h3 { font-size: 19px; }
  .pdc { grid-column: 1; align-self: start; display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: 12px; align-items: center; }
  .pdc-label { font-size: 13.5px; color: var(--ink-3); }
  .meter { position: relative; height: 6px; border-radius: 3px; background: var(--band); }
  .fill { position: absolute; inset: 0 auto 0 0; border-radius: 3px; background: var(--good); }
  .fill.low { background: var(--serious); }
  .mark { position: absolute; left: 80%; top: -4px; width: 1.5px; height: 14px; background: var(--ink-2); }
  .pdc-val { font-weight: 500; }
  .effects { grid-column: 2; grid-row: 1 / span 2; }
  .e-title { font-size: 13px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-3); margin-bottom: 6px; }
  .effects ul { list-style: none; margin: 0 0 8px; padding: 0; display: grid; gap: 4px; }
  .dir { display: inline-block; min-width: 110px; color: var(--ink-3); font-size: 14px; }
  .dir.down { color: var(--ink); font-weight: 500; }
  .interp { color: var(--ink-2); font-size: 15px; margin-bottom: 6px; }
  .foot { margin-top: 16px; }
  .affected { list-style: none; margin: 0; padding: 0; }
  .affected li { padding: 16px 0; border-top: 1px solid var(--line); }
  .affected p { color: var(--ink-2); margin-top: 2px; }
  @media (max-width: 860px) {
    .med { grid-template-columns: 1fr; }
    .effects { grid-column: 1; grid-row: auto; }
    .figures { grid-template-columns: 1fr; row-gap: 20px; }
    .figures div { border-right: 0; padding: 0 !important; }
  }
</style>
