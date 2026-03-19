#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

if ! command_exists "${PYTHON_BIN}"; then
  error "Python 3.12 is required for this repository."
  error "Install Python 3.12, then rerun 'make bootstrap'."
  error "Optional override: PYTHON_BIN=/path/to/python3.12 make bootstrap"
  exit 1
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  info "Created .env from .env.example"
else
  info ".env already exists"
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  info "Creating Python virtual environment in ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

python_bin="${VENV_DIR}/bin/python"
pip_bin="${VENV_DIR}/bin/pip"

info "Upgrading pip tooling"
"${python_bin}" -m pip install --upgrade pip setuptools wheel

if [[ -f pyproject.toml ]]; then
  info "Installing project with dev dependencies from pyproject.toml"
  "${pip_bin}" install -e ".[dev]"
else
  warn "No pyproject.toml found; skipping dependency installation"
fi

if command_exists npm && [[ -f apps/web/package.json ]]; then
  info "Installing frontend dependencies in apps/web"
  npm --prefix apps/web install
else
  warn "npm or apps/web/package.json missing; skipping frontend dependency install"
fi

if command_exists docker; then
  info "Docker detected: $(docker --version)"
else
  warn "Docker not found. Install Docker Desktop before running 'make dev'."
fi

info "Resolved tool versions"
info "python: $("${python_bin}" --version 2>&1)"
info "pip: $("${pip_bin}" --version 2>&1)"

for tool in pytest ruff mypy; do
  if tool_path="$(resolve_command "${tool}")"; then
    info "${tool}: $("${tool_path}" --version 2>&1 | head -n 1)"
  else
    warn "${tool}: not found in .venv or PATH"
  fi
done

if compose_available; then
  if command_exists docker && docker compose version >/dev/null 2>&1; then
    info "compose: $(docker compose version)"
  else
    info "compose: $(docker-compose version | head -n 1)"
  fi
else
  warn "compose: not found (required by 'make dev' and 'make verify-foundation')"
fi

info "Bootstrap complete"
