<script lang="ts">
  import type { Analyte } from "../lib/api";

  // Illustrative ¹H NMR spectrum drawn from the lab's quantified values. The system never processes raw spectra.
  let { values, byId, height = 200 }: { values: Record<string, number>; byId: Record<string, Analyte>; height?: number } = $props();

  // [ppm, half-width, height] per analyte; heights scale with value / reference midpoint
  const PEAKS: Record<string, [number, number, number][]> = {
    tg: [[0.87, 0.05, 1.3], [1.27, 0.06, 2.4], [2.02, 0.035, 0.35], [5.3, 0.04, 0.35]],
    total_c: [[0.7, 0.03, 0.35], [0.87, 0.04, 0.5], [1.2, 0.05, 0.6]],
    glyca: [[2.03, 0.012, 0.9]],
    lactate: [[1.32, 0.005, 1.0], [1.34, 0.005, 1.0], [4.11, 0.008, 0.25]],
    glucose: [[3.24, 0.008, 0.45], [3.41, 0.01, 0.55], [3.47, 0.01, 0.6], [3.53, 0.008, 0.45], [3.72, 0.012, 0.65], [3.84, 0.012, 0.6], [3.89, 0.01, 0.5], [5.23, 0.006, 0.3]],
    creatinine: [[3.04, 0.006, 0.55], [4.05, 0.006, 0.4]],
    citrate: [[2.53, 0.006, 0.35], [2.67, 0.006, 0.35]],
    valine: [[0.99, 0.005, 0.4], [1.04, 0.005, 0.4]],
    leucine: [[0.96, 0.006, 0.45]],
    isoleucine: [[0.94, 0.005, 0.25], [1.01, 0.005, 0.3]],
    alanine: [[1.48, 0.005, 0.55]],
    bohb: [[1.2, 0.006, 0.3]],
    acetone: [[2.23, 0.005, 0.25]],
  };
  const LABELS: [string, number, string][] = [["tg", 1.27, "ไขมัน (–CH₂–)"], ["glyca", 2.03, "GlycA"], ["glucose", 3.72, "กลูโคส"], ["creatinine", 3.04, "Crea"], ["valine", 0.99, "BCAA"]];
  const PPM_MAX = 5.6, PPM_MIN = 0.5;

  let canvas: HTMLCanvasElement;
  let wrap: HTMLDivElement;
  let progress = $state(1);
  let raf = 0;

  const count = $derived(Object.keys(values).length);
  const summary = $derived(`ภาพประกอบ spectrum ¹H NMR จากค่าที่ห้องแล็บคำนวณแล้ว ${count} สาร จุดสูงสุดคือสัญญาณไขมันที่ 1.3 ppm รายละเอียดค่าแต่ละสารอยู่ในรายการด้านล่าง`);

  function signal(ppm: number, peaks: [number, number, number][]) {
    let y = 0;
    for (const [p, w, h] of peaks) y += h / (1 + ((ppm - p) / w) ** 2);
    return y + 0.012 * Math.sin(ppm * 97) * Math.cos(ppm * 31);
  }

  function draw(k: number) {
    if (!canvas) return;
    const css = getComputedStyle(document.documentElement);
    const color = css.getPropertyValue("--series-1").trim();
    const grid = css.getPropertyValue("--grid").trim();
    const muted = css.getPropertyValue("--ink-3").trim();
    const surface = css.getPropertyValue("--surface").trim();
    const dpr = window.devicePixelRatio || 1;
    const W = wrap.clientWidth, H = height;
    canvas.width = W * dpr; canvas.height = H * dpr;
    const ctx = canvas.getContext("2d")!;
    ctx.scale(dpr, dpr);

    const peaks: [number, number, number][] = [];
    for (const [id, list] of Object.entries(PEAKS)) {
      const a = byId[id], v = values[id];
      if (!a || v == null) continue;
      const mid = a.ref_low != null && a.ref_high != null ? (a.ref_low + a.ref_high) / 2 : (a.ref_high ?? a.ref_low ?? v);
      const s = Math.max(0.25, Math.min(2.5, v / mid));
      for (const [p, w, h] of list) peaks.push([p, w, h * s]);
    }
    const pad = { l: 8, r: 8, t: 22, b: 26 };
    const N = Math.max(500, Math.floor(W * 2));
    const pts: [number, number][] = [];
    let ymax = 0;
    for (let i = 0; i <= N; i++) {
      const ppm = PPM_MAX - (PPM_MAX - PPM_MIN) * (i / N);
      const y = Math.abs(ppm - 4.75) < 0.12 ? 0 : signal(ppm, peaks);
      pts.push([ppm, y]); ymax = Math.max(ymax, y);
    }
    const x = (p: number) => pad.l + ((PPM_MAX - p) / (PPM_MAX - PPM_MIN)) * (W - pad.l - pad.r);
    const y = (v: number) => H - pad.b - (v / (ymax * 1.08)) * (H - pad.t - pad.b);

    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 1; ctx.strokeStyle = grid; ctx.fillStyle = muted;
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.textAlign = "center";
    for (let p = 5; p >= 1; p--) {
      ctx.beginPath(); ctx.moveTo(x(p), pad.t); ctx.lineTo(x(p), H - pad.b); ctx.stroke();
      ctx.fillText(`${p}.0`, x(p), H - 8);
    }
    ctx.textAlign = "right"; ctx.fillText("ppm", W - pad.r, H - 8);

    const upto = Math.floor(pts.length * k);
    // area wash (~10%) + 2px line
    ctx.beginPath();
    for (let i = 0; i < upto; i++) { const [p, v] = pts[i]; i ? ctx.lineTo(x(p), y(v)) : ctx.moveTo(x(p), y(v)); }
    ctx.lineWidth = 2; ctx.lineJoin = "round"; ctx.lineCap = "round"; ctx.strokeStyle = color; ctx.stroke();
    if (upto > 1) {
      ctx.lineTo(x(pts[upto - 1][0]), y(0)); ctx.lineTo(x(pts[0][0]), y(0)); ctx.closePath();
      ctx.globalAlpha = 0.1; ctx.fillStyle = color; ctx.fill(); ctx.globalAlpha = 1;
    }
    if (k < 1) {
      const sx = x(pts[upto]?.[0] ?? PPM_MIN);
      ctx.fillStyle = color; ctx.globalAlpha = 0.18; ctx.fillRect(sx - 5, pad.t, 10, H - pad.t - pad.b); ctx.globalAlpha = 1;
    } else {
      ctx.textAlign = "center"; ctx.font = "12px 'IBM Plex Sans Thai', sans-serif";
      for (const [id, ppm, label] of LABELS) {
        if (values[id] == null) continue;
        const ty = Math.max(14, y(signal(ppm, peaks)) - 8);
        ctx.lineWidth = 4; ctx.strokeStyle = surface; ctx.strokeText(label, x(ppm), ty);
        ctx.fillStyle = muted; ctx.fillText(label, x(ppm), ty);
      }
    }
  }

  function animate() {
    cancelAnimationFrame(raf);
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { progress = 1; draw(1); return; }
    let t0: number | null = null;
    const step = (now: number) => {
      t0 ??= now;
      progress = Math.min(1, (now - t0) / 1400);
      draw(progress);
      if (progress < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  }

  $effect(() => {
    void values;
    animate();
    const redraw = () => draw(progress);
    const ro = new ResizeObserver(redraw);
    ro.observe(wrap);
    window.addEventListener("themechange", redraw);
    const mq = matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", redraw);
    return () => { cancelAnimationFrame(raf); ro.disconnect(); window.removeEventListener("themechange", redraw); mq.removeEventListener("change", redraw); };
  });
</script>

<figure class="spectrum">
  <div bind:this={wrap} class="plot" role="img" aria-label={summary}>
    <canvas bind:this={canvas} aria-hidden="true" style={`height:${height}px`}></canvas>
  </div>
  <figcaption>
    <span>ภาพประกอบ ¹H NMR สร้างจากค่าที่ห้องแล็บคำนวณแล้ว — ระบบไม่ประมวลผล spectrum เอง</span>
    <span class="status" aria-hidden="true">{progress < 1 ? `กำลังอ่านสัญญาณ… ${Math.round(progress * 100)}%` : `วัดได้ ${count} สาร ✓`}</span>
  </figcaption>
</figure>

<style>
  .spectrum { margin: 0; background: var(--sunken); border-radius: 12px; padding: 10px 10px 8px; }
  .plot { width: 100%; min-width: 0; overflow: hidden; }
  canvas { display: block; width: 100%; }
  figcaption { display: flex; justify-content: space-between; gap: 8px 16px; flex-wrap: wrap; font-size: 12px; color: var(--ink-3); padding: 4px 4px 0; }
  .status { font-family: var(--mono); color: var(--ink-2); }
</style>
