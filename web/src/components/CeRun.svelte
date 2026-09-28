<script lang="ts">
  import { onMount } from "svelte";
  import Sources from "./Sources.svelte";
  import { api, type Fact } from "../lib/api";

  interface Rep { name: string; main_peak_bp: number; conc_ng_ul: number; qc_status: string; hmw_fraction: number; short_fraction: number; sizes_bp: number[]; rfu: number[] }
  interface Tube { tube: string; tube_label: string; average_size_bp: number; peak_cv_pct: number | null; mean_conc_ng_ul: number; conc_cv_pct: number | null;
    total_ng: number; external_score: { name: string; value: number; source: string; ruo: boolean } | null; replicates: Rep[]; qc_status: string }
  interface Run { id: string; sample_label: string; instrument: string; date: string; elution_ul: number; tubes: Tube[]; fact_ids: string[]; facts: Record<string, Fact> }

  const QC = { pass: ["good", "ผ่าน QC"], warning: ["warning", "ควรตรวจสอบ"], fail: ["critical", "พบ DNA ขนาดใหญ่"] } as Record<string, [string, string]>;
  let runs = $state<{ id: string; label: string }[]>([]);
  let run = $state<Run | null>(null);

  // QIAxcel-like log size axis 10–5000 bp
  const W = 360, H = 170, L = 8, R = 8, T = 14, B = 26;
  const lx = (bp: number) => L + (Math.log(bp / 10) / Math.log(5000 / 10)) * (W - L - R);
  const TICKS = [15, 100, 200, 300, 500, 1000, 3000];
  function path(rep: Rep, maxY: number) {
    return rep.sizes_bp.map((s, i) => `${i ? "L" : "M"}${lx(s).toFixed(1)},${(H - B - (rep.rfu[i] / maxY) * (H - B - T)).toFixed(1)}`).join("");
  }
  const peakY = (rep: Rep, maxY: number) => {
    let best = 0;
    rep.sizes_bp.forEach((s, i) => { if (Math.abs(s - rep.main_peak_bp) < Math.abs(rep.sizes_bp[best] - rep.main_peak_bp)) best = i; });
    return H - B - (rep.rfu[best] / maxY) * (H - B - T);
  };

  async function load(id: string) { run = await api<Run>(`/api/cfdna/runs/${id}`); }
  onMount(async () => { runs = await api<typeof runs>("/api/cfdna/runs"); if (runs.length) await load(runs[0].id); });
</script>

{#if run}
  <header class="rhead">
    <div>
      <h2 class="rtitle">{run.sample_label}</h2>
      <p class="muted small">{run.instrument} · {run.date} · elution {run.elution_ul} µl (อนุมานจากตัวเลขในสไลด์)</p>
    </div>
    {#if runs.length > 1}
      <select class="select" onchange={(e) => load((e.currentTarget as HTMLSelectElement).value)}>{#each runs as r}<option value={r.id}>{r.label}</option>{/each}</select>
    {/if}
  </header>

  {#each run.tubes as t (t.tube)}
    {@const maxY = Math.max(...t.replicates.flatMap((r) => r.rfu)) * 1.1}
    <section class="tube" aria-labelledby={`t-${t.tube}`}>
      <div class="summary">
        <h3 id={`t-${t.tube}`}>{t.tube_label}</h3>
        <dl>
          <div><dt>Ave size</dt><dd class="num">{t.average_size_bp} bp</dd><dd class="muted small">CV {t.peak_cv_pct ?? "–"}%</dd></div>
          <div><dt>Total concentration</dt><dd class="num">{t.total_ng} ng</dd><dd class="muted small">เฉลี่ย {t.mean_conc_ng_ul} ng/µl · CV {t.conc_cv_pct ?? "–"}%</dd></div>
          {#if t.external_score}
            <div><dt>{t.external_score.name}</dt><dd class="num">{t.external_score.value.toFixed(2)}</dd><dd class="muted small">{t.external_score.source} · RUO</dd></div>
          {/if}
          <div><dt>คุณภาพตัวอย่าง</dt><dd><span class="status {QC[t.qc_status][0]}">{QC[t.qc_status][1]}</span></dd></div>
        </dl>
      </div>
      <ul class="reps">
        {#each t.replicates as rep (rep.name)}
          <li>
            <p class="rep-head"><strong>Main peak = {rep.main_peak_bp} bp</strong><span>Conc. {rep.conc_ng_ul} ng/µl</span></p>
            <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${t.tube_label} ${rep.name}: main peak ${rep.main_peak_bp} bp, ${rep.conc_ng_ul} ng/µl${rep.qc_status === "fail" ? ", พบ DNA ขนาดใหญ่" : ""}`}>
              <rect x={lx(100)} y={T} width={lx(250) - lx(100)} height={H - B - T} class="smear" />
              {#each TICKS as tk}
                <line x1={lx(tk)} x2={lx(tk)} y1={T} y2={H - B} class="grid" />
                <text x={lx(tk)} y={H - 9} class="tick" text-anchor="middle">{tk}</text>
              {/each}
              <line x1={L} x2={W - R} y1={H - B} y2={H - B} class="axis" />
              <path d={path(rep, maxY)} class="trace" />
              <text x={lx(15) + 3} y={T + 8} class="mk">15 bp marker</text>
              <text x={lx(3000) - 3} y={T + 8} class="mk" text-anchor="end">3000 bp marker</text>
              <circle cx={lx(rep.main_peak_bp)} cy={peakY(rep, maxY)} r="3.5" class="pk" />
              <text x={lx(rep.main_peak_bp) + 6} y={peakY(rep, maxY) - 4} class="pkl">{rep.main_peak_bp} bp</text>
            </svg>
            <p class="rep-foot muted small">{rep.name} · DNA &gt; 700 bp {(rep.hmw_fraction * 100).toFixed(0)}%{rep.qc_status === "fail" ? " — อาจปนเปื้อน genomic DNA" : ""}</p>
          </li>
        {/each}
      </ul>
    </section>
  {/each}

  <p class="note">
    แถบฟ้า = ช่วง cfDNA 100–250 bp · marker 15/3000 bp ใช้จัดแนว ไม่นับเป็น DNA ของผู้ป่วย · Ave size = ค่าเฉลี่ย main peak · Total = conc. เฉลี่ย × elution ·
    คะแนนจากโมเดลวิจัยแสดงตามที่ได้รับ ระบบไม่แปลผลเป็นการวินิจฉัย — การวัดขนาด fragment ด้วย CE ยังไม่ใช่การคัดกรองมะเร็งที่ validate แล้ว ·
    <Sources ids={run.fact_ids} facts={run.facts} />
  </p>
{:else}
  <p class="muted">กำลังโหลด…</p>
{/if}

<style>
  .rhead { display: flex; justify-content: space-between; gap: 12px; align-items: flex-end; flex-wrap: wrap; margin-bottom: 8px; }
  .rtitle { font-size: 20px; font-weight: 600; letter-spacing: 0; text-transform: none; color: var(--ink); }
  .tube { border-top: 1px solid var(--line); padding: 28px 0; }
  .summary { display: flex; justify-content: space-between; gap: 16px 32px; flex-wrap: wrap; align-items: baseline; }
  .summary h3 { font-size: 18px; }
  dl { display: flex; flex-wrap: wrap; gap: 8px 32px; margin: 0; }
  dt { font-size: 13px; color: var(--ink-3); }
  dd { margin: 0; }
  dd.num { font-size: 22px; font-weight: 500; }
  .reps { list-style: none; margin: 18px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
  .reps li { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px; }
  .rep-head { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; font-size: 14px; margin-bottom: 4px; }
  svg { width: 100%; height: auto; display: block; }
  .smear { fill: color-mix(in srgb, #2a78d6 9%, transparent); }
  .grid { stroke: var(--line); stroke-width: 1; }
  .axis { stroke: var(--line-strong); }
  .tick, .mk { font-size: 9.5px; fill: var(--ink-3); font-family: var(--font); }
  .trace { fill: none; stroke: #2a78d6; stroke-width: 1.4; stroke-linejoin: round; }
  .pk { fill: #e0703f; stroke: var(--surface); stroke-width: 1.5; }
  .pkl { font-size: 10.5px; fill: var(--ink); font-family: var(--font); }
  .rep-foot { margin-top: 4px; }
  .note { font-size: 13px; color: var(--ink-3); margin-top: 12px; }
  @media (max-width: 860px) { .reps { grid-template-columns: 1fr; } }
</style>
