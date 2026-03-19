#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_tool mypy
mypy_bin="$(resolve_command mypy)"

paths=(packages/schemas/python tests/unit)

info "Running mypy"
MYPYPATH="${ROOT_DIR}/packages/schemas/python" "${mypy_bin}" "${paths[@]}"
