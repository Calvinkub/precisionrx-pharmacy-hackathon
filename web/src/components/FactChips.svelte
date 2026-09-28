<script lang="ts">
  import type { Fact } from "../lib/api";

  let { ids, facts }: { ids: string[]; facts: Record<string, Fact> } = $props();
  const uid = Math.random().toString(36).slice(2, 8);
</script>

<ul class="facts" aria-label="หลักฐานอ้างอิง">
  {#each ids as id (id)}
    {@const f = facts[id]}
    <li>
      <button type="button" class="fact" class:unverified={f && !f.verified} popovertarget={`fact-${uid}-${id}`}>
        <span aria-hidden="true">§</span>{id}
      </button>
      {#if f}
        <div popover id={`fact-${uid}-${id}`} class="fact-pop">
          <p class="meta"><strong>{id}</strong> · {f.level}{#if !f.verified} · <em>ยังไม่ได้ตรวจถ้อยคำ</em>{/if}</p>
          <p>{f.text}</p>
          <p class="src">{f.source}</p>
          <div class="pop-actions">
            <a href={f.url} target="_blank" rel="noopener">เปิดแหล่งที่มา <span class="sr-only">(แท็บใหม่)</span>↗</a>
            <button type="button" class="btn btn-sm" popovertarget={`fact-${uid}-${id}`} popovertargetaction="hide">ปิด</button>
          </div>
        </div>
      {/if}
    </li>
  {/each}
</ul>

<style>
  .facts { display: flex; flex-wrap: wrap; gap: 6px; list-style: none; margin: 10px 0 0; padding: 0; }
  .fact {
    font: 500 11.5px/1 var(--mono); padding: 6px 8px; border-radius: 7px; cursor: pointer; min-height: 28px;
    border: 1px solid var(--border-strong); background: var(--raised); color: var(--ink-2);
    display: inline-flex; gap: 4px; align-items: center;
  }
  .fact:hover { color: var(--ink); border-color: var(--ink-3); }
  .fact.unverified { border-style: dashed; }
  .fact-pop p + p { margin-top: 6px; }
  .meta { font-size: 12px; color: var(--ink-3); }
  .src { font-size: 12.5px; color: var(--ink-2); }
  .pop-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; gap: 12px; }
  .pop-actions a { font-weight: 600; }
</style>
