import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  SessionBlock,
  TrainingSession,
  TrainingSet,
  getSession,
  reviewSession,
  searchSessions,
  updateBlock,
  updateSession,
  updateSet,
} from "../services/sessions";

interface SearchFormState {
  q: string;
  distance: string;
  intensity: string;
  type: string;
}

export function SessionsScreen(): JSX.Element {
  const [searchState, setSearchState] = useState<SearchFormState>({
    q: "",
    distance: "",
    intensity: "",
    type: "",
  });
  const [sessions, setSessions] = useState<TrainingSession[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [selectedSession, setSelectedSession] = useState<TrainingSession | null>(null);
  const [selectedBlockId, setSelectedBlockId] = useState<string>("");
  const [selectedSetId, setSelectedSetId] = useState<string>("");
  const [sessionTitleEdit, setSessionTitleEdit] = useState<string>("");
  const [sessionNotesEdit, setSessionNotesEdit] = useState<string>("");
  const [blockTypeEdit, setBlockTypeEdit] = useState<string>("");
  const [setDistanceEdit, setSetDistanceEdit] = useState<string>("");
  const [setIntensityEdit, setSetIntensityEdit] = useState<string>("");
  const [reviewComment, setReviewComment] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const selectedBlock = useMemo<SessionBlock | null>(() => {
    if (!selectedSession) {
      return null;
    }
    return (
      selectedSession.blocks.find((block) => block.id === selectedBlockId) ??
      selectedSession.blocks[0] ??
      null
    );
  }, [selectedBlockId, selectedSession]);

  const selectedSet = useMemo<TrainingSet | null>(() => {
    if (!selectedBlock) {
      return null;
    }
    return (
      selectedBlock.sets.find((trainingSet) => trainingSet.id === selectedSetId) ??
      selectedBlock.sets[0] ??
      null
    );
  }, [selectedBlock, selectedSetId]);

  useEffect(() => {
    void runSearch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function runSearch(): Promise<void> {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const distance = searchState.distance.trim()
        ? Number.parseInt(searchState.distance, 10)
        : undefined;
      const items = await searchSessions({
        q: searchState.q,
        distance_m: Number.isNaN(distance ?? NaN) ? undefined : distance,
        intensity: searchState.intensity,
        type: searchState.type,
      });
      setSessions(items);
      if (items.length === 0) {
        setSelectedSessionId(null);
        setSelectedSession(null);
        return;
      }

      const targetId = selectedSessionId && items.some((item) => item.id === selectedSessionId)
        ? selectedSessionId
        : items[0].id;
      setSelectedSessionId(targetId);
      await loadSessionDetail(targetId);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Suche fehlgeschlagen.");
    } finally {
      setIsLoading(false);
    }
  }

  async function loadSessionDetail(sessionId: string): Promise<void> {
    const detail = await getSession(sessionId);
    setSelectedSession(detail);
    setSessionTitleEdit(detail.title ?? "");
    setSessionNotesEdit(detail.notes ?? "");

    const initialBlock = detail.blocks[0] ?? null;
    if (!initialBlock) {
      setSelectedBlockId("");
      setBlockTypeEdit("");
      setSelectedSetId("");
      setSetDistanceEdit("");
      setSetIntensityEdit("");
      return;
    }

    setSelectedBlockId(initialBlock.id);
    setBlockTypeEdit(initialBlock.block_type ?? "");
    const initialSet = initialBlock.sets[0] ?? null;
    if (!initialSet) {
      setSelectedSetId("");
      setSetDistanceEdit("");
      setSetIntensityEdit("");
      return;
    }

    setSelectedSetId(initialSet.id);
    setSetDistanceEdit(initialSet.distance_m ? String(initialSet.distance_m) : "");
    setSetIntensityEdit(initialSet.intensity_note ?? "");
  }

  function onSearchInputChange(field: keyof SearchFormState, value: string): void {
    setSearchState((current) => ({ ...current, [field]: value }));
  }

  async function onSearchSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    await runSearch();
  }

  async function onSelectSession(sessionId: string): Promise<void> {
    setSelectedSessionId(sessionId);
    setErrorMessage(null);
    try {
      await loadSessionDetail(sessionId);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Laden fehlgeschlagen.");
    }
  }

  async function onSessionCorrectionSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    if (!selectedSessionId) {
      return;
    }

    setIsMutating(true);
    setErrorMessage(null);
    try {
      const updated = await updateSession(selectedSessionId, {
        title: sessionTitleEdit.trim() || null,
        notes: sessionNotesEdit.trim() || null,
      });
      setSelectedSession(updated);
      await runSearch();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Session-Update fehlgeschlagen.");
    } finally {
      setIsMutating(false);
    }
  }

  async function onBlockCorrectionSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    if (!selectedSessionId || !selectedBlockId) {
      return;
    }

    setIsMutating(true);
    setErrorMessage(null);
    try {
      const updated = await updateBlock(selectedSessionId, selectedBlockId, {
        block_type: blockTypeEdit.trim() || null,
      });
      setSelectedSession(updated);
      await runSearch();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Block-Update fehlgeschlagen.");
    } finally {
      setIsMutating(false);
    }
  }

  async function onSetCorrectionSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    if (!selectedSessionId || !selectedBlockId || !selectedSetId) {
      return;
    }

    setIsMutating(true);
    setErrorMessage(null);
    try {
      const parsedDistance = setDistanceEdit.trim()
        ? Number.parseInt(setDistanceEdit, 10)
        : undefined;
      const updated = await updateSet(selectedSessionId, selectedBlockId, selectedSetId, {
        distance_m: Number.isNaN(parsedDistance ?? NaN) ? null : parsedDistance,
        intensity_note: setIntensityEdit.trim() || null,
      });
      setSelectedSession(updated);
      await runSearch();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Set-Update fehlgeschlagen.");
    } finally {
      setIsMutating(false);
    }
  }

  async function onReviewDecision(decision: "reviewed" | "corrected" | "rejected"): Promise<void> {
    if (!selectedSessionId) {
      return;
    }

    setIsMutating(true);
    setErrorMessage(null);
    try {
      const updated = await reviewSession(selectedSessionId, {
        decision,
        comment: reviewComment.trim() || undefined,
      });
      setSelectedSession(updated);
      await runSearch();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Review fehlgeschlagen.");
    } finally {
      setIsMutating(false);
    }
  }

  function onSelectBlock(blockId: string): void {
    setSelectedBlockId(blockId);
    const block = selectedSession?.blocks.find((entry) => entry.id === blockId);
    if (!block) {
      setBlockTypeEdit("");
      setSelectedSetId("");
      setSetDistanceEdit("");
      setSetIntensityEdit("");
      return;
    }

    setBlockTypeEdit(block.block_type ?? "");
    const firstSet = block.sets[0] ?? null;
    if (!firstSet) {
      setSelectedSetId("");
      setSetDistanceEdit("");
      setSetIntensityEdit("");
      return;
    }

    setSelectedSetId(firstSet.id);
    setSetDistanceEdit(firstSet.distance_m ? String(firstSet.distance_m) : "");
    setSetIntensityEdit(firstSet.intensity_note ?? "");
  }

  function onSelectSet(setId: string): void {
    setSelectedSetId(setId);
    const trainingSet = selectedBlock?.sets.find((entry) => entry.id === setId);
    setSetDistanceEdit(trainingSet?.distance_m ? String(trainingSet.distance_m) : "");
    setSetIntensityEdit(trainingSet?.intensity_note ?? "");
  }

  return (
    <section className="sessions-screen" aria-label="Sessions Review and Search">
      <div className="screen-card">
        <h2>Session Search & Filter v1</h2>
        <form className="sessions-search-form" onSubmit={(event) => void onSearchSubmit(event)}>
          <label>
            Query
            <input
              value={searchState.q}
              onChange={(event) => onSearchInputChange("q", event.target.value)}
              placeholder="z. B. aerobic"
            />
          </label>
          <label>
            Distanz (m)
            <input
              value={searchState.distance}
              onChange={(event) => onSearchInputChange("distance", event.target.value)}
              inputMode="numeric"
              placeholder="z. B. 400"
            />
          </label>
          <label>
            Intensitaet
            <input
              value={searchState.intensity}
              onChange={(event) => onSearchInputChange("intensity", event.target.value)}
              placeholder="z. B. low"
            />
          </label>
          <label>
            Typ
            <input
              value={searchState.type}
              onChange={(event) => onSearchInputChange("type", event.target.value)}
              placeholder="z. B. kick / endurance"
            />
          </label>
          <button type="submit" disabled={isLoading || isMutating}>
            {isLoading ? "Suche laeuft..." : "Suchen"}
          </button>
        </form>

        {errorMessage ? <p className="error-text">{errorMessage}</p> : null}

        <ul className="session-results">
          {sessions.map((session) => (
            <li key={session.id}>
              <button
                type="button"
                className={
                  selectedSessionId === session.id
                    ? "session-result-button session-result-button-active"
                    : "session-result-button"
                }
                onClick={() => void onSelectSession(session.id)}
              >
                <span>{session.title ?? "Untitled Session"}</span>
                <small>
                  {session.review_status} | {session.total_distance_m ?? 0}m
                </small>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="screen-card">
        <h3>Review / Korrektur</h3>
        {selectedSession ? (
          <>
            <p>
              Status: <strong>{selectedSession.review_status}</strong> | Approval: {" "}
              <strong>{selectedSession.approval_status}</strong>
            </p>

            <form className="editor-form" onSubmit={(event) => void onSessionCorrectionSubmit(event)}>
              <label>
                Session Titel
                <input
                  value={sessionTitleEdit}
                  onChange={(event) => setSessionTitleEdit(event.target.value)}
                />
              </label>
              <label>
                Session Notiz
                <textarea
                  value={sessionNotesEdit}
                  onChange={(event) => setSessionNotesEdit(event.target.value)}
                  rows={3}
                />
              </label>
              <button type="submit" disabled={isMutating}>Session korrigieren</button>
            </form>

            <form className="editor-form" onSubmit={(event) => void onBlockCorrectionSubmit(event)}>
              <label>
                Block
                <select
                  value={selectedBlockId}
                  onChange={(event) => onSelectBlock(event.target.value)}
                >
                  {selectedSession.blocks.map((block) => (
                    <option key={block.id} value={block.id}>
                      {block.title ?? "Untitled Block"}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Block Typ
                <input
                  value={blockTypeEdit}
                  onChange={(event) => setBlockTypeEdit(event.target.value)}
                />
              </label>
              <button type="submit" disabled={isMutating || !selectedBlock}>Block korrigieren</button>
            </form>

            <form className="editor-form" onSubmit={(event) => void onSetCorrectionSubmit(event)}>
              <label>
                Set
                <select
                  value={selectedSetId}
                  onChange={(event) => onSelectSet(event.target.value)}
                >
                  {selectedBlock?.sets.map((trainingSet) => (
                    <option key={trainingSet.id} value={trainingSet.id}>
                      {trainingSet.label ?? "Untitled Set"}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Set Distanz (m)
                <input
                  value={setDistanceEdit}
                  onChange={(event) => setSetDistanceEdit(event.target.value)}
                  inputMode="numeric"
                />
              </label>
              <label>
                Set Intensitaet
                <input
                  value={setIntensityEdit}
                  onChange={(event) => setSetIntensityEdit(event.target.value)}
                />
              </label>
              <button type="submit" disabled={isMutating || !selectedSet}>Set korrigieren</button>
            </form>

            <div className="review-actions">
              <label>
                Review-Kommentar
                <input
                  value={reviewComment}
                  onChange={(event) => setReviewComment(event.target.value)}
                  placeholder="optional"
                />
              </label>
              <div className="review-action-buttons">
                <button
                  type="button"
                  onClick={() => void onReviewDecision("reviewed")}
                  disabled={isMutating}
                >
                  Als reviewed markieren
                </button>
                <button
                  type="button"
                  onClick={() => void onReviewDecision("corrected")}
                  disabled={isMutating}
                >
                  Als corrected markieren
                </button>
                <button
                  type="button"
                  onClick={() => void onReviewDecision("rejected")}
                  disabled={isMutating}
                >
                  Zurueckweisen
                </button>
              </div>
            </div>
          </>
        ) : (
          <p>Keine Session ausgewaehlt.</p>
        )}
      </div>
    </section>
  );
}
