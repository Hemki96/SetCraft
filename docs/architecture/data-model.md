# Datenmodell

## Modellierungsprinzipien

### 1. Historische Quelle und strukturierte Fachdaten sind getrennt
Eine hochgeladene Datei ist **nicht** selbst die fachliche Wahrheit.  
Sie ist die Quelle, aus der strukturierte Domänenobjekte erzeugt werden.

### 2. Rohdaten und Normalform sind getrennt
Extrahierte Rohtexte und normalisierte Felder werden getrennt gespeichert.

### 3. Reviewbarkeit ist Pflicht
Extrahierte Inhalte müssen manuell korrigierbar sein, ohne dass Originalwerte verloren gehen.

### 4. Generierte Inhalte sind eigenständige Objekte
Generierte Sets, Einheiten oder Wochenpläne dürfen nicht als historische Originale gespeichert werden.

### 5. Mehrstufige Granularität
Das Modell unterstützt:
- Trainingseinheit
- Trainingsblock
- Set

## Domänenmodell v1 (P0-003)

### Kernentitäten (MVP-Pflicht)
- `SourceFile`
- `TrainingSession`
- `SessionBlock`
- `TrainingSet`
- `GeneratedPlan`
- `ValidationResult`
- `ReviewDecision`

### Beziehungen und Kardinalitäten
- `SourceFile (1) -> (n) TrainingSession`
- `TrainingSession (1) -> (n) SessionBlock`
- `SessionBlock (1) -> (n) TrainingSet`
- `GeneratedPlan (n) -> (n) TrainingSession` über `reference_session_ids`
- `ValidationResult` referenziert genau ein Ziel über `(target_type, target_id)` mit Zieltyp `session` oder `generated_plan`
- `ReviewDecision` referenziert genau ein Ziel über `(target_type, target_id)` mit Zieltyp `session` oder `generated_plan`

## Entitätsdefinitionen v1

### 1) SourceFile (historische Quelle)
Zweck: Upload-Artefakt, Metadaten und Extraktionskontext.

Pflichtfelder:
- `id`
- `source_type` (`docx|pdf|text`)
- `source_status`
- `ingested_at`

Wichtige optionale Felder:
- `original_filename`
- `raw_text` (roher extrahierter Text)
- `extraction_confidence` (`0.0..1.0`, Gesamtvertrauen der Extraktion)
- `details_json` (z. B. Parser-Metadaten)

Hinweis: `SourceFile` enthält keine normalisierte Fachstruktur (keine Blöcke/Sets).

### 2) TrainingSession (normalisierte historische Einheit)
Zweck: Fachlich strukturierte Einheit aus historischen Quellen.

Pflichtfelder:
- `id`
- `source_file_id` (FK auf `SourceFile`)
- `review_status`
- `approval_status`
- `blocks` (kann initial leer sein, aber Feld existiert immer)

Wichtige optionale Felder:
- `title`
- `total_distance_m`, `duration_min`
- `raw_snapshot` (Rohsegment der Quelle)
- `extraction_confidence` (`0.0..1.0`)
- `tags`, `notes`, `details_json`

Zustandsregel:
- `approval_status=approved` ist nur zulässig, wenn `review_status IN (reviewed_with_changes, reviewed_ok)`.

### 3) SessionBlock (normalisierter Abschnitt)
Zweck: Strukturierung einer Session in logisch/fachlich getrennte Blöcke.

Pflichtfelder:
- `id`
- `order_index` (`>= 0`)
- `sets` (kann leer starten)

Wichtige optionale Felder:
- `title`
- `block_type`
- `raw_snapshot`
- `extraction_confidence` (`0.0..1.0`)
- `details_json`

Ordnungsregel:
- pro Session ist `order_index` eindeutig.

### 4) TrainingSet (normalisierte kleinste Trainingseinheit)
Zweck: Ausführbare Set-Definition als wiederverwendbares Domänenobjekt.

Pflichtfelder:
- `id`
- `order_index` (`>= 0`)
- `label`
- `repeat_count` (`> 0`)
- `distance_m` (`> 0`)
- `stroke` (`freestyle|backstroke|breaststroke|butterfly|medley|kick|drill|mixed`)
- `intensity_zone` (`z1|z2|z3|z4|z5`)
- `is_generated` (`true|false`)

Wichtige optionale Felder:
- `duration_sec` (`>= 0`)
- `sendoff_seconds` (`> 0`)
- `rest_seconds` (`>= 0`)
- `intensity_note`
- `rpe_min`, `rpe_max` (`1..10`)
- `raw_snapshot`
- `extraction_confidence` (`0.0..1.0`)
- `normalized_notes`
- `tags`, `details_json`

Ordnungsregel:
- pro Block ist `order_index` eindeutig.

Validierungsregel:
- Für generierte Sets soll mindestens eines von `sendoff_seconds` oder `rest_seconds` gesetzt sein; fehlt beides, erzeugt die Regel-Engine mindestens `warning`.

### 5) GeneratedPlan (generierter Inhalt, nie historisch)
Zweck: Neu erzeugte Session- oder Wochenplanung.

Pflichtfelder:
- `id`
- `plan_type` (`session_plan|week_plan`)
- `is_generated=true` (harte Invariante)
- `review_status`
- `approval_status`
- `content_snapshot`

Wichtige optionale Felder:
- `reference_session_ids` (Traceability zu historischen Referenzen)
- `validation_results`
- `notes`, `details_json`

Zustandsregel:
- `approval_status=approved` ist nur zulässig, wenn `review_status IN (reviewed_with_changes, reviewed_ok)`.

### 6) ValidationResult (regelbasierte Qualitätsbewertung)
Zweck: maschinelle Plausibilitäts- und Regelprüfung.

Pflichtfelder:
- `id`
- `target_type` (`session|generated_plan`)
- `target_id`
- `severity` (`warning|error`)
- `rule_code`
- `message`

Wichtige optionale Felder:
- `field_path`
- `confidence` (`0.0..1.0`, falls probabilistischer Check)
- `details_json`

### 7) ReviewDecision (menschliche Entscheidung)
Zweck: Nachvollziehbarer Review-/Korrekturentscheid.

Pflichtfelder:
- `id`
- `target_type` (`session|generated_plan`)
- `target_id`
- `decision` (`reviewed|corrected|rejected`)
- `decided_at`

Wichtige optionale Felder:
- `comment`
- `decided_by_user_id`

## Statusmodell Review/Freigabe (MVP)

Für `TrainingSession` und `GeneratedPlan` gelten zwei getrennte Statusachsen:

- `review_status`
  - `pending_review`
  - `in_review`
  - `reviewed_with_changes`
  - `reviewed_ok`
- `approval_status`
  - `not_submitted`
  - `submitted`
  - `approved`
  - `rejected`

Auditfelder:
- `reviewed_by`, `reviewed_at`
- `approved_by`, `approved_at`
- `rejection_reason` (nullable)

Invariante:
- `approval_status=approved` nur bei `review_status IN (reviewed_with_changes, reviewed_ok)`.

## Toleranzlogik Umfang/Dauer (MVP)

`ValidationResult` unterstützt strukturierte Toleranzbewertung mit:
- `metric` (`volume_m|duration_min`)
- `target_value`
- `actual_value`
- `allowed_deviation_abs`
- `allowed_deviation_rel_percent`
- `effective_allowed_deviation`
- `status` (`pass|warn|fail`)
- `message`

Standardwerte:
- Umfang: `8%`, absolute Guardrails `min=100m`, `max=400m`
- Dauer: `10%`, absolute Guardrails `min=5min`, `max=12min`

Einstufung:
- `pass`: innerhalb Toleranz
- `warn`: Abweichung > Toleranz und <= `1.5 * effective_allowed_deviation`
- `fail`: darüber

## Trennung Rohdaten vs. normalisierte Daten

Rohdaten (extraktionsnah):
- `SourceFile.raw_text`
- `TrainingSession.raw_snapshot`
- `SessionBlock.raw_snapshot`
- `TrainingSet.raw_snapshot`
- `details_json` für technische Extraktionsdetails

Normalisierte Fachdaten:
- `TrainingSession.title`, `total_distance_m`, `duration_min`
- `SessionBlock.title`, `block_type`
- `TrainingSet.distance_m`, `duration_sec`, `intensity_note`

Regel:
- Rohinformationen werden nicht überschrieben, sondern bleiben für Review/Audit erhalten.

## Trennung historisch vs. generiert

Historisch:
- `SourceFile`, `TrainingSession`, `SessionBlock`, `TrainingSet`

Generiert:
- `GeneratedPlan` mit harter Invariante `is_generated=true`

Regeln:
- Generierte Inhalte werden nie als historische Session gespeichert.
- Historische Inhalte behalten Quellreferenz über `source_file_id`.
- Generierung kann historische Inhalte referenzieren (`reference_session_ids`), aber nicht umklassifizieren.

## Unsicherheit und Confidence im Modell

Extraktionsunsicherheit ist explizit abbildbar über:
- `SourceFile.extraction_confidence`
- `TrainingSession.extraction_confidence`
- `SessionBlock.extraction_confidence`
- `TrainingSet.extraction_confidence`

Regel-/Validierungsunsicherheit ist explizit abbildbar über:
- `ValidationResult.confidence`

Alle Confidence-Werte liegen im Intervall `0.0..1.0`.

## Referenz auf implementierte Schemas

Die initialen Pydantic-Schemas zu diesem Modell liegen in:
- `packages/schemas/python/training_plan_schemas/domain_v1.py`
