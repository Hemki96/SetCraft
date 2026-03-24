# ADR 0002 – Primäre Datenbank PostgreSQL

## Status
Accepted

## Kontext
Das System benötigt eine relationale, migrationsfähige und auditierbare Persistenz für:
- historische Quellen und Metadaten
- strukturierte Trainingsdaten (`Session`, `Block`, `Set`)
- Review-/Freigabeobjekte
- generierte Inhalte mit klarer Trennung zu historischen Daten

## Entscheidung
Als primäre Datenbank wird **PostgreSQL** eingesetzt.

Die Entscheidung zur semantischen Retrieval-Strategie wird in einer separaten ADR geführt:
- `ADR 0005 – Vektorsuche im Retrieval mit pgvector (hybrid)`

## Begründung
- einheitlicher Datenstack
- weniger Betriebsaufwand
- gute Grundlage für Migrationen und Erweiterung
- starke Unterstützung für Constraints und Transaktionen (wichtig für Nachvollziehbarkeit und Freigabe-Workflows)

## Konsequenzen
- Schema-Entwicklung erfolgt migrationsbasiert.
- Historische Originaldaten und generierte Inhalte werden in getrennten Tabellen-/Objektkonzepten abgebildet.
- Relationale Integrität ist Teil des fachlichen Sicherheitsnetzes, nicht nur ein Infrastrukturdetail.

## Open Questions
- Open Question: Welche konkrete Backup-/Restore-Strategie ist für self-hosted MVP als Mindeststandard verpflichtend?
- Open Question: Welche Retention-Strategie gilt für große Upload-Originaldateien und Zwischenergebnisse der Extraktion?
