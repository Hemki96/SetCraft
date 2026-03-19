# Interaction Model

## Zweck dieses Dokuments

Dieses Dokument definiert das Interaktions-, Zustands- und Feedbackmodell der Oberfläche. Es legt fest, wie das System auf Nutzeraktionen reagiert und wie Status, Warnungen und Fehler dargestellt werden sollen.

---

## 1. Kernprinzipien

### 1.1 Sichtbarkeit vor Überraschung
Das System muss jederzeit klar machen:
- was gerade passiert
- welcher Status vorliegt
- welche Aktion möglich ist
- welche Konsequenz eine Aktion hat

### 1.2 Keine stillen Statuswechsel
Review, Freigabe und Ablehnung müssen immer bewusst ausgelöst werden.

### 1.3 Wichtige Objekte sind immer klar typisiert
- historische Session
- generierter Plan
- Quelle

Diese Typen müssen in der Oberfläche erkennbar sein.

### 1.4 Warnungen und Fehler unterscheiden
Warnung = prüfbedürftig  
Fehler = blockierend oder kritisch

---

## 2. Standardzustände je View

Jede datengetriebene View soll diese Zustände explizit behandeln:

- loading
- empty
- success / populated
- error

Zusätzliche Zustände je Kontext:
- saving
- queued
- running
- validation_warning
- validation_failed
- reviewed
- approved
- rejected

---

## 3. Statusdarstellung

## 3.1 Quellenstatus
Empfohlene Darstellung:
- uploaded
- queued
- extracting
- extracted
- normalizing
- needs_review
- approved
- rejected
- failed

UX-Regel:
Jeder Status erhält
- Textlabel
- visuelles Badge
- optional Icon
- kurze Erklärung im Tooltip

## 3.2 Sessionstatus
Zwei Statusfamilien sichtbar machen:
- Reviewstatus
- Freigabestatus

Beide dürfen nicht visuell vermischt werden.

## 3.3 Generierter Plan
Immer sichtbar:
- Planstatus
- Validierungsstatus
- generiert-Hinweis
- Freigabebedarf

---

## 4. Standardaktionen und deren UX-Verhalten

## 4.1 Speichern
- Button wird während Request deaktiviert
- Erfolgsmeldung sichtbar
- Fehler klar beschreiben
- Formulardaten nicht verlieren

## 4.2 Review speichern
- optional Kommentarfeld
- nach Erfolg Status aktualisieren
- Audit-Hinweis nicht prominent, aber nachvollziehbar

## 4.3 Freigeben
- bewusste Primäraktion
- Confirmation Dialog empfohlen
- nach Erfolg sichtbarer Statuswechsel
- Folgeaktionen wie Export freischalten

## 4.4 Ablehnen
- Kommentar empfohlen
- Statuswechsel sichtbar
- spätere Wiederbearbeitung weiter möglich

## 4.5 Reprocessing
- nur dort sichtbar, wo fachlich sinnvoll
- Confirmation Dialog empfohlen
- bisherige Ergebnisse nicht stillschweigend unkenntlich machen

## 4.6 Generierung starten
- Formular validieren
- Jobstatus sichtbar
- Ergebnisansicht nach Abschluss anbieten
- laufende Jobs klar kenntlich machen

## 4.7 Exportieren
- nur für zulässige Zustände aktiv
- Jobstatus anzeigen
- Downloadzustand klar machen

---

## 5. Formverhalten

### Pflichtfelder
- deutlich kennzeichnen
- verständliche Fehlertexte

### Validierung
- möglichst sofort für einfache Formfehler
- serverseitig als Quelle der Wahrheit

### Editierbarkeit
- read mode und edit mode klar trennen
- Block-/Set-Edit nicht unnötig global machen
- Teiländerungen speichern können

---

## 6. Listenverhalten

### Listen müssen immer zeigen
- Kerndaten
- Status
- Navigationsmöglichkeit zur Detailansicht

### Filterverhalten
- aktive Filter sichtbar
- Filter leicht rücksetzbar
- Ergebnisse bei Filteränderung nachvollziehbar neu laden

---

## 7. Detailansichtsverhalten

Detailseiten sollen:
- oben Kerndaten und Status zeigen
- darunter strukturierte Inhalte
- Rohdaten, Validierung und Historie nachgelagert darstellen
- primäre Aktionen im sichtbaren Bereich halten

---

## 8. Fehlerkommunikation

### Nutzerfehler
Beispiel:
- ungültiger Dateityp
- Pflichtfeld fehlt
- Umfang negativ

Darstellung:
- nah am Eingabefeld oder in klarer Fehlermeldungsbox

### Systemfehler
Beispiel:
- Netzwerkfehler
- Worker fehlgeschlagen
- Export nicht erzeugbar

Darstellung:
- verständliche Meldung
- optional Fehler-ID / Request-ID
- keine internen Stacktraces im UI

---

## 9. Bestätigungen und Hinweise

### Bestätigung sinnvoll bei
- Freigabe
- Ablehnung
- Reprocessing
- potenziell verlustbehafteter Navigation bei ungespeicherten Änderungen

### Keine unnötige Bestätigung bei
- einfacher Navigation
- ungefährlichem Filterwechsel
- reiner Detailansicht

---

## 10. Historisch vs. generiert

Diese Unterscheidung muss in mehreren Ebenen sichtbar sein:
- Badge im Header
- Markierung in Listen
- Kennzeichnung im Exportkontext
- unterschiedliche Primäraktionen möglich

Historisch:
- Review / Korrektur / Freigabe historischer Referenz

Generiert:
- Review / Validierung / Freigabe / Export generierter Vorschlag

---

## 11. Mobile und responsive Grundregel

Auch wenn keine native Mobile-App im MVP vorgesehen ist, sollen zentrale Arbeitsflächen responsiv soweit bleiben, dass:
- Suche
- Session-Lesen
- Generierungsstatus
- einfache Freigaben

auch auf kleineren Screens grundsätzlich funktionieren.

Komplexe Review-Flows dürfen aber im MVP desktop-first optimiert werden.

---

## 12. Designfolgen für Implementierung

Das Frontend sollte Komponenten für diese wiederkehrenden Muster bereitstellen:

- StatusBadge
- ValidationSummary
- ReviewActionBar
- SourceStatusPanel
- SessionMetadataCard
- BlockCard
- SetRow
- RawTextPanel
- AuditTimeline
- ExportStatusCard
- GenerationRequestForm
- EmptyState
- ErrorState
- LoadingState
