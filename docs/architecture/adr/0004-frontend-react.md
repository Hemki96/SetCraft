# ADR 0004 – Frontend mit React und TypeScript

## Status
Accepted

## Kontext
Die Plattform benötigt eine Weboberfläche für Upload, Review, Suche, Generierung, Freigabe und Export.

Relevante Anforderungen:
- `FR-001` Upload von Quelldateien
- `FR-005` Manuelle Review- und Korrekturfunktion
- `FR-006` Suche und Filter
- `FR-011` Freigabeprozess

## Entscheidung
Für das Frontend wird **React mit TypeScript** verwendet.

## Begründung
- komplexe UI-Flows modular aufbaubar
- Review- und Formularlogik klar modellierbar
- langfristige Erweiterbarkeit
- robuste Grundlage für spätere komplexere Screens

## Konsequenzen
- Fachliche API-Verträge werden aus Shared-Schemas konsumiert, nicht im Frontend dupliziert.
- Review- und Freigabezustände werden als explizite UI-States modelliert.
- Die Web-UI bleibt der primäre MVP-Client (keine native Mobile-App im MVP).

## Open Questions
- Open Question: Welche UI-Bibliothek wird im MVP verwendet (Headless-first vs. opinionated Component Library)?
- Open Question: Wird Server State im MVP mit dediziertem Query-Layer verwaltet oder zunächst schlanker gehalten?
- Open Question: Welche Accessibility-Mindestanforderungen gelten bereits für den MVP als verpflichtend?
