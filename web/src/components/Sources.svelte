<script lang="ts">
  import type { Fact } from "../lib/api";

  // One quiet "แหล่งอ้างอิง" link per item; details live in a popover.
  let { ids, facts, label = "แหล่งอ้างอิง" }: { ids: string[]; facts: Record<string, Fact>; label?: string } = $props();
  const uid = `src-${Math.random().toString(36).slice(2, 9)}`;
  const list = $derived(ids.map((id) => [id, facts[id]] as const).filter(([, f]) => f));
</script>

{#if list.length}
  <button type="button" class="link-btn src-btn" popovertarget={uid}>{label}</button>
  <div popover id={uid} class="src-pop">
    <h3>{label}</h3>
    <ul>
      {#each list as [id, f] (id)}
        <li>
          <p>{f.text}</p>
          <p class="meta">{f.source}{f.verified ? "" : " · ยังไม่ได้ตรวจถ้อยคำกับต้นฉบับ"}</p>
          <a href={f.url} target="_blank" rel="noopener">เปิดแหล่งที่มา<span class="sr-only"> (แท็บใหม่)</span></a>
        </li>
      {/each}
    </ul>
    <button type="button" class="btn btn-sm close" popovertarget={uid} popovertargetaction="hide">ปิด</button>
  </div>
{/if}

<style>
  .src-btn { font-size: 13.5px; }
  .src-pop h3 { font-size: 17px; margin-bottom: 12px; }
  ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 16px; }
  li { padding-bottom: 16px; border-bottom: 1px solid var(--line); }
  li p { font-size: 15px; }
  .meta { font-size: 13.5px; color: var(--ink-3); margin-top: 6px; }
  li a { display: inline-block; margin-top: 6px; font-size: 14px; }
  .close { margin-top: 16px; }
</style>
