# ADR 0005 – Vektorsuche im Retrieval mit pgvector (hybrid)

## Status
Accepted

## Kontext
`FR-006` fordert strukturierte und semantische Suche. Gleichzeitig gelten:
- self-hosted by default
- geringe Abhängigkeit von proprietären Diensten
- klare Trennung zwischen fachlichen Filtern und semantischer Ähnlichkeit

Eine reine Vektorsuche würde fachliche Filter (z. B. Umfang, Niveau, Kontext) nicht ausreichend abbilden.

## Entscheidung
Semantische Suche wird als **hybrides Retrieval** umgesetzt:
- relationale Filterung und Sortierung in PostgreSQL
- Vektorähnlichkeit über `pgvector` in derselben PostgreSQL-Instanz

`pgvector` ist damit Standard für den MVP, aber nur über eine austauschbare Retrieval-Schnittstelle.

## Begründung
- erfüllt `structured + semantic search` ohne zusätzlichen proprietären Suchdienst
- reduziert Betriebsaufwand im MVP durch einen konsistenten DB-Stack
- bleibt kompatibel mit dem Architekturprinzip `Replaceable AI Components`

## Konsequenzen
- Retrieval-Logik wird als eigener Service/Adapter modelliert, nicht als verteilt implementierte SQL-Details in beliebigen Modulen.
- Scoring kombiniert fachliche Filter mit semantischer Relevanz nachvollziehbar.
- Austausch gegen alternative Suchtechnologie bleibt möglich, solange die Retrieval-Schnittstelle stabil bleibt.

## Open Questions
- Open Question: Welches Embedding-Modell wird für den MVP als Default genutzt?
- Open Question: Welche Mindestqualität gilt für semantische Treffer (z. B. Offline-Evaluationsdatensatz und Metrik)?
- Open Question: Wird zusätzlich ein Re-Ranking-Schritt benötigt oder reicht Hybrid-Retrieval im MVP?
