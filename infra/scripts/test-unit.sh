#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_tool pytest
pytest_bin="$(resolve_command pytest)"

if [[ ! -d tests/unit ]]; then
  warn "No unit test directory found (tests/unit)."
  exit 0
fi

info "Running unit tests"
"${pytest_bin}" tests/unit "$@"
