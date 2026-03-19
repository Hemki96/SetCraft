# Coding Standards

## Grundprinzipien
- Verständlichkeit vor Cleverness
- kleine, klar abgegrenzte Module
- explizite Typisierung
- Business-Logik nicht in Randbereichen verstecken
- Tests für relevante Fachlogik sind Pflicht
- keine impliziten Architekturentscheidungen im Code

## Python-Standards
- öffentliche Funktionen immer typannotieren
- Rückgabetypen explizit angeben
- `Any` vermeiden
- Pydantic für Request-/Response-Schemata
- Business-Logik nicht in Route-Handlern implementieren

## TypeScript-/Frontend-Standards
- `any` vermeiden
- API-Verträge typisiert halten
- Präsentationslogik und Datenlogik trennen
- große Container-Komponenten vermeiden

## Architekturbezogene Code-Regeln
- historische und generierte Inhalte nie vermischen
- Rohdaten und Normalform getrennt halten
- Fachregeln zentralisieren
- KI nur über definierte Adapter anbinden
- Side Effects isolieren
