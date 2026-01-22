import { jsonFetch, API_BASE } from "./utils";
import type {
  IngestOut,
  HabitsListResponse,
  SystemConfigResponse,
  ProfileFormKey,
  ProfileLatestUpsertOut,
  ProfileLatestGetOut,
  ProfileAnswerItem
} from "./types";

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

// ---------------------------
// Workflow2: Profile
// ---------------------------
export async function putProfileLatest(
  profile_uuid: string,
  form: ProfileFormKey,
  data: ProfileAnswerItem[] | Record<string, any>
): Promise<ProfileLatestUpsertOut> {
  return jsonFetch<ProfileLatestUpsertOut>(
    `${API_BASE}/profile/${encodeURIComponent(profile_uuid)}/latest`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ form, data }),
    }
  );
}

export async function getProfileLatest(
  profile_uuid: string,
  form: ProfileFormKey
): Promise<ProfileLatestGetOut> {
  const q = new URLSearchParams({ form });
  return jsonFetch<ProfileLatestGetOut>(
    `${API_BASE}/profile/${encodeURIComponent(profile_uuid)}/latest?${q.toString()}`
  );
}
