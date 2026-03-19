#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root

if [[ ! -d sample-data ]]; then
  warn "No sample-data directory found."
  exit 0
fi

info "Sample data directory is present at ./sample-data"
info "Seed pipeline is not implemented yet; no data was imported."
