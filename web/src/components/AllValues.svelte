<script lang="ts">
  import { fmt, refText, status, type Analyte, type TrendRow } from "../lib/api";

  let { catalog, values, trend }: { catalog: Analyte[]; values: Record<string, number>; trend: TrendRow[] } = $props();

  const T = $derived(Object.fromEntries(trend.map((t) => [t.id, t])));
  const TREND: Record<string, string> = {
    improved: "ดีขึ้นจริง", worsened: "แย่ลงจริง", within_variation: "เท่าเดิม", changed: "เปลี่ยนจริง", not_assessable: "บอกไม่ได้",
  };
  const ST = { normal: "", high: "สูง", low: "ต่ำ" } as const;
  const groups = $derived.by(() => {
    const out: { name: string; items: Analyte[] }[] = [];
    for (const a of catalog.filter((x) => values[x.id] != null)) {
      const g = out.at(-1);
      if (g && g.name === a.group) g.items.push(a); else out.push({ name: a.group, items: [a] });
    }
    return out;
  });
</script>

<p class="note">ช่วงปกติ = ประชากร UK Biobank เปอร์เซ็นไทล์ที่ 10–90 (ยังไม่ใช่ค่าของคนไทย) ยกเว้นกลูโคสใช้เกณฑ์ ADA · "เปลี่ยนจริง" ตัดสินด้วย Reference Change Value</p>
<table>
  <caption class="sr-only">ค่า NMR ทั้งหมด</caption>
  <thead>
    <tr><th scope="col">สาร</th><th scope="col" class="r">ค่า</th><th scope="col">ช่วงปกติ</th>{#if trend.length}<th scope="col">เทียบครั้งก่อน</th>{/if}</tr>
  </thead>
  {#each groups as g (g.name)}
    <tbody>
      <tr class="group"><th scope="rowgroup" colspan={trend.length ? 4 : 3}>{g.name}</th></tr>
      {#each g.items as a (a.id)}
        {@const st = status(a, values[a.id])}
        {@const t = T[a.id]}
        <tr>
          <th scope="row"><span class="abbr">{a.abbr}</span><span class="name">{a.name}</span></th>
          <td class="r"><span class="num v">{fmt(values[a.id])}</span> <span class="unit">{a.unit}</span>{#if st !== "normal"}<span class="flag">{ST[st]}</span>{/if}</td>
          <td class="num muted">{refText(a)}</td>
          {#if trend.length}
            <td>{#if t}<span class="num muted">{fmt(t.previous)} → </span>{TREND[t.verdict]}{:else}<span class="muted">–</span>{/if}</td>
          {/if}
        </tr>
      {/each}
    </tbody>
  {/each}
</table>

<style>
  .note { font-size: 13.5px; color: var(--ink-3); margin-bottom: 16px; }
  .group th { padding-top: 22px; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; border-bottom: 1px solid var(--line-strong); }
  th[scope="row"] { font-weight: 400; border-bottom: 1px solid var(--line); padding: 10px 8px; }
  .abbr { display: block; font-size: 15px; color: var(--ink); font-weight: 500; }
  .name { display: block; font-size: 12.5px; color: var(--ink-3); }
  td { font-size: 14.5px; padding: 10px 8px; }
  .v { font-weight: 500; }
  .unit { font-size: 12.5px; color: var(--ink-3); }
  .flag { margin-left: 8px; font-size: 12.5px; font-weight: 600; color: var(--ink); }
</style>
