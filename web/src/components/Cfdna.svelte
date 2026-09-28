<script lang="ts">
  import { onMount } from "svelte";
  import Sources from "./Sources.svelte";
  import { api, type Fact } from "../lib/api";

  interface Flag { id: string; label: string; detail: string; fact_ids: string[] }
  interface Variant { gene: string; variant: string; vaf: number; tier: string; lab_note: string; flags: Flag[] }
  interface OFinding { id: string; severity: "stop" | "action" | "monitor" | "info"; title: string; detail: string; fact_ids: string[]; audience: string }
  interface OCase {
    id: string; label: string; story: string;
    patient: { age: number; sex: string; dx: string };
    meds: { drug: string; dose_mg?: number; status: string }[];
    pgx: Record<string, string>;
    ctdna: { date: string; lab: string; specimen: string };
    variants: Variant[]; findings: OFinding[]; facts: Record<string, Fact>;
  }

  const SEV = { stop: ["critical", "ห้ามใช้"], action: ["serious", "ต้องพิจารณา"], monitor: ["info", "ติดตาม"], info: ["good", "ข้อมูล"] } as const;
  const AUD: Record<string, string> = { oncologist: "สำหรับแพทย์มะเร็ง", pharmacist: "สำหรับเภสัชกร", genetics: "ส่งปรึกษาพันธุศาสตร์" };
  const MAX_VAF = 60;

  let list = $state<{ id: string; label: string }[]>([]);
  let id = $state("");
  let c = $state<OCase | null>(null);

  const groups = $derived.by(() => {
    if (!c) return [];
    return ["oncologist", "pharmacist", "genetics"].map((a) => ({ a, items: c!.findings.filter((f) => f.audience === a) })).filter((g) => g.items.length);
  });

  async function load(next: string) {
    id = next;
    c = await api<OCase>(`/api/oncology/cases/${next}`);
    const u = new URL(location.href); u.searchParams.set("case", next); history.replaceState(null, "", u);
  }
  onMount(async () => {
    list = await api<typeof list>("/api/oncology/cases");
    const q = new URLSearchParams(location.search).get("case");
    await load(list.some((x) => x.id === q) ? q! : list[0].id);
  });
  const x = (vaf: number) => `${Math.min(100, (vaf / MAX_VAF) * 100)}%`;
</script>

<label class="case-pick">
  <span>เคสตัวอย่าง</span>
  <select value={id} onchange={(e) => load((e.currentTarget as HTMLSelectElement).value)}>
    {#each list as o (o.id)}<option value={o.id}>{o.label}</option>{/each}
  </select>
</label>

{#if c}
  <header class="head">
    <p class="name">{c.patient.sex === "female" ? "ผู้ป่วยหญิง" : "ผู้ป่วยชาย"} {c.patient.age} ปี</p>
    <p class="dx">{c.patient.dx}</p>
    <p class="story">{c.story}</p>
    <dl class="ctx">
      <div><dt>ยาปัจจุบัน</dt><dd>{c.meds.filter((m) => m.status === "current").map((m) => `${m.drug}${m.dose_mg ? ` ${m.dose_mg} mg` : ""}`).join(", ") || "–"}</dd></div>
      <div><dt>ยาที่วางแผน</dt><dd>{c.meds.filter((m) => m.status === "planned").map((m) => m.drug).join(", ") || "–"}</dd></div>
      <div><dt>ยีนของผู้ป่วย (germline)</dt><dd>{Object.entries(c.pgx).map(([k, v]) => `${k} ${v}`).join(" · ") || "ยังไม่ได้ตรวจ"}</dd></div>
    </dl>
  </header>

  <section class="section" aria-labelledby="h-ct">
    <div class="section-head">
      <h2 id="h-ct">ผล ctDNA · {c.ctdna.date}</h2>
      <span class="muted small">{c.ctdna.lab} · {c.ctdna.specimen}</span>
    </div>
    {#if c.variants.length}
      <ul class="variants">
        {#each c.variants as v (v.gene + v.variant)}
          <li class="variant">
            <div class="v-name"><h3>{v.gene}</h3><p>{v.variant}</p></div>
            <div class="v-plot" aria-hidden="true">
              <span class="germ-band" style={`left:${x(40)};width:calc(${x(60)} - ${x(40)})`}></span>
              <span class="stem" style={`width:${x(v.vaf)}`}></span>
              <span class="dot" class:flagged={v.flags.length} style={`left:${x(v.vaf)}`}></span>
            </div>
            <p class="vaf num">{v.vaf.toFixed(1)}%</p>
            <p class="tier muted small">{v.tier}</p>
            <div class="v-flags">
              {#each v.flags as f (f.id)}<span class="status {f.id === 'germline' ? 'serious' : 'info'}">{f.label}</span>{/each}
              {#if v.lab_note}<span class="muted small">{v.lab_note}</span>{/if}
            </div>
            <span class="sr-only">VAF {v.vaf} เปอร์เซ็นต์ {v.flags.map((f) => f.label).join(", ")}</span>
          </li>
        {/each}
      </ul>
      <p class="legend muted small" aria-hidden="true"><span class="lg-band"></span>ช่วง VAF ~40–60% ที่ variant อาจเป็นยีนถ่ายทอดทางพันธุกรรม · แกน 0–{MAX_VAF}%</p>
    {:else}
      <p class="none">ไม่พบ variant ในเลือด</p>
    {/if}
  </section>

  {#each groups as g (g.a)}
    <section class="section" aria-labelledby={`h-${g.a}`}>
      <h2 id={`h-${g.a}`}>{AUD[g.a]}</h2>
      <ol class="findings">
        {#each g.items as f (f.id)}
          <li class:stop={f.severity === "stop"}>
            <div class="f-top"><h3>{f.title}</h3><span class="status {SEV[f.severity][0]}">{SEV[f.severity][1]}</span></div>
            <p>{f.detail}</p>
            <Sources ids={f.fact_ids} facts={c.facts} />
          </li>
        {/each}
      </ol>
    </section>
  {/each}

  <p class="disclaimer">ระบบแสดง variant และ tier ตามรายงานของห้องแล็บ ไม่ได้ call variant เอง · การเลือกยารักษามะเร็งเป็นการตัดสินใจของแพทย์ · ข้อมูลจำลอง</p>
{:else}
  <p class="muted">กำลังโหลด…</p>
{/if}

<style>
  .case-pick { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--ink-3); max-width: 100%; }
  .case-pick > span { white-space: nowrap; }
  .case-pick select {
    appearance: none; border: 0; color: var(--ink-2); cursor: pointer; padding: 4px 22px 4px 0; min-width: 0; max-width: 100%;
    font: 500 14px/1.3 var(--font); background: none; text-overflow: ellipsis;
    background-image: linear-gradient(45deg, transparent 50%, var(--ink-3) 50%), linear-gradient(135deg, var(--ink-3) 50%, transparent 50%);
    background-position: right 7px center, right 2px center; background-size: 5px 5px; background-repeat: no-repeat;
  }
  .head { padding: 16px 0 36px; }
  .name { font-size: clamp(28px, 3.4vw, 38px); font-weight: 600; letter-spacing: -0.015em; line-height: 1.25; }
  .dx { font-size: 17px; color: var(--ink-2); margin-top: 4px; }
  .story { color: var(--ink-3); margin-top: 6px; max-width: 70ch; }
  .ctx { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px 32px; margin: 24px 0 0; }
  .ctx dt { font-size: 13px; color: var(--ink-3); }
  .ctx dd { margin: 2px 0 0; font-weight: 500; }
  .variants { list-style: none; margin: 0; padding: 0; }
  .variant { display: grid; grid-template-columns: 200px minmax(0, 1fr) 70px 80px; grid-template-rows: auto auto; gap: 4px 20px; align-items: center; padding: 18px 0; border-top: 1px solid var(--line); }
  .v-name p { font-size: 14px; color: var(--ink-3); }
  .v-plot { position: relative; height: 18px; }
  .v-plot::before { content: ""; position: absolute; left: 0; right: 0; top: 8px; height: 1px; background: var(--line-strong); }
  .germ-band { position: absolute; top: 3px; height: 12px; border-radius: 6px; background: color-mix(in srgb, var(--warning) 28%, transparent); }
  .stem { position: absolute; left: 0; top: 8px; height: 2px; background: var(--ink-3); }
  .dot { position: absolute; top: 3px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); transform: translateX(-6px); box-shadow: 0 0 0 2px var(--bg); }
  .dot.flagged { background: var(--serious); }
  .vaf { text-align: right; font-size: 18px; font-weight: 500; }
  .v-flags { grid-column: 2 / -1; display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: baseline; }
  .legend { display: flex; align-items: center; gap: 8px; margin-top: 12px; }
  .lg-band { display: inline-block; width: 22px; height: 10px; border-radius: 5px; background: color-mix(in srgb, var(--warning) 28%, transparent); }
  .none { font-size: 18px; }
  .findings { list-style: none; margin: 16px 0 0; padding: 0; }
  .findings li { padding: 18px 0; border-top: 1px solid var(--line); }
  .findings li.stop { background: var(--critical-soft); border-radius: var(--radius); padding: 20px; border-top: 0; }
  .f-top { display: flex; justify-content: space-between; gap: 16px; align-items: baseline; }
  .findings p { color: var(--ink-2); margin: 4px 0 8px; max-width: 72ch; }
  .disclaimer { margin-top: 32px; font-size: 13px; color: var(--ink-3); }
  @media (max-width: 860px) {
    .ctx { grid-template-columns: 1fr; }
    .variant { grid-template-columns: minmax(0, 1fr) auto; }
    .v-plot { grid-column: 1 / -1; grid-row: 2; }
    .tier { display: none; }
    .v-flags { grid-column: 1 / -1; }
    .f-top { flex-direction: column; gap: 4px; }
  }
</style>
