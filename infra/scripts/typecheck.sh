#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_python312_venv
require_venv_tool mypy
require_command npm
mypy_bin="$(resolve_venv_tool mypy)"

paths=(packages/schemas/python services/api/app tests/unit)

info "Running mypy"
MYPYPATH="${ROOT_DIR}/packages/schemas/python:${ROOT_DIR}/services/api" "${mypy_bin}" "${paths[@]}"

info "Running frontend typecheck"
npm --prefix apps/web run typecheck
