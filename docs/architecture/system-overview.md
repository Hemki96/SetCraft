# System Overview

## Architekturziele

Die Architektur muss folgende Ziele unterstützen:
- self-hosted Betrieb
- lokale Entwicklungsfähigkeit
- saubere Trennung fachlicher Verantwortungen
- kontrollierte, nachvollziehbare KI-Nutzung
- testbare Kernlogik
- schrittweise Erweiterbarkeit
- geringe Abhängigkeit von proprietären Diensten

## Architekturprinzipien

### 1. Structured Data First
Freitext ist nur Input oder Darstellung, nicht primäre Fachwahrheit.

### 2. Source Traceability
Jeder strukturierte Datensatz muss auf seine Quelle zurückführbar sein.

### 3. Clear Separation of Concerns
Upload, Extraktion, Normalisierung, Suche, Generierung, Validierung und Export sind getrennte Verantwortungen.

### 4. Human Review Before Trust
Automatisch extrahierte und generierte Inhalte müssen überprüfbar und korrigierbar sein.

### 5. Replaceable AI Components
LLM-, Embedding- und Retrieval-Komponenten sind austauschbar zu halten.

### 6. Local-First, Server-Ready
Das System soll lokal starten können, aber ohne Architekturbruch später serverfähig sein.

## Hauptkomponenten

### 1. Web Application
Verantwortlich für Upload, Review, Suche, Generierung, Freigabe und Export.

### 2. API Service
Verantwortlich für fachliche Endpunkte, Authentifizierung, Orchestrierung und Statusmanagement.

### 3. Ingestion Service
Verantwortlich für Annahme hochgeladener Dateien, Vorvalidierung und Übergabe an Extraktionspipeline.

### 4. Extraction Service
Verantwortlich für Text- und Strukturgewinnung aus DOCX/PDF/Freitext.

### 5. Normalization Service
Verantwortlich für Mapping extrahierter Inhalte auf das Domänenmodell.

### 6. Retrieval Service
Verantwortlich für strukturierte Suche und semantische Suche.

### 7. Generation Service
Verantwortlich für Erstellung neuer Sets, Einheiten und Wochenpläne.

### 8. Validation Service
Verantwortlich für Plausibilitätsregeln, Qualitätschecks und Kennzeichnung von Warnungen/Fehlern.

### 9. Persistence Layer
Verantwortlich für relationale Speicherung, Auditierbarkeit und Vektorspeicherung.

### 10. Background Worker
Verantwortlich für asynchrone Verarbeitung, Extraktion, Embeddings, Generierung und Exportjobs.
