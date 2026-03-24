# Anforderungen

## Dokumentzweck

Dieses Dokument definiert die fachlichen und systemischen Anforderungen für die Training Plan Platform in einer Form, die für Produktentscheidungen, Architekturarbeit und agentische Implementierung belastbar ist.

## Produktvision

Die Plattform soll historisches Trainingswissen aus unstrukturierten Dokumenten in strukturierte, wiederverwendbare Trainingslogik überführen und daraus neue Trainingsinhalte kontrolliert ableiten.

## MVP

### Im MVP enthalten
- Upload von DOCX, PDF und Freitext
- Speicherung von Quelldateien und Metadaten
- automatische Extraktion von Trainingsinhalten
- Normalisierung in ein strukturiertes Datenmodell
- Review und Korrektur extrahierter Inhalte
- Trainingsdatenbank für Einheiten, Blöcke und Sets
- Suche und Filter
- Vorschläge für neue Sets
- Vorschläge bzw. Generierung neuer Einheiten
- Generierung von Wochenplänen
- Export in nutzbare Ausgabeformate
- automatische Plausibilitäts- und Qualitätschecks
- Freigabeprozess durch Trainer

### Nicht im MVP
- native Mobile-App
- Wearable-Integrationen
- vollautomatische Langfristplanung ohne Review
- komplexe Mehrmandantenfähigkeit
- Athletenportal mit umfangreicher Selbstbedienung
- tiefe Outcome-Analytik auf Basis von Leistungsdaten

## Funktionale Anforderungen

### FR-001 Upload von Quelldateien
Das System muss unstrukturierte historische Trainingspläne als Datei oder Text entgegennehmen können.

### FR-002 Nachvollziehbare Quellspeicherung
Das System muss jede importierte Quelle nachvollziehbar speichern und referenzierbar machen.

### FR-003 Automatische Extraktion
Das System muss aus unstrukturierten Trainingsplänen fachlich relevante Inhalte extrahieren können.

### FR-004 Strukturierung und Normalisierung
Das System muss extrahierte Inhalte in ein konsistentes Datenmodell überführen.

### FR-005 Manuelle Review- und Korrekturfunktion
Das System muss manuelle Korrekturen an extrahierten Inhalten erlauben.

### FR-006 Suche und Filter
Das System muss historische Inhalte strukturiert und semantisch durchsuchbar machen.

### FR-007 Vorschläge für neue Sets
Das System muss basierend auf historischen Daten und Regeln neue Sets vorschlagen können.

### FR-008 Generierung neuer Einheiten
Das System muss neue Trainingseinheiten aus strukturierten Daten, Regeln und historischen Mustern erzeugen können.

### FR-009 Generierung von Wochenplänen
Das System muss mehrere Einheiten in einem Wochenkontext erzeugen können.

### FR-010 Qualitäts- und Plausibilitätsprüfung
Das System muss generierte Inhalte vor Freigabe automatisch prüfen.

### FR-011 Freigabeprozess
Generierte Inhalte dürfen erst nach expliziter Trainerfreigabe als freigegeben gelten.

### FR-012 Export
Das System muss Trainingsinhalte in nutzbare Formate exportieren können.

## Harte fachliche Regeln

- jede Einheit benötigt eine erkennbare Grundstruktur
- generierte Inhalte sind als generiert markiert
- historische Originale bleiben unverändert nachvollziehbar
- Zielumfang muss innerhalb definierter Toleranzen liegen
- unlogische Intensitäts- oder Belastungssprünge sind zu vermeiden
- Regelverstöße müssen sichtbar werden, nicht stillschweigend toleriert

## Entscheidungsreife Präzisierungen (MVP)

Dieser Abschnitt konkretisiert die offenen Punkte aus `TASKS.md` so, dass nachfolgende Implementierungs-Tasks ohne Grundsatzklärung starten können.

### E-001 Pflichtfelder pro Set

**Alternativen**
- A: Minimal (`label`, `distance_m`)
- B: Mittel (A + `stroke`, `intensity_zone`, `repeat_count`)
- C: Vollständig (B + `sendoff_seconds` oder `rest_seconds`, `equipment`, `technique_focus`, `notes`)

**Empfehlung**
- B als MVP-Pflicht, C als optionale Felder mit Qualitätsgewinn.

**Begründung**
- A ist zu schwach für regelbasierte Validierung und Wiederverwendung.
- C ist fachlich stark, erhöht aber Extraktionsunsicherheit und Review-Aufwand früh.
- B balanciert Datenqualität, Extraktionsrobustheit und Nutzwert für Suche/Generierung.

**Auswirkungen**
- Jedes `TrainingSet` braucht mindestens: `label`, `distance_m`, `stroke`, `intensity_zone`, `repeat_count`.
- `sendoff_seconds` und `rest_seconds` bleiben optional, aber mindestens eines davon wird für generierte Sets empfohlen.
- Unvollständige extrahierte Sets bleiben speicherbar, aber erhalten zwingend Review-Flags.

**Offene Risiken**
- Historische Pläne ohne eindeutige Wiederholungsangaben (`repeat_count`) erzeugen mehr manuelle Korrekturen.
- Uneinheitliche Schreibweisen bei `stroke` erfordern saubere Normalisierungstabellen.

### E-002 Intensitätszonen

**Alternativen**
- A: 3-Zonen-Modell (`easy`, `moderate`, `hard`)
- B: 5-Zonen-Modell (`z1` bis `z5`)
- C: 7+ Zonen inkl. wettkampfspezifischer Feingranularität

**Empfehlung**
- B als MVP-Standard mit optionaler Mapping-Ebene zu RPE und CSS-/Schwellenbezug.

**Begründung**
- A ist zu grob für Schwimmsets mit differenzierten Reizen.
- C erhöht Komplexität in Review und UI zu früh.
- B ist fachlich ausreichend präzise und bleibt für Trainer gut bedienbar.

**Auswirkungen**
- Verbindliche Zonendefinition:
  - `z1`: sehr locker / Technik
  - `z2`: locker aerob
  - `z3`: aerob stabil / GA
  - `z4`: Schwelle / Toleranz
  - `z5`: hochintensiv / VO2max-Sprintnah
- Pro Set wird genau eine Primärzone gespeichert.
- Optional können Hilfsfelder (`rpe_min`, `rpe_max`) zur Kalibrierung abgelegt werden.

**Offene Risiken**
- Unterschiedliche Vereins- und Trainerterminologie kann zu Mapping-Konflikten führen.
- Fehlklassifikation bei sehr kurzen Sprints oder Techniksets mit Mischcharakter.

### E-003 Toleranzlogik Umfang/Dauer

**Alternativen**
- A: starre absolute Toleranz (z. B. immer +/- 200 m, +/- 5 min)
- B: relative Toleranz in Prozent
- C: hybride Toleranz (prozentual + Mindest-/Höchstgrenzen)

**Empfehlung**
- C als MVP: relative Basis mit absoluten Guardrails.

**Begründung**
- A skaliert schlecht über kurze und lange Einheiten.
- B ist konsistent, kann aber bei kleinen Umfängen zu eng und bei großen zu weit sein.
- C ist robust und transparent.

**Auswirkungen**
- Standardtoleranzen für Validierung:
  - Gesamtumfang: Sollwert +/- 8%, mindestens +/- 100 m, maximal +/- 400 m
  - Gesamtdauer: Sollwert +/- 10%, mindestens +/- 5 min, maximal +/- 12 min
- Ergebnisstufen:
  - `pass`: innerhalb Toleranz
  - `warn`: außerhalb Toleranz, aber <= 1.5x Toleranzfenster
  - `fail`: darüber hinaus

**Offene Risiken**
- Für Sonderformate (Sprint-only, Technik-only, Wasserlage-Fokus) können Standardgrenzen zu streng sein.
- Dauerberechnung ist bei unvollständigen Pausen-/Abgangsangaben unsicher.

### E-004 Statusmodell Review/Freigabe

**Alternativen**
- A: binär (`draft`, `approved`)
- B: lineares 4-Status-Modell
- C: separates Review- und Approval-Statusmodell

**Empfehlung**
- C als MVP, um fachliche Prüfung und Freigabe getrennt auditierbar zu halten.

**Begründung**
- A und B verschleifen fachliche Prüfung mit Governance.
- C unterstützt `human review before trust` ohne späteren Migrationsbruch.

**Auswirkungen**
- Review-Status (`review_status`):
  - `pending_review`
  - `in_review`
  - `reviewed_with_changes`
  - `reviewed_ok`
- Freigabe-Status (`approval_status`):
  - `not_submitted`
  - `submitted`
  - `approved`
  - `rejected`
- Freigabe ist nur erlaubt, wenn `review_status` in `{reviewed_with_changes, reviewed_ok}` liegt.

**Offene Risiken**
- Mehr Zustände erhöhen UI- und API-Komplexität.
- Rollen- und Berechtigungskonzept muss diese Trennung konsistent absichern.

### E-005 Exportlayout Word/PDF

**Alternativen**
- A: Plain-Text-Export ohne Layoutvorgaben
- B: Tabellenorientiertes Standardlayout
- C: stark designorientierte, freie Layout-Templates

**Empfehlung**
- B als MVP mit fixem Grundlayout und wenigen konfigurierbaren Elementen.

**Begründung**
- A ist zu wenig nutzbar für den Traineralltag.
- C ist aufwendig und erhöht Pflegekosten früh.
- B bietet gute Lesbarkeit und reproduzierbare Ausgabe.

**Auswirkungen**
- Pflichtstruktur im Export:
  - Kopf: Titel, Datum, Gruppe, Plan-Typ, Quelle (historisch/generiert), Freigabestatus
  - Blöcke: Ziel/Schwerpunkt + Set-Tabelle
  - Set-Tabelle: `repeat_count x distance_m`, `stroke`, `intensity_zone`, `sendoff/rest`, Notiz
  - Footer: Gesamtumfang, geschätzte Dauer, Versions-/Freigabeinfo
- Word und PDF teilen dasselbe semantische Layout; PDF ist Render-Ableitung aus derselben Struktur.

**Offene Risiken**
- Komplexe Sonderdarstellungen (z. B. Pyramiden- oder Leiter-Sets) passen nicht immer gut in starre Tabellen.
- Umbruchverhalten bei langen Notizen kann in PDF variieren.

### E-006 Erstes lokales LLM/Embedding-Setup

**Alternativen**
- A: ein einziges Modell für alles
- B: getrenntes Modell für Generierung und Embeddings
- C: zusätzlich spezialisiertes Extraktionsmodell

**Empfehlung**
- B als MVP-Standard: getrennte Modelle für Textgenerierung und Embeddings, beide über Ollama-Adapter.

**Begründung**
- A ist einfach, aber meist qualitativ schwächer bei Retrieval.
- C kann später sinnvoll sein, ist aber im MVP betrieblich unnötig komplex.
- B erfüllt Qualität/Komplexität-Balance und bleibt austauschbar.

**Auswirkungen**
- Initiale Baseline:
  - Generierung/Umformulierung: `qwen2.5:14b-instruct` (lokal über Ollama)
  - Embeddings: `nomic-embed-text` (lokal über Ollama)
- Modellwahl wird zentral versioniert; jedes Generierungs-/Retrieval-Ergebnis referenziert Modellname + Version.
- Fallback auf kleineres Generierungsmodell ist zulässig, muss aber im Audit-Log sichtbar sein.

**Offene Risiken**
- Hardwaregrenzen lokaler Umgebungen können Latenz stark beeinflussen.
- Deutschsprachige Schwimmterminologie kann je nach Modell uneinheitlich behandelt werden.
