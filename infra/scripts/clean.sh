#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root

info "Removing local caches and build artifacts"
rm -rf .pytest_cache .mypy_cache .ruff_cache build dist coverage .coverage
find . -type d -name '__pycache__' -prune -exec rm -rf {} +

info "Clean complete"
