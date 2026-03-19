export interface HealthStatus {
  state: "ok" | "unreachable";
  source: "api" | "fallback";
  checkedAtIso: string;
}

export async function checkApiHealth(): Promise<HealthStatus> {
  const checkedAtIso = new Date().toISOString();

  try {
    const response = await fetch("/api/v1/health", {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      return {
        state: "unreachable",
        source: "api",
        checkedAtIso,
      };
    }

    return {
      state: "ok",
      source: "api",
      checkedAtIso,
    };
  } catch {
    return {
      state: "unreachable",
      source: "fallback",
      checkedAtIso,
    };
  }
}
