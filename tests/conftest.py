from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "services" / "api"
SCHEMA_ROOT = REPO_ROOT / "packages" / "schemas" / "python"

for candidate in (API_ROOT, SCHEMA_ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)
