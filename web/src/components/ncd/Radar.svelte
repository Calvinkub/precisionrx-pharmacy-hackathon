<script lang="ts">
  // Metabolic phenotype: each spoke = position inside the population band (0 = P10, 1 = P90).
  interface Axis { id: string; abbr: string; value: number; unit: string; low: number; high: number; position: number }
  let { axes }: { axes: Axis[] } = $props();
  const R = 110, C = 150, MAXP = 1.8;
  const pt = (i: number, p: number) => {
    const a = -Math.PI / 2 + (i / axes.length) * Math.PI * 2;
    const r = (Math.max(-0.2, Math.min(MAXP, p)) + 0.2) / (MAXP + 0.2) * R;
    return [C + r * Math.cos(a), C + r * Math.sin(a)] as const;
  };
  const poly = (p: (i: number) => number) => axes.map((_, i) => pt(i, p(i)).join(",")).join(" ");
</script>

<figure class="radar">
  <svg viewBox="-35 -30 370 360" role="img" aria-label={`ตำแหน่งสาร metabolic เทียบช่วงประชากร: ${axes.map((a) => `${a.abbr} ${a.position > 1 ? "เหนือ P90" : a.position < 0 ? "ต่ำกว่า P10" : "ในช่วง"}`).join(", ")}`}>
    <polygon points={poly(() => 1)} class="band-hi" />
    <polygon points={poly(() => 0)} class="band-lo" />
    {#each axes as a, i (a.id)}
      {@const [ex, ey] = pt(i, MAXP)}
      {@const [lx, ly] = pt(i, MAXP + 0.75)}
      <line x1={C} y1={C} x2={ex} y2={ey} class="spoke" />
      <text x={lx} y={ly} class="lbl" text-anchor="middle" dominant-baseline="middle">{a.abbr}</text>
    {/each}
    <polygon points={poly((i) => axes[i].position)} class="shape" />
    {#each axes as a, i (a.id)}
      {@const [px, py] = pt(i, a.position)}
      <circle cx={px} cy={py} r="4" class:out={a.position > 1 || a.position < 0} class="dot"><title>{a.abbr} {a.value} {a.unit} (P10 {a.low} – P90 {a.high})</title></circle>
    {/each}
  </svg>
  <figcaption>วงในเส้นประ = P10 · วงเทาทึบ = P90 ของประชากร UK Biobank (ยังไม่ใช่ค่าคนไทย) · จุดส้ม = นอกช่วง</figcaption>
</figure>

<style>
  .radar { margin: 0; }
  svg { width: 100%; max-width: 360px; height: auto; display: block; margin: 0 auto; overflow: visible; }
  .band-hi { fill: var(--band); stroke: var(--line-strong); }
  .band-lo { fill: var(--bg); stroke: var(--line-strong); stroke-dasharray: 3 3; }
  .spoke { stroke: var(--line); }
  .lbl { font-size: 11px; fill: var(--ink-2); font-family: var(--font); }
  .shape { fill: color-mix(in srgb, #2a78d6 14%, transparent); stroke: #2a78d6; stroke-width: 2; stroke-linejoin: round; }
  .dot { fill: #2a78d6; stroke: var(--bg); stroke-width: 2; }
  .dot.out { fill: #e0703f; }
  figcaption { font-size: 12.5px; color: var(--ink-3); text-align: center; margin-top: 6px; }
</style>
