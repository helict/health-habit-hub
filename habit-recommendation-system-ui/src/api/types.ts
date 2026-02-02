// ---------------------------
// Shared: Habit / Context
// ---------------------------

export type MappingParams = {
  threshold: number;
  top_n: number;
};

export type BcioMapping = {
  bcio_label: string;
  iri: string;
  probability: number;
};

export type ContextItem = {
  name: string;
  value: string | null;
  classification: number; // 0/1
  confidence: number;
  bcio_mappings?: BcioMapping[];
};

// ---------------------------
// Workflow1: Ingest + Habits
// ---------------------------

export type IngestDataHabit = {
  habit_key: string;
  habit: string;
  language: string;
  result: ContextItem[];
  bcio_mapping_error?: string | null;
};

export type IngestDataNotHabit = {
  habit_key: string;
  habit: string;
  language: string;
  habit_class: number; // 0/1
  confidence: number | null;
};

/** LLM meta for ingest/listHabits: { habit: {...}, context: {...} } */
export type LlmMeta = {
  habit: Record<string, any>;
  context: Record<string, any>;
};

export type IngestOut = {
  ok: boolean;
  message: string;
  data: IngestDataHabit | IngestDataNotHabit;

  mapping_params?: MappingParams | null;
  llm_meta?: LlmMeta | null;
  created_at?: string | null;
};

export type HabitItem = {
  habit_key: string;
  _id?: string | null;
  created_at?: string | null;
  uuid?: string | null;

  habit: string;
  language: string;

  habit_class: number;
  confidence: number | null;

  contexts_raw: ContextItem[];
  contexts_mapped: ContextItem[];

  bcio_mapping_error?: string | null;
  mapping_params?: MappingParams | null;

  llm_meta?: LlmMeta | null;
};

export type HabitsListResponse = {
  ok: boolean;
  total: number;
  limit: number;
  skip: number;
  items: HabitItem[];
};

// ---------------------------
// Workflow2: Profile
// ---------------------------

export type ProfileFormKey = "basic" | "sliq" | "rand36";

export type ApiOut<T> = {
  success: boolean; // was: ok
  message: string;  // now more detailed
  data: T | null;
};

export type ProfileLatestUpsertData = {
  form: ProfileFormKey;
  created_at?: string;
  updated_at?: string;
};

export type ProfileLatestUpsertOut = ApiOut<ProfileLatestUpsertData>;

export type ProfileAnswerItem = {
  id: string;
  question: string;
  value: any;
  label?: string | null;
};

export type ProfileLatestItem = {
  form: ProfileFormKey;
  data: ProfileAnswerItem[];
  created_at?: string | null;
  updated_at?: string | null;
};

export type ProfileLatestGetOut = ApiOut<
  ProfileLatestItem | Partial<Record<ProfileFormKey, ProfileLatestItem>>
>;

// ---------------------------
// Workflow3: Recommendation
// ---------------------------

/** LLM meta for workflow3 */
export type LlmMetaWorkflow3 = {
  provider?: string;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  top_k?: number;
};

export type RetrievalInfo = {
  top_n?: number;
  score_threshold?: number;
};

export type KbHit = {
  score: number;
  doc_id: string;
  domain: string;
  chunk_id: number;
  page_number: number;
  text: string;
  doc_title?: string | null;
  doc_summary?: string | null;
};

export type HabitRecommendation = {
  context: string;
  behavior: string;
  explanation: string;
};

export type SelectedHabitOut = {
  habit: string;
  habit_key: string;
  score: number;
  reason: string;
  contexts: ContextItem[];
  retrieval?: any;
};

export type RecommendOut = {
  request_uuid: string;
  text: string;
  text_signature?: string | null;
  created_at?: string;

  selected_habits?: {
    llm_meta?: LlmMetaWorkflow3;
    selected_habits: SelectedHabitOut[];
    selected_habits_summary?: string;
  };

  bilded_profiles?: {
    llm_meta?: LlmMetaWorkflow3;
    profile_detailed?: string;
    profile_summary?: string;
  };

  kb_queries?: {
    query?: string;
    llm_meta?: LlmMetaWorkflow3;
    retrieval?: RetrievalInfo;
    hits?: KbHit[];
  };

  recommendation_results_outputs?: {
    habit_recommendations?: HabitRecommendation[];
    llm_meta?: LlmMetaWorkflow3;
    message?: string;
  };

  user_feedback?: string | null;
};

export type RecommendCommentReq = {
  request_uuid: string;
  text: string;
  text_signature: string;
  comment: string;
};
