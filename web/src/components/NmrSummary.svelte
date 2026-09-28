<script lang="ts">
  import { fmt, type NmrDomain } from "../lib/api";

  let { domains }: { domains: NmrDomain[] } = $props();

  const ICON: Record<string, string> = { good: "✓", warning: "!", serious: "⚠", none: "–" };
  const counts = $derived({
    serious: domains.filter((d) => d.status === "serious").length,
    warning: domains.filter((d) => d.status === "warning").length,
    good: domains.filter((d) => d.status === "good").length,
  });

  const W = 300, H = 44, PAD = 10, Y = 22;
  function scale(d: NmrDomain) {
    const k = d.key!;
    const max = Math.max((k.ref_high ?? k.value) * 1.5, k.value * 1.12, (k.previous ?? 0) * 1.12, (k.target ?? 0) * 1.3) || 1;
    return (v: number) => PAD + Math.min(1, Math.max(0, v / max)) * (W - PAD * 2);
  }
</script>

<div class="overview" aria-label="ภาพรวมผล NMR">
  {#if counts.serious}<span class="chip serious"><span aria-hidden="true">⚠</span>ควรดูแล {counts.serious}</span>{/if}
  {#if counts.warning}<span class="chip warning"><span aria-hidden="true">!</span>ควรติดตาม {counts.warning}</span>{/if}
  <span class="chip good"><span aria-hidden="true">✓</span>อยู่ในเกณฑ์ {counts.good}</span>
  <span class="muted">จาก {domains.length} หัวข้อสุขภาพ</span>
</div>

<ul class="tiles">
  {#each domains as d (d.id)}
    <li class="tile st-{d.status}">
      <div class="top">
        <h3>{d.title}</h3>
        <span class="chip {d.status === 'none' ? '' : d.status}"><span aria-hidden="true">{ICON[d.status]}</span>{d.status_label}</span>
      </div>
      {#if d.key}
        {@const k = d.key}
        {@const x = scale(d)}
        <p class="value"><span class="big">{fmt(k.value)}</span> <span class="unit">{k.unit}</span> <span class="abbr">{k.abbr}</span></p>
        <svg viewBox={`0 0 ${W} ${H}`} class="gauge" aria-hidden="true">
          <line x1={PAD} x2={W - PAD} y1={Y} y2={Y} class="track" />
          {#if k.ref_low != null || k.ref_high != null}
            <rect x={x(k.ref_low ?? 0)} width={Math.max(2, x(k.ref_high ?? k.value * 1.12) - x(k.ref_low ?? 0))} y={Y - 7} height="14" rx="4" class="band" />
          {/if}
          {#if k.target != null}
            <line x1={x(k.target)} x2={x(k.target)} y1={Y - 12} y2={Y + 12} class="target" />
          {/if}
          {#if k.previous != null && Math.abs(x(k.previous) - x(k.value)) > 12}
            <line x1={x(k.previous)} x2={x(k.value) + (k.value > k.previous ? -9 : 9)} y1={Y} y2={Y} class="arrow" />
            <path d={k.value > k.previous ? `M${x(k.value) - 9} ${Y - 4} L${x(k.value) - 5} ${Y} L${x(k.value) - 9} ${Y + 4}` : `M${x(k.value) + 9} ${Y - 4} L${x(k.value) + 5} ${Y} L${x(k.value) + 9} ${Y + 4}`} class="arrowhead" />
          {/if}
          {#if k.previous != null}<circle cx={x(k.previous)} cy={Y} r="5" class="prev" />{/if}
          <circle cx={x(k.value)} cy={Y} r="7" class="now" />
        </svg>
        <div class="axis" aria-hidden="true">
          <span>ช่วงปกติ {k.ref_low != null ? fmt(k.ref_low) : "0"}–{k.ref_high != null ? fmt(k.ref_high) : "?"}</span>
          {#if k.target != null}<span>│ เป้า {fmt(k.target)}</span>{/if}
          {#if k.previous != null}<span>○ ครั้งก่อน {fmt(k.previous)}</span>{/if}
        </div>
      {/if}
      <p class="headline">{d.headline}</p>
      {#if d.out_of_range.filter((a) => a !== d.key?.abbr).length}
        <p class="others">ค่าอื่นนอกช่วง: {d.out_of_range.filter((a) => a !== d.key?.abbr).join(", ")}</p>
      {/if}
      <p class="what">{d.what}</p>
    </li>
  {/each}
</ul>

<style>
  .overview { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 16px 0 12px; }
  .overview .chip { font-size: 13px; padding: 5px 12px; }
  .tiles { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .tile { border: 1px solid var(--border); border-radius: 14px; padding: 14px 16px; background: var(--raised); border-top: 4px solid var(--border-strong); display: grid; gap: 6px; align-content: start; }
  .st-good { border-top-color: var(--good); }
  .st-warning { border-top-color: var(--warning); }
  .st-serious { border-top-color: var(--serious); }
  .top { display: flex; justify-content: space-between; gap: 8px; align-items: flex-start; }
  h3 { font-size: 15px; }
  .value { line-height: 1.1; margin-top: 2px; }
  .big { font-size: 26px; font-weight: 600; }
  .unit { font-size: 13px; color: var(--ink-2); }
  .abbr { font-size: 12px; color: var(--ink-3); margin-left: 4px; }
  .gauge { width: 100%; height: auto; max-height: 64px; display: block; overflow: visible; }
  .track { stroke: var(--grid); stroke-width: 2; }
  .band { fill: var(--band); }
  .target { stroke: var(--ink-2); stroke-width: 2; }
  .arrow { stroke: var(--ink-3); stroke-width: 2; stroke-linecap: round; }
  .arrowhead { fill: none; stroke: var(--ink-3); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  .prev { fill: var(--raised); stroke: var(--ink-2); stroke-width: 2; }
  .now { fill: var(--ink); stroke: var(--raised); stroke-width: 2; }
  .st-good .now { fill: var(--good); }
  .st-warning .now { fill: var(--warning); }
  .st-serious .now { fill: var(--serious); }
  .axis { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11.5px; color: var(--ink-3); font-family: var(--mono); }
  .headline { font-size: 14px; font-weight: 500; margin-top: 4px; }
  .others { font-size: 12.5px; color: var(--ink-2); }
  .what { font-size: 12.5px; color: var(--ink-3); }
  @media (max-width: 640px) { .tiles { grid-template-columns: 1fr; } }
</style>
