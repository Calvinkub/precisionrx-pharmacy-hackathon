import mock from "../data/mockPatient.json";
import { ClipboardList, Dna, FlaskConical, Magnet, Stethoscope } from "@lucide/astro";

export const SOURCES = mock.sources;
export const ICONS = { form: ClipboardList, clinic: Stethoscope, lab: FlaskConical, nmr: Magnet, ce: Dna } as const;
export const source = (no: number) => SOURCES.find((s) => s.no === no)!;
