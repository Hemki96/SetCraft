export interface SourceSummary {
  id: string;
  source_type: "docx" | "pdf" | "text";
  source_status: string;
  original_filename: string | null;
  ingested_at: string;
}

export interface TrainingSet {
  id: string;
  label: string | null;
  distance_m: number | null;
}

export interface SessionBlock {
  id: string;
  title: string | null;
  block_type: string | null;
  sets: TrainingSet[];
}

export interface SessionItem {
  id: string;
  title: string | null;
  review_status: string;
  approval_status: string;
  total_distance_m: number | null;
  duration_min: number | null;
  tags: string[];
  blocks: SessionBlock[];
}

export interface GeneratedPlan {
  id: string;
  plan_type: "session_plan" | "week_plan";
  review_status: string;
  approval_status: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { message?: string }
      | null;
    throw new Error(payload?.message ?? `Request failed (${response.status})`);
  }

  return (await response.json()) as T;
}

export function createSource(params: {
  source_type: "docx" | "pdf" | "text";
  content: string;
  original_filename?: string;
}): Promise<SourceSummary> {
  return request<SourceSummary>("/api/v1/sources", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export function listSources(): Promise<{ items: SourceSummary[] }> {
  return request<{ items: SourceSummary[] }>("/api/v1/sources");
}

export function listSessions(): Promise<{ items: SessionItem[] }> {
  return request<{ items: SessionItem[] }>("/api/v1/sessions");
}

export function reviewSession(sessionId: string, decision: "reviewed" | "corrected"): Promise<SessionItem> {
  return request<SessionItem>(`/api/v1/sessions/${sessionId}/review`, {
    method: "POST",
    body: JSON.stringify({ decision }),
  });
}

export function approveSession(sessionId: string): Promise<SessionItem> {
  return request<SessionItem>(`/api/v1/sessions/${sessionId}/approve`, {
    method: "POST",
    headers: {
      "x-user-id": "web-admin",
      "x-user-role": "admin",
    },
  });
}

export function generateSessionPlan(target_distance_m: number): Promise<GeneratedPlan> {
  return request<GeneratedPlan>("/api/v1/generation/sessions", {
    method: "POST",
    body: JSON.stringify({ target_distance_m }),
  });
}

export function generateWeekPlan(target_total_distance_m: number, sessions_per_week: number): Promise<GeneratedPlan> {
  return request<GeneratedPlan>("/api/v1/generation/week-plans", {
    method: "POST",
    body: JSON.stringify({ target_total_distance_m, sessions_per_week }),
  });
}

export function approveGeneratedPlan(planId: string): Promise<{ approved: boolean; plan: GeneratedPlan }> {
  return request<{ approved: boolean; plan: GeneratedPlan }>(`/api/v1/generation/plans/${planId}/approve`, {
    method: "POST",
    headers: {
      "x-user-id": "web-admin",
      "x-user-role": "admin",
    },
  });
}

export function createExport(planId: string): Promise<{ id: string; status: string }> {
  return request<{ id: string; status: string }>("/api/v1/exports", {
    method: "POST",
    body: JSON.stringify({ generated_plan_id: planId, export_format: "json" }),
  });
}
