# System Usage

## Zweck dieses Dokuments

Dieses Dokument beschreibt die genaue Benutzung des Systems aus Sicht des primären Nutzers, also des Trainers. Es dokumentiert die empfohlene Reihenfolge, die Kernabläufe und die fachliche Nutzung des Systems im Alltag.

---

## 1. Grundidee der Nutzung

Das System wird in zwei Modi genutzt:

### Modus A – Historisches Wissen erschließen
Ziel:
- alte Trainingspläne importieren
- strukturieren
- prüfen
- als belastbare Bibliothek verfügbar machen

### Modus B – Neue Inhalte erstellen
Ziel:
- passende historische Inhalte finden
- daraus neue Sets, Einheiten oder Wochenpläne erzeugen
- prüfen
- freigeben
- exportieren

Diese beiden Modi hängen direkt zusammen. Ohne saubere Review der historischen Bibliothek verliert die Generierung an Qualität.

---

## 2. Empfohlene Reihenfolge für Erstnutzung

## Phase 1 – System vorbereiten
1. Admin oder Trainer meldet sich an
2. Referenzdaten prüfen:
   - Gruppen
   - Saisonphasen
   - Equipment
3. Dateiformate und Upload-Konventionen kennen

## Phase 2 – Historische Pläne importieren
1. Upload-Seite öffnen
2. Datei oder Text hochladen
3. Verarbeitungsstatus beobachten
4. verarbeitete Quellen öffnen

## Phase 3 – Strukturierte Inhalte reviewen
1. Session Detail öffnen
2. Session prüfen
3. Blockstruktur prüfen
4. Sets prüfen
5. Korrekturen speichern
6. Datensatz als reviewed markieren
7. bei fachlicher Eignung freigeben

## Phase 4 – Bibliothek nutzen
1. Session Search öffnen
2. nach Fokus, Phase, Umfang etc. filtern
3. relevante historische Inhalte als Referenz anschauen

## Phase 5 – Neue Inhalte erzeugen
1. Generierungsview öffnen
2. Parameter eingeben
3. Ergebnis prüfen
4. Warnungen und Validierung lesen
5. Inhalt überarbeiten oder freigeben

## Phase 6 – Exportieren
1. freigegebenen Inhalt öffnen
2. Export anstoßen
3. Ergebnis herunterladen

---

## 3. Täglicher Standardworkflow für Trainer

## 3.1 Historische Inhalte ergänzen
Dieser Ablauf wird genutzt, wenn neue Altbestände eingepflegt werden.

Schritte:
1. Quellen hochladen
2. Quelle in `needs_review` wechseln lassen
3. Session prüfen
4. Korrekturen vornehmen
5. Review speichern
6. Freigabe erteilen

Ziel:
- Bibliothek wächst kontrolliert
- Generierungsgrundlage verbessert sich

## 3.2 Neue Einheit erstellen
Dieser Ablauf wird genutzt, wenn eine neue Trainingseinheit geplant werden soll.

Schritte:
1. Session Search oder Generate Session öffnen
2. bei Bedarf erst historische Referenzen ansehen
3. Zielparameter festlegen
4. Generierung starten
5. Ergebnis prüfen
6. bei Warnungen korrigieren oder neu generieren
7. freigeben
8. exportieren

## 3.3 Wochenplan erstellen
Schritte:
1. Generate Week Plan öffnen
2. Wochenparameter setzen
3. Generierung starten
4. Woche als Übersicht prüfen
5. einzelne Einheiten in Detail öffnen
6. Validierung und Warnungen prüfen
7. freigeben
8. exportieren

---

## 4. Detaillierter Nutzungsablauf je Kernprozess

## 4.1 Quelle hochladen

### Ziel
Historischen Plan ins System bringen.

### Nutzeraktion
- Datei auswählen oder Text einfügen
- optional Metadaten ergänzen
- Upload bestätigen

### Systemreaktion
- Quelle wird angelegt
- Status wird sichtbar
- Job wird gestartet

### Nächster sinnvoller Schritt
- Quellenliste oder Quelldetail öffnen

---

## 4.2 Quelle nach Verarbeitung prüfen

### Ziel
Sicherstellen, dass aus der Quelle sinnvolle strukturierte Daten entstanden sind.

### Nutzeraktion
- Source Detail öffnen
- verknüpfte Sessions ansehen

### Systemreaktion
- Status, Fehler, Warnungen und verknüpfte Sessions werden angezeigt

### Nächster sinnvoller Schritt
- Session Detail / Review öffnen

---

## 4.3 Session reviewen

### Ziel
Aus automatisch extrahierten Daten einen fachlich belastbaren Datensatz machen.

### Nutzeraktion
- Fokus, Umfang, Phase, Blocktyp, Set-Beschreibungen prüfen
- fehlerhafte Felder korrigieren
- Review-Kommentar speichern

### Systemreaktion
- Änderungen werden protokolliert
- Status wechselt auf reviewed oder corrected

### Nächster sinnvoller Schritt
- Freigabe oder spätere Wiederbearbeitung

---

## 4.4 Historische Bibliothek durchsuchen

### Ziel
Passende Inhalte für neue Trainingsplanung finden.

### Nutzeraktion
- Suche nach Fokus, Umfang, Phase, Intensität, Material oder Freitext
- Treffer öffnen
- Sessionstruktur und Quelle lesen

### Systemreaktion
- Trefferliste mit Kontext anzeigen
- Detailansicht bereitstellen

### Nächster sinnvoller Schritt
- Referenz mental oder technisch in Generierung übernehmen

---

## 4.5 Neue Einheit generieren

### Ziel
Einen fachlich brauchbaren Vorschlag erzeugen.

### Nutzeraktion
- Gruppe, Fokus, Umfang, Dauer und Einschränkungen eingeben
- Generierung starten

### Systemreaktion
- passende historische Referenzen laden
- neue Einheit generieren
- Validierung durchführen
- Ergebnis + Warnungen + Referenzen anzeigen

### Nächster sinnvoller Schritt
- Review, Freigabe, Export

---

## 4.6 Wochenplan generieren

### Ziel
Mehrere Einheiten mit Wochenkontext erzeugen.

### Nutzeraktion
- Wochenvolumen, Anzahl Einheiten, Phasenbezug, Constraints eingeben
- Generierung starten

### Systemreaktion
- mehrere Einheiten generieren
- Wochenkontext validieren
- Übersicht + Details anzeigen

### Nächster sinnvoller Schritt
- Einheiten prüfen
- Plan freigeben
- exportieren

---

## 4.7 Freigeben

### Ziel
Einen Inhalt bewusst als nutzbar markieren.

### Nutzeraktion
- in Session Detail oder Generated Plan Detail auf Freigeben klicken
- Kommentar optional ergänzen

### Systemreaktion
- Freigabe protokollieren
- Status aktualisieren

### Nächster sinnvoller Schritt
- exportieren oder archivieren

---

## 4.8 Exportieren

### Ziel
Inhalt außerhalb des Systems verwenden.

### Nutzeraktion
- Exportformat wählen
- Export starten
- Datei herunterladen

### Systemreaktion
- Exportjob startet
- Status wechselt zu queued/running/completed
- Download wird freigegeben

---

## 5. Bedienregeln für den Nutzer

### Regel 1
Historische Inhalte möglichst immer reviewen, bevor sie als belastbare Referenz gelten.

### Regel 2
Generierte Inhalte nie ungeprüft als finale Trainingsplanung verwenden.

### Regel 3
Warnungen und Validierungsfehler nicht ignorieren.

### Regel 4
Generierte Inhalte fachlich an Zielgruppe, Phase und Kontext anpassen.

### Regel 5
Importe und Korrekturen möglichst früh und sauber durchführen, damit die Bibliothek langfristig an Qualität gewinnt.

---

## 6. Fehlersituationen und erwartetes Nutzerverhalten

## Upload schlägt fehl
Nutzer:
- Format, Größe und Datei prüfen
- verständliche Fehlermeldung lesen
- korrigiert erneut versuchen

## Extraktion unvollständig
Nutzer:
- Session Review öffnen
- fehlende Felder ergänzen
- bei gravierendem Fehler Reprocessing auslösen

## Generierung liefert Warnungen
Nutzer:
- Warnungen lesen
- Inhalt prüfen
- ggf. Parameter ändern und neu generieren

## Export schlägt fehl
Nutzer:
- Exportstatus prüfen
- erneut versuchen
- falls nötig anderen Exporttyp nutzen

---

## 7. Erfolgskriterium aus Nutzersicht

Der Nutzer muss in der Lage sein:

1. alte Inhalte schnell ins System zu bringen,
2. diese mit vertretbarem Aufwand zu korrigieren,
3. relevante Trainingsmuster wiederzufinden,
4. daraus neue Inhalte zu erzeugen,
5. und diese kontrolliert zu exportieren.

Wenn diese Kette praktisch funktioniert, erfüllt das System seinen MVP-Zweck.
