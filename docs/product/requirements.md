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
