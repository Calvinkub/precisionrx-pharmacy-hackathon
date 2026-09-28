// Shared case loading for every page: case + visit from the URL, regular meds from the dispensing
// record, profile edits kept per case in sessionStorage so they follow the user across pages.
import { api, postJson, type Assessment, type Case, type Med, type Profile } from "./api";

export interface RegularMed {
  drug: string; dose_mg: number | null; sig: string; first_fill: string; last_fill: string; fills: number;
  pdc_pct: number; status: "regular" | "new" | "stopped"; start_visit: number | null;
  class: string | null; label: string | null; interpretation: string; fact_ids: string[];
  effects: { analytes: string[]; ids: string[]; direction: "down" | "up" | "stable"; note: string | null }[];
}
export interface MedRecord { as_of: string; source: string; medications: RegularMed[]; facts: Assessment["facts"] }

export function readQuery(): { caseId: string | null; visit: number } {
  const q = new URLSearchParams(location.search);
  return { caseId: q.get("case"), visit: Math.max(1, Number(q.get("visit") ?? 0) || 0) };
}

export function writeQuery(caseId: string, visitIdx: number) {
  const u = new URL(location.href);
  u.searchParams.set("case", caseId);
  u.searchParams.set("visit", String(visitIdx + 1));
  history.replaceState(null, "", u);
  window.dispatchEvent(new CustomEvent("casechange", { detail: { caseId, visit: visitIdx + 1 } }));
}

const key = (caseId: string) => `prx:edits:${caseId}`;
export function loadEdits(caseId: string): { profile?: Profile; pgx?: Record<string, string> } {
  try { return JSON.parse(sessionStorage.getItem(key(caseId)) ?? "{}"); } catch { return {}; }
}
export function saveEdits(caseId: string, edits: { profile: Profile; pgx: Record<string, string> }) {
  try { sessionStorage.setItem(key(caseId), JSON.stringify(edits)); } catch { /* storage unavailable */ }
}

export const listCases = () => api<{ id: string; label: string; story: string }[]>("/api/cases");
export const getCase = (id: string) => api<Case>(`/api/cases/${id}`);
export const getMeds = (id: string, visitIdx: number) => api<MedRecord>(`/api/cases/${id}/medications?visit=${visitIdx + 1}`);

export function medsForAssess(rec: MedRecord): Med[] {
  return rec.medications.filter((m) => m.status !== "stopped").map((m) => ({
    drug: m.drug, dose_mg: m.dose_mg, pdc_pct: m.status === "new" ? null : m.pdc_pct, start_visit: m.start_visit,
  }));
}

export async function runAssess(c: Case, visitIdx: number, meds: Med[], profile: Profile, pgx: Record<string, string>) {
  const n = (x: unknown) => (x === "" || x == null ? null : Number(x));
  return postJson<Assessment>("/api/assess", {
    profile: { ...profile, age: n(profile.age), sbp: n(profile.sbp), weight_kg: n(profile.weight_kg), height_cm: n(profile.height_cm), waist_cm: n(profile.waist_cm) },
    meds: meds.filter((m) => m.drug.trim()).map((m) => ({ ...m, dose_mg: n(m.dose_mg), pdc_pct: n(m.pdc_pct) })),
    pgx: Object.fromEntries(Object.entries(pgx).filter(([, v]) => v)),
    alcohol_drinks_per_day: n(profile.alcohol_drinks_per_day) ?? 0,
    activity_min_week: n(profile.activity_min_week),
    visits: c.visits.slice(0, visitIdx + 1),
  });
}

/** Load everything a page needs for one case + visit. */
export async function loadAll(caseId: string, visitIdx: number) {
  const c = await getCase(caseId);
  const v = Math.min(visitIdx, c.visits.length - 1);
  const rec = await getMeds(caseId, v);
  const edits = loadEdits(caseId);
  const profile = { ...c.profile, ...(edits.profile ?? {}) };
  const pgx = { ...c.pgx, ...(edits.pgx ?? {}) };
  const meds = medsForAssess(rec);
  const r = await runAssess(c, v, meds, profile, pgx);
  return { c, visitIdx: v, rec, profile, pgx, meds, r };
}
