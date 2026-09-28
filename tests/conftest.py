import os

# tests never call the Claude API; the deterministic fallback path is what CI checks
os.environ.setdefault("PRECISIONRX_LLM", "off")
