<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../lib/api";

  interface Summary {
    cases: number; passed: number; expected_findings: number; omissions: number; false_flags: number;
    citations: number; citations_missing: number; unverified_fact_ids_cited: string[];
    alerts_per_case_naive: number; alerts_per_case_precisionrx: number; alert_reduction_pct: number;
  }
  let s = $state<Summary | null>(null);
  let failed = $state(false);
  onMount(async () => {
    try { s = (await api<{ summary: Summary }>("/api/eval")).summary; } catch { failed = true; }
  });
</script>

{#if s}
  <div class="hero-stat">
    <span class="label">จำนวนการเตือนต่อเคส</span>
    <span class="value">−{s.alert_reduction_pct}%</span>
    <span class="sub">{s.alerts_per_case_naive} → {s.alerts_per_case_precisionrx} เทียบกับระบบที่เตือนทุกข้อมูลที่มี</span>
  </div>
  <dl class="tiles">
    <div><dt>เคสที่ผ่าน</dt><dd>{s.passed}/{s.cases}</dd></div>
    <div><dt>การเตือนที่หลุด</dt><dd>{s.omissions}<small> / {s.expected_findings}</small></dd></div>
    <div><dt>เตือนผิด</dt><dd>{s.false_flags}</dd></div>
    <div><dt>การอ้างอิงที่ตรวจแล้ว</dt><dd>{s.citations - s.citations_missing}/{s.citations}</dd></div>
  </dl>
  <p class="note">ชุดทดสอบข้อมูลจำลอง 46 เคส เฉลยเขียนจาก guideline ก่อนรัน engine — วัดว่า rule ทำงานตามที่เขียน ไม่ใช่ความแม่นยำทางคลินิก · รอเภสัชกรตรวจเฉลย</p>
{:else if failed}
  <p class="note">โหลดผลชุดทดสอบไม่ได้ — รัน <code>uv run python -m eval.run_eval</code> ก่อน</p>
{:else}
  <p class="note">กำลังโหลดผลชุดทดสอบ…</p>
{/if}

<style>
  .hero-stat { display: grid; gap: 2px; margin-bottom: 18px; }
  .hero-stat .label { font-size: 14px; color: var(--ink-2); }
  .hero-stat .value { font-size: 56px; font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; }
  .hero-stat .sub { font-size: 13.5px; color: var(--ink-2); }
  .tiles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin: 0; }
  .tiles div { background: var(--sunken); border-radius: 12px; padding: 10px 14px; }
  dt { font-size: 12.5px; color: var(--ink-2); }
  dd { margin: 0; font-size: 22px; font-weight: 600; }
  dd small { font-size: 14px; color: var(--ink-3); font-weight: 500; }
  .note { font-size: 12.5px; color: var(--ink-3); margin-top: 12px; }
</style>
