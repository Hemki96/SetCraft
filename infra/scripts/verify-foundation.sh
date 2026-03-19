#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root

info "[1/5] Shell syntax check"
bash -n infra/scripts/*.sh

info "[2/5] Make target resolution (dry run)"
make -n bootstrap dev test lint format typecheck >/dev/null

info "[3/5] Compose YAML parse"
if command_exists ruby; then
  ruby -e 'require "yaml"; YAML.load_file("docker-compose.yml")'
else
  python3 - <<'PY'
import pathlib
import sys

try:
    import yaml
except ModuleNotFoundError:
    print("[setcraft][error] Missing parser: install ruby or pyyaml for YAML validation", file=sys.stderr)
    raise SystemExit(1)

with pathlib.Path("docker-compose.yml").open("r", encoding="utf-8") as fp:
    yaml.safe_load(fp)
PY
fi

info "[4/5] Compose config render"
if compose_available; then
  run_compose config >/dev/null
else
  error "Docker Compose is required for config render validation."
  error "Install Docker Desktop (or docker-compose) and rerun 'make verify-foundation'."
  exit 1
fi

info "[5/5] Scope reminder"
info "This verification mode validates operationalization only (no repo-wide feature test gates)."

info "Foundation verification passed"
