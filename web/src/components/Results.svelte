<script lang="ts">
  import FactChips from "./FactChips.svelte";
  import {
    CAT_TH, CAT_TONE, SEV_ICON, SEV_TH, SEV_TONE, VERDICT_ICON, VERDICT_TH, VERDICT_TONE, fmt,
    type Assessment, type Verdict,
  } from "../lib/api";

  let { r, hasPrev }: { r: Assessment; hasPrev: boolean } = $props();

  let decisions = $state<Record<string, string>>({});
  let showNa = $state(false);

  const review = $derived(r.findings.filter((f) => f.severity === "stop" || f.severity === "action"));
  const order: Record<Verdict, number> = { worsened: 0, improved: 1, changed: 2, within_variation: 3, not_assessable: 4 };
  const trend = $derived([...r.trend].sort((a, b) => order[a.verdict] - order[b.verdict]));
  const naCount = $derived(trend.filter((t) => t.verdict === "not_assessable").length);
  const counts = $derived.by(() => {
    const c: Partial<Record<Verdict, number>> = {};
    for (const t of r.trend) c[t.verdict] = (c[t.verdict] ?? 0) + 1;
    return c;
  });
  const riskValue = (k: Assessment["risks"][number]) => (k.value == null ? "–" : k.id === "dm" ? `${k.value}/17` : k.display);
</script>

<section class="stats" aria-label="สรุปผลการประเมิน">
  <div class="stat"><span class="label">ต้องให้เภสัชกรทบทวน</span><span class="value">{review.length}</span><span class="sub">เรื่องยา</span></div>
  <div class="stat"><span class="label">ความเสี่ยงหัวใจ 10 ปี</span><span class="value">{riskValue(r.risks[0])}</span><span class="sub">{CAT_TH[r.risks[0].category]}</span></div>
  <div class="stat"><span class="label">ปัจจัยเสริมจาก NMR</span><span class="value">{r.nmr_factors.length}</span><span class="sub">ไม่รวมในคะแนน</span></div>
  {#if hasPrev}
    <div class="stat"><span class="label">เทียบครั้งก่อน: ดีขึ้นจริง / แย่ลงจริง</span><span class="value">{counts.improved ?? 0} / {counts.worsened ?? 0}</span><span class="sub">ตัดสินด้วย RCV</span></div>
  {/if}
</section>

<div class="cols">
  <section class="card" aria-labelledby="h-risk">
    <div class="card-head"><h2 id="h-risk"><span class="step">3</span>ความเสี่ยงรายโรค</h2><p>คะแนนที่ validate แล้วในคนไทย</p></div>
    <ul class="list">
      {#each r.risks as k (k.id)}
        <li class="risk">
          <div class="risk-top">
            <div>
              <h3>{k.disease}</h3>
              <p class="muted">{k.score_name}{k.method !== "-" ? ` · ${k.method}` : ""}</p>
            </div>
            <div class="risk-val">
              <span class="big">{riskValue(k)}</span>
              <span class="chip {CAT_TONE[k.category]}"><span class="dot"></span>{CAT_TH[k.category]}</span>
            </div>
          </div>
          {#if k.value == null || k.id === "dm" || k.notes.length}
            <p class="notes">{[...(k.value == null || k.id === "dm" ? [k.display] : []), ...k.notes].join(" · ")}</p>
          {/if}
          <FactChips ids={k.fact_ids} facts={r.facts} />
        </li>
      {/each}
    </ul>
    <h3 class="sub-h">ปัจจัยเสริมจาก NMR <span class="muted">— แสดงแยก ไม่ผสมเข้าคะแนน</span></h3>
    {#if r.nmr_factors.length}
      <ul class="list">
        {#each r.nmr_factors as x (x.id)}
          <li class="item tone-{x.severity === 'monitor' ? 'info' : 'good'}">
            <div class="item-top"><h3>{x.title}</h3><span class="level">{x.level === "emerging" ? "หลักฐาน EMERGING" : "GUIDELINE"}</span></div>
            <p>{x.detail}</p>
            <FactChips ids={x.fact_ids} facts={r.facts} />
          </li>
        {/each}
      </ul>
    {:else}
      <p class="empty">ไม่พบปัจจัยเสริม</p>
    {/if}
  </section>

  <section class="card" aria-labelledby="h-meds">
    <div class="card-head"><h2 id="h-meds">เรื่องยา → คิวเภสัชกร</h2><p>{review.length ? `ต้องทบทวน ${review.length} รายการ` : "ไม่มีรายการต้องทบทวน"}</p></div>
    {#if r.findings.length}
      <ul class="list">
        {#each r.findings as f (f.id)}
          <li class="item tone-{SEV_TONE[f.severity]}">
            <div class="item-top">
              <h3>{f.title}</h3>
              <span class="chip {SEV_TONE[f.severity]}"><span aria-hidden="true">{SEV_ICON[f.severity]}</span>{SEV_TH[f.severity]}</span>
            </div>
            <p>{f.detail}</p>
            <FactChips ids={f.fact_ids} facts={r.facts} />
            <details class="why">
              <summary>ทำไมระบบถึงเตือน (Why?)</summary>
              <ol>
                {#each f.trace as t}<li>{t}</li>{/each}
                <li>ใช้ rule: {f.fact_ids.join(", ")}</li>
              </ol>
            </details>
            {#if f.severity !== "info"}
              <div class="decide" role="group" aria-label={`การตัดสินใจของเภสัชกร: ${f.title}`}>
                {#each [["accept", "ยอมรับ"], ["modify", "แก้ไข"], ["reject", "ไม่ยอมรับ"]] as [k, label]}
                  <button type="button" class="btn btn-sm" aria-pressed={decisions[f.id] === k} onclick={() => (decisions[f.id] = k)}>{label}</button>
                {/each}
              </div>
            {/if}
          </li>
        {/each}
      </ul>
    {:else}
      <p class="empty">ไม่พบประเด็นเรื่องยา</p>
    {/if}
  </section>

  <section class="card" aria-labelledby="h-life">
    <div class="card-head"><h2 id="h-life">การดูแลตัวเอง</h2><p>คำแนะนำตาม guideline</p></div>
    {#if r.advice.length}
      <ul class="list">
        {#each r.advice as a (a.id)}
          <li class="item">
            <h3>{a.topic}</h3>
            <p>{a.advice}</p>
            <p class="muted">เพราะ: {a.reason}</p>
            <FactChips ids={a.fact_ids} facts={r.facts} />
          </li>
        {/each}
      </ul>
    {:else}
      <p class="empty">ไม่มีคำแนะนำเพิ่มเติม — พฤติกรรมตอนนี้อยู่ในเกณฑ์</p>
    {/if}
  </section>
</div>

{#if r.trend.length}
  <section class="card trend-card" aria-labelledby="h-trend">
    <div class="card-head">
      <h2 id="h-trend"><span class="step">4</span>เทียบกับการตรวจครั้งก่อน</h2>
      <p>Reference Change Value (RCV) แยก "เปลี่ยนจริง" ออกจากความแปรปรวนตามธรรมชาติ</p>
    </div>
    <ul class="pills" aria-label="สรุปผลการเปลี่ยนแปลง">
      {#each (["improved", "worsened", "within_variation", "changed", "not_assessable"] as Verdict[]) as v}
        {#if counts[v]}<li class="chip {VERDICT_TONE[v]}"><span aria-hidden="true">{VERDICT_ICON[v]}</span>{VERDICT_TH[v]} {counts[v]}</li>{/if}
      {/each}
    </ul>
    <div class="table-wrap">
      <table>
        <caption class="sr-only">การเปลี่ยนแปลงของแต่ละสารเทียบกับครั้งก่อน</caption>
        <thead><tr><th scope="col">สาร</th><th scope="col" class="r">ครั้งก่อน</th><th scope="col" class="r">ครั้งนี้</th><th scope="col" class="r">เปลี่ยน</th><th scope="col" class="r">RCV</th><th scope="col">ผล</th></tr></thead>
        <tbody>
          {#each trend as t (t.id)}
            {#if t.verdict !== "not_assessable" || showNa}
              <tr>
                <th scope="row">{t.abbr}</th>
                <td class="r num">{fmt(t.previous)}</td>
                <td class="r num">{fmt(t.current)} <span class="muted">{t.unit}</span></td>
                <td class="r num">{t.pct_change > 0 ? "+" : ""}{t.pct_change.toFixed(0)}%</td>
                <td class="r num">{t.rcv_pct == null ? "–" : `±${t.rcv_pct.toFixed(0)}%`}</td>
                <td><span class="chip {VERDICT_TONE[t.verdict]}"><span aria-hidden="true">{VERDICT_ICON[t.verdict]}</span>{VERDICT_TH[t.verdict]}</span></td>
              </tr>
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
    {#if naCount}
      <button type="button" class="btn btn-ghost btn-sm more" aria-expanded={showNa} onclick={() => (showNa = !showNa)}>
        {showNa ? "ซ่อน" : "แสดง"}สารที่ยังไม่มีข้อมูล CVi ({naCount}) — เห็นค่าได้ แต่ตัดสินไม่ได้ว่าเปลี่ยนจริง
      </button>
    {/if}
  </section>
{/if}

<style>
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-bottom: 16px; }
  .stat { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; display: grid; gap: 2px; box-shadow: var(--shadow); }
  .stat .label { font-size: 13px; color: var(--ink-2); }
  .stat .value { font-size: 28px; font-weight: 600; line-height: 1.2; }
  .stat .sub { font-size: 12.5px; color: var(--ink-3); }
  .cols { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; align-items: start; }
  .list { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
  .risk { border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; }
  .risk-top { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
  .risk-val { display: grid; justify-items: end; gap: 4px; }
  .big { font-size: 26px; font-weight: 600; line-height: 1.1; }
  .notes { font-size: 12.5px; color: var(--ink-2); margin-top: 6px; }
  .sub-h { margin: 18px 0 10px; font-size: 14px; }
  .item { border-radius: 12px; padding: 12px 14px; background: var(--sunken); border-left: 4px solid var(--border-strong); }
  .item h3 { font-size: 14.5px; font-weight: 600; }
  .item p { font-size: 14px; margin-top: 4px; }
  .item-top { display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; }
  .tone-critical { background: var(--critical-soft); border-left-color: var(--critical); }
  .tone-serious { background: var(--serious-soft); border-left-color: var(--serious); }
  .tone-info { background: var(--info-soft); border-left-color: var(--series-1); }
  .tone-good { background: var(--good-soft); border-left-color: var(--good); }
  .level { font: 600 10.5px/1.4 var(--mono); letter-spacing: .04em; color: var(--ink-2); white-space: nowrap; }
  .why { margin-top: 10px; font-size: 13px; }
  .why summary { cursor: pointer; font-weight: 600; color: var(--ink-2); min-height: 32px; display: flex; align-items: center; gap: 6px; list-style: none; }
  .why summary::-webkit-details-marker { display: none; }
  .why summary::before { content: "▸"; transition: transform .15s; }
  .why[open] summary::before { transform: rotate(90deg); }
  .why ol { margin: 6px 0 0; padding: 10px 12px 10px 30px; background: var(--raised); border-radius: 8px; }
  .decide { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
  .empty { color: var(--ink-3); font-size: 14px; padding: 4px 0; }
  .trend-card { margin-top: 16px; }
  .pills { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; margin: 0 0 12px; padding: 0; }
  .pills .chip { font-size: 13px; padding: 5px 12px; }
  .table-wrap { overflow-x: auto; }
  .more { margin-top: 12px; }
  @media (max-width: 1100px) { .cols { grid-template-columns: 1fr; } }
</style>
