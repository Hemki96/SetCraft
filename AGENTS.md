# AGENTS.md

## Zweck dieser Datei

Diese Datei definiert verbindliche Regeln für Codex und andere Coding-Agents, die in diesem Repository arbeiten.

Ziel ist, dass Agents:
- die Produktabsicht korrekt verstehen,
- Architektur und Qualitätsansprüche respektieren,
- keine spekulativen Großumbauten durchführen,
- kleine, saubere und überprüfbare Änderungen liefern.

## Produktkontext in Kurzform

Dieses Repository beschreibt eine selbst hostbare Plattform zur:
- Aufnahme unstrukturierter historischer Trainingspläne,
- automatischen Extraktion und Strukturierung,
- Speicherung in einer Trainingsdatenbank,
- Suche nach historischen Inhalten,
- Generierung neuer Sets, Einheiten und Wochenpläne auf Basis strukturierter Daten, Regeln und KI.

Fokusdomäne zu Beginn: **Schwimmtraining**

## Repo-Struktur

Wichtige Verzeichnisse:

- `docs/product/` – Produktdefinition und Anforderungen
- `docs/architecture/` – Architektur, Schnittstellen, Deployment, Sicherheit
- `docs/quality/` – Qualitätsanforderungen und Teststrategie
- `docs/ux/` – Systemnutzung, View-Spezifikation, Interaktionsmodell
- `docs/operations/` – CI/CD, Branching, Releases, Observability
- `apps/` – UI- und App-bezogene Komponenten
- `services/` – Backend- und Verarbeitungsdienste
- `packages/` – gemeinsam genutzte Domain- und Schema-Pakete
- `tests/` – Unit-, Integrations- und E2E-Tests
- `sample-data/` – Testdaten und Fixtures

## Welche Dateien zuerst gelesen werden müssen

Jeder Agent muss vor Änderungen mindestens diese Dateien lesen:

1. `README.md`
2. `AGENTS.md`
3. `docs/product/requirements.md`
4. `docs/architecture/system-overview.md`
5. `TASKS.md`

Bei Architektur- oder Datenmodelländerungen zusätzlich:
6. `docs/architecture/data-model.md`
7. `docs/architecture/api-design.md`
8. passende ADRs in `docs/architecture/adr/`

## Arbeitsmodus für Agents

### Grundsatz
Nicht raten. Nicht halluzinieren. Nicht implizit entscheiden, wenn eine Entscheidung fachlich oder architektonisch relevant ist.

### Erwartetes Vorgehen
1. Kontext lesen
2. betroffene Anforderungen identifizieren
3. kleinstmögliche sinnvolle Änderung planen
4. Änderung implementieren
5. Tests und Validierung durchführen
6. Ergebnis und Restrisiken klar dokumentieren

## Build-, Test- und Lint-Kommandos

Agents sollen diese Kommandos bevorzugen und keine ad-hoc Alternativen einführen:

```bash
make bootstrap
make dev
make test
make test-unit
make test-int
make lint
make format
make typecheck
```

Falls ein Kommando noch nicht existiert:
- nicht stillschweigend ersetzen,
- sondern fehlendes Kommando konsistent im Projekt ergänzen oder dokumentieren.

## Coding-Konventionen

### Allgemein
- kleine, fokussierte Commits
- keine unnötigen Abhängigkeiten
- klare Namen
- keine toten Pfade oder ungenutzten Artefakte
- keine „temporary hacks“ ohne explizite Markierung

### Python
- Typannotationen verpflichtend
- Pydantic für Ein-/Ausgabeschemata und Validierung
- klare Trennung zwischen API, Domain, Infrastruktur und Worker-Logik
- Business-Logik nicht in Controller/Route-Handler legen

### TypeScript / Frontend
- strikte Typisierung
- UI und fachliche Logik trennen
- keine API-Verträge im Frontend duplizieren, wenn shared schemas möglich sind
- Formular- und Review-Flows explizit modellieren

### Tests
- neue fachliche Logik immer mit Tests absichern
- Fehlerpfade und Grenzfälle testen
- keine Implementierung ohne zumindest minimale Verifikation

## Architekturprinzipien

- **structured data first**
- **rule-guided generation**
- **human review before trust**
- **source traceability**
- **clear separation of concerns**
- **self-hosted by default**
- **local-first development**
- **replaceable AI components**
- **auditability for generated content**

### Konkret
- Extraktion, Normalisierung, Suche, Generierung und Validierung sind getrennte Verantwortungen.
- Historische Quelldaten und generierte Inhalte dürfen nicht vermischt werden.
- Jede generierte Einheit muss als generiert gekennzeichnet sein.
- Extraktionsunsicherheit soll speicherbar sein.
- Datenmodell ist zentraler Vertrag des Systems.

## Sicherheitsregeln

- keine Secrets im Repo
- keine echten personenbezogenen oder sensiblen Produktionsdaten in Tests
- `.env.example` aktuell halten
- hochgeladene Dateien nie ungeprüft ausführen
- Dateityp, Größe und Inhalt validieren
- Pfadmanipulation und unsichere Dateizugriffe vermeiden
- keine stillen Fallbacks, wenn Sicherheitschecks fehlschlagen
- Zugriffe und kritische Änderungen nachvollziehbar loggen

## Dinge, die der Agent niemals tun soll

- keine großflächigen Refactorings ohne klaren Auftrag
- keine Architekturänderungen ohne Dokumentationsanpassung
- keine implizite Änderung fachlicher Regeln
- keine Löschung bestehender Dokumentation ohne Ersatz
- keine Einführung proprietärer Cloud-Abhängigkeiten ohne explizite Entscheidung
- keine „magische“ KI-Logik ohne nachvollziehbare Ein- und Ausgaben
- keine Speicherung generierter Inhalte als historische Originaldaten
- keine Umgehung von Qualitätschecks oder Freigabeschritten

## Definition of Done

Ein Task ist nur fertig, wenn:
- Anforderungen verstanden und berücksichtigt wurden
- Änderung minimal und zielgerichtet ist
- relevante Tests vorhanden und grün sind
- Linting und Typprüfung erfolgreich sind
- Dokumentation angepasst wurde, falls nötig
- keine bekannten Widersprüche offen bleiben
- Unsicherheiten explizit benannt wurden

## Review- und Verifikationsschritte

Vor Abschluss einer Änderung muss der Agent prüfen:

1. Passt die Änderung zu `requirements.md`?
2. Wurde die bestehende Architektur respektiert?
3. Ist die Änderung die kleinste sinnvolle Lösung?
4. Wurden Tests ergänzt oder angepasst?
5. Sind Fehler- und Grenzfälle berücksichtigt?
6. Wurden neue Annahmen dokumentiert?
7. Bleiben generierte und historische Daten sauber getrennt?
8. Ist Nachvollziehbarkeit gewährleistet?

## Verhalten bei Unsicherheit

Wenn Unsicherheit besteht:
- keine große spekulative Implementierung bauen
- Annahmen explizit dokumentieren
- lieber kleine vorbereitende Änderungen liefern
- TODOs nur mit Kontext und klarer Anschlussfähigkeit anlegen
- fehlende Entscheidungen in passende Doku-Dateien schreiben

## Priorisierung

Bevorzugt wird immer:

1. kleine saubere Änderung
2. saubere Schnittstelle
3. klare Tests
4. gute Dokumentation
5. erst danach Komfort oder Generalisierung

**Lieber kleiner und korrekt als groß und unklar.**
