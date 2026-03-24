import { FormEvent, useEffect, useState } from "react";
import { createSource, listSources, SourceSummary } from "../services/api";

export function SourcesScreen(): JSX.Element {
  const [content, setContent] = useState("4x100 easy\n8x50 pace");
  const [sourceType, setSourceType] = useState<"text" | "docx" | "pdf">("text");
  const [sources, setSources] = useState<SourceSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async (): Promise<void> => {
    try {
      const response = await listSources();
      setSources(response.items);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const onSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createSource({ source_type: sourceType, content });
      await load();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen-stack">
      <section className="screen-card">
        <h2>Sources</h2>
        <p>Import historischer Quellen mit direkter Extraktion und Normalisierung.</p>
        <form className="form-grid" onSubmit={onSubmit}>
          <label>
            Typ
            <select value={sourceType} onChange={(event) => setSourceType(event.target.value as "text" | "docx" | "pdf")}>
              <option value="text">Text</option>
              <option value="docx">DOCX</option>
              <option value="pdf">PDF</option>
            </select>
          </label>
          <label>
            Inhalt
            <textarea value={content} onChange={(event) => setContent(event.target.value)} rows={6} />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Import läuft..." : "Quelle importieren"}
          </button>
        </form>
        {error ? <p className="error-text">{error}</p> : null}
      </section>

      <section className="screen-card">
        <h3>Quellen</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Typ</th>
                <th>Status</th>
                <th>Zeit</th>
              </tr>
            </thead>
            <tbody>
              {sources.map((source) => (
                <tr key={source.id}>
                  <td className="mono">{source.id.slice(0, 8)}</td>
                  <td>{source.source_type}</td>
                  <td>{source.source_status}</td>
                  <td>{new Date(source.ingested_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
