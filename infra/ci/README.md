# CI Setup

Dieses Verzeichnis dokumentiert das minimale CI/Lint/Test-Setup fuer das Repository-Fundament.

## Ziel

- kleine, robuste Qualitaetspruefung fuer Pull Requests
- dieselben Kommandos lokal und in CI
- keine Fachlogik in CI-Skripten

## Verwendete Kommandos

- `make lint`
- `make typecheck`
- `make test`

## Lokale Qualitaetspruefung

- Python `3.12` ist verbindlich fuer die lokale `.venv`.
- Optional kann `pre-commit` genutzt werden:
  - `make lint`
  - `make typecheck`
  - `make test-unit`

Die konkrete Pipeline liegt unter `.github/workflows/quality.yml`.
