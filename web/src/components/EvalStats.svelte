<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../lib/api";

  interface Summary {
    cases: number; passed: number; expected_findings: number; omissions: number; false_flags: number;
    citations: number; citations_missing: number; alerts_per_case_naive: number; alerts_per_case_precisionrx: number; alert_reduction_pct: number;
  }
  let s = $state<Summary | null>(null);
  let failed = $state(false);
  onMount(async () => {
    try { s = (await api<{ summary: Summary }>("/api/eval")).summary; } catch { failed = true; }
  });
</script>

{#if s}
  <dl class="stats">
    <div><dt>การเตือนที่ลดลง</dt><dd>{Math.round(s.alert_reduction_pct)}%</dd><dd class="note">{s.alerts_per_case_naive} → {s.alerts_per_case_precisionrx} ต่อเคส</dd></div>
    <div><dt>เคสทดสอบที่ผ่าน</dt><dd>{s.passed}/{s.cases}</dd><dd class="note">ไม่มีการเตือนที่หลุดหรือเตือนผิด</dd></div>
    <div><dt>ข้อความที่มีแหล่งอ้างอิง</dt><dd>{s.citations - s.citations_missing}/{s.citations}</dd><dd class="note">ตรวจกับต้นฉบับแล้ว</dd></div>
  </dl>
  <p class="caveat">ชุดทดสอบข้อมูลจำลอง เฉลยเขียนจาก guideline ก่อนรันระบบ — วัดว่ากฎทำงานตามที่เขียน ยังไม่ใช่ความแม่นยำทางคลินิก</p>
{:else if failed}
  <p class="caveat">ยังไม่มีผลชุดทดสอบ</p>
{/if}

<style>
  .stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 0; }
  .stats div { padding: 0 32px; border-left: 1px solid var(--line); }
  .stats div:first-child { padding-left: 0; border-left: 0; }
  dt { font-size: 14px; color: var(--ink-3); }
  dd { margin: 0; font-size: clamp(36px, 4.5vw, 52px); font-weight: 500; letter-spacing: -0.02em; line-height: 1.2; font-variant-numeric: tabular-nums; }
  dd.note { font-size: 14px; color: var(--ink-2); letter-spacing: 0; font-weight: 400; line-height: 1.5; }
  .caveat { font-size: 13.5px; color: var(--ink-3); margin-top: 24px; }
  @media (max-width: 720px) {
    .stats { grid-template-columns: 1fr; gap: 24px; }
    .stats div { padding: 0; border-left: 0; }
  }
</style>
