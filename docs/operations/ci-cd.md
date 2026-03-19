# CI/CD-Empfehlung

## Ziel

Die CI/CD-Pipeline soll für den MVP vor allem:
- Qualitätsregeln erzwingen
- Regressionen früh sichtbar machen
- Build- und Testfähigkeit absichern
- spätere Deployments vorbereiten

## Empfohlene Mindestpipeline

### Bei jedem Pull Request
1. Checkout
2. Python-Abhängigkeiten installieren
3. Node-Abhängigkeiten installieren
4. Lint Backend
5. Lint Frontend
6. Typecheck Backend
7. Typecheck Frontend
8. Unit-Tests
9. relevante Integrationstests
10. optional Build-Check für Web und API

## Aktueller Stand im Repository-Fundament

- Workflow: `.github/workflows/quality.yml`
- Jobs: `lint`, `typecheck`, `test`
- Ausfuehrung ausschliesslich ueber die zentralen Make-Targets:
  - `make lint`
  - `make typecheck`
  - `make test`

Dadurch bleiben lokale Qualitaetspruefung und CI deckungsgleich.

### Vor Release
1. gesamte Test-Suite
2. E2E-Smoke-Tests
3. Container-Build
4. Doku-Konsistenzprüfung
5. manuelle Freigabe
