<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../lib/api";

  interface Item {
    time: string; patient_id: string; summary: string; indicator: "critical" | "warning" | "info";
    finding_id: string; fact_ids: string[]; outcome: string; reason: string | null; comment: string | null; status: string;
  }
  const TONE = { critical: "critical", warning: "serious", info: "info" } as const;
  const ST: Record<string, string> = { open: "รอทบทวน", reviewed: "ทบทวนแล้ว", "contacted-prescriber": "ติดต่อแพทย์แล้ว" };

  let items = $state<Item[]>([]);
  let loaded = $state(false);
  let filter = $state<"open" | "all">("open");
  let announce = $state("");
  let last = "";

  const shown = $derived(filter === "open" ? items.map((x, i) => [x, i] as const).filter(([x]) => x.status === "open") : items.map((x, i) => [x, i] as const));
  const openCount = $derived(items.filter((x) => x.status === "open").length);

  async function load() {
    const q = await api<Item[]>("/api/queue");
    const sig = JSON.stringify(q);
    if (sig !== last) {
      if (loaded && q.length > items.length) announce = `มีรายการใหม่ ${q.length - items.length} รายการ`;
      last = sig; items = q;
    }
    loaded = true;
  }
  async function setStatus(i: number, s: string) {
    await fetch(`/api/queue/${i}/${s}`, { method: "POST" });
    await load();
    announce = `เปลี่ยนสถานะเป็น ${ST[s]}`;
  }
  onMount(() => {
    load();
    const t = setInterval(load, 2500);
    return () => clearInterval(t);
  });
  const time = (t: string) => new Date(t).toLocaleString("th-TH", { dateStyle: "medium", timeStyle: "short" });
</script>

<div class="sr-only" role="status" aria-live="polite">{announce}</div>

<div class="head">
  <div class="seg" role="group" aria-label="กรองรายการ">
    <button type="button" class="btn btn-sm" aria-pressed={filter === "open"} onclick={() => (filter = "open")}>รอทบทวน ({openCount})</button>
    <button type="button" class="btn btn-sm" aria-pressed={filter === "all"} onclick={() => (filter = "all")}>ทั้งหมด ({items.length})</button>
  </div>
  <p class="muted">อัปเดตอัตโนมัติทุก 2.5 วินาที</p>
</div>

{#if !loaded}
  <p class="muted">กำลังโหลด…</p>
{:else if !shown.length}
  <div class="card empty">
    <h2>ยังไม่มีรายการ{filter === "open" ? "ที่รอทบทวน" : ""}</h2>
    <p>ลองสั่งยาใน <a href="/his/?hn=HN-0002&drug=simvastatin&dose=40">หน้าสั่งยา (HIS)</a> แล้ว override คำเตือน — รายการจะมาแสดงที่นี่</p>
  </div>
{:else}
  <ul class="list">
    {#each shown as [x, i] (x.time + x.finding_id + i)}
      <li class="card item tone-{TONE[x.indicator]}">
        <div class="body">
          <div class="top">
            <h2>{x.summary}</h2>
            <span class="chip {x.status === 'open' ? 'warning' : 'good'}"><span class="dot"></span>{ST[x.status]}</span>
          </div>
          <p class="what">
            {#if x.outcome === "overridden"}
              แพทย์ <strong>override</strong> — {x.reason}{#if x.comment}<span class="quote"> “{x.comment}”</span>{/if}
            {:else}
              แพทย์<strong>ทำตามคำแนะนำ</strong>
            {/if}
          </p>
          <p class="muted">HN {x.patient_id} · {time(x.time)} · <span class="mono">{x.finding_id}</span> · {x.fact_ids.join(", ")}</p>
        </div>
        <div class="acts" role="group" aria-label={`เปลี่ยนสถานะ: ${x.summary}`}>
          <button type="button" class="btn btn-sm" aria-pressed={x.status === "reviewed"} onclick={() => setStatus(i, "reviewed")}>ทบทวนแล้ว</button>
          <button type="button" class="btn btn-sm" aria-pressed={x.status === "contacted-prescriber"} onclick={() => setStatus(i, "contacted-prescriber")}>ติดต่อแพทย์แล้ว</button>
        </div>
      </li>
    {/each}
  </ul>
{/if}

<style>
  .head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
  .seg { display: flex; gap: 6px; }
  .list { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }
  .item { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 12px 20px; align-items: center; border-left: 5px solid var(--border-strong); }
  .top { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  .top h2 { font-size: 16px; }
  .what { margin: 6px 0 4px; font-size: 14.5px; }
  .quote { color: var(--ink-2); }
  .acts { display: flex; gap: 6px; flex-wrap: wrap; justify-content: flex-end; }
  .tone-critical { border-left-color: var(--critical); }
  .tone-serious { border-left-color: var(--serious); }
  .tone-info { border-left-color: var(--series-1); }
  .empty { text-align: center; padding: 40px 20px; }
  .empty p { margin-top: 8px; color: var(--ink-2); }
  @media (max-width: 640px) { .item { grid-template-columns: 1fr; } .acts { justify-content: flex-start; } }
</style>
