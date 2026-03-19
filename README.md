# Training Plan Platform

## Projektüberblick

Die Training Plan Platform ist eine selbst hostbare Plattform zur Verarbeitung historischer, unstrukturierter Trainingspläne und zur KI-gestützten Erstellung neuer Trainingsinhalte.

Das System ermöglicht es, alte Trainingspläne aus unstrukturierten Dateien zu importieren, automatisiert in ein fachlich konsistentes Datenmodell zu überführen, in einer Trainingsdatenbank zu speichern und anschließend für Suche, Wiederverwendung, Vorschläge und Generierung neuer Sets, Einheiten und Wochenpläne zu nutzen.

Das Produkt wird so aufgesetzt, dass es als professionelles Entwickler-Repository mit Codex und anderen Coding-Agents zuverlässig weiterentwickelt werden kann.

## Problem

Historische Trainingspläne liegen häufig in heterogenen, unstrukturierten Formaten vor, insbesondere als Word-Dokumente, PDFs oder Freitext. Dadurch entstehen folgende Probleme:

- Trainingswissen ist schwer auffindbar
- bewährte Sets und Planmuster sind nicht systematisch wiederverwendbar
- neue Trainingspläne werden oft manuell und redundant erstellt
- fachliche Logik und historische Qualität sind nicht datenbasiert nutzbar
- individuelle und gruppenspezifische Planung ist nur mit hohem Aufwand skalierbar

## Ziel

Ziel ist der Aufbau einer selbst entwickelten, möglichst kostenfreien bzw. selbst hostbaren Plattform, die:

1. unstrukturierte Trainingspläne importiert,
2. diese automatisiert analysiert und strukturiert,
3. als Trainingsdatenbank speichert,
4. relevante Inhalte durchsuchbar und filterbar macht,
5. daraus neue Sets, Einheiten, Wochenpläne und später längerfristige Planungen vorschlägt oder erzeugt,
6. dabei fachliche Regeln, Qualitätsprüfungen und Trainerfreigaben berücksichtigt.

## Kernfunktionen

### MVP
- Upload von DOCX, PDF und Copy-Paste-Text
- automatische Extraktion und Strukturierung historischer Trainingspläne
- Speicherung in einem domänenspezifischen Datenmodell
- Review- und Korrekturmöglichkeit für extrahierte Inhalte
- Suche und Filterung nach Trainingsmerkmalen
- Vorschläge für neue Sets und Einheiten
- Generierung von Wochenplänen
- Export generierter Inhalte
- Qualitäts- und Plausibilitätsprüfungen
- Trainerfreigabe vor produktiver Nutzung

### Spätere Ausbaustufen
- längerfristige Planungslogik über mehrere Wochen oder Monate
- Athletenverwaltung
- Leistungsdaten und Testwerte
- Wirksamkeitsbewertung historischer Inhalte
- teamfähige Kollaboration
- mobile Nutzung und feinere Rollenmodelle

## Zielgruppe

### Primäre Zielgruppe
- Schwimmtrainer
- Trainerteams
- leistungsorientierte Trainingsplaner

### Sekundäre Zielgruppe
- sportliche Leiter
- spätere administrative Nutzer
- perspektivisch Athleten im Read-only- oder Feedback-Modus

## Scope

### Im Scope
- Schwimmtraining als erste fachliche Domäne
- self-hosted Architektur
- lokale und serverfähige Ausführung
- strukturierte Speicherung von Einheiten, Blöcken und Sets
- KI-unterstützte, aber kontrollierte Generierung
- Auditierbarkeit von Herkunft und Freigabe

### Nicht-Ziele
- native Mobile-App im MVP
- Wearable- oder Live-Sensordatenintegration im MVP
- vollautonome Planerstellung ohne Trainerfreigabe
- komplexe Multi-Tenant-SaaS-Funktionalität im MVP
- generische Verbands- oder Verwaltungsplattform

## Fachliche Grundannahmen

- Historische Trainingspläne sind inhaltlich wertvoll, aber formal inkonsistent.
- Der größte Mehrwert entsteht durch die Strukturierung auf mehreren Ebenen:
  - Trainingseinheit
  - Trainingsblock
  - Set
- Generierung neuer Inhalte muss fachlich kontrolliert erfolgen.
- Generierte Inhalte sind von historischen Originalen klar zu unterscheiden.
- Nachvollziehbarkeit und manuelle Korrektur sind Pflicht.

## Lokales Setup

> Stand: Repository-Fundament. Implementierung folgt schrittweise.

### Voraussichtliche Kernkomponenten
- Python
- FastAPI
- PostgreSQL
- pgvector
- React
- lokales LLM über Ollama
- Docker Compose

### Ziel für lokale Entwicklung
```bash
make bootstrap
make dev
make test
make lint
```

## Wichtigste Kommandos

```bash
make bootstrap     # lokale Entwicklungsumgebung vorbereiten
make dev           # API, Worker und Web lokal starten
make test          # gesamte Test-Suite ausführen
make test-unit     # Unit-Tests ausführen
make test-int      # Integrationstests ausführen
make lint          # Linting ausführen
make format        # Code formatieren
make typecheck     # statische Typprüfung
make seed          # Beispiel-/Fixture-Daten einspielen
make clean         # lokale Build-Artefakte bereinigen
```

## Projektstatus

**Status:** Discovery / Repository Foundation

Bisher festgelegt:
- Produktziel
- MVP-Rahmen
- Architekturleitlinien
- initiale Repo-Struktur
- Aufgabenpriorisierung
- Regeln für Coding-Agents

Noch offen:
- finale Datenmodell-Tiefe
- genaue API-Verträge
- Extraktions- und Normalisierungsstrategie im Detail
- Qualitätsregelwerk
- UI-Scope des ersten MVP

## Leitprinzipien

- erst saubere Grundlagen, dann Implementierung
- kleine, verifizierbare Schritte
- fachliche Korrektheit vor KI-Komfort
- strukturierte Daten vor Freitext
- self-hosted und kostenarm by default
- nachvollziehbare Entscheidungen statt impliziter Annahmen
