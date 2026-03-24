# ADR 0003 – Lokales Modell-Gateway über Ollama

## Status
Accepted

## Kontext
Das Produkt soll self-hosted und kostenarm betrieben werden, gleichzeitig aber KI-Funktionen für Extraktion, Embeddings und Generierung nutzen.

Die Architektur verlangt austauschbare KI-Komponenten (`Replaceable AI Components`), daher darf die Entscheidung keinen Vendor-Lock-in im Anwendungscode erzeugen.

## Entscheidung
Für lokale Modellnutzung wird **Ollama** als Standard-Gateway für den MVP vorgesehen.

## Begründung
- einfacher lokaler Betrieb
- Modellwechsel mit geringer Integrationshürde
- self-hosted Nutzung
- pragmatische Anbindung für Text- und Embedding-Use-Cases

## Konsequenzen
- Modellaufrufe werden über eine interne Adapter-Schnittstelle gekapselt, nicht direkt in Fachlogik verdrahtet.
- Prompting-, Embedding- und Modellkonfigurationen werden zentral versioniert und nachvollziehbar gehalten.
- Alternative lokale oder serverseitige Modellprovider bleiben als spätere Option offen.

## Open Questions
- Open Question: Welches konkrete lokale Standardmodell wird für Extraktion und Generierung im MVP initial freigegeben?
- Open Question: Werden Embeddings über dasselbe Gateway oder über einen getrennten Adapter betrieben?
- Open Question: Welche Minimal-Hardware wird als unterstützte lokale Entwicklungsumgebung dokumentiert?
