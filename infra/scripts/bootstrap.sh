#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

if ! command_exists "${PYTHON_BIN}"; then
  error "Python 3.12 is required. Install Python 3.12 and retry."
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

if command_exists docker; then
  info "Docker detected: $(docker --version)"
else
  warn "Docker not found. 'make dev' requires Docker + Docker Compose."
fi

info "Bootstrap complete"
