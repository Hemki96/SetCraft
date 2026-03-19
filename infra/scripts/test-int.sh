#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_python312_venv
require_venv_tool pytest
pytest_bin="$(resolve_venv_tool pytest)"

if [[ ! -d tests/integration ]]; then
  info "No integration tests found (tests/integration)."
  exit 0
fi

info "Running integration tests"
PYTHONPATH="${ROOT_DIR}/packages/schemas/python:${ROOT_DIR}/services/api" \
  "${pytest_bin}" tests/integration "$@"
