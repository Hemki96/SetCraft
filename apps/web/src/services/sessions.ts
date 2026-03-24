export type ReviewStatus = "needs_review" | "reviewed" | "corrected";
export type ReviewDecision = "reviewed" | "corrected" | "rejected";

export interface TrainingSet {
  id: string;
  order_index: number;
  label: string | null;
  distance_m: number | null;
  duration_sec: number | null;
  intensity_note: string | null;
  tags: string[];
}

export interface SessionBlock {
  id: string;
  order_index: number;
  title: string | null;
  block_type: string | null;
  sets: TrainingSet[];
}

export interface TrainingSession {
  id: string;
  title: string | null;
  notes: string | null;
  total_distance_m: number | null;
  duration_min: number | null;
  review_status: ReviewStatus;
  approval_status: "pending" | "approved" | "rejected";
  blocks: SessionBlock[];
}

interface SessionListResponse {
  items: TrainingSession[];
}

export interface SessionSearchFilters {
  q?: string;
  distance_m?: number;
  intensity?: string;
  type?: string;
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    let errorMessage = `Request failed: ${response.status}`;
    try {
      const payload = (await response.json()) as { message?: string };
      if (payload.message) {
        errorMessage = payload.message;
      }
    } catch {
      // Keep fallback message if parsing fails.
    }
    throw new Error(errorMessage);
  }

  return (await response.json()) as T;
}

export async function searchSessions(
  filters: SessionSearchFilters,
): Promise<TrainingSession[]> {
  const params = new URLSearchParams();
  if (filters.q && filters.q.trim()) {
    params.set("q", filters.q.trim());
  }
  if (typeof filters.distance_m === "number" && !Number.isNaN(filters.distance_m)) {
    params.set("distance_m", String(filters.distance_m));
  }
  if (filters.intensity && filters.intensity.trim()) {
    params.set("intensity", filters.intensity.trim());
  }
  if (filters.type && filters.type.trim()) {
    params.set("type", filters.type.trim());
  }

  const query = params.toString();
  const path = query ? `/api/v1/retrieval/search?${query}` : "/api/v1/retrieval/search";
  const payload = await apiFetch<SessionListResponse>(path);
  return payload.items;
}

export async function getSession(sessionId: string): Promise<TrainingSession> {
  return apiFetch<TrainingSession>(`/api/v1/sessions/${sessionId}`);
}

export async function updateSession(
  sessionId: string,
  payload: {
    title?: string | null;
    notes?: string | null;
    total_distance_m?: number | null;
  },
): Promise<TrainingSession> {
  return apiFetch<TrainingSession>(`/api/v1/sessions/${sessionId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function updateBlock(
  sessionId: string,
  blockId: string,
  payload: { title?: string | null; block_type?: string | null },
): Promise<TrainingSession> {
  return apiFetch<TrainingSession>(`/api/v1/sessions/${sessionId}/blocks/${blockId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function updateSet(
  sessionId: string,
  blockId: string,
  setId: string,
  payload: {
    distance_m?: number | null;
    intensity_note?: string | null;
    label?: string | null;
  },
): Promise<TrainingSession> {
  return apiFetch<TrainingSession>(
    `/api/v1/sessions/${sessionId}/blocks/${blockId}/sets/${setId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
    },
  );
}

export async function reviewSession(
  sessionId: string,
  payload: { decision: ReviewDecision; comment?: string },
): Promise<TrainingSession> {
  return apiFetch<TrainingSession>(`/api/v1/sessions/${sessionId}/review`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
