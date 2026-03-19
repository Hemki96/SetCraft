#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_tool ruff
ruff_bin="$(resolve_command ruff)"

paths=(packages services apps tests)

info "Running ruff format"
"${ruff_bin}" format "${paths[@]}"

if command_exists shfmt; then
  info "Running shfmt"
  shfmt -w infra/scripts/*.sh
else
  warn "shfmt not found; skipping shell formatting"
fi
