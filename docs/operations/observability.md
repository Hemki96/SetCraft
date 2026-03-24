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

## Audit-Events v1 (kritische Aktionen)
- `session.approve`: Freigabe einer Trainingseinheit
- `generated_plan.approve`: Freigabe eines generierten Plans
- `export.create`: Erzeugung eines Export-Jobs
- `export.download`: Download einer Export-Datei
- `auth.login`: erfolgreiche Anmeldung

## Pflichtfelder pro Audit-Event
- `event_id` (UUID)
- `event_type` (z. B. `approval`, `export`, `auth`)
- `action`
- `outcome` (`success`, `denied`, `rejected`, `failed`)
- `actor_user_id`
- `actor_role` (`admin`, `trainer`)
- `entity_type`
- `entity_id`
- `occurred_at` (UTC)
- `message`

## MVP-Policy
- Export ist nur für Inhalte mit `approval_status=approved` zulässig.
- Freigabeaktionen (`*.approve`) sind nur mit Rolle `admin` erlaubt.
- Abgelehnte Freigaben und Exportversuche werden als Audit-Event mit `outcome=denied` erfasst.
