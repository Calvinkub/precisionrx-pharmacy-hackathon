<script lang="ts">
  let { cases, caseId, visits, visitIdx, onselect }: {
    cases: { id: string; label: string }[];
    caseId: string;
    visits: { date: string }[];
    visitIdx: number;
    onselect: (caseId: string, visitIdx: number) => void;
  } = $props();
  const name = `visit-${Math.random().toString(36).slice(2, 7)}`;
</script>

<div class="casebar">
  <label class="case-pick">
    <span>เคสตัวอย่าง</span>
    <select value={caseId} onchange={(e) => onselect((e.currentTarget as HTMLSelectElement).value, 0)}>
      {#each cases as c (c.id)}<option value={c.id}>{c.label}</option>{/each}
    </select>
  </label>
  {#if visits.length > 1}
    <fieldset class="segmented">
      <legend class="sr-only">ผลตรวจครั้งที่</legend>
      {#each visits as v, i (i)}
        <label><input type="radio" {name} checked={i === visitIdx} onchange={() => onselect(caseId, i)} />ครั้งที่ {i + 1}<span class="date">{v.date}</span></label>
      {/each}
    </fieldset>
  {:else if visits.length}
    <span class="muted small">ตรวจ {visits[0].date}</span>
  {/if}
</div>

<style>
  .casebar { display: flex; justify-content: space-between; align-items: center; gap: 12px 24px; flex-wrap: wrap; }
  .case-pick { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--ink-3); max-width: 100%; min-width: 0; }
  .case-pick > span { white-space: nowrap; }
  .case-pick select {
    appearance: none; border: 0; color: var(--ink-2); cursor: pointer; padding: 4px 22px 4px 0; max-width: 100%; min-width: 0;
    font: 500 14px/1.3 var(--font); background: none; text-overflow: ellipsis;
    background-image: linear-gradient(45deg, transparent 50%, var(--ink-3) 50%), linear-gradient(135deg, var(--ink-3) 50%, transparent 50%);
    background-position: right 7px center, right 2px center; background-size: 5px 5px; background-repeat: no-repeat;
  }
  .date { font-size: 12px; color: var(--ink-3); margin-left: 8px; }
</style>
