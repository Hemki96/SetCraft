# ADR 0006 – Initialer lokaler LLM-/Embedding-Stack (MVP)

## Status
Accepted

## Kontext

`ADR 0003` legt Ollama als lokales Modell-Gateway fest, lässt aber die konkrete Erstbelegung offen.  
`ADR 0005` fordert semantische Suche über Embeddings, ebenfalls ohne Default-Modell.

Für umsetzbare MVP-Tickets werden konkrete Standardmodelle benötigt, inklusive klarer Ausweichlogik bei schwächerer Hardware.

## Alternativen

- A: Ein Modell für Generierung und Embeddings
- B: Getrennte Modelle für Generierung und Embeddings
- C: Drei Modelle (Extraktion, Generierung, Embeddings getrennt)

## Entscheidung

Es wird **Alternative B** verwendet:
- Generierung/Umformulierung: `qwen2.5:14b-instruct`
- Embeddings: `nomic-embed-text`
- Provider: `ollama`

## Begründung

- B bietet bessere Retrieval-Qualität als A, ohne die operative Komplexität von C.
- Beide Modelle sind lokal betreibbar und passen zum Self-Hosted-Anspruch.
- Die Trennung bleibt kompatibel mit `Replaceable AI Components`.

## Auswirkungen

- AI-Adapter verwaltet getrennte Konfigurationen für `generation_model` und `embedding_model`.
- Jeder Generierungs- und Embedding-Run speichert `provider`, `model_name` und `model_version` auditierbar.
- Bei unzureichender Hardware ist ein dokumentierter Fallback für Generierung zulässig (kleineres Modell), aber nur mit explizitem Lauf-Tag im Audit-Log.

## Offene Risiken

- 14B-Modelle können auf schwachen lokalen Systemen hohe Latenzen verursachen.
- Deutschsprachige Schwimmterminologie kann modellabhängig inkonsistent sein.
- Embedding-Qualität muss in einem späteren Evaluations-Task mit realen Vereinsdaten abgesichert werden.

## Nicht Teil dieser ADR

- Finale Modellwahl für Extraktionspipeline v2+
- Feintuning-/LoRA-Strategie
- GPU-spezifische Betriebsprofile pro Betriebssystem
