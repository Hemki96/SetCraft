# Migration Workflow (P1-002)

Dieses Verzeichnis enthaelt die Alembic-Konfiguration fuer relationale Schema-Migrationen im MVP.

## Zielbild

- Relationale Kernobjekte fuer `SourceFile`, `TrainingSession`, `SessionBlock`, `TrainingSet`, `GeneratedPlan`, `ValidationResult`
- Trennung historischer und generierter Inhalte im Schema
- Reproduzierbarer Upgrade-/Downgrade-Workflow
- Testbarer Smoke-Check gegen PostgreSQL

## Voraussetzungen

- Python `3.12` (Projektstandard)
- virtuelle Umgebung via `make bootstrap`
- PostgreSQL lokal verfuegbar (typisch via `make dev`, Service `db`)

## Migrationen ausfuehren

Upgrade auf den aktuellen Stand:

```bash
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini upgrade head
```

Downgrade auf Basisstand:

```bash
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini downgrade base
```

Roundtrip pruefen:

```bash
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini upgrade head
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini downgrade base
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini upgrade head
```

## Neue Revision erstellen

Autogenerate (auf Basis ORM-Metadaten):

```bash
PYTHONPATH=services/api .venv/bin/alembic -c migrations/alembic.ini revision --autogenerate -m "kurze-beschreibung"
```

Manuelle Nachbearbeitung ist Pflicht:
- Constraint-Namen konsistent halten (Naming Conventions beachten)
- fachliche Invarianten als DB-Constraints absichern
- `downgrade()` vollstaendig pflegen

## Verifikation (Smoke)

Der verbindliche Smoke-Pfad ist:

```bash
make db-smoke
```

Der Smoke-Test in `tests/integration/test_db_smoke.py` prueft:
- Tabellenaufbau via Migration
- Persistierung zentraler Entitaeten
- Integritaets-Constraints (`is_generated=true`, Status-Constraints)
- Upgrade/Downgrade/Upgrade-Roundtrip
