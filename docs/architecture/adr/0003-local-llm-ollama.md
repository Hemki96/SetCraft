# ADR 0003 – Lokales Modell-Gateway über Ollama

## Status
Accepted

## Kontext
Das Produkt soll möglichst kostenfrei und self-hosted betrieben werden, gleichzeitig aber KI-Funktionen für Extraktion, Embeddings und Generierung nutzen.

## Entscheidung
Für lokale Modellnutzung wird **Ollama** als Standard-Gateway für den MVP vorgesehen.

## Begründung
- einfacher lokaler Betrieb
- Modellwechsel mit geringer Integrationshürde
- self-hosted Nutzung
- pragmatische Anbindung für Text- und Embedding-Use-Cases
