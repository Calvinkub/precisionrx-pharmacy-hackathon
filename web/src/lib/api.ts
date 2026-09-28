// Types mirror the FastAPI responses (app/assess.py, app/cds_hooks.py).

export interface Analyte {
  id: string; abbr: string; name: string; group: string; unit: string;
  ref_low: number | null; ref_high: number | null;
  cva: number | null; cvi: number | null; better: "lower" | "higher" | null;
  note?: string; ref_source?: string;
}
export interface Fact { text: string; source: string; url: string; level: string; verified: boolean }
export interface Visit { date: string; label?: string; values: Record<string, number> }
export interface Med { drug: string; dose_mg: number | null; pdc_pct: number | null; start_visit: number | null }
export interface Profile {
  age: number | null; sex: "male" | "female"; sbp: number | null;
  weight_kg: number | null; height_cm: number | null; waist_cm: number | null;
  smoker: boolean; diabetes: boolean; hypertension: boolean; family_history_dm: boolean;
  alcohol_drinks_per_day?: number; activity_min_week?: number | null;
}
export interface Case { id: string; label: string; story: string; profile: Profile; meds: Med[]; pgx: Record<string, string>; visits: Visit[] }

export interface Risk { id: string; disease: string; score_name: string; value: number | null; display: string; category: string; method: string; fact_ids: string[]; notes: string[] }
export interface Finding { id: string; category: string; severity: "stop" | "action" | "monitor" | "info"; title: string; detail: string; fact_ids: string[]; trace: string[] }
export interface NmrFactor { id: string; title: string; detail: string; severity: string; level: string; fact_ids: string[] }
export interface Advice { id: string; topic: string; reason: string; advice: string; fact_ids: string[] }
export interface TrendRow { id: string; abbr: string; unit: string; previous: number; current: number; pct_change: number; rcv_pct: number | null; verdict: Verdict }
export type Verdict = "improved" | "worsened" | "within_variation" | "changed" | "not_assessable";
export interface NmrDomain {
  id: string; title: string; what: string; status: "good" | "warning" | "serious" | "none"; status_label: string; headline: string;
  key: { id: string; abbr: string; name: string; unit: string; value: number; ref_low: number | null; ref_high: number | null;
         target: number | null; previous: number | null; pct_change: number | null; verdict: Verdict | null } | null;
  out_of_range: string[]; fact_ids: string[]; drug_note: string | null; drugs: string[];
}
export interface Assessment {
  snapshot: string; nmr_summary: NmrDomain[]; risks: Risk[]; nmr_factors: NmrFactor[]; findings: Finding[];
  advice: Advice[]; trend: TrendRow[]; facts: Record<string, Fact>;
  follow_up: { id: string; text: string; fact_ids: string[] }[];
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, init);
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json() as Promise<T>;
}
export const postJson = <T>(path: string, body: unknown) =>
  api<T>(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

export function fmt(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "–";
  const a = Math.abs(v);
  return a >= 100 ? v.toFixed(0) : a >= 10 ? v.toFixed(1) : v.toFixed(2);
}

export type Status = "normal" | "high" | "low";
export function status(a: Analyte, v: number): Status {
  if (a.ref_high != null && v > a.ref_high) return "high";
  if (a.ref_low != null && v < a.ref_low) return "low";
  return "normal";
}
export function refText(a: Analyte): string {
  if (a.ref_low != null && a.ref_high != null) return `${fmt(a.ref_low)}–${fmt(a.ref_high)}`;
  if (a.ref_high != null) return `< ${fmt(a.ref_high)}`;
  if (a.ref_low != null) return `> ${fmt(a.ref_low)}`;
  return "ไม่มีช่วงอ้างอิง";
}

export const VERDICT_TH: Record<Verdict, string> = {
  improved: "ดีขึ้นจริง", worsened: "แย่ลงจริง", within_variation: "อยู่ในความแปรปรวนปกติ",
  changed: "เปลี่ยนจริง", not_assessable: "ประเมินไม่ได้ (ไม่มี CVi)",
};
export const VERDICT_TONE: Record<Verdict, string> = {
  improved: "good", worsened: "critical", within_variation: "", changed: "info", not_assessable: "",
};
export const VERDICT_ICON: Record<Verdict, string> = {
  improved: "↗", worsened: "↘", within_variation: "≈", changed: "↔", not_assessable: "?",
};
export const CAT_TH: Record<string, string> = { low: "ต่ำ", moderate: "ปานกลาง", high: "สูง", very_high: "สูงมาก", not_assessable: "ประเมินไม่ได้" };
export const CAT_TONE: Record<string, string> = { low: "good", moderate: "warning", high: "serious", very_high: "critical", not_assessable: "" };
export const SEV_TH = { stop: "หยุด — ห้ามใช้", action: "ต้องทบทวน", monitor: "ติดตาม", info: "ปกติ" } as const;
export const SEV_TONE = { stop: "critical", action: "serious", monitor: "info", info: "good" } as const;
export const SEV_ICON = { stop: "⛔", action: "⚠", monitor: "!", info: "✓" } as const;
