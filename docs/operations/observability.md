# Observability und Logging – Grundlagen

## Ziel

Das System soll fachlich und technisch nachvollziehbar sein, ohne im MVP unnötig komplexe Observability-Infrastruktur aufzubauen.

## Mindestziele
- technische Fehler erkennen
- Verarbeitungsstatus nachvollziehen
- Audit-relevante Aktionen protokollieren
- Debugging für Import-, Review- und Generierungsflüsse unterstützen

## Log-Kategorien
- Application Logs
- Worker Logs
- Audit Logs

## Mindestfelder pro Logeintrag
- Zeitstempel
- Level
- Service
- Umgebung
- Request-ID oder Job-ID
- Nutzer-ID falls vorhanden
- betroffene Entität
- Nachricht
