// Weekly time blocks for the Advices page. The same list draws the calendar and builds the .ics export.
// Aerobic 3 × 50 min = 150 min/week (WHO lower target) · resistance 2 days/week (WHO ≥ 2) · short movement breaks on workdays.
export type Kind = "aerobic" | "resistance" | "break";
export const KINDS: Record<Kind, { label: string; color: string; soft: string }> = {
  aerobic: { label: "Aerobic", color: "var(--accent)", soft: "var(--accent-soft)" },
  resistance: { label: "Resistance", color: "var(--good)", soft: "var(--good-soft)" },
  break: { label: "Movement break", color: "var(--warn)", soft: "var(--warn-soft)" },
};
export const DAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"] as const;
export const DAY_TH = ["จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"];
export type Block = { kind: Kind; title: string; days: (typeof DAYS)[number][]; start: string; end: string };
export const SCHEDULE: Block[] = [
  { kind: "aerobic", title: "เดินเร็ว / ปั่นจักรยาน 50 นาที", days: ["MO", "WE", "FR"], start: "07:00", end: "07:50" },
  { kind: "resistance", title: "เวทเทรนนิ่ง 45 นาที", days: ["TU", "SA"], start: "18:00", end: "18:45" },
  { kind: "break", title: "ลุกขยับ 10 นาที", days: ["MO", "TU", "WE", "TH", "FR"], start: "10:30", end: "10:40" },
  { kind: "break", title: "ลุกขยับ 10 นาที", days: ["MO", "TU", "WE", "TH", "FR"], start: "15:00", end: "15:10" },
];
export const HOURS = [6, 21] as const; // visible window
export const toMin = (t: string) => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
export const weeklyMinutes = (k: Kind) => SCHEDULE.filter((b) => b.kind === k).reduce((s, b) => s + (toMin(b.end) - toMin(b.start)) * b.days.length, 0);
