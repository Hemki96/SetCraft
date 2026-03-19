#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_python312_venv
require_venv_tool ruff
require_command npm
ruff_bin="$(resolve_venv_tool ruff)"

paths=(
  packages/schemas/python
  services/api
  tests/unit
  tests/fixtures
  infra/scripts
)

info "Running ruff check"
"${ruff_bin}" check "${paths[@]}"

if command_exists shellcheck; then
  info "Running shellcheck"
  shellcheck infra/scripts/*.sh
else
  warn "shellcheck not found; skipping shell script linting"
fi

info "Running frontend lint"
npm --prefix apps/web run lint
