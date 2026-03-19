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

Die konkrete Pipeline liegt unter `.github/workflows/quality.yml`.
