import { jsonFetch, API_BASE } from "./utils";
import type { IngestOut, HabitsListResponse, SystemConfigResponse } from "./types";

export async function ingest(habit: string, language: string): Promise<IngestOut> {
  return jsonFetch<IngestOut>(`${API_BASE}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ habit, language }),
  });
}

export async function listHabits(params: {
  limit: number;
  skip: number;
  only_habits: boolean;
}): Promise<HabitsListResponse> {
  const q = new URLSearchParams({
    limit: String(params.limit),
    skip: String(params.skip),
    only_habits: String(params.only_habits),
  });
  return jsonFetch<HabitsListResponse>(`${API_BASE}/habits?${q.toString()}`);
}

export async function systemConfig(): Promise<SystemConfigResponse> {
  return jsonFetch<SystemConfigResponse>(`${API_BASE}/system/config`);
}
