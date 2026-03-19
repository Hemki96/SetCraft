# API Service

Minimales FastAPI-Scaffold fuer den Backend-Strang.

## Struktur

- `services/api/main.py` - ASGI-Einstiegspunkt
- `services/api/app/main.py` - App-Fabrik und Router-/Error-Wiring
- `services/api/app/api/` - Versionierte Routing-Struktur (`/api/v1`)
- `services/api/app/core/config.py` - Konfigurationslayer (Umgebungsvariablen)
- `services/api/app/core/errors.py` - Standardisierte Fehlerantworten
- `services/api/app/services/` - Service-Layer fuer Handler

## Vorhandene Endpunkte

- `GET /api/v1/health`

## Setup (lokal)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/api/requirements-dev.txt
```

## Datenbank und Migrationen

- Standard-DB-Konfiguration erfolgt ueber `POSTGRES_*` in `.env`.
- Optional kann `DATABASE_URL` gesetzt werden, um die Einzelwerte zu ueberschreiben.
- Alembic-Konfiguration liegt in `migrations/alembic.ini`.

Migrationen ausfuehren:

```bash
alembic -c migrations/alembic.ini upgrade head
```
