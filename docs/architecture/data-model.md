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

## Kernentitäten
- `SourceFile`
- `ExtractionRun`
- `NormalizationRun`
- `TrainingSession`
- `SessionBlock`
- `TrainingSet`
- `GeneratedPlan`
- `GenerationRequest`
- `ValidationResult`
- `ReviewDecision`
- `User`
- `Group`
- `Athlete`
- `SeasonPhase`
- `Competition`
- `Equipment`
- `Tag`

## Empfehlung für MVP

Für den Start gilt:
- `TrainingSession`, `SessionBlock`, `TrainingSet`, `SourceFile`, `GeneratedPlan`, `ValidationResult` sind Pflicht
- `Athlete` bleibt optional
- Wochenpläne können zunächst als `GeneratedPlan(plan_type=week_plan)` abgebildet werden
- zusätzliche Flexibilität kommt über `tags`, `notes` und `details_json`, nicht über frühe Übermodellierung
