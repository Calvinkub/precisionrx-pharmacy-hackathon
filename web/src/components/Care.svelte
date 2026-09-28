<script lang="ts">
  import { onMount } from "svelte";
  import CaseBar from "./CaseBar.svelte";
  import Sources from "./Sources.svelte";
  import { CAT_TH, type Assessment, type Case, type Profile, type Risk } from "../lib/api";
  import { listCases, loadAll, readQuery, writeQuery } from "../lib/case";

  let cases = $state<{ id: string; label: string }[]>([]);
  let caseId = $state("");
  let data = $state<Case | null>(null);
  let visitIdx = $state(0);
  let profile = $state<Profile | null>(null);
  let r = $state<Assessment | null>(null);

  // category bands exactly as the validated scores define them
  const CVD_BANDS = [
    { to: 10, label: "ต่ำ", tone: "good" }, { to: 20, label: "ปานกลาง", tone: "warning" },
    { to: 30, label: "สูง", tone: "serious" }, { to: 40, label: "สูงมาก", tone: "critical" },
  ];
  const DM_BANDS = [
    { to: 2.5, label: "ต่ำ", tone: "good" }, { to: 5.5, label: "ปานกลาง", tone: "warning" },
    { to: 8.5, label: "สูง", tone: "serious" }, { to: 17, label: "สูงมาก", tone: "critical" },
  ];
  const cvd = $derived(r?.risks.find((x) => x.id === "cvd"));
  const dm = $derived(r?.risks.find((x) => x.id === "dm"));
  const drugNotes = $derived(r ? r.nmr_summary.filter((d) => d.drug_note) : []);
  const today = new Date().toLocaleDateString("th-TH", { dateStyle: "long" });

  function pos(value: number, max: number) { return `${Math.min(100, Math.max(0, (value / max) * 100))}%`; }

  async function load(id: string, v: number) {
    const all = await loadAll(id, v);
    caseId = id; data = all.c; visitIdx = all.visitIdx; profile = all.profile; r = all.r;
    writeQuery(caseId, visitIdx);
  }
  onMount(async () => {
    cases = await listCases();
    const { caseId: qc, visit } = readQuery();
    await load(cases.some((c) => c.id === qc) ? qc! : cases[0].id, visit ? visit - 1 : 99);
  });
</script>

{#snippet scale(risk: Risk, bands: typeof CVD_BANDS, max: number, value: number)}
  <div class="scale" aria-hidden="true">
    <div class="bands">
      {#each bands as b, i}
        {@const from = i ? bands[i - 1].to : 0}
        <span class="band tone-{b.tone}" style={`width:${((b.to - from) / max) * 100}%`}></span>
      {/each}
    </div>
    <span class="marker" style={`left:${pos(value, max)}`}></span>
    <div class="labels">
      {#each bands as b, i}
        {@const from = i ? bands[i - 1].to : 0}
        <span style={`width:${((b.to - from) / max) * 100}%`} class:on={CAT_TH[risk.category] === b.label}>{b.label}</span>
      {/each}
    </div>
  </div>
{/snippet}

{#if data}
  <div class="no-print"><CaseBar {cases} {caseId} visits={data.visits} {visitIdx} onselect={(c, v) => load(c, v)} /></div>
{/if}

{#if r && profile && cvd && dm}
  <header class="head">
    <div>
      <p class="muted">{profile.sex === "female" ? "ผู้ป่วยหญิง" : "ผู้ป่วยชาย"} {profile.age} ปี · ผลตรวจวันที่ {data?.visits[visitIdx].date}</p>
      <h1>ความเสี่ยงและการดูแลตัวเอง</h1>
    </div>
    <button type="button" class="btn no-print" onclick={() => window.print()}>พิมพ์หรือบันทึก PDF</button>
  </header>

  <section class="risks" aria-label="ความเสี่ยงรายโรค">
    <article class="risk">
      <h2>โรคหัวใจและหลอดเลือด ใน 10 ปี</h2>
      <p class="big num">{cvd.value == null ? "–" : cvd.display}</p>
      <p class="cat">ความเสี่ยง<strong>{CAT_TH[cvd.category]}</strong></p>
      {#if cvd.value != null}{@render scale(cvd, CVD_BANDS, 40, cvd.value)}{/if}
      <p class="explain">โอกาสเกิดโรคหัวใจหรือหลอดเลือดสมองใน 10 ปีข้างหน้า จาก Thai CV Risk Score{cvd.notes.length ? ` · ${cvd.notes.join(" · ")}` : ""}</p>
      <Sources ids={cvd.fact_ids} facts={r.facts} />
    </article>
    <article class="risk">
      <h2>เบาหวานชนิดที่ 2 ใน 12 ปี</h2>
      {#if dm.value == null}
        <p class="big">–</p>
        <p class="cat">{profile.diabetes ? "เป็นเบาหวานแล้ว — ใช้การควบคุมน้ำตาลแทนคะแนนคัดกรอง" : dm.display}</p>
      {:else}
        <p class="big num">{dm.value}<span class="of">/17</span></p>
        <p class="cat">ความเสี่ยง<strong>{CAT_TH[dm.category]}</strong></p>
        {@render scale(dm, DM_BANDS, 17, dm.value)}
        <p class="explain">คะแนนจาก Thai Diabetes Risk Score: อายุ เพศ ดัชนีมวลกาย รอบเอว ความดัน และประวัติครอบครัว</p>
      {/if}
      <Sources ids={dm.fact_ids} facts={r.facts} />
    </article>
  </section>

  {#if r.nmr_factors.length || drugNotes.length}
    <section class="section" aria-labelledby="h-signals">
      <h2 id="h-signals">สิ่งที่ผลเลือดบอกเพิ่ม</h2>
      <ul class="signals">
        {#each r.nmr_factors as x (x.id)}
          <li><h3>{x.title}</h3><p>{x.detail}</p><p class="muted small">{x.level === "emerging" ? "หลักฐานเบื้องต้น ยังไม่ได้นำไปคำนวณความเสี่ยง" : "ตาม guideline"} · <Sources ids={x.fact_ids} facts={r.facts} /></p></li>
        {/each}
        {#each drugNotes as d (d.id)}
          <li><h3>{d.title} — มีผลจากยา</h3><p>{d.drug_note}</p></li>
        {/each}
      </ul>
    </section>
  {/if}

  <section class="section" aria-labelledby="h-care">
    <h2 id="h-care">สิ่งที่ควรทำ</h2>
    {#if r.advice.length}
      <ol class="advice">
        {#each r.advice as a, i (a.id)}
          <li>
            <span class="n num" aria-hidden="true">{i + 1}</span>
            <div>
              <h3>{a.topic}</h3>
              <p class="do">{a.advice}</p>
              <p class="muted small">เพราะ{a.reason} · <Sources ids={a.fact_ids} facts={r.facts} /></p>
            </div>
          </li>
        {/each}
      </ol>
    {:else}
      <p class="muted">พฤติกรรมตอนนี้อยู่ในเกณฑ์ดี รักษาไว้ต่อเนื่อง</p>
    {/if}
  </section>

  {#if r.follow_up.length}
    <section class="section" aria-labelledby="h-next">
      <h2 id="h-next">นัดติดตาม</h2>
      <ul class="next">
        {#each r.follow_up as f (f.id)}
          <li><p>{f.text}</p><Sources ids={f.fact_ids} facts={r.facts} /></li>
        {/each}
      </ul>
    </section>
  {/if}

  <p class="disclaimer">เอกสารนี้สร้างจากข้อมูลจำลองเพื่อการสาธิต · ไม่ใช่การวินิจฉัย ควรปรึกษาแพทย์หรือเภสัชกรก่อนปรับยาหรือพฤติกรรม · พิมพ์วันที่ {today}</p>
{:else}
  <p class="muted loading">กำลังโหลด…</p>
{/if}

<style>
  .head { display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; flex-wrap: wrap; padding: 24px 0 32px; }
  .head h1 { margin-top: 6px; }
  .risks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
  .risk { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 32px; display: grid; gap: 6px; align-content: start; }
  .risk h2 { color: var(--ink-3); }
  .risk :global(.src-btn) { justify-self: start; }
  .big { font-size: clamp(56px, 7vw, 84px); font-weight: 500; letter-spacing: -0.03em; line-height: 1.05; margin-top: 10px; }
  .of { font-size: .4em; color: var(--ink-3); letter-spacing: 0; margin-left: 4px; }
  .cat { font-size: 18px; color: var(--ink-2); }
  .cat strong { color: var(--ink); margin-left: 6px; font-weight: 600; }
  .scale { position: relative; margin: 20px 0 8px; }
  .bands { display: flex; gap: 3px; height: 10px; }
  .band { border-radius: 5px; opacity: .85; }
  .tone-good { background: var(--good); } .tone-warning { background: var(--warning); }
  .tone-serious { background: var(--serious); } .tone-critical { background: var(--critical); }
  .marker { position: absolute; top: -6px; width: 4px; height: 22px; border-radius: 2px; background: var(--ink); transform: translateX(-2px); box-shadow: 0 0 0 3px var(--surface); }
  .labels { display: flex; gap: 3px; margin-top: 8px; font-size: 13px; color: var(--ink-3); }
  .labels span.on { color: var(--ink); font-weight: 600; }
  .explain { color: var(--ink-2); font-size: 14.5px; margin-top: 8px; }
  .signals { list-style: none; margin: 16px 0 0; padding: 0; }
  .signals li { padding: 16px 0; border-top: 1px solid var(--line); }
  .signals p { color: var(--ink-2); margin-top: 2px; }
  .advice { list-style: none; margin: 20px 0 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px 48px; }
  .advice li { display: grid; grid-template-columns: 40px minmax(0, 1fr); gap: 12px; }
  .n { width: 32px; height: 32px; border-radius: 50%; background: var(--ink); color: var(--bg); display: grid; place-items: center; font-weight: 600; font-size: 15px; }
  .advice h3 { font-size: 18px; }
  .do { font-size: 17px; color: var(--ink); margin: 4px 0 6px; line-height: 1.6; }
  .next { list-style: none; margin: 16px 0 0; padding: 0; }
  .next li { display: flex; justify-content: space-between; gap: 16px; align-items: baseline; padding: 16px 0; border-top: 1px solid var(--line); font-size: 17px; }
  .disclaimer { margin-top: 40px; font-size: 13px; color: var(--ink-3); }
  .loading { padding: 40px 0; }
  @media (max-width: 860px) {
    .risks, .advice { grid-template-columns: 1fr; }
    .risk { padding: 24px; }
  }
  @media print {
    .no-print, :global(.site-header), :global(.site-footer), :global(.src-btn) { display: none !important; }
    .risk { break-inside: avoid; border-color: #bbb; }
    .advice li, .next li, .signals li { break-inside: avoid; }
  }
</style>
