# Testing Strategy

## Testziele

Die Tests sollen sicherstellen, dass:
- historische Daten korrekt verarbeitet werden
- Extraktion und Normalisierung nachvollziehbar bleiben
- Fachlogik nicht unbemerkt regressiert
- Generierung kontrolliert und validierbar bleibt
- Review- und Freigabeflüsse zuverlässig funktionieren
- API und UI für Kernflows stabil bleiben

## Testpyramide

### 1. Unit-Tests
- Domänenlogik
- Validierungsregeln
- Mapping-Funktionen
- Statuswechsel
- Hilfsfunktionen

### 2. Integrationstests
- API + DB
- Upload + Persistenz
- Extraktion + Normalisierung
- Retrieval
- Generierung + Validierung

### 3. End-to-End-Tests
- zentrale Nutzerflows
- UI und API gemeinsam
- Freigabe und Export-Grundpfade

## Mindest-E2E-Szenarien für MVP
- Historischen Plan importieren und reviewen
- Historische Einheit suchen
- Neue Einheit erzeugen
- Wochenplan erzeugen und exportieren
