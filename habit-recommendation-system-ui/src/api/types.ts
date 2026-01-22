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

export type IngestOut = {
  ok: boolean;
  message: string;
  data: {
    uuid: string;
    habit: string;
    language: string;
    result: ContextItem[];
    mapping_params?: MappingParams;
    _meta?: {
      mongo_id?: string;
      created_at?: string;
      mapping_params?: MappingParams;
    };
    bcio_mapping_error?: string | null;
  };
};

export type HabitItem = {
  _id: string | null;
  created_at: string | null;

  uuid: string;
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
  ok: boolean;
  message: string;
  data: T | null;
};

export type ProfileMeta = {
  mongo_id?: string;
  created_at?: string;
  updated_at?: string;
  collection?: ProfileFormKey;
};

export type ProfileLatestUpsertData = {
  profile_uuid: string;
  form: ProfileFormKey;
  _meta?: ProfileMeta;
};

export type ProfileLatestUpsertOut = ApiOut<ProfileLatestUpsertData>;

export type ProfileLatestItem = {
  profile_uuid: string;
  form: ProfileFormKey;
  data: Record<string, any>;
  updated_at?: string;
  _meta?: ProfileMeta;
};

export type ProfileLatestGetOut = ApiOut<ProfileLatestItem | Partial<Record<ProfileFormKey, ProfileLatestItem>>>;
