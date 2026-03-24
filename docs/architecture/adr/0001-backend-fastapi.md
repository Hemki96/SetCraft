# ADR 0001 – Backend-Framework FastAPI

## Status
Accepted

## Kontext
Die Plattform benötigt ein API-zentriertes Backend mit klaren Request-/Response-Verträgen, guter Typisierung und sauberer Trennung zwischen API-, Domain- und Worker-Logik.

Relevante Anforderungen:
- `FR-003` Automatische Extraktion
- `FR-004` Strukturierung und Normalisierung
- `FR-010` Qualitäts- und Plausibilitätsprüfung
- `FR-011` Freigabeprozess

## Entscheidung
Als Backend-Framework wird **FastAPI** verwendet.

## Begründung
- API-zentrierte Architektur
- direkte Pydantic-Integration
- automatische OpenAPI-Dokumentation
- gute Testbarkeit

## Konsequenzen
- API-Verträge werden über Pydantic-Schemas zentral definiert.
- Asynchrone Fachprozesse (Extraktion, Generierung, Export) bleiben in dedizierten Worker-Prozessen; FastAPI orchestriert und exponiert den Status.
- Die Entscheidung ist kompatibel mit `Local-First, Server-Ready` aus `system-overview.md`.

## Open Questions
- Open Question: Welche Auth-Strategie wird für den MVP genutzt (`JWT`, Session-Cookie oder hybrid)?
- Open Question: Welche Rate-Limits und Request-Size-Limits werden für Upload- und Generierungsendpunkte im MVP verpflichtend?
