#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

info() {
  echo "[setcraft] $*"
}

warn() {
  echo "[setcraft][warn] $*" >&2
}

error() {
  echo "[setcraft][error] $*" >&2
}

run_from_root() {
  cd "${ROOT_DIR}"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

resolve_command() {
  local cmd="$1"

  if [[ -x "${VENV_DIR}/bin/${cmd}" ]]; then
    echo "${VENV_DIR}/bin/${cmd}"
    return 0
  fi

  if command_exists "${cmd}"; then
    command -v "${cmd}"
    return 0
  fi

  return 1
}

require_command() {
  local cmd="$1"
  if ! command_exists "${cmd}"; then
    error "Missing command '${cmd}'."
    return 1
  fi
}

require_tool() {
  local cmd="$1"
  if ! resolve_command "${cmd}" >/dev/null; then
    error "Missing tool '${cmd}'. Run 'make bootstrap' first."
    return 1
  fi
}

run_compose() {
  if command_exists docker && docker compose version >/dev/null 2>&1; then
    docker compose "$@"
    return 0
  fi

  if command_exists docker-compose; then
    docker-compose "$@"
    return 0
  fi

  error "Docker Compose not found. Install Docker Desktop (or docker-compose) first."
  return 1
}
