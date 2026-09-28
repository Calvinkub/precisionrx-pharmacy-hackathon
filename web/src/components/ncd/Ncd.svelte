<script lang="ts">
  import { onMount } from "svelte";
  import Sources from "../Sources.svelte";
  import Electropherogram from "./Electropherogram.svelte";
  import Radar from "./Radar.svelte";
  import Waterfall from "./Waterfall.svelte";
  import { api, postJson, type Fact } from "../../lib/api";

  interface Risk { id: string; disease: string; method: string; value: number | null; display: string; unit: string; category: string; category_label: string;
    scale: string; baseline: number | null; contributions: any[]; interval: [number, number] | null; fact_ids: string[]; notes: string[]; missing: string[] }
  interface Plan { id: string; category: string; title: string; detail: string; interval_weeks: number; rationale: string; fact_ids: string[]; selected: boolean }
  interface Run {
    patient_id: string; execution_status: Record<string, string>; risk_vectors: Risk[];
    normalized_json: any; raw_data: any; retrieved_evidence: any[]; tool_outputs: any[];
    agent_messages: { agent: string; content: string }[];
    intermediate_features: { plan: string[]; plan_source: string; phenotype: any[]; flags: any[]; cfdna?: any; care_plan: Plan[]; features: any };
    summary: { mode: string; llm_status: string; sentences: { text: string; fact_ids: string[] }[]; dropped_unsupported: number };
    facts: Record<string, Fact>;
  }

  const TONE: Record<string, string> = { low: "good", moderate: "warning", high: "serious", very_high: "critical", present: "serious", at_risk: "warning",
    absent: "good", not_assessable: "", not_applicable: "info" };
  const NODES = ["orchestrator", "data_extraction", "risk_scoring", "clinical_reasoning", "cfdna_qc", "guideline_lookup", "care_plan", "summarizer"];
  const NODE_TH: Record<string, string> = { orchestrator: "วางแผน", data_extraction: "ดึง/ปรับมาตรฐานข้อมูล", risk_scoring: "คำนวณความเสี่ยง",
    clinical_reasoning: "วิเคราะห์ข้าม modality", cfdna_qc: "cfDNA QC", guideline_lookup: "ค้น guideline", care_plan: "เสนอแผนดูแล", summarizer: "สรุป + ตรวจหลักฐาน" };
  const CAT_ICON: Record<string, string> = { nutrition: "โภชนาการ", exercise: "ออกกำลังกาย", lab: "ตรวจแล็บ", imaging: "ตรวจภาพ", medication: "ยา" };

  let patients = $state<{ id: string; sex: string; age: number; sources: string[]; conditions: string[] }[]>([]);
  let pid = $state("");
  let r = $state<Run | null>(null);
  let busy = $state(false);
  let error = $state("");
  let selected = $state("cvd");
  let plan = $state<Plan[]>([]);
  let approver = $state("");
  let note = $state("");
  let exported = $state<any>(null);
  let exportErr = $state("");
  let live = $state<Record<string, string>>({});
  let traceOpen = $state(false);

  const risk = $derived(r?.risk_vectors.find((x) => x.id === selected));
  const demo = $derived(r?.normalized_json.demographics);
  const issues = $derived(r ? r.normalized_json.issues.filter((i: any) => i.severity !== "info") : []);

  async function runPipeline(id: string) {
    pid = id; busy = true; error = ""; exported = null; live = {};
    const u = new URL(location.href); u.searchParams.set("patient", id); history.replaceState(null, "", u);
    // live progress over WebSocket when the host supports it; the REST call is the source of truth
    try {
      const ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/v2/patients/${id}/run`);
      ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.node && m.node !== "__end__") live = { ...live, [m.node]: "done" }; };
      ws.onerror = () => ws.close();
    } catch { /* no websocket (e.g. serverless) */ }
    try {
      r = await postJson<Run>(`/api/v2/patients/${id}/run`, {});
      plan = r.intermediate_features.care_plan.map((p) => ({ ...p }));
      selected = r.risk_vectors.find((v) => v.contributions.some((c: any) => Math.abs(c.contribution) > 1e-9))?.id ?? "cvd";
    } catch (e) { error = (e as Error).message; } finally { busy = false; }
  }

  async function approve() {
    exportErr = "";
    try { exported = await postJson("/api/v2/careplan/export", { patient_id: pid, items: plan, approver, note }); }
    catch (e) { exportErr = (e as Error).message.includes("approver") ? "กรุณาใส่ชื่อผู้อนุมัติ" : "เลือกอย่างน้อย 1 รายการ"; }
  }
  function download() {
    const blob = new Blob([JSON.stringify(exported, null, 2)], { type: "application/fhir+json" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `careplan-${pid}.json`; a.click();
    URL.revokeObjectURL(a.href);
  }

  onMount(async () => {
    patients = await api<typeof patients>("/api/v2/patients");
    const q = new URLSearchParams(location.search).get("patient");
    await runPipeline(patients.some((p) => p.id === q) ? q! : patients[0].id);
  });
  const fmtIv = (iv: [number, number] | null, unit: string) => (iv ? `ช่วง 95%: ${iv[0]}–${iv[1]}${unit.startsWith("%") ? "%" : ""}` : "");
</script>

<div class="picker">
  <div class="segmented" role="group" aria-label="เลือกผู้ป่วย">
    {#each patients as p (p.id)}
      <button type="button" aria-pressed={pid === p.id} onclick={() => runPipeline(p.id)}>{p.id} · {p.sex === "female" ? "หญิง" : "ชาย"} {p.age}</button>
    {/each}
  </div>
  <button type="button" class="link-btn" onclick={() => (traceOpen = !traceOpen)} aria-expanded={traceOpen}>{traceOpen ? "ซ่อน" : "ดู"}การทำงานของ agent</button>
</div>

{#if busy}
  <ol class="progress" aria-live="polite">
    {#each NODES as n}<li class:done={live[n]}>{NODE_TH[n]}</li>{/each}
  </ol>
{/if}
{#if error}<p class="error" role="alert">{error}</p>{/if}

{#if r && demo}
  <section class="head" aria-busy={busy}>
    <p class="muted small">{r.patient_id} · {demo.age} ปี · {demo.sex === "female" ? "หญิง" : "ชาย"} · BMI {(demo.weight_kg / (demo.height_cm / 100) ** 2).toFixed(1)} · ความดัน {demo.sbp}/{demo.dbp}{demo.smoker ? " · สูบบุหรี่" : ""}</p>
    <h2 class="title">ภาพรวมความเสี่ยงโรค NCDs</h2>
    <ul class="sources" aria-label="แหล่งข้อมูล">
      {#each r.normalized_json.sources as s}<li>{s}</li>{/each}
    </ul>
    {#if issues.length}<p class="issues">ข้อมูลที่ต้องดู: {issues.map((i: any) => i.detail).join(" · ")}</p>{/if}
  </section>

  {#if traceOpen}
    <section class="section trace" aria-labelledby="h-trace">
      <h2 id="h-trace">การทำงานของ agent (LangGraph)</h2>
      <p class="muted small">แผน: {r.intermediate_features.plan_source === "llm" ? "Claude เลือกลำดับ" : "ลำดับมาตรฐาน"} · สรุป: {r.summary.mode === "llm" ? "Claude" : "template"} ({r.summary.llm_status})</p>
      <ol class="nodes">
        {#each r.agent_messages as m, i (i)}
          <li><span class="status {r.execution_status[m.agent] === 'done' ? 'good' : ''}">{NODE_TH[m.agent] ?? m.agent}</span><p>{m.content}</p></li>
        {/each}
      </ol>
      <details><summary class="link-btn">การเรียก tool {r.tool_outputs.length} ครั้ง</summary>
        <ul class="tools">{#each r.tool_outputs as t, i (i)}<li><code>{t.tool}</code> {JSON.stringify(t.args)} → {JSON.stringify(t.output).slice(0, 120)}</li>{/each}</ul>
      </details>
      <details><summary class="link-btn">หลักฐานที่ค้นได้ {r.retrieved_evidence.length} ชิ้น</summary>
        <ul class="tools">{#each r.retrieved_evidence as e, i (i)}<li><code>{e.fact_id}</code> {e.score ?? "cited"} · {e.source}</li>{/each}</ul>
      </details>
    </section>
  {/if}

  <section class="section summary" aria-labelledby="h-sum">
    <div class="section-head"><h2 id="h-sum">สรุปสำหรับแพทย์</h2><span class="muted small">{r.summary.mode === "llm" ? "เรียบเรียงโดย Claude" : "สรุปจากกฎ"} · ทุกประโยคผ่านตัวตรวจหลักฐาน</span></div>
    <ul class="sentences">
      {#each r.summary.sentences as s, i (i)}<li><p>{s.text}</p><Sources ids={s.fact_ids} facts={r.facts} /></li>{/each}
    </ul>
  </section>

  <section class="section" aria-labelledby="h-risk">
    <div class="section-head"><h2 id="h-risk">Disease risk vector</h2><span class="muted small">เลือกโรคเพื่อดูว่าปัจจัยไหนผลักความเสี่ยง</span></div>
    <div class="risks" role="tablist" aria-label="เลือกโรค">
      {#each r.risk_vectors as v (v.id)}
        <button type="button" role="tab" aria-selected={selected === v.id} class="risk" onclick={() => (selected = v.id)}>
          <span class="rname">{v.disease}</span>
          <span class="rval num">{v.display}</span>
          <span class="status {TONE[v.category] ?? ''}">{v.category_label}</span>
          <span class="rmeta">{v.method}{v.interval ? ` · ${fmtIv(v.interval, v.unit)}` : ""}</span>
        </button>
      {/each}
    </div>
    {#if risk}
      <div class="detail" role="tabpanel">
        <div class="d-head">
          <h3>{risk.disease} — {risk.display}</h3>
          <Sources ids={risk.fact_ids} facts={r.facts} />
        </div>
        {#if risk.scale === "inputs"}
          <table class="inputs"><tbody>
            {#each risk.contributions as c (c.feature)}
              <tr><th scope="row">{c.label}</th><td class="num">{c.value} {c.unit}</td><td class="muted small">{c.note}{c.source ? ` · ${c.source.document} ${c.source.locator}` : ""}</td></tr>
            {/each}
          </tbody></table>
          <p class="muted small">eGFR เป็นสูตรยกกำลัง ไม่แยกเป็นผลบวกได้ จึงแสดงค่าที่ใช้คำนวณพร้อมที่มา</p>
        {:else}
          <Waterfall contributions={risk.contributions} scale={risk.scale}
            baselineLabel={risk.baseline != null ? `คนอ้างอิง ${risk.baseline}${risk.unit.startsWith("%") ? "%" : ""}` : "เริ่มที่ 0"}
            finalLabel={`ผู้ป่วยนี้ ${risk.display}`} />
        {/if}
        {#if risk.notes.length}<ul class="notes">{#each risk.notes as n}<li>{n}</li>{/each}</ul>{/if}
      </div>
    {/if}
  </section>

  <section class="section" aria-labelledby="h-pheno">
    <div class="section-head"><h2 id="h-pheno">Metabolic phenotype (NMR)</h2><span class="muted small">{r.raw_data.n_metabolites} ค่าจาก NMR · ตีความได้ {r.raw_data.n_interpreted_metabolites} ค่า</span></div>
    <div class="pheno">
      <Radar axes={r.intermediate_features.phenotype} />
      <ul class="flags">
        {#each r.intermediate_features.flags.filter((f) => f.kind !== "data") as f (f.id)}
          <li><div class="f-top"><h3>{f.title}</h3><span class="status {f.severity === 'action' ? 'serious' : f.severity === 'monitor' ? 'warning' : 'info'}">{f.kind}</span></div>
            <p>{f.detail}</p>{#if f.fact_ids.length}<Sources ids={f.fact_ids} facts={r.facts} />{/if}</li>
        {/each}
      </ul>
    </div>
  </section>

  {#if r.intermediate_features.cfdna}
    {@const q = r.intermediate_features.cfdna}
    <section class="section" aria-labelledby="h-cf">
      <div class="section-head"><h2 id="h-cf">cfDNA · คุณภาพตัวอย่าง</h2>
        <span class="status {q.status === 'pass' ? 'good' : q.status === 'warning' ? 'warning' : 'critical'}">{q.status === "pass" ? "ผ่าน QC" : q.status === "warning" ? "ควรตรวจสอบ" : "ไม่ผ่าน QC"}</span></div>
      <Electropherogram sizes={q.trace.sizes_bp} rfu={q.trace.rfu} peak={q.main_peak_bp} />
      <dl class="qc">
        <div><dt>จุดยอดหลัก</dt><dd class="num">{q.main_peak_bp.toFixed(0)} bp</dd></div>
        <div><dt>สัดส่วน cfDNA (100–250 bp)</dt><dd class="num">{(q.mono_fraction * 100).toFixed(0)}%</dd></div>
        <div><dt>DNA ขนาดใหญ่ (&gt; 700 bp)</dt><dd class="num">{(q.hmw_fraction * 100).toFixed(0)}%</dd></div>
        <div><dt>fragment สั้น 90–150 bp (RUO)</dt><dd class="num">{(q.short_fraction * 100).toFixed(0)}%</dd></div>
      </dl>
      <ul class="flags">
        {#each q.findings as f (f.id)}<li><h3>{f.title}</h3><p>{f.detail}</p><Sources ids={f.fact_ids} facts={r.facts} /></li>{/each}
      </ul>
    </section>
  {/if}

  <section class="section" aria-labelledby="h-plan">
    <div class="section-head"><h2 id="h-plan">แผนดูแล (แพทย์แก้ไขและอนุมัติ)</h2><span class="muted small">ระบบเสนอ แพทย์ตัดสินใจ</span></div>
    <ul class="plan">
      {#each plan as p, i (p.id)}
        <li class:off={!p.selected}>
          <label class="check"><input type="checkbox" bind:checked={p.selected} /><span class="sr-only">เลือก {p.title}</span></label>
          <div class="p-body">
            <p class="cat muted small">{CAT_ICON[p.category] ?? p.category}</p>
            <label class="field"><span class="sr-only">หัวข้อ</span><input class="input title-in" bind:value={p.title} /></label>
            <label class="field"><span class="sr-only">รายละเอียด</span><textarea class="input" rows="2" bind:value={p.detail}></textarea></label>
            <p class="muted small">เหตุผล: {p.rationale} · <Sources ids={p.fact_ids} facts={r.facts} /></p>
          </div>
          <label class="field iv">ติดตามใน
            <select class="select" bind:value={p.interval_weeks}>
              {#each [2, 4, 6, 8, 12, 24, 52] as w}<option value={w}>{w} สัปดาห์</option>{/each}
            </select>
          </label>
        </li>
      {/each}
    </ul>
    <div class="approve">
      <label class="field">ผู้อนุมัติ<input class="input" bind:value={approver} placeholder="ชื่อแพทย์ / เภสัชกร" /></label>
      <label class="field grow">หมายเหตุ<input class="input" bind:value={note} /></label>
      <button type="button" class="btn btn-primary" onclick={approve}>อนุมัติและส่งออก (FHIR)</button>
    </div>
    {#if exportErr}<p class="error" role="alert">{exportErr}</p>{/if}
    {#if exported}
      <div class="exported" role="status">
        <p><strong>อนุมัติแล้ว</strong> · CarePlan + ServiceRequest {exported.entry.length - 1} รายการ · {exported.meta.tag[0].display}</p>
        <div class="row"><button type="button" class="btn btn-sm" onclick={download}>ดาวน์โหลด FHIR Bundle</button></div>
        <details><summary class="link-btn">ดู JSON</summary><pre>{JSON.stringify(exported, null, 2)}</pre></details>
      </div>
    {/if}
  </section>
{/if}

<style>
  .picker { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
  .progress { list-style: none; display: flex; flex-wrap: wrap; gap: 8px 16px; padding: 0; margin: 20px 0 0; font-size: 13.5px; color: var(--ink-3); }
  .progress li::before { content: "○ "; }
  .progress li.done { color: var(--ink); }
  .progress li.done::before { content: "● "; color: var(--good); }
  .error { color: var(--critical); margin-top: 12px; }
  .head { padding: 28px 0 32px; }
  .title { font-size: clamp(26px, 3.2vw, 36px); font-weight: 600; letter-spacing: -0.015em; text-transform: none; color: var(--ink); margin-top: 6px; }
  .sources { list-style: none; display: flex; flex-wrap: wrap; gap: 6px; padding: 0; margin: 14px 0 0; }
  .sources li { font-size: 12.5px; color: var(--ink-2); background: var(--subtle); border-radius: 999px; padding: 3px 10px; }
  .issues { margin-top: 10px; font-size: 13.5px; color: var(--ink-2); }
  .trace .nodes { list-style: none; padding: 0; margin: 12px 0; }
  .trace .nodes li { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 12px; padding: 8px 0; border-top: 1px solid var(--line); font-size: 14px; }
  .tools { font-size: 12.5px; color: var(--ink-2); overflow-wrap: anywhere; }
  .sentences { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }
  .sentences p { font-size: 18px; line-height: 1.55; }
  .risks { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
  .risk { display: grid; gap: 4px; align-content: start; text-align: left; padding: 16px 14px; border: 0; border-right: 1px solid var(--line); background: none; font: inherit; color: var(--ink); cursor: pointer; }
  .risk:last-child { border-right: 0; }
  .risk:hover { background: var(--subtle); }
  .risk[aria-selected="true"] { background: var(--surface); box-shadow: inset 0 -3px 0 var(--ink); }
  .rname { font-size: 13.5px; color: var(--ink-3); }
  .rval { font-size: 24px; font-weight: 500; letter-spacing: -0.01em; }
  .rmeta { font-size: 12px; color: var(--ink-3); }
  .detail { padding: 24px 0 0; }
  .d-head { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; margin-bottom: 12px; flex-wrap: wrap; }
  .inputs th { font-weight: 500; color: var(--ink); border-bottom: 1px solid var(--line); }
  .notes { margin: 12px 0 0; padding-left: 18px; color: var(--ink-2); font-size: 14px; }
  .pheno { display: grid; grid-template-columns: minmax(0, 360px) minmax(0, 1fr); gap: 32px; align-items: start; }
  .flags { list-style: none; margin: 0; padding: 0; }
  .flags li { padding: 14px 0; border-top: 1px solid var(--line); }
  .flags p { color: var(--ink-2); font-size: 14.5px; margin-top: 2px; }
  .f-top { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }
  .qc { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 16px 0 0; }
  .qc div { padding-right: 16px; }
  .qc dt { font-size: 13px; color: var(--ink-3); }
  .qc dd { margin: 0; font-size: 22px; font-weight: 500; }
  .plan { list-style: none; margin: 0; padding: 0; }
  .plan li { display: grid; grid-template-columns: 32px minmax(0, 1fr) 160px; gap: 12px 16px; padding: 18px 0; border-top: 1px solid var(--line); align-items: start; }
  .plan li.off .title-in { text-decoration: line-through; color: var(--ink-3); }
  .plan li.off textarea { color: var(--ink-3); }
  .p-body { display: grid; gap: 6px; }
  .title-in { font-weight: 600; }
  textarea.input { resize: vertical; min-height: 60px; }
  .approve { display: flex; gap: 12px; align-items: end; flex-wrap: wrap; margin-top: 20px; }
  .approve .grow { flex: 1; min-width: 200px; }
  .exported { margin-top: 16px; padding: 16px 18px; border-radius: var(--radius); background: var(--subtle); }
  .exported .row { margin: 10px 0; }
  pre { max-height: 320px; overflow: auto; font-size: 12px; background: var(--surface); padding: 12px; border-radius: 10px; }
  @media (max-width: 960px) {
    .risks { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .risk { border-bottom: 1px solid var(--line); }
    .pheno { grid-template-columns: 1fr; }
    .qc { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 12px; }
    .plan li { grid-template-columns: 32px minmax(0, 1fr); }
    .iv { grid-column: 2; }
    .trace .nodes li { grid-template-columns: 1fr; }
  }
</style>
