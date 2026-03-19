# TASKS.md

## Zweck dieses Dokuments

Dieses Dokument beschreibt den priorisierten Initial-Backlog für den Aufbau des Projekts. Fokus ist ein fachlich tragfähiger MVP in sinnvoller Reihenfolge.

Grundsatz:
- erst belastbare Grundlagen
- dann Infrastruktur
- dann Datenmodell und Pipelines
- dann Generierung
- dann UI-Qualität und Exporte

## Priorisierung

### Priorität P0
Unverzichtbare Grundlage für saubere Implementierung

### Priorität P1
Unverzichtbar für MVP-Nutzbarkeit

### Priorität P2
Wichtig für MVP-Qualität und Alltagstauglichkeit

### Priorität P3
Nachgelagerte Optimierung oder Ausbau

## P0-001 Repo-Scaffold und Entwicklungsgrundlagen
**Ziel**  
Ein konsistentes, lokal startbares Repository-Grundgerüst schaffen.

**Kontext**  
Bevor fachliche Logik implementiert wird, braucht das Projekt eine belastbare Struktur für API, Web, Worker, Tests, Docs und Infrastruktur.

**Betroffene Dateien**
- `README.md`
- `AGENTS.md`
- `Makefile`
- `.gitignore`
- `.env.example`
- `docker-compose.yml`
- `apps/`
- `services/`
- `packages/`
- `tests/`

**Akzeptanzkriterien**
- Basisstruktur existiert
- lokale Entwicklungsumgebung ist dokumentiert
- zentrale Make-Kommandos sind definiert
- Docker-Compose-Setup ist vorbereitet
- keine unnötigen Technologien ohne Entscheidung eingeführt

## P0-002 Architektur- und ADR-Grundlagen anlegen
**Ziel**  
Zentrale Architekturentscheidungen explizit dokumentieren.

**Akzeptanzkriterien**
- erste ADRs für Backend, DB, Vektorsuche, lokales Modell und Frontend vorhanden
- offene Punkte explizit markiert
- Widersprüche zu README und Requirements aufgelöst

## P0-003 Domänenmodell v1 definieren
**Ziel**  
Ein minimales, aber tragfähiges Datenmodell für Quellen, Einheiten, Blöcke und Sets definieren.

**Akzeptanzkriterien**
- SourceFile modelliert
- TrainingSession modelliert
- SessionBlock modelliert
- TrainingSet modelliert
- GeneratedPlan modelliert
- Review- und Validation-Objekte berücksichtigt
- Rohdaten und normalisierte Daten sind getrennt denkbar

## P1-001 Backend-Basis mit API-Skelett
**Ziel**  
Ein erstes API-Skelett für Gesundheitscheck, Konfiguration und Basismodule bereitstellen.

## P1-002 Datenbank-Setup und Migration-Strategie
**Ziel**  
Relationale Datenbankstruktur für das MVP vorbereiten.

## P1-003 Sichere Upload-Pipeline
**Ziel**  
Dateien sicher annehmen, validieren und speichern.

## P1-004 Extraktionspipeline v1
**Ziel**  
Aus Quelldateien Rohtext und Segmentstruktur gewinnen.

## P1-005 Normalisierung in Domänenobjekte v1
**Ziel**  
Extrahierte Inhalte in Sessions, Blocks und Sets überführen.

## P1-006 Review- und Korrekturworkflow
**Ziel**  
Extrahierte Inhalte manuell prüfen und korrigieren können.

## P1-007 Suche und Filter v1
**Ziel**  
Historische Trainingsdaten strukturiert auffindbar machen.

## P1-008 Semantische Suche vorbereiten
**Ziel**  
Ähnliche Sets und Einheiten zusätzlich per Vektorsuche auffindbar machen.

## P1-009 Generierung neuer Sets v1
**Ziel**  
Auf Basis historischer Daten und Regeln neue Sets vorschlagen.

## P1-010 Generierung neuer Einheiten v1
**Ziel**  
Neue Trainingseinheiten aus Bausteinen, Regeln und historischen Referenzen erzeugen.

## P1-011 Wochenplangenerierung v1
**Ziel**  
Mehrere Einheiten in einem Wochenkontext erzeugen.

## P2-001 Validierungs- und Regel-Engine v1
**Ziel**  
Fachliche Qualitätsprüfungen zentralisieren.

## P2-002 Export v1
**Ziel**  
Freigegebene Inhalte in nutzbare Formate exportieren.

## P2-003 Rollen und Freigaben v1
**Ziel**  
Mindestens Admin- und Trainerrollen definieren.

## P2-004 Audit-Trail und Observability-Grundlagen
**Ziel**  
Wichtige Systemereignisse nachvollziehbar machen.

## P3-001 OCR-Fallback
**Ziel**  
Scan- oder bildbasierte Quellen unterstützbar machen.

## P3-002 Langfristige Planungslogik
**Ziel**  
Generierung über Wochen oder Monate fachlich unterstützen.

## Offene Punkte für frühe Präzisierung
- minimale Pflichtfelder pro Set
- Definition von Intensitätszonen
- Toleranzlogik für Umfang und Dauer
- Statusmodell für Review und Freigabe
- Exportlayout für Word/PDF
- Auswahl des ersten lokalen LLM/Embedding-Stacks
