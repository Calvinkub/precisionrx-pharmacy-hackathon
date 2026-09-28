<script lang="ts">
  import { fmt, refText, status, type Analyte } from "../lib/api";

  let { catalog, values, prev }: { catalog: Analyte[]; values: Record<string, number>; prev: Record<string, number> | null } = $props();

  let tableView = $state(false);
  let ready = $state(false);
  let tip = $state<{ x: number; y: number; a: Analyte } | null>(null);

  const STATUS_TH = { normal: "ในช่วง", high: "สูง", low: "ต่ำ" } as const;
  const STATUS_ICON = { normal: "", high: "▲", low: "▼" } as const;

  const rows = $derived(catalog.filter((a) => values[a.id] != null));
  const groups = $derived.by(() => {
    const out: { name: string; items: Analyte[] }[] = [];
    for (const a of rows) {
      const g = out.at(-1);
      if (g && g.name === a.group) g.items.push(a); else out.push({ name: a.group, items: [a] });
    }
    return out;
  });
  const outCount = $derived(rows.filter((a) => status(a, values[a.id]) !== "normal").length);

  // fixed domain per analyte so a higher value really sits further right
  function domain(a: Analyte) {
    const v = values[a.id];
    return Math.max((a.ref_high ?? v) * 1.6, v * 1.08, (prev?.[a.id] ?? 0) * 1.08) || 1;
  }
  const pct = (a: Analyte, v: number) => `${Math.min(100, Math.max(0, (v / domain(a)) * 100))}%`;
  const change = (a: Analyte) => {
    const p = prev?.[a.id];
    return p ? ((values[a.id] - p) / p) * 100 : null;
  };

  $effect(() => {
    void values;
    ready = false;
    const t = setTimeout(() => (ready = true), 30);
    return () => clearTimeout(t);
  });

  function showTip(e: PointerEvent, a: Analyte) {
    const box = (e.currentTarget as HTMLElement).closest(".panel")!.getBoundingClientRect();
    tip = { x: e.clientX - box.left, y: e.clientY - box.top, a };
  }
</script>

<div class="panel-head">
  <p class="summary">
    <strong>{rows.length}</strong> สาร · <span class="chip serious"><span class="dot"></span>นอกช่วง {outCount}</span>
  </p>
  <div class="legend" aria-hidden={tableView}>
    <span><i class="sw band"></i>ช่วงอ้างอิง</span>
    {#if prev}<span><i class="sw prev"></i>ครั้งก่อน</span>{/if}
    <span><i class="sw in"></i>ในช่วง</span>
    <span><i class="sw out"></i>นอกช่วง</span>
  </div>
  <button type="button" class="btn btn-sm" aria-pressed={tableView} onclick={() => (tableView = !tableView)}>
    {tableView ? "มุมมองกราฟ" : "มุมมองตาราง"}
  </button>
</div>
<p class="ref-note">ช่วงอ้างอิง = ประชากร UK Biobank P10–P90 (ไม่ใช่ค่าคนไทย และไม่ใช่เกณฑ์ทางคลินิก) ยกเว้นกลูโคสใช้เกณฑ์ ADA</p>

{#if tableView}
  <div class="table-wrap">
    <table>
      <caption class="sr-only">ผล NMR ทั้งหมด</caption>
      <thead><tr><th scope="col">สาร</th><th scope="col" class="r">ค่า</th><th scope="col">หน่วย</th><th scope="col">ช่วงอ้างอิง</th><th scope="col">สถานะ</th>{#if prev}<th scope="col" class="r">ครั้งก่อน</th>{/if}</tr></thead>
      <tbody>
        {#each rows as a (a.id)}
          {@const st = status(a, values[a.id])}
          <tr>
            <th scope="row">{a.abbr} <span class="muted">{a.name}</span></th>
            <td class="r num">{fmt(values[a.id])}</td>
            <td>{a.unit}</td>
            <td class="num">{refText(a)}</td>
            <td>{STATUS_ICON[st]} {STATUS_TH[st]}</td>
            {#if prev}<td class="r num">{fmt(prev[a.id])}</td>{/if}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else}
  <div class="panel" role="list" aria-label="ผล NMR แยกตามกลุ่ม">
    {#each groups as g (g.name)}
      <div role="listitem" class="group">
        <h3 class="group-title">{g.name}</h3>
        <ul>
          {#each g.items as a, i (a.id)}
            {@const v = values[a.id]}
            {@const st = status(a, v)}
            <li class="row" class:ready style={`--delay:${i * 35}ms`}
                onpointermove={(e) => showTip(e, a)} onpointerleave={() => (tip = null)}>
              <span class="name"><strong>{a.abbr}</strong><small>{a.name}</small></span>
              <span class="track" aria-hidden="true">
                {#if a.ref_low != null || a.ref_high != null}
                  <span class="band" style={`left:${pct(a, a.ref_low ?? 0)};width:calc(${pct(a, a.ref_high ?? domain(a))} - ${pct(a, a.ref_low ?? 0)})`}></span>
                {/if}
                <span class="bar {a.ref_low == null && a.ref_high == null ? 'none' : st === 'normal' ? 'in' : 'out'}" style={`width:${ready ? pct(a, v) : "0%"}`}></span>
                {#if prev?.[a.id] != null}<span class="prev" style={`left:${pct(a, prev[a.id])}`}></span>{/if}
              </span>
              <span class="val">
                <span class="num v">{fmt(v)}</span> <small>{a.unit}</small>
                {#if st !== "normal"}<span class="flag">{STATUS_ICON[st]} {STATUS_TH[st]}</span>{/if}
                <small class="ref">ช่วง {refText(a)}</small>
              </span>
              <span class="sr-only">{a.name} {fmt(v)} {a.unit}, {STATUS_TH[st]}, ช่วงอ้างอิง {refText(a)}{prev?.[a.id] != null ? `, ครั้งก่อน ${fmt(prev[a.id])}` : ""}</span>
            </li>
          {/each}
        </ul>
      </div>
    {/each}
    {#if tip}
      {@const c = change(tip.a)}
      <div class="tip" style={`left:${tip.x}px;top:${tip.y}px`} aria-hidden="true">
        <strong class="num">{fmt(values[tip.a.id])} {tip.a.unit}</strong>
        <span>{tip.a.name}</span>
        <span class="muted">ช่วง {refText(tip.a)}{prev?.[tip.a.id] != null ? ` · ครั้งก่อน ${fmt(prev[tip.a.id])}` : ""}{c != null ? ` (${c > 0 ? "+" : ""}${c.toFixed(0)}%)` : ""}</span>
        {#if tip.a.note}<span class="muted">{tip.a.note}</span>{/if}
      </div>
    {/if}
  </div>
{/if}

<style>
  .panel-head { display: flex; align-items: center; gap: 8px 16px; flex-wrap: wrap; margin: 16px 0 4px; }
  .summary { font-size: 14px; display: flex; gap: 8px; align-items: center; }
  .legend { display: flex; gap: 14px; flex-wrap: wrap; font-size: 12.5px; color: var(--ink-2); flex: 1; }
  .legend span { display: inline-flex; gap: 6px; align-items: center; }
  .sw { display: inline-block; width: 16px; height: 8px; border-radius: 2px; }
  .sw.band { background: var(--band); height: 12px; }
  .sw.prev { width: 2px; height: 14px; background: var(--ink-2); }
  .sw.in { background: var(--good); }
  .sw.out { background: var(--serious); }
  .ref-note { font-size: 12px; color: var(--ink-3); margin-bottom: 4px; }

  .panel { position: relative; }
  .group-title { font-size: 12px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: var(--ink-3); margin: 18px 0 4px; padding-bottom: 4px; border-bottom: 1px solid var(--border); }
  ul { list-style: none; margin: 0; padding: 0; }
  .row {
    display: grid; grid-template-columns: minmax(0, 170px) minmax(0, 1fr) 128px; gap: 14px; align-items: center;
    padding: 7px 6px; border-radius: 8px; opacity: 0; transform: translateY(4px);
    transition: opacity .35s ease var(--delay), transform .35s ease var(--delay);
  }
  .row.ready { opacity: 1; transform: none; }
  .row:hover { background: var(--sunken); }
  .name { display: grid; line-height: 1.25; min-width: 0; }
  .name strong { font-size: 14px; font-weight: 600; }
  .name small { font-size: 12px; color: var(--ink-3); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .track { position: relative; height: 18px; }
  .track::before { content: ""; position: absolute; left: 0; right: 0; top: 8px; height: 2px; background: var(--grid); border-radius: 1px; }
  .band { position: absolute; top: 2px; bottom: 2px; background: var(--band); border-radius: 4px; }
  .bar {
    position: absolute; left: 0; top: 5px; height: 8px; border-radius: 0 4px 4px 0;
    transition: width .8s cubic-bezier(.2, .8, .2, 1) var(--delay);
  }
  .bar.in { background: var(--good); }
  .bar.out { background: var(--serious); }
  .bar.none { background: var(--ink-3); }
  .prev { position: absolute; top: 0; width: 2px; height: 18px; background: var(--ink-2); transform: translateX(-1px); border-radius: 1px; box-shadow: 0 0 0 2px var(--surface); }
  .val { text-align: right; line-height: 1.25; }
  .val .v { font-size: 15px; font-weight: 600; }
  .val small { font-size: 12px; color: var(--ink-3); }
  .val .ref { display: block; }
  .flag { font-size: 12px; font-weight: 600; color: var(--ink); margin-left: 4px; }
  .tip {
    position: absolute; z-index: 5; pointer-events: none; transform: translate(12px, -110%);
    display: grid; gap: 2px; background: var(--raised); border: 1px solid var(--border-strong); border-radius: 10px;
    padding: 8px 12px; font-size: 13px; box-shadow: 0 8px 24px rgba(0, 0, 0, .15); max-width: 280px;
  }
  .tip strong { font-size: 15px; }
  .table-wrap { overflow-x: auto; margin-top: 8px; }
  .table-wrap th[scope="row"] { font-size: 14px; color: var(--ink); font-weight: 600; border-bottom: 1px solid var(--border); }
  @media (max-width: 720px) {
    .row { grid-template-columns: minmax(0, 1fr) 118px; gap: 4px 10px; }
    .track { grid-column: 1 / -1; grid-row: 2; }
    .name small { white-space: normal; }
  }
</style>
