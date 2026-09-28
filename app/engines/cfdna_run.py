"""cfDNA electropherogram run (e.g. QIAxcel Connect): replicates per blood-collection tube.

Summary follows the lab's own slide conventions:
  average size = mean main peak across replicates
  total amount (ng) = mean concentration (ng/µl) × elution volume (µl)
Alignment markers (15 bp lower, 3000 bp upper) are excluded before any area calculation.
External model scores (e.g. a research classifier) are displayed as provided, never re-interpreted.
"""

from statistics import mean, pstdev

from app.engines.cfdna_qc import analyse

MARKERS = (15.0, 3000.0)


def _strip_markers(sizes, rfu):
    out_s, out_r = [], []
    for s, r in zip(sizes, rfu):
        if any(abs(s - m) <= m * 0.08 for m in MARKERS):
            continue
        out_s.append(s); out_r.append(r)
    return out_s, out_r


def _cv(xs):
    return round(pstdev(xs) / mean(xs) * 100, 1) if len(xs) > 1 and mean(xs) else None


def summarize_tube(tube: dict, elution_ul: float) -> dict:
    reps = []
    for rep in tube["replicates"]:
        s, r = _strip_markers(rep["sizes_bp"], rep["rfu"])
        qc = analyse(s, r, rep.get("conc_ng_ul"))
        reps.append({"name": rep["name"], "main_peak_bp": rep.get("main_peak_bp") or qc["main_peak_bp"], "conc_ng_ul": rep.get("conc_ng_ul"),
                     "qc_status": qc["status"], "hmw_fraction": qc["hmw_fraction"], "short_fraction": qc["short_fraction"],
                     "sizes_bp": rep["sizes_bp"], "rfu": rep["rfu"]})
    peaks = [x["main_peak_bp"] for x in reps]
    concs = [x["conc_ng_ul"] for x in reps if x["conc_ng_ul"] is not None]
    return {"tube": tube["tube"], "tube_label": tube.get("tube_label", tube["tube"]),
            "average_size_bp": round(mean(peaks), 1), "peak_cv_pct": _cv(peaks),
            "mean_conc_ng_ul": round(mean(concs), 3) if concs else None, "conc_cv_pct": _cv(concs),
            "total_ng": round(mean(concs) * elution_ul, 2) if concs else None,
            "external_score": tube.get("external_score"), "replicates": reps,
            "qc_status": "fail" if any(x["qc_status"] == "fail" for x in reps) else "warning" if any(x["qc_status"] == "warning" for x in reps) else "pass"}


def summarize_run(run: dict) -> dict:
    ev = float(run.get("elution_ul", 12.5))
    tubes = [summarize_tube(t, ev) for t in run["tubes"]]
    return {**{k: v for k, v in run.items() if k != "tubes"}, "elution_ul": ev, "tubes": tubes,
            "fact_ids": ["CFDNA-NUCLEOSOME", "CFDNA-HMW-QC", "CFDNA-FRAGMENTOMICS-SEQ"]}
