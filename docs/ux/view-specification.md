# View Specification

## Zweck dieses Dokuments

Dieses Dokument beschreibt jede zentrale View des Systems im Detail. Für jede View werden festgelegt:

- Route
- Ziel der View
- Zielnutzer
- Hauptobjekt
- sichtbare UI-Elemente
- Aktionen
- verknüpfte Funktionen / Backend-Endpunkte
- Zustände
- Fehlerfälle
- Berechtigungen

Dieses Dokument dient als direkte Grundlage für UI-Umsetzung, Routing, Komponentenstruktur und API-Anbindung.

---

# 1. Login View

## Route
`/login`

## Ziel
Anmeldung eines Nutzers am System.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- User Session

## Elemente
- Logo / Produkttitel
- Eingabefeld E-Mail
- Eingabefeld Passwort
- Button „Anmelden“
- Fehlermeldungsbereich
- optional Info bei laufender Session

## Aktionen
- Login absenden

## Verknüpfte Funktionen
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

## Zustände
- idle
- submitting
- success
- error

## Fehlerfälle
- ungültige Zugangsdaten
- Backend nicht erreichbar

## Berechtigungen
- öffentlich

---

# 2. Dashboard View

## Route
`/`

## Ziel
Schneller Einstieg in die wichtigsten Kernaufgaben.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekte
- offene Quellen
- offene Reviews
- letzte Generierungen
- letzte Exporte

## Elemente
- Header mit Hauptnavigation
- KPI-Karten:
  - offene Reviews
  - Quellen in Verarbeitung
  - letzte generierte Inhalte
  - Validierungswarnungen
- Schnellaktionen:
  - Neue Quelle hochladen
  - Sessions durchsuchen
  - Neue Einheit generieren
  - Wochenplan generieren
- Listen:
  - zuletzt hochgeladene Quellen
  - zuletzt bearbeitete Sessions
  - zuletzt generierte Pläne

## Aktionen
- Navigation zu Kernflows

## Verknüpfte Funktionen
- `GET /api/v1/sources?status=needs_review`
- `GET /api/v1/sessions?...`
- `GET /api/v1/generation/...` oder äquivalente Listenendpunkte

## Zustände
- loading
- empty
- populated
- error

## Fehlerfälle
- Teillisten laden nicht
- Netzwerkfehler

## Berechtigungen
- angemeldete Nutzer

---

# 3. Source Upload View

## Route
`/sources/upload`

## Ziel
Neue Quelle in das System bringen.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- SourceFile

## Elemente
- Seitenkopf mit Titel und Kurzbeschreibung
- Tabs oder Umschalter:
  - Datei hochladen
  - Text einfügen
- File Dropzone / Dateiauswahl
- Textarea für Freitext
- Hinweise:
  - erlaubte Formate
  - Dateigrößenlimit
  - Datenschutz-/Nutzungshinweis
- optional Metadatenfelder:
  - eigener Kommentar
  - grober Quellkontext
- Primärbutton „Upload starten“
- Sekundärbutton „Abbrechen“
- Status-/Progressbereich

## Aktionen
- Datei wählen
- Text einfügen
- Upload absenden

## Verknüpfte Funktionen
- `POST /api/v1/sources`

## Zustände
- idle
- file_selected
- validating
- uploading
- success
- error

## Fehlerfälle
- ungültiger Dateityp
- Datei zu groß
- leerer Text
- Uploadfehler

## Berechtigungen
- angemeldete Nutzer

---

# 4. Source List View

## Route
`/sources`

## Ziel
Überblick über alle importierten Quellen.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- SourceFile

## Elemente
- Filterleiste:
  - Status
  - Typ
  - Upload-Zeitraum
  - hochgeladen von
- Tabelle oder Listenansicht mit Spalten:
  - Dateiname
  - Typ
  - Status
  - Upload-Zeit
  - verknüpfte Sessions
  - letzter Fehler
- Suchfeld
- Link zu Upload-View

## Aktionen
- Quelle filtern
- Quelle öffnen
- Upload starten

## Verknüpfte Funktionen
- `GET /api/v1/sources`

## Zustände
- loading
- empty
- results
- error

## Fehlerfälle
- Liste nicht ladbar

## Berechtigungen
- angemeldete Nutzer

---

# 5. Source Detail View

## Route
`/sources/:sourceId`

## Ziel
Status, Verarbeitung und abgeleitete Inhalte einer Quelle einsehen.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- SourceFile

## Elemente
- Source Header:
  - Dateiname
  - Typ
  - Upload-Zeit
  - Statusbadge
- Bereich „Verarbeitung“
  - aktueller Status
  - Fehler/Warnungen
  - OCR verwendet ja/nein
  - Reprocess-Button
- Bereich „Extraktion“
  - Rohtext-Vorschau
  - Segmente-Vorschau
  - Confidence
- Bereich „Verknüpfte Sessions“
  - Liste der entstandenen Sessions
  - Links zur Detailansicht

## Aktionen
- Reprocessing auslösen
- Session öffnen

## Verknüpfte Funktionen
- `GET /api/v1/sources/{id}`
- `GET /api/v1/extractions/{id}`
- `POST /api/v1/sources/{id}/reprocess`

## Zustände
- loading
- extracted
- needs_review
- failed
- approved

## Fehlerfälle
- Quelle nicht gefunden
- Reprocessing fehlgeschlagen

## Berechtigungen
- angemeldete Nutzer

---

# 6. Session Search View

## Route
`/sessions`

## Ziel
Historische Sessions strukturiert durchsuchen.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- TrainingSession

## Elemente
- Suchfeld
- Filterpanel:
  - Fokus
  - Phase
  - Gruppe
  - Umfang min/max
  - Dauer min/max
  - Intensität
  - Schwimmart
  - Material
  - Herkunft historisch/generiert
- Ergebnisliste
- pro Treffer:
  - Titel/Kurzbeschreibung
  - Fokus
  - Umfang
  - Status
  - Quelle
  - Review-/Freigabestatus
  - Confidence-Hinweis optional
- Paginierung oder Infinite Scroll

## Aktionen
- Suche ausführen
- Filter setzen
- Session öffnen

## Verknüpfte Funktionen
- `GET /api/v1/sessions`
- optional `GET /api/v1/retrieval/search`

## Zustände
- idle
- loading
- no_results
- results
- error

## Fehlerfälle
- Suchanfrage fehlgeschlagen

## Berechtigungen
- angemeldete Nutzer

---

# 7. Session Detail / Review View

## Route
`/sessions/:sessionId`

## Ziel
Strukturierte Session ansehen, prüfen, korrigieren und freigeben.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- TrainingSession

## Elemente

### A. Header
- Titel
- Herkunft: historical / generated / manual
- Review-Status
- Freigabestatus
- Fokus
- Umfang
- Dauer
- Gruppe / Phase

### B. Aktionsleiste
- Bearbeiten
- Review speichern
- Freigeben
- Ablehnen
- Validierung ausführen
- Exportieren

### C. Session-Metadaten-Panel
- Fokus primär
- Fokus sekundär
- Gesamtmeter
- Dauer
- Phase
- Wettkampfbezug
- Notizen

### D. Blockliste
Pro Block:
- Reihenfolge
- Blocktyp
- Ziel
- Umfang
- Intensität
- Rohtext
- Normalisierte Beschreibung
- Editieren-Button

### E. Setliste je Block
Pro Set:
- Reihenfolge
- Kategorie
- Wiederholungen
- Distanz
- Pause/Abgang
- Intensität
- Schwimmart
- Material
- Rohtext
- Normalisierte Beschreibung
- Confidence
- Editieren-Button

### F. Rohtext-/Quellbereich
- Rohtext der Quelle
- Link zur Source Detail View

### G. Validierungsbereich
- Warnungen
- Fehler
- Hinweise

### H. Review-Historie
- wer reviewed/freigegeben hat
- Kommentare
- Zeitstempel

## Aktionen
- Session patchen
- Block patchen
- Set patchen
- Review speichern
- Freigeben
- Validierung neu ausführen
- Export auslösen

## Verknüpfte Funktionen
- `GET /api/v1/sessions/{id}`
- `PATCH /api/v1/sessions/{id}`
- `PATCH /api/v1/sessions/{id}/blocks/{blockId}`
- `PATCH /api/v1/sessions/{id}/blocks/{blockId}/sets/{setId}`
- `POST /api/v1/sessions/{id}/review`
- `POST /api/v1/sessions/{id}/approve`
- `POST /api/v1/validation/session/{id}/run`
- `POST /api/v1/exports`

## Zustände
- loading
- read_only
- editing
- saving
- reviewed
- approved
- rejected
- validation_warning
- validation_failed

## Fehlerfälle
- Session nicht gefunden
- Patch fehlgeschlagen
- Freigabe nicht erlaubt
- Validierung schlägt fehl

## Berechtigungen
- Trainer/Admin
- Freigabe nur gemäß Rollenmodell

---

# 8. Generate Session View

## Route
`/generate/session`

## Ziel
Neue Einheit generieren.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- GenerationRequest (session)

## Elemente
- Formularbereich:
  - Zielgruppe
  - Fokus primär
  - Fokus sekundär
  - gewünschter Umfang
  - Toleranz
  - gewünschte Dauer
  - Phase
  - Wettkampfbezug
  - Material erlauben/verbieten
  - Freitext-Constraints
- Button „Generieren“
- Bereich „Verwendete Referenzen“ nach Jobabschluss
- Statusbereich für laufenden Job

## Aktionen
- Generierung starten

## Verknüpfte Funktionen
- `POST /api/v1/generation/sessions`
- `GET /api/v1/generation/requests/{id}`

## Zustände
- idle
- validating_input
- queued
- running
- completed
- failed

## Fehlerfälle
- ungültige Eingaben
- Generierung fehlgeschlagen

## Berechtigungen
- Trainer/Admin

---

# 9. Generate Week Plan View

## Route
`/generate/week-plan`

## Ziel
Wochenplan generieren.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- GenerationRequest (week_plan)

## Elemente
- Formularbereich:
  - Zielgruppe
  - Wochenumfang
  - Sessions pro Woche
  - Phase
  - Schwerpunktbeschreibung
  - Regenerationseinschränkungen
  - Materialeinschränkungen
  - Freitext-Constraints
- Button „Wochenplan generieren“
- Jobstatus
- nach Abschluss Link zum Ergebnis

## Aktionen
- Wochenplan generieren

## Verknüpfte Funktionen
- `POST /api/v1/generation/week-plans`
- `GET /api/v1/generation/requests/{id}`

## Zustände
- idle
- queued
- running
- completed
- failed

## Fehlerfälle
- Parameter unplausibel
- Job scheitert

## Berechtigungen
- Trainer/Admin

---

# 10. Generated Plan List View

## Route
`/generated`

## Ziel
Überblick über generierte Inhalte.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- GeneratedPlan

## Elemente
- Filter:
  - Typ
  - Status
  - Validierungsstatus
  - Ersteller
  - Zeitraum
- Liste mit:
  - Titel
  - Typ
  - Status
  - Validierungsstatus
  - erstellt am
  - requires_human_review
- Link zur Detailansicht

## Aktionen
- Filtern
- Detail öffnen

## Verknüpfte Funktionen
- empfohlener Listenendpunkt für Generated Plans
- oder generation request/result browse API

## Zustände
- loading
- empty
- results
- error

## Fehlerfälle
- Liste nicht ladbar

## Berechtigungen
- Trainer/Admin

---

# 11. Generated Plan Detail View

## Route
`/generated/:generatedPlanId`

## Ziel
Generierten Inhalt vollständig prüfen, validieren, freigeben, ablehnen und exportieren.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- GeneratedPlan

## Elemente

### A. Header
- Titel
- Typ
- Status
- Validierungsstatus
- Hinweis „Generiert“

### B. Aktionsleiste
- Erneut validieren
- Freigeben
- Ablehnen
- Exportieren
- Als Session speichern, falls Konzept vorgesehen

### C. Ergebnisbereich
- Zusammenfassung
- strukturierte Inhalte
- je nach Typ:
  - Set
  - Session
  - Wochenübersicht
- Referenzen / Quellenbasis

### D. Validierungsbereich
- Liste Warnungen/Fehler/Hinweise

### E. Review-/Freigabebereich
- Kommentar
- Historie
- Freigabestatus

## Aktionen
- Freigeben
- Ablehnen
- Validierung erneut ausführen
- Export starten

## Verknüpfte Funktionen
- `GET /api/v1/generation/plans/{id}`
- `POST /api/v1/generation/plans/{id}/approve`
- `POST /api/v1/generation/plans/{id}/reject`
- `POST /api/v1/validation/generated_plan/{id}/run`
- `POST /api/v1/exports`

## Zustände
- loading
- generated
- validation_warning
- validation_failed
- reviewed
- approved
- rejected
- exported

## Fehlerfälle
- Plan nicht gefunden
- Freigabe scheitert
- Export scheitert

## Berechtigungen
- Trainer/Admin

---

# 12. Export Status View

## Route
`/exports/:exportJobId`

## Ziel
Status und Ergebnis eines Exports anzeigen.

## Zielnutzer
- Trainer
- Admin

## Hauptobjekt
- ExportJob

## Elemente
- Exporttyp
- Zielobjekt
- Status
- Fehlerdetails falls vorhanden
- Download-Button bei Erfolg

## Aktionen
- Download

## Verknüpfte Funktionen
- `GET /api/v1/exports/{id}`
- `GET /api/v1/exports/{id}/download`

## Zustände
- queued
- running
- completed
- failed

## Fehlerfälle
- Export fehlgeschlagen
- Datei nicht mehr vorhanden

## Berechtigungen
- Trainer/Admin

---

# 13. Admin Reference Data View

## Route
`/admin/reference-data`

## Ziel
Pflege der Referenzdaten.

## Zielnutzer
- Admin

## Hauptobjekte
- Group
- SeasonPhase
- Equipment

## Elemente
- Tabs:
  - Gruppen
  - Phasen
  - Equipment
- Listen und einfache CRUD-Formulare

## Aktionen
- anlegen
- bearbeiten
- deaktivieren

## Verknüpfte Funktionen
- `GET /api/v1/admin/reference-data`
- `POST /api/v1/admin/groups`
- `POST /api/v1/admin/phases`
- `POST /api/v1/admin/equipment`

## Zustände
- loading
- empty
- editing
- saving
- error

## Fehlerfälle
- Duplikate
- ungültige Pflichtfelder

## Berechtigungen
- nur Admin
