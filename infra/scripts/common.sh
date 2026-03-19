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

resolve_venv_tool() {
  local cmd="$1"
  local tool_path="${VENV_DIR}/bin/${cmd}"
  if [[ -x "${tool_path}" ]]; then
    echo "${tool_path}"
    return 0
  fi
  return 1
}

require_command() {
  local cmd="$1"
  local hint="${2:-}"
  if ! command_exists "${cmd}"; then
    error "Missing command '${cmd}'."
    if [[ -n "${hint}" ]]; then
      error "${hint}"
    fi
    return 1
  fi
}

require_tool() {
  local cmd="$1"
  if ! resolve_command "${cmd}" >/dev/null; then
    error "Missing tool '${cmd}'."
    error "Run 'make bootstrap' with Python 3.12 to install development tools."
    return 1
  fi
}

require_venv_tool() {
  local cmd="$1"
  if ! resolve_venv_tool "${cmd}" >/dev/null; then
    error "Missing venv tool '${cmd}'."
    error "Run 'make bootstrap' with Python 3.12 to install development tools."
    return 1
  fi
}

require_python312_venv() {
  local python_bin="${VENV_DIR}/bin/python"
  if [[ ! -x "${python_bin}" ]]; then
    error "Missing virtualenv python at '${python_bin}'."
    error "Run 'make bootstrap' with Python 3.12 first."
    return 1
  fi

  local version
  version="$("${python_bin}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  if [[ "${version}" != "3.12" ]]; then
    error "Expected Python 3.12 in .venv, found ${version}."
    error "Re-run bootstrap with Python 3.12."
    return 1
  fi
}

compose_available() {
  if command_exists docker && docker compose version >/dev/null 2>&1; then
    return 0
  fi

  if command_exists docker-compose; then
    return 0
  fi

  return 1
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

  error "Docker Compose not found."
  error "Install Docker Desktop (recommended) or docker-compose, then rerun the command."
  return 1
}
