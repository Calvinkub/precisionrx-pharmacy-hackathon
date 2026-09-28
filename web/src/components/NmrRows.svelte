<script lang="ts">
  import { fmt, type NmrDomain } from "../lib/api";

  let { domains }: { domains: NmrDomain[] } = $props();

  const TREND: Record<string, string> = {
    improved: "ดีขึ้น", worsened: "แย่ลง", within_variation: "เท่าเดิม", changed: "เปลี่ยน", not_assessable: "ยังบอกไม่ได้",
  };
  const W = 200, H = 24, Y = 12, PAD = 6;
  function x(d: NmrDomain, v: number) {
    const k = d.key!;
    const max = Math.max((k.ref_high ?? k.value) * 1.5, k.value * 1.12, (k.previous ?? 0) * 1.12, (k.target ?? 0) * 1.3) || 1;
    return PAD + Math.min(1, Math.max(0, v / max)) * (W - PAD * 2);
  }
  // headline without the trend clause — the trend column carries it
  const lead = (h: string) => h.split(" · เทียบครั้งก่อน")[0];
</script>

<ul class="rows">
  {#each domains as d (d.id)}
    {@const k = d.key}
    <li class="row">
      <div class="what">
        <h3>{d.title}</h3>
        <p>{lead(d.headline)}{d.out_of_range.filter((a) => a !== k?.abbr).length ? ` · ค่าอื่นที่ควรดู: ${d.out_of_range.filter((a) => a !== k?.abbr).join(", ")}` : ""}</p>
        {#if d.drug_note}<p class="drug"><span class="pill">ยา</span>{d.drug_note}</p>{/if}
      </div>
      {#if k}
        <p class="value"><span class="num">{fmt(k.value)}</span> <span class="unit">{k.unit}</span><span class="abbr">{k.abbr}</span></p>
        <svg class="gauge" viewBox={`0 0 ${W} ${H}`} aria-hidden="true">
          <line x1={PAD} x2={W - PAD} y1={Y} y2={Y} class="track" />
          {#if k.ref_low != null || k.ref_high != null}
            <rect x={x(d, k.ref_low ?? 0)} y={Y - 4} height="8" rx="4"
                  width={Math.max(2, x(d, k.ref_high ?? k.value) - x(d, k.ref_low ?? 0))} class="band" />
          {/if}
          {#if k.target != null}<line x1={x(d, k.target)} x2={x(d, k.target)} y1={Y - 8} y2={Y + 8} class="target" />{/if}
          {#if k.previous != null}<circle cx={x(d, k.previous)} cy={Y} r="3.5" class="prev" />{/if}
          <circle cx={x(d, k.value)} cy={Y} r="5" class="now st-{d.status}" />
        </svg>
        <p class="trend">
          {#if k.verdict}
            {@const real = k.verdict === "improved" || k.verdict === "worsened" || k.verdict === "changed"}
            <span class="arrow" aria-hidden="true">{real && k.pct_change != null ? (k.pct_change < 0 ? "↓" : "↑") : "–"}</span>
            {TREND[k.verdict]}{#if real && k.pct_change != null}&nbsp;<span class="muted num">{k.pct_change > 0 ? "+" : ""}{k.pct_change.toFixed(0)}%</span>{/if}
          {:else}
            <span class="muted">ครั้งแรก</span>
          {/if}
        </p>
      {:else}
        <p class="value muted">–</p><span></span><span></span>
      {/if}
      <span class="status {d.status === 'none' ? '' : d.status}">{d.status_label}</span>
      <span class="sr-only">
        {k ? `ช่วงปกติ ${k.ref_low ?? 0} ถึง ${k.ref_high ?? "ไม่ระบุ"}${k.target != null ? `, เป้า ${k.target}` : ""}${k.previous != null ? `, ครั้งก่อน ${fmt(k.previous)}` : ""}` : ""}
      </span>
    </li>
  {/each}
</ul>
<p class="legend muted" aria-hidden="true">
  <span><i class="lg band"></i>ช่วงปกติ</span><span><i class="lg tgt"></i>เป้าหมาย</span><span><i class="lg prev"></i>ครั้งก่อน</span><span><i class="lg now"></i>ครั้งนี้</span>
</p>

<style>
  .rows { list-style: none; margin: 0; padding: 0; }
  .row {
    display: grid; grid-template-columns: minmax(0, 1fr) 150px 180px 130px 120px; gap: 20px; align-items: center;
    padding: 18px 0; border-bottom: 1px solid var(--line);
  }
  .row:first-child { border-top: 1px solid var(--line); }
  .what p { font-size: 14px; color: var(--ink-3); margin-top: 2px; }
  .what .drug { color: var(--ink-2); display: flex; gap: 8px; align-items: baseline; }
  .pill { font-size: 11.5px; font-weight: 600; padding: 1px 8px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); flex: none; }
  .value { text-align: right; white-space: nowrap; }
  .value .num { font-size: 22px; font-weight: 500; letter-spacing: -0.01em; }
  .unit { font-size: 13px; color: var(--ink-3); }
  .abbr { display: block; font-size: 12.5px; color: var(--ink-3); }
  .gauge { width: 100%; height: auto; overflow: visible; }
  .track { stroke: var(--line-strong); stroke-width: 1; }
  .band { fill: var(--band); }
  .target { stroke: var(--ink-2); stroke-width: 1.5; }
  .prev { fill: var(--bg); stroke: var(--ink-3); stroke-width: 1.5; }
  .now { fill: var(--ink); stroke: var(--bg); stroke-width: 2; }
  .now.st-good { fill: var(--good); } .now.st-warning { fill: var(--warning); } .now.st-serious { fill: var(--serious); }
  .trend { font-size: 14px; white-space: nowrap; }
  .arrow { display: inline-block; width: 14px; color: var(--ink-3); }
  .legend { display: flex; flex-wrap: wrap; gap: 18px; font-size: 13px; margin-top: 14px; }
  .legend span { display: inline-flex; align-items: center; gap: 7px; }
  .lg { display: inline-block; }
  .lg.band { width: 18px; height: 8px; border-radius: 4px; background: var(--band); }
  .lg.tgt { width: 1.5px; height: 14px; background: var(--ink-2); }
  .lg.prev { width: 8px; height: 8px; border-radius: 50%; border: 1.5px solid var(--ink-3); }
  .lg.now { width: 10px; height: 10px; border-radius: 50%; background: var(--ink); }
  @media (max-width: 900px) {
    .row { grid-template-columns: minmax(0, 1fr) auto; gap: 8px 16px; }
    .what { grid-column: 1 / -1; }
    .value { text-align: left; }
    .gauge { grid-column: 1 / -1; grid-row: 3; max-width: 360px; }
    .trend { grid-column: 1; }
    .status { grid-column: 2; grid-row: 2; justify-self: end; }
  }
</style>
