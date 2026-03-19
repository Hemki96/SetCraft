#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_tool ruff
ruff_bin="$(resolve_command ruff)"

paths=(packages services apps tests infra/scripts)

info "Running ruff check"
"${ruff_bin}" check "${paths[@]}"

if command_exists shellcheck; then
  info "Running shellcheck"
  shellcheck infra/scripts/*.sh
else
  warn "shellcheck not found; skipping shell script linting"
fi
