# PLANS.md

## Zweck dieses Dokuments

Dieses Dokument definiert die Standardstruktur für Umsetzungspläne im Repository.

Jeder größere Arbeitsblock wird als Plan dokumentiert, bevor umfangreichere Implementierung beginnt. Ziel ist:

- nachvollziehbare Zerlegung
- klare Risiken
- explizite Abhängigkeiten
- kontrollierte Umsetzung in kleinen Schritten
- gute Arbeitsgrundlage für Codex und andere Coding-Agents

## Grundregeln für Pläne

- erst Problem und Ziel klären, dann Aufgaben formulieren
- lieber mehrere kleine Pläne als ein unübersichtlicher Masterplan
- Risiken und Annahmen explizit benennen
- offene Fragen nicht verstecken
- Tasks nur so schneiden, dass sie überprüfbar umsetzbar sind
- technische und fachliche Aspekte gemeinsam betrachten
- Rollout-Reihenfolge von Anfang an mitdenken

## Vorlage für einen Umsetzungsplan

### 1. Plan-Metadaten
- **Plan-ID:** `PLAN-XXXX`
- **Titel:** Kurzer, präziser Titel
- **Status:** `draft | ready | in_progress | blocked | done`
- **Owner:** Name oder Rolle
- **Erstellt am:** Datum
- **Letzte Aktualisierung:** Datum
- **Bezug zu Task(s):** Links oder IDs aus `TASKS.md`

### 2. Ziel
Beschreibe in 3–6 Sätzen:
- welches Problem gelöst wird
- warum es jetzt relevant ist
- welches Ergebnis am Ende konkret vorliegen soll

### 3. Scope
#### Im Scope
- konkrete enthaltene Funktionen / Komponenten

#### Nicht im Scope
- bewusst ausgeschlossene Aspekte

### 4. Fachlicher Kontext
Beschreibe:
- betroffene Nutzer
- betroffene Kernprozesse
- Abhängigkeit zu Produktzielen
- relevante Regeln oder Qualitätsanforderungen

### 5. Technischer Kontext
Beschreibe:
- betroffene Services / Apps / Pakete
- relevante Schnittstellen
- Datenmodellbezug
- Infrastrukturbezug
- Test- und Betriebsrelevanz

### 6. Annahmen
Liste alle Annahmen explizit auf.

### 7. Offene Fragen
Liste ungeklärte Punkte auf, die vor oder während der Umsetzung entschieden werden müssen.

### 8. Epics
Epics sind fachlich oder technisch zusammenhängende Hauptblöcke.

### 9. Features
Features zerlegen ein Epic in konkrete nutzbare Ergebnisse.

### 10. Tasks
Tasks müssen implementierbar und überprüfbar sein.

### 11. Risiken
Risiken werden früh dokumentiert und aktiv gesteuert.

### 12. Abhängigkeiten
Erfasse:
- fachliche Vorbedingungen
- technische Vorbedingungen
- externe Bibliotheken oder Infrastruktur
- Reihenfolgeabhängigkeiten zu anderen Plänen

### 13. Rollout-Reihenfolge
Beschreibe in welcher Reihenfolge das Ergebnis sinnvoll eingeführt wird.

### 14. Verifikation
Für jeden Plan muss definiert sein:
- wie überprüft wird, dass das Ziel erreicht wurde
- welche Tests oder Reviews nötig sind
- welche Artefakte als Nachweis gelten

### 15. Abschlusskriterien
Ein Plan ist nur abgeschlossen, wenn:
- alle Muss-Akzeptanzkriterien erfüllt sind
- relevante Tests grün sind
- Dokumentation aktualisiert ist
- offene Risiken transparent sind
- kein stiller Architekturbruch entstanden ist

## Empfehlung für die Praxis

Jeder Plan sollte so klein bleiben, dass er:
- in wenigen PRs umsetzbar ist
- klar testbar ist
- keine Mehrdeutigkeit in Scope und Erfolgskriterium lässt

Lieber:
- `PLAN-0003 Normalisierung Sessions v1`
als
- `PLAN-0003 Komplette KI-Engine`
