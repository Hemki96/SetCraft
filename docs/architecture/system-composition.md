# System Composition

## Zweck dieses Dokuments

Dieses Dokument beschreibt den vollständigen Systemaufbau der Training Plan Platform aus Produkt-, Architektur- und Bedienungssicht. Ziel ist eine für Entwicklung und UX belastbare Gesamtsicht.

---

## 1. Gesamtziel des Systems

Die Plattform nimmt unstrukturierte historische Trainingspläne auf, analysiert sie, überführt sie in strukturierte Trainingsobjekte und nutzt diese Datenbasis für Suche, Wiederverwendung, Vorschläge und kontrollierte Generierung neuer Trainingsinhalte.

Das System ist als trainerzentriertes Arbeitswerkzeug ausgelegt. Es dient nicht dazu, fachliche Verantwortung zu automatisieren, sondern Trainingswissen technisch nutzbar und produktiv wiederverwendbar zu machen.

---

## 2. Systemschichten

## 2.1 Presentation Layer
Bestandteile:
- Web-Frontend für Trainer und Admins
- strukturierte Arbeitsoberflächen für Upload, Review, Suche, Generierung, Freigabe und Export

Verantwortung:
- Nutzerführung
- Darstellung von Status, Warnungen und Fehlern
- Eingabe von Generierungsparametern
- Editierbare Review-Oberflächen
- Navigation durch historische und generierte Inhalte

## 2.2 Application Layer
Bestandteile:
- API
- Authentifizierung
- Workflow-Orchestrierung
- Zustandsverwaltung
- Rechteprüfung

Verantwortung:
- alle UI-Aktionen in klar definierte Endpunkte übersetzen
- Zustand eines Objekts fachlich korrekt fortschreiben
- asynchrone Jobs anstoßen
- Auditierbarkeit sicherstellen

## 2.3 Domain Layer
Bestandteile:
- Session-, Block- und Set-Modelle
- Review-Logik
- Validierungslogik
- Generierungsverträge
- Statusmodelle

Verantwortung:
- fachliche Wahrheit und Regeln abbilden
- Trennung zwischen historischen und generierten Daten erzwingen
- Pflichtstruktur und Qualitätsregeln definieren

## 2.4 Processing Layer
Bestandteile:
- Ingestion
- Extraction
- Normalization
- Retrieval
- Generation
- Validation
- Export

Verantwortung:
- unstrukturierte Eingänge in nutzbare Fachobjekte überführen
- ähnliche Inhalte suchen
- neue Inhalte erzeugen
- Ergebnisse validieren
- Dokumente exportieren

## 2.5 Infrastructure Layer
Bestandteile:
- PostgreSQL
- pgvector
- Redis / Queue
- lokaler Dateispeicher
- lokales Modell-Gateway
- Containerbetrieb

Verantwortung:
- Persistenz
- Performance
- asynchrone Verarbeitung
- self-hosted Betrieb

---

## 3. Fachliche Hauptmodule

## 3.1 Source Management
Beschreibt alles rund um hochgeladene Quelldateien.

Funktionen:
- Upload von DOCX, PDF und Text
- Dateivalidierung
- Speicherung
- Reprocessing
- Statusdarstellung

Primäre Views:
- Source Upload
- Source List
- Source Detail

## 3.2 Extraction & Normalization
Verarbeitet Rohquellen zu strukturierten Domänenobjekten.

Funktionen:
- Rohtext-Extraktion
- Segmentierung
- Mapping auf Session, Block, Set
- Confidence-Bewertung
- Fehlermarkierung

Primäre Views:
- Source Detail
- Session Detail / Review

## 3.3 Historical Library
Stellt strukturierte historische Inhalte bereit.

Funktionen:
- Suche
- Filter
- Detailansichten
- Quellbezug
- Wiederverwendung als Referenz

Primäre Views:
- Session Search
- Session Detail

## 3.4 Review & Approval
Absicherung von Qualität und Nachvollziehbarkeit.

Funktionen:
- Korrektur von Sessions, Blocks und Sets
- Review-Status
- Freigabe
- Ablehnung
- Audit-Trail

Primäre Views:
- Session Detail / Review
- Generated Plan Detail

## 3.5 Generation
Erzeugt neue Inhalte auf Basis von Daten und Regeln.

Funktionen:
- Set-Generierung
- Session-Generierung
- Wochenplan-Generierung
- Referenzbasierter Kontext
- Kennzeichnung generierter Inhalte

Primäre Views:
- Generate Session
- Generate Week Plan
- Generated Plan Detail

## 3.6 Validation
Prüft Plausibilität und Regelkonformität.

Funktionen:
- Pflichtstrukturprüfung
- Umfangsprüfung
- Kennzeichnungsprüfung
- Warnungen und Fehler
- erneuter Validierungslauf

Primäre Views:
- Generated Plan Detail
- Session Detail / Review

## 3.7 Export
Macht Inhalte außerhalb des Systems nutzbar.

Funktionen:
- DOCX-Export
- JSON/API-Ausgabe
- später PDF
- Exportstatus
- Download

Primäre Views:
- Generated Plan Detail
- Export Status

---

## 4. Primäre Nutzerrollen

## 4.1 Trainer
Darf:
- Quellen hochladen
- Sessions reviewen und korrigieren
- suchen
- generieren
- validieren
- freigeben
- exportieren

## 4.2 Admin
Darf zusätzlich:
- Referenzdaten verwalten
- Nutzerrollen pflegen
- Systemeinstellungen einsehen
- Reprocessing und Wartungsaktionen steuern

---

## 5. Zentrale End-to-End-Kette

Die primäre Produktkette lautet:

1. Quelle hochladen
2. Quelle verarbeiten
3. strukturierte Sessions prüfen
4. Session korrigieren
5. Session freigeben
6. historische Inhalte durchsuchen
7. neue Einheit oder Woche generieren
8. Ergebnis validieren
9. Ergebnis prüfen und freigeben
10. Ergebnis exportieren

Diese Kette ist die wichtigste Leitlinie für UX, Architektur, API und Task-Priorisierung.

---

## 6. Hauptnavigation im Frontend

Empfohlene Hauptnavigation:

- Dashboard
- Quellen
- Sessions
- Generieren
  - Neue Einheit
  - Neuer Wochenplan
- Generierte Inhalte
- Exporte
- Admin (nur Admin)

Sekundäre Navigation kontextabhängig:
- Source Detail Tabs
- Session Detail Tabs
- Generated Plan Detail Tabs

---

## 7. Routing-Struktur

- `/login`
- `/`
- `/sources/upload`
- `/sources`
- `/sources/:sourceId`
- `/sessions`
- `/sessions/:sessionId`
- `/generate/session`
- `/generate/week-plan`
- `/generated`
- `/generated/:generatedPlanId`
- `/exports/:exportJobId`
- `/admin/reference-data`

---

## 8. Zustandsmodell über das System

## 8.1 Quelle
- uploaded
- queued
- extracting
- extracted
- normalizing
- needs_review
- approved
- rejected
- failed

## 8.2 Historische Session
Review:
- pending
- in_review
- reviewed
- corrected

Freigabe:
- draft
- approved
- rejected
- archived

## 8.3 Generierter Plan
- draft
- generated
- reviewed
- approved
- rejected
- exported

Validation:
- not_run
- passed
- warning
- failed

---

## 9. UI-Architekturprinzip

Die UI wird um drei Grundobjekte herum aufgebaut:

1. Quelle
2. Session
3. Generated Plan

Jede View muss genau wissen, welches dieser Grundobjekte sie primär bearbeitet.

Dadurch bleibt die Nutzerführung klar:
- Quelle = Eingang
- Session = strukturierte fachliche Wahrheit
- Generated Plan = neuer Vorschlag

---

## 10. Verbindung zwischen Frontend und Backend

## 10.1 Frontend-Aufrufe pro Modul
- Auth → `/auth/*`
- Upload / Sources → `/sources/*`
- Sessions / Review → `/sessions/*`
- Suche / Retrieval → `/retrieval/*`, `/sessions`
- Generierung → `/generation/*`
- Validierung → `/validation/*`
- Export → `/exports/*`

## 10.2 Grundregel
Jede wichtige UI-Aktion muss auf eine klar benannte Backend-Funktion zeigen. Es darf keine UX-Aktion geben, deren technische Wirkung unklar bleibt.

Beispiele:
- Klick auf „Review speichern“ → `POST /sessions/{id}/review`
- Klick auf „Freigeben“ → `POST /sessions/{id}/approve` oder `POST /generation/plans/{id}/approve`
- Klick auf „Erneut verarbeiten“ → `POST /sources/{id}/reprocess`

---

## 11. MVP-Grenzen für die UI

Im MVP bewusst nicht notwendig:
- native Mobile-App
- paralleles Bulk-Editing großer Datenmengen
- komplexe Kalenderansichten
- Echtzeit-Kollaboration
- Drag-and-drop-Planbaukasten mit vielen Interaktionsfreiheiten

Die MVP-Oberfläche soll primär ein klares, robustes Arbeitswerkzeug sein.

---

## 12. Entscheidende UX-/Architektur-Folgerung

Der Systemaufbau muss nicht auf „kreative KI-Ausgabe“ optimiert werden, sondern auf:

- Vertrauen
- Reviewbarkeit
- Nachvollziehbarkeit
- fachliche Korrektheit
- Wiederverwendbarkeit

Das beeinflusst direkt:
- Datenmodell
- Screen-Reihenfolge
- Statusdarstellung
- API-Struktur
- Logging
- Freigabemodell
