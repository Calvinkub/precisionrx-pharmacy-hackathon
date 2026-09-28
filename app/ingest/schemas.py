"""Tier 1 — the central Structured Patient JSON and the agent PatientState.

Every value keeps its provenance (which document, which line/segment) so the audit trail in
Tier 4 can point back to it.
"""

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class Provenance(BaseModel):
    source: Literal["fhir", "hl7v2", "pdf", "nmr", "cfdna", "wearable", "claims", "manual", "dispensing"]
    document: str
    locator: str = ""  # e.g. "OBX|3", "page 1 line 12", "row 5"
    received_at: datetime | None = None


class Coding(BaseModel):
    system: str  # http://loinc.org | http://hl7.org/fhir/sid/icd-10 | ...
    code: str
    display: str = ""


class Observation(BaseModel):
    """A lab result normalized to a canonical unit (UCUM)."""
    key: str  # internal id, e.g. "ldl_c", "alt", "creatinine"
    name: str
    value: float
    unit: str  # UCUM, canonical for this key
    original_value: float | None = None
    original_unit: str | None = None
    coding: Coding | None = None
    effective: date | None = None
    provenance: Provenance
    flags: list[str] = Field(default_factory=list)  # "converted", "implausible", ...


class Condition(BaseModel):
    coding: Coding
    onset: date | None = None
    provenance: Provenance


class MedicationStatement(BaseModel):
    drug: str
    dose_mg: float | None = None
    sig: str = ""
    status: Literal["active", "stopped", "planned"] = "active"
    provenance: Provenance


class Metabolite(BaseModel):
    key: str  # catalog id when known, else normalized name
    name: str
    value: float
    unit: str
    interpreted: bool  # True = in our analyte catalog (has reference band / meaning)
    provenance: Provenance


class CfdnaProfile(BaseModel):
    """Fragment-size distribution from capillary electrophoresis (e.g. QIAxcel)."""
    sizes_bp: list[float]
    intensity: list[float]
    concentration_ng_ul: float | None = None
    instrument: str = ""
    provenance: Provenance


class LifestyleDay(BaseModel):
    day: date
    steps: int | None = None
    active_minutes: int | None = None
    resting_hr: int | None = None
    sleep_hours: float | None = None


class Claim(BaseModel):
    service_date: date
    coding: Coding
    description: str = ""
    provenance: Provenance


class Demographics(BaseModel):
    patient_id: str
    sex: Literal["male", "female"]
    birth_date: date | None = None
    age: int | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    waist_cm: float | None = None
    sbp: float | None = None
    dbp: float | None = None
    smoker: bool = False
    family_history_dm: bool = False
    alcohol_drinks_per_day: float = 0


class DataIssue(BaseModel):
    field: str
    kind: Literal["missing", "implausible", "unit_unknown", "unmapped", "stale", "duplicate"]
    detail: str
    severity: Literal["info", "warning", "blocking"] = "warning"


class PatientRecord(BaseModel):
    """Structured Patient JSON — output of Tier 1."""
    demographics: Demographics
    observations: list[Observation] = Field(default_factory=list)
    conditions: list[Condition] = Field(default_factory=list)
    medications: list[MedicationStatement] = Field(default_factory=list)
    metabolomics: list[Metabolite] = Field(default_factory=list)
    cfdna: CfdnaProfile | None = None
    lifestyle: list[LifestyleDay] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    issues: list[DataIssue] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)

    def obs(self, key: str) -> Observation | None:
        """Latest observation for a key."""
        found = [o for o in self.observations if o.key == key]
        return max(found, key=lambda o: o.effective or date.min) if found else None

    def value(self, key: str) -> float | None:
        o = self.obs(key)
        return o.value if o else None

    def has_condition(self, prefix: str) -> bool:
        return any(c.coding.code.upper().startswith(prefix.upper()) for c in self.conditions)


class AgentMessage(BaseModel):
    agent: str
    content: str
    at: datetime = Field(default_factory=datetime.now)


class ToolCall(BaseModel):
    tool: str
    args: dict[str, Any]
    output: Any
    agent: str


class PatientState(BaseModel):
    """Tier 2 shared state (LangGraph memory bus)."""
    patient_id: str
    raw_data: dict[str, Any] = Field(default_factory=dict)
    normalized_json: PatientRecord | None = None
    retrieved_evidence: list[dict[str, Any]] = Field(default_factory=list)
    intermediate_features: dict[str, Any] = Field(default_factory=dict)
    risk_vectors: list[dict[str, Any]] = Field(default_factory=list)
    agent_messages: list[AgentMessage] = Field(default_factory=list)
    tool_outputs: list[ToolCall] = Field(default_factory=list)
    execution_status: dict[str, str] = Field(default_factory=dict)  # node -> pending|done|skipped|error
    summary: dict[str, Any] = Field(default_factory=dict)
