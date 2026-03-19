# API-Design

## API-Prinzipien

### 1. Ressourcenorientiert
Die API ist primär REST-orientiert.

### 2. Explizite Zustandsübergänge
Review, Freigabe und Generierung sind keine impliziten Nebeneffekte.

### 3. Asynchrone Jobs für teure Operationen
Upload-Verarbeitung, Extraktion, Embedding-Erzeugung, Generierung und Export laufen als Jobs.

### 4. Klare Trennung von historischen und generierten Daten
Es gibt keine Endpunkte, die generierte Inhalte als historische Einheiten maskieren.

### 5. Vorhersehbare Fehlerantworten
Fehler werden standardisiert zurückgegeben.

## Basisstruktur

### API-Version
`/api/v1`

### Hauptbereiche
- `auth`
- `health`
- `sources`
- `extractions`
- `sessions`
- `retrieval`
- `generation`
- `validation`
- `reviews`
- `exports`
- `admin`

## Wichtige Endpunkte
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/health`
- `POST /api/v1/sources`
- `GET /api/v1/sources` (optional Filter: `source_status`, `source_type`)
- `GET /api/v1/sources/{sourceId}`
- `POST /api/v1/sources/{sourceId}/reprocess`
- `GET /api/v1/sessions`
- `GET /api/v1/sessions/{sessionId}`
- `PATCH /api/v1/sessions/{sessionId}`
- `PATCH /api/v1/sessions/{sessionId}/blocks/{blockId}`
- `PATCH /api/v1/sessions/{sessionId}/blocks/{blockId}/sets/{setId}`
- `POST /api/v1/sessions/{sessionId}/review`
- `POST /api/v1/sessions/{sessionId}/approve`
- `GET /api/v1/retrieval/search`
- `POST /api/v1/generation/sessions`
- `POST /api/v1/generation/week-plans`
- `GET /api/v1/generation/plans/{generatedPlanId}`
- `POST /api/v1/generation/plans/{generatedPlanId}/approve`
- `POST /api/v1/exports`
- `GET /api/v1/exports/{exportJobId}`
- `GET /api/v1/exports/{exportJobId}/download`
