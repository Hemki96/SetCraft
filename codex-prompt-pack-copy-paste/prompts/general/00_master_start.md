# Master Start Prompt

```text
Du arbeitest in einem vorbereiteten Repository für eine selbst hostbare Plattform zur Verarbeitung historischer Trainingspläne.

Arbeite strikt dokumentationsgetrieben. Lies vor der Umsetzung mindestens:
README.md, AGENTS.md, TASKS.md, docs/product/requirements.md, docs/architecture/system-overview.md, docs/architecture/data-model.md, docs/architecture/api-design.md, docs/architecture/tech-stack.md, docs/quality/coding-standards.md, docs/quality/testing-strategy.md, docs/quality/definition-of-done.md sowie die relevanten UX-Dokumente und ADRs.

Regeln:
- keine spekulativen Großumbauten
- vorhandene Dateien inkrementell erweitern
- kleine, saubere, testbare Änderungen
- historical vs. generated strikt trennen
- raw vs. normalized strikt trennen
- keine Business-Logik in Route-Handlern
- keine Secrets hardcoden
- self-hosted / local-first respektieren

Setze den nächsten sinnvollen priorisierten Schritt aus TASKS.md um.

Antwortformat:
1. Verstandene Anforderungen
2. Gewählter Task
3. Kurzplan
4. Betroffene Dateien
5. Umsetzung
6. Tests / Verifikation
7. Checkliste
8. Offene Punkte / Annahmen

Checkliste, die du explizit beantworten musst:
- [ ] relevante Doku gelesen
- [ ] Scope klein gehalten
- [ ] bestehende Dateien inkrementell erweitert
- [ ] Tests ergänzt oder bewusst begründet weggelassen
- [ ] Architekturregeln eingehalten
- [ ] keine stillen Fachentscheidungen getroffen
- [ ] offene Punkte klar benannt
```
