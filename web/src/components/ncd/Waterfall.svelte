<script lang="ts">
  // Exact explanation: baseline + signed contributions = patient score (in the score's own scale).
  // HTML rows (not SVG) so labels stay readable at any width.
  interface Contribution { feature: string; label: string; value: number | string | null; unit: string; contribution: number; direction: string; note: string; source: { document: string; locator: string } | null }
  let { contributions, scale, baselineLabel, finalLabel }: { contributions: Contribution[]; scale: string; baselineLabel: string; finalLabel: string } = $props();

  const SCALE_TH: Record<string, string> = { "log-hazard": "log-hazard", points: "คะแนน", criteria: "เกณฑ์", logit: "logit" };
  const rows = $derived(contributions.filter((c) => Math.abs(c.contribution) > 1e-9));
  const zero = $derived(contributions.filter((c) => Math.abs(c.contribution) <= 1e-9));
  const steps = $derived.by(() => {
    let acc = 0;
    return rows.map((c) => { const start = acc; acc += c.contribution; return { c, start, end: acc }; });
  });
  const extent = $derived.by(() => {
    const xs = [0, ...steps.flatMap((s) => [s.start, s.end])];
    return [Math.min(...xs), Math.max(...xs)] as const;
  });
  const pct = (v: number) => ((v - extent[0]) / ((extent[1] - extent[0]) || 1)) * 100;
  const fmt = (v: number) => (Math.abs(v) >= 10 ? v.toFixed(0) : Math.abs(v) >= 1 ? v.toFixed(1) : v.toFixed(2));
  let open = $state<number | null>(null);
</script>

{#if rows.length}
  <div class="wf" role="table" aria-label="ปัจจัยที่ผลักคะแนนความเสี่ยง">
    <div class="row base" role="row"><span class="lbl" role="rowheader">{baselineLabel}</span><span class="track" role="cell"><span class="zero" style={`left:${pct(0)}%`}></span></span><span class="val" role="cell"></span></div>
    {#each steps as s, i (s.c.feature)}
      {@const up = s.c.contribution > 0}
      <div class="row" role="row">
        <span class="lbl" role="rowheader">
          <button type="button" class="link-btn" aria-expanded={open === i} onclick={() => (open = open === i ? null : i)}>
            {s.c.label}{s.c.value != null && s.c.value !== "" ? ` (${s.c.value}${s.c.unit ? " " + s.c.unit : ""})` : ""}
          </button>
        </span>
        <span class="track" role="cell">
          <span class="zero" style={`left:${pct(0)}%`}></span>
          <span class="bar {up ? 'up' : 'down'}" style={`left:${Math.min(pct(s.start), pct(s.end))}%;width:${Math.max(0.8, Math.abs(pct(s.end) - pct(s.start)))}%`}></span>
        </span>
        <span class="val num" role="cell">{up ? "+" : "−"}{fmt(Math.abs(s.c.contribution))}<span class="sr-only">{up ? " เพิ่มความเสี่ยง" : " ลดความเสี่ยง"}</span></span>
      </div>
      {#if open === i}
        <p class="audit">{s.c.note}{#if s.c.source} · ที่มา: <span class="mono">{s.c.source.document} · {s.c.source.locator}</span>{/if}</p>
      {/if}
    {/each}
    <div class="row final" role="row"><span class="lbl" role="rowheader">{finalLabel}</span><span class="track" role="cell"></span><span class="val" role="cell"></span></div>
  </div>
  <p class="cap">หน่วย: {SCALE_TH[scale] ?? scale} เทียบกับคนอ้างอิง · ส้ม = ดันความเสี่ยงขึ้น · น้ำเงิน = ลดลง · ผลรวมเท่ากับคะแนนจริง (คำนวณตรงตัว ไม่ใช่ค่าประมาณ) · กดชื่อปัจจัยเพื่อดูที่มาของข้อมูล{#if zero.length}<br />ไม่มีผล: {zero.map((z) => z.label).join(", ")}{/if}</p>
{:else}
  <p class="muted small">ไม่มีปัจจัยที่เพิ่มหรือลดคะแนนจากค่าอ้างอิง</p>
{/if}

<style>
  .wf { display: grid; gap: 2px; }
  .row { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.4fr) 64px; gap: 12px; align-items: center; min-height: 34px; }
  .lbl { text-align: right; font-size: 14px; color: var(--ink-2); line-height: 1.3; }
  .lbl .link-btn { color: var(--ink-2); text-align: right; font-size: 14px; }
  .base .lbl, .final .lbl { color: var(--ink); }
  .final .lbl { font-weight: 600; }
  .track { position: relative; height: 18px; }
  .zero { position: absolute; top: -8px; bottom: -8px; width: 1px; background: var(--line-strong); }
  .bar { position: absolute; top: 2px; height: 14px; border-radius: 3px; }
  .up { background: #e0703f; }
  .down { background: #2a78d6; }
  .val { font-size: 13px; color: var(--ink-2); }
  .audit { font-size: 13.5px; background: var(--subtle); border-radius: 10px; padding: 8px 12px; margin: 2px 0 6px; }
  .mono { font-family: ui-monospace, monospace; font-size: 12.5px; }
  .cap { font-size: 12.5px; color: var(--ink-3); margin-top: 10px; }
  @media (max-width: 560px) {
    .row { grid-template-columns: minmax(0, 1fr) 56px; gap: 4px 10px; padding: 4px 0; }
    .lbl, .lbl .link-btn { text-align: left; }
    .track { grid-column: 1 / -1; grid-row: 2; }
    .base .track, .final .track { display: none; }
  }
</style>
