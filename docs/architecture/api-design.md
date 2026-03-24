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

## Präzisierungen für offene MVP-Entscheidungen

### 1) Pflichtfelder pro Set (API-Vertrag)

Beim Schreiben von Sets (`PATCH /sessions/.../sets/{setId}`) sind mindestens erforderlich:
- `label`
- `repeat_count`
- `distance_m`
- `stroke`
- `intensity_zone`

Validierungsverhalten:
- fehlende Pflichtfelder -> `422` mit feldgenauer Fehlerliste
- unbekannte `stroke`-/`intensity_zone`-Werte -> `422`
- für generierte Sets ohne `sendoff_seconds` und ohne `rest_seconds` -> Validation-Warnung, kein harter Persistenzfehler

### 2) Intensitätszonen

Der API-Enum für `intensity_zone` ist fix auf:
- `z1`, `z2`, `z3`, `z4`, `z5`

Hinweis:
- UI-Labels sind lokalisierbar, aber API-Werte bleiben stabil.

### 3) Toleranzlogik Umfang/Dauer

`GET /api/v1/validation/{targetType}/{targetId}` liefert je Kennzahl:
- `metric`
- `target_value`
- `actual_value`
- `effective_allowed_deviation`
- `status` (`pass|warn|fail`)
- `rule_code`
- `message`

MVP-Defaults werden serverseitig versioniert und im Response als `tolerance_profile_version` ausgegeben.

### 4) Review-/Freigabe-Statusmodell

Explizite Zustandsübergänge:
- `POST /api/v1/sessions/{sessionId}/review/start`
- `POST /api/v1/sessions/{sessionId}/review/complete`
- `POST /api/v1/sessions/{sessionId}/submit-approval`
- `POST /api/v1/sessions/{sessionId}/approve`
- `POST /api/v1/sessions/{sessionId}/reject`

Analoge Endpunkte gelten für `generated_plan`.

Serverregeln:
- `approve` nur erlaubt, wenn `review_status IN (reviewed_with_changes, reviewed_ok)` und `approval_status=submitted`
- unzulässige Transition -> `409 Conflict` mit aktuellem Status im Body

### 5) Exportlayout Word/PDF

`POST /api/v1/exports` erhält:
- `target_type` (`session|generated_plan`)
- `target_id`
- `format` (`docx|pdf`)
- `layout_profile` (MVP: `standard_v1`)

Layoutvertrag `standard_v1`:
- Kopfbereich, Blockdarstellung, Set-Tabelle, Footer mit Summen und Freigabeinfo
- PDF basiert auf derselben semantischen Layoutstruktur wie DOCX

### 6) Erstes lokales LLM/Embedding-Setup

`GET /api/v1/admin/ai-config` liefert die aktive Modellbelegung:
- `generation_model`
- `embedding_model`
- `provider` (MVP: `ollama`)
- `config_version`

Auditanforderung:
- Generierungs- und Embedding-Jobs persistieren `model_name` und `model_version` pro Lauf.
