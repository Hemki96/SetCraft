# ADR 0002 – Datenbank PostgreSQL mit pgvector

## Status
Accepted

## Kontext
Das System benötigt relationale Modellierung für Sessions, Blocks, Sets, Reviews und Freigaben sowie ergänzende semantische Suche.

## Entscheidung
Als primäre Datenbank wird **PostgreSQL** eingesetzt.  
Für semantische Suche wird **pgvector** als Erweiterung im selben Stack verwendet.

## Begründung
- einheitlicher Datenstack
- weniger Betriebsaufwand
- strukturierte und semantische Suche kombinierbar
- gute Grundlage für Migrationen und Erweiterung
