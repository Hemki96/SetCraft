#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"

run_from_root
require_python312_venv
require_venv_tool pytest

if ! compose_available; then
  error "Docker Compose is required for DB smoke validation."
  error "Install Docker Desktop (or docker-compose) and rerun 'make db-smoke'."
  exit 1
fi

pytest_bin="$(resolve_venv_tool pytest)"

db_name="${POSTGRES_DB:-training_plan_platform}"
db_user="${POSTGRES_USER:-postgres}"
db_password="${POSTGRES_PASSWORD:-postgres}"
db_host="${POSTGRES_HOST:-localhost}"
db_port="${POSTGRES_PORT:-5432}"

if [[ -z "${TEST_DATABASE_URL:-}" ]]; then
  export TEST_DATABASE_URL="postgresql+psycopg://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}"
  info "Using TEST_DATABASE_URL derived from local compose defaults"
fi

info "Starting PostgreSQL service for migration smoke test"
run_compose up -d db

info "Running integration DB smoke test"
PYTHONPATH="${ROOT_DIR}/packages/schemas/python:${ROOT_DIR}/services/api" \
  "${pytest_bin}" tests/integration/test_db_smoke.py "$@"

info "DB smoke test completed"
