<script lang="ts">
  let { sizes, rfu, peak }: { sizes: number[]; rfu: number[]; peak: number } = $props();
  const W = 1000, H = 240, L = 20, B = 28, T = 10;
  // log-x like instrument software: 35–1500 bp
  const lx = (bp: number) => L + (Math.log(bp / 35) / Math.log(1500 / 35)) * (W - L - 8);
  const maxY = $derived(Math.max(...rfu) * 1.08 || 1);
  const y = (v: number) => H - B - (v / maxY) * (H - B - T);
  const path = $derived(sizes.map((s, i) => `${i ? "L" : "M"}${lx(s).toFixed(1)},${y(rfu[i]).toFixed(1)}`).join(""));
  const ticks = [50, 100, 167, 300, 500, 700, 1000, 1500];
</script>

<figure class="ep">
  <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Electropherogram ของ cfDNA จุดยอดหลักที่ ${peak.toFixed(0)} bp`}>
    <rect x={lx(100)} y={T} width={lx(250) - lx(100)} height={H - B - T} class="mono" />
    <rect x={lx(700)} y={T} width={lx(1500) - lx(700)} height={H - B - T} class="hmw" />
    <text x={(lx(100) + lx(250)) / 2} y={T + 12} class="rl" text-anchor="middle">cfDNA 100–250 bp</text>
    <text x={(lx(700) + lx(1500)) / 2} y={T + 12} class="rl" text-anchor="middle">gDNA &gt; 700 bp</text>
    <line x1={L} x2={W - 8} y1={H - B} y2={H - B} class="axis" />
    {#each ticks as t}
      <line x1={lx(t)} x2={lx(t)} y1={H - B} y2={H - B + 4} class="axis" />
      <text x={lx(t)} y={H - 8} class="tick" text-anchor="middle">{t}</text>
    {/each}
    <path d={path} class="trace" />
    <line x1={lx(peak)} x2={lx(peak)} y1={T + 16} y2={H - B} class="pk" />
    <text x={lx(peak) + 6} y={T + 48} class="tick">จุดยอด {peak.toFixed(0)} bp</text>
  </svg>
  <figcaption>ขนาด fragment (bp, สเกล log) · ข้อมูลจำลองจากเครื่อง capillary electrophoresis</figcaption>
</figure>

<style>
  .ep { margin: 0; }
  svg { width: 100%; height: auto; overflow: visible; }
  .mono { fill: color-mix(in srgb, #2a78d6 8%, transparent); }
  .hmw { fill: color-mix(in srgb, #e0703f 10%, transparent); }
  .rl, .tick { font-size: 13px; fill: var(--ink-3); font-family: var(--font); }
  .axis { stroke: var(--line-strong); }
  .trace { fill: none; stroke: var(--ink); stroke-width: 1.5; stroke-linejoin: round; }
  .pk { stroke: #2a78d6; stroke-width: 1.2; }
  figcaption { font-size: 12.5px; color: var(--ink-3); margin-top: 4px; }
</style>
