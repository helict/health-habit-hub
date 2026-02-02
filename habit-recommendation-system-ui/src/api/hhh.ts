import { jsonFetch, API_BASE } from "./utils";
import type {
  IngestOut,
  HabitsListResponse,
  ProfileFormKey,
  ProfileLatestUpsertOut,
  ProfileLatestGetOut,
  ProfileAnswerItem,

  // workflow3
  RecommendOut,
  RecommendCommentReq,
} from "./types";

// ---------------------------
// Workflow1: Habit ingest + list
// ---------------------------

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

// ---------------------------
// Workflow3: Recommendation
// ---------------------------

/**
 * /recommend
 */
export async function recommend(text: string): Promise<RecommendOut> {
  return jsonFetch<RecommendOut>(`${API_BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

/**
 * /recommend/comment
 */
export async function recommendComment(req: RecommendCommentReq): Promise<any> {
  return jsonFetch<any>(`${API_BASE}/recommend/comment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
}

// ---------------------------
// Workflow3: Recommendation (History)
// ---------------------------

export type RecommendHistoryListResponse = {
  ok: boolean;
  total: number;
  limit: number;
  skip: number;
  items: RecommendOut[];
};

/**
 * GET /recommend/history
 */
export async function listRecommendHistory(params: {
  limit: number;
  skip: number;
}): Promise<RecommendHistoryListResponse> {
  const q = new URLSearchParams({
    limit: String(params.limit),
    skip: String(params.skip),
  });
  return jsonFetch<RecommendHistoryListResponse>(
    `${API_BASE}/recommend/history?${q.toString()}`
  );
}