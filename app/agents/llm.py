"""Claude calls for the two LLM roles (planner, summarizer). Everything else is code.

Both roles return structured JSON validated here; any failure (no credentials, network, refusal,
schema mismatch) falls back to a deterministic template so the demo never depends on the network.
Set PRECISIONRX_LLM=off to force the template.
"""

import json
import os

import anthropic

MODEL = os.environ.get("PRECISIONRX_MODEL", "claude-opus-5")
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def enabled() -> bool:
    return os.environ.get("PRECISIONRX_LLM", "on").lower() != "off"


def _call(system: str, user: str, schema: dict, effort: str = "low") -> tuple[dict | None, str]:
    """Returns (parsed JSON or None, status string)."""
    if not enabled():
        return None, "llm disabled (PRECISIONRX_LLM=off)"
    try:
        client = anthropic.Anthropic(max_retries=1, timeout=60.0)
        resp = client.beta.messages.create(
            model=MODEL,
            max_tokens=4000,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            system=system,
            messages=[{"role": "user", "content": user}],
            output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        )
    except anthropic.AuthenticationError:
        return None, "no valid Anthropic credentials"
    except anthropic.RateLimitError:
        return None, "rate limited"
    except anthropic.APIStatusError as e:
        return None, f"API error {e.status_code}"
    except anthropic.APIConnectionError:
        return None, "network unavailable"
    except TypeError:  # SDK raises before any request when no credential source is configured
        return None, "no Anthropic credentials configured — template used"
    except Exception as e:
        return None, f"llm unavailable: {type(e).__name__}"
    if resp.stop_reason == "refusal":
        return None, "model declined"
    text = next((b.text for b in resp.content if b.type == "text"), "")
    try:
        return json.loads(text), f"ok ({resp.model})"
    except json.JSONDecodeError:
        return None, "invalid JSON from model"


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "steps": {"type": "array", "items": {"type": "string", "enum": ["data_extraction", "risk_scoring", "clinical_reasoning", "cfdna_qc", "guideline_lookup", "care_plan", "summarizer"]}},
        "rationale": {"type": "string"},
    },
    "required": ["steps", "rationale"], "additionalProperties": False,
}


def plan(available: dict) -> tuple[dict | None, str]:
    system = ("You are the planner of a clinical decision-support pipeline for NCD risk screening. "
              "Choose which modules to run for this patient, in order, based only on which data sources are present. "
              "Rules: data_extraction first; risk_scoring before clinical_reasoning; run cfdna_qc only when a cfDNA "
              "electropherogram is present; guideline_lookup after reasoning; care_plan then summarizer last. "
              "Explain the choice in one or two short Thai sentences.")
    return _call(system, json.dumps({"available_sources": available}, ensure_ascii=False), PLAN_SCHEMA)


SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {"sentences": {"type": "array", "items": {"type": "object", "properties": {
        "text": {"type": "string"}, "fact_ids": {"type": "array", "items": {"type": "string"}}},
        "required": ["text", "fact_ids"], "additionalProperties": False}}},
    "required": ["sentences"], "additionalProperties": False,
}


def summarize(payload: dict) -> tuple[dict | None, str]:
    system = ("You write a short clinical summary in Thai for a physician from structured findings. "
              "Use ONLY the findings given. Every sentence must cite one or more fact_ids that appear in the "
              "input's allowed_fact_ids; never introduce numbers, drugs or diagnoses that are not in the input. "
              "At most 6 sentences. No treatment decisions — recommendations are for the clinician to review.")
    return _call(system, json.dumps(payload, ensure_ascii=False), SUMMARY_SCHEMA)
