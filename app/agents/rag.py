"""Guideline retrieval (Tier 3 `vector_db_search`).

Corpus = the verified evidence store (facts.yaml) + drug-effect interpretations — every chunk has
a source and URL, so any retrieved text is citable. Vectors are character 3-gram TF-IDF (works for
Thai, which has no spaces) with cosine similarity; no external embedding service, deterministic.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from functools import cache

from app.engines.drug_effects import _classes
from app.engines.panel import facts

DOMAINS = {  # fact-id prefix -> domain tag used for filtering
    "ADA": "diabetes", "TDRS": "diabetes", "HIRST": "diabetes", "BCAA": "diabetes", "PREISS": "diabetes",
    "TCVRS": "cardiovascular", "ESC": "cardiovascular", "RCPT": "cardiovascular", "OTVOS": "cardiovascular", "GLYCA": "cardiovascular",
    "WURTZ": "cardiovascular", "OMEGA3": "cardiovascular", "CHAN": "cardiovascular", "BALLANTYNE": "cardiovascular",
    "KDIGO": "kidney", "CKD": "kidney", "FIB4": "liver", "FLI": "liver", "METS": "metabolic", "THAI": "lifestyle", "WHO": "lifestyle",
    "CPIC": "pharmacogenomics", "LABEL": "drug-label", "ACR": "pharmacogenomics", "PQA": "adherence", "DISPENSING": "adherence",
    "RAZAVI": "oncology", "MANDELKER": "oncology", "CFDNA": "cfdna", "UKB": "reference", "NIGHTINGALE": "reference",
    "EFLM": "reference", "RCV": "reference", "ENGELBRECHTSEN": "diabetes",
}


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    url: str
    level: str
    domain: str


def _domain(fid: str) -> str:
    for prefix, d in DOMAINS.items():
        if fid.startswith(prefix):
            return d
    return "general"


def _grams(s: str) -> Counter:
    s = re.sub(r"\s+", " ", s.lower())
    return Counter(s[i:i + 3] for i in range(max(0, len(s) - 2)))


@cache
def index() -> tuple[list[Chunk], list[dict[str, float]], dict[str, float]]:
    chunks = [Chunk(fid, f["text"], f["source"], f["url"], f["level"], _domain(fid)) for fid, f in facts()["facts"].items()]
    for cid, c in _classes().items():
        chunks.append(Chunk(f"DRUGFX-{cid}", f"{c['label']}: {c['interpretation']}", "PrecisionRx drug-effect table",
                            "", "emerging", "drug-effects"))
    tfs = [_grams(f"{c.id} {c.text} {c.source}") for c in chunks]
    df = Counter(g for tf in tfs for g in tf)
    n = len(chunks)
    idf = {g: math.log((1 + n) / (1 + d)) + 1 for g, d in df.items()}
    vecs = []
    for tf in tfs:
        v = {g: c * idf[g] for g, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vecs.append({g: x / norm for g, x in v.items()})
    return chunks, vecs, idf


def search(query: str, domain: str | None = None, k: int = 5) -> list[dict]:
    chunks, vecs, idf = index()
    q = {g: c * idf.get(g, 0) for g, c in _grams(query).items()}
    qn = math.sqrt(sum(x * x for x in q.values())) or 1
    scored = []
    for c, v in zip(chunks, vecs):
        if domain and domain != "any" and c.domain != domain:
            continue
        s = sum(w / qn * v.get(g, 0) for g, w in q.items())
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return [{"fact_id": c.id, "score": round(s, 3), "text": c.text, "source": c.source, "url": c.url, "level": c.level,
             "domain": c.domain} for s, c in scored[:k]]
