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

export type IngestOut = {
  ok: boolean;
  message: string;
  data: IngestDataHabit | IngestDataNotHabit;

  mapping_params?: MappingParams | null;
  llm_meta?: Record<string, any> | null;
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
};

export type HabitsListResponse = {
  ok: boolean;
  total: number;
  limit: number;
  skip: number;
  items: HabitItem[];
};

export type SystemConfigResponse = {
  ok: boolean;
  api_base: string;
  mapping_params: MappingParams;
};

// ---------------------------
// Workflow2: Profile
// ---------------------------
export type ProfileFormKey = "basic" | "sliq" | "rand36";

export type ApiOut<T> = {
  success: boolean;   // was: ok
  message: string;    // now more detailed
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