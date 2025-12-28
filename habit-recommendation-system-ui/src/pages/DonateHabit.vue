<script setup lang="ts">
import { ref } from "vue";
import { ingest } from "../api/hhh";
import type { HabitItem, IngestOut } from "../api/types";
import HabitCard from "../components/HabitCard.vue";
import JsonBlock from "../components/JsonBlock.vue";

const habit = ref("");
const language = ref("en");

const loading = ref(false);
const error = ref<string | null>(null);
const resp = ref<IngestOut | null>(null);

function toHabitItem(r: IngestOut): HabitItem {
  const d = r.data;
  const meta = d._meta || {};
  return {
    _id: meta.mongo_id ?? null,
    created_at: meta.created_at ?? null,
    uuid: d.uuid,
    habit: d.habit,
    language: d.language,
    habit_class: r.ok ? 1 : 0,
    confidence: null,
    contexts_raw: [],
    contexts_mapped: d.result ?? [],
    bcio_mapping_error: d.bcio_mapping_error ?? null,
    mapping_params: meta.mapping_params ?? d.mapping_params ?? null,
  };
}

async function submit() {
  error.value = null;
  resp.value = null;

  const text = habit.value.trim();
  if (!text) {
    error.value = "Please enter a habit sentence first.";
    return;
  }

  loading.value = true;
  try {
    resp.value = await ingest(text, language.value);
    habit.value = "";
  } catch (e: any) {
    error.value = e?.message || String(e);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card">
    <div class="row" style="justify-content:space-between; align-items:flex-start">
      <div>
        <div style="font-weight:950; font-size:18px">Donate a Habit (Workflow 1)</div>
        <div class="muted" style="font-size:13px; margin-top:6px">
          Calls <code>POST /ingest</code>: habit detection → context extraction → BCIO mapping → MongoDB.
        </div>
      </div>
      <div class="badge">/ingest</div>
    </div>

    <div class="hr"></div>

    <div class="row">
      <div style="flex:1; min-width:300px">
        <label class="muted" style="font-size:13px">Habit sentence</label>
        <textarea
          class="textarea"
          v-model="habit"
          placeholder='e.g., "I try to disconnect from screens an hour before sleep to unwind."'
        />
      </div>

      <div style="width:240px; min-width:220px" class="col">
        <div>
          <label class="muted" style="font-size:13px">Language</label>
          <select class="select" v-model="language">
            <option value="en">en</option>
            <option value="de">de</option>
            <option value="zh">zh</option>
          </select>
        </div>

        <button class="btn primary" :disabled="loading" @click="submit">
          {{ loading ? "Processing..." : "Submit /ingest" }}
        </button>

        <RouterLink class="btn" to="/manage">Go to management →</RouterLink>
      </div>
    </div>

    <div v-if="error" class="hr"></div>
    <div v-if="error" class="card" style="border-color: rgba(239,68,68,.25)">
      <div style="font-weight:900">Error</div>
      <div class="muted" style="white-space:pre-wrap">{{ error }}</div>
    </div>

    <div v-if="resp" class="hr"></div>
    <div v-if="resp" class="card" style="background:#fff">
      <div class="row" style="justify-content:space-between; align-items:center">
        <div style="font-weight:900">Response</div>
        <span class="badge" :class="resp.ok ? 'ok' : 'no'">
          {{ resp.ok ? "OK" : "Not a habit" }}
        </span>
      </div>

      <div class="muted" style="margin-top:8px; white-space:pre-wrap">{{ resp.message }}</div>

      <div class="hr"></div>

      <HabitCard :item="toHabitItem(resp)" />

      <div style="margin-top:12px">
        <details>
          <summary style="cursor:pointer; font-weight:900">Raw JSON</summary>
          <JsonBlock :value="resp" />
        </details>
      </div>
    </div>
  </div>
</template>
