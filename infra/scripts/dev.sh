#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root

if ! command_exists docker; then
  error "Docker is required for local development services."
  exit 1
fi

compose_args=()
services=(db redis)

if [[ "${ENABLE_OLLAMA:-0}" == "1" ]]; then
  compose_args+=(--profile ai)
  services+=(ollama)
fi

if [[ "${ENABLE_APP_CONTAINERS:-0}" == "1" ]]; then
  compose_args+=(--profile app)
  services+=(api worker web)
fi

info "Starting local infrastructure: ${services[*]}"
run_compose "${compose_args[@]}" up -d --remove-orphans "${services[@]}"

info "Current compose status"
run_compose "${compose_args[@]}" ps

info "Development stack is ready"
info "Tip: set ENABLE_OLLAMA=1 to include local model runtime"
info "Tip: set ENABLE_APP_CONTAINERS=1 to include API/Web/Worker scaffold containers"
