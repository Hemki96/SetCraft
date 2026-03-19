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
- `GET /api/v1/health/db`
- `POST /api/v1/auth/login` (Placeholder)
- `GET /api/v1/auth/me` (Placeholder)
- `POST /api/v1/sources` (Placeholder)
- `GET /api/v1/sources` (Placeholder)
- `GET /api/v1/sources/{sourceId}` (Placeholder)
- `POST /api/v1/sources/{sourceId}/reprocess` (Placeholder)
- `GET /api/v1/sessions` (Placeholder)
- `GET /api/v1/sessions/{sessionId}` (Placeholder)
- `GET /api/v1/retrieval/search` (Placeholder)

Diese Endpunkte liefern bewusst nur einen stabilen API-Rahmen ohne fachliche Business-Logik.
