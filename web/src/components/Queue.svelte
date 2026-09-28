<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../lib/api";

  interface Item {
    time: string; patient_id: string; summary: string; indicator: "critical" | "warning" | "info";
    finding_id: string; fact_ids: string[]; outcome: string; reason: string | null; comment: string | null; status: string;
  }
  const TONE = { critical: "critical", warning: "serious", info: "info" } as const;
  const IND_TH = { critical: "ห้ามสั่ง", warning: "คำเตือน", info: "ข้อมูล" } as const;
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
  <div class="segmented" role="group" aria-label="กรองรายการ">
    <button type="button" aria-pressed={filter === "open"} onclick={() => (filter = "open")}>รอทบทวน {openCount}</button>
    <button type="button" aria-pressed={filter === "all"} onclick={() => (filter = "all")}>ทั้งหมด {items.length}</button>
  </div>
  <p class="muted small">อัปเดตอัตโนมัติ</p>
</div>

{#if !loaded}
  <p class="muted">กำลังโหลด…</p>
{:else if !shown.length}
  <div class="empty">
    <p class="e-title">ยังไม่มีรายการ{filter === "open" ? "ที่รอทบทวน" : ""}</p>
    <p class="muted">ลองสั่งยาใน <a href="/his/?hn=HN-0002&drug=simvastatin&dose=40">หน้าสั่งยา</a> แล้ว override คำเตือน รายการจะมาแสดงที่นี่</p>
  </div>
{:else}
  <ul class="list">
    {#each shown as [x, i] (x.time + x.finding_id + i)}
      <li class="item" class:done={x.status !== "open"}>
        <div class="i-top">
          <span class="status {TONE[x.indicator]}">{IND_TH[x.indicator]}</span>
          <span class="muted small num">{x.patient_id} · {time(x.time)}</span>
        </div>
        <h2 class="title">{x.summary}</h2>
        <p class="what">
          {#if x.outcome === "overridden"}
            แพทย์สั่งต่อ (override) เพราะ{x.reason}{#if x.comment} — “{x.comment}”{/if}
          {:else}
            แพทย์ทำตามคำแนะนำแล้ว
          {/if}
        </p>
        <div class="acts" role="group" aria-label={`สถานะ: ${x.summary}`}>
          <span class="muted small">{ST[x.status]}</span>
          <div class="segmented">
            <button type="button" aria-pressed={x.status === "reviewed"} onclick={() => setStatus(i, "reviewed")}>ทบทวนแล้ว</button>
            <button type="button" aria-pressed={x.status === "contacted-prescriber"} onclick={() => setStatus(i, "contacted-prescriber")}>ติดต่อแพทย์แล้ว</button>
          </div>
        </div>
      </li>
    {/each}
  </ul>
{/if}

<style>
  .head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin: 32px 0 8px; }
  .list { list-style: none; margin: 0; padding: 0; }
  .item { padding: 28px 0; border-bottom: 1px solid var(--line); }
  .item.done { opacity: .6; }
  .i-top { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
  .title { font-size: 19px; font-weight: 600; letter-spacing: 0; text-transform: none; color: var(--ink); margin-top: 8px; }
  .what { color: var(--ink-2); margin-top: 4px; }
  .acts { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
  .empty { padding: 72px 0; text-align: center; border-top: 1px solid var(--line); margin-top: 16px; }
  .e-title { font-size: 20px; margin-bottom: 6px; }
</style>
