<script setup lang="ts">
import { ref, computed } from "vue";
import { ingest } from "../api/hhh";
import type { HabitItem, IngestOut } from "../api/types";
import HabitCard from "../components/HabitCard.vue";
import JsonBlock from "../components/JsonBlock.vue";

const habit = ref("");
const language = ref("en");

const loading = ref(false);
const error = ref<string | null>(null);
const resp = ref<IngestOut | null>(null);

/**
 * UI-safe response:
 * remove fields you never want to show in the UI (e.g., created_at)
 */
const respUi = computed(() => {
  if (!resp.value) return null;
  const { created_at, ...rest } = resp.value as any;
  return rest;
});

function toHabitItem(r: IngestOut): HabitItem {
  const d: any = r.data || {};
  const isHabit = r.ok === true;

  return {
    habit_key: d.habit_key,
    habit: d.habit,
    language: d.language,

    uuid: null,
    created_at: null, // never show created_at in HabitCard

    habit_class: isHabit ? 1 : (d.habit_class ?? 0),
    confidence: isHabit ? null : (d.confidence ?? null),

    contexts_raw: [],
    contexts_mapped: isHabit ? (d.result ?? []) : [],

    bcio_mapping_error: d.bcio_mapping_error ?? null,
    mapping_params: r.mapping_params ?? null,
    llm_meta: r.llm_meta ?? null,
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
  <div class="page">
    <div class="card donateCard">
      <div class="row headerRow">
        <div>
          <div class="title">Donate a Habit (Workflow 1)</div>
          <div class="muted desc">
            Calls <code>POST /ingest</code>: habit detection → context extraction → BCIO mapping → MongoDB.
          </div>
        </div>
        <!-- <div class="badge">/ingest</div> -->
      </div>

      <div class="hr"></div>

      <div class="row mainRow">
        <div class="left">
          <label class="muted label">Habit sentence</label>
          <textarea
            class="textarea bigTextarea"
            v-model="habit"
            placeholder='e.g., "I try to disconnect from screens an hour before sleep to unwind."'
          ></textarea>
          <div class="hint muted">Tip: one sentence is enough. Context like time/place/people helps.</div>
        </div>

        <div class="right col">
          <div>
            <label class="muted label">Language</label>
            <select class="select" v-model="language">
              <option value="en">en</option>
              <option value="de">de</option>
              <option value="zh">zh</option>
            </select>
          </div>

          <div class="spacer"></div>

          <button class="btn primary bigBtn btnFx" :disabled="loading" @click="submit">
            {{ loading ? "Processing..." : "Submit /ingest" }}
          </button>

          <RouterLink class="btn bigBtn btnFx" to="/manage">Go to management →</RouterLink>
        </div>
      </div>

      <div v-if="error" class="hr"></div>
      <div v-if="error" class="card errorCard">
        <div class="errTitle">Error</div>
        <div class="muted" style="white-space: pre-wrap">{{ error }}</div>
      </div>

      <div v-if="resp" class="hr"></div>
      <div v-if="resp" class="card respCard">
        <div class="row" style="justify-content: space-between; align-items: center">
          <div class="respTitle">Response</div>
          <span class="badge" :class="resp.ok ? 'ok' : 'no'">
            {{ resp.ok ? "OK" : "Not a habit" }}
          </span>
        </div>

        <div class="muted" style="margin-top: 8px; white-space: pre-wrap">{{ resp.message }}</div>

        <div class="hr"></div>

        <HabitCard :item="toHabitItem(resp)" />

        <div style="margin-top: 12px">
          <details>
            <summary style="cursor: pointer; font-weight: 900">Raw JSON</summary>
            <!-- use respUi so created_at never appears -->
            <JsonBlock :value="respUi" />
          </details>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.page {
  max-width: 1100px;
  margin: 22px auto 0;
  padding: 0 14px 60px;
}

.donateCard {
  padding: 16px 18px 20px;
  border-radius: 18px;
  min-height: 600px;
}

.headerRow {
  justify-content: space-between;
  align-items: flex-start;
}

.title {
  font-weight: 950;
  font-size: 18px;
}

.desc {
  font-size: 13px;
  margin-top: 6px;
}

.mainRow {
  gap: 16px;
  align-items: stretch;
}

.left {
  flex: 1;
  min-width: 340px;
}

.label {
  font-size: 13px;
}

.bigTextarea {
  min-height: 440px;
  resize: vertical;
}

.hint {
  margin-top: 8px;
  font-size: 12px;
  opacity: 0.75;
}

.right {
  width: 260px;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
}

.bigBtn {
  padding: 10px 12px;
  border-radius: 12px;
}

.right .bigBtn {
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.2;
}

.spacer {
  flex: 1;
  min-height: 0;
  max-height: 315px;
}

.errorCard {
  border-color: rgba(239, 68, 68, 0.25);
  background: rgba(239, 68, 68, 0.04);
}
.errTitle {
  font-weight: 900;
  margin-bottom: 4px;
}

.respCard {
  background: #fff;
}
.respTitle {
  font-weight: 900;
}


.btnFx{
  background: rgb(248, 250, 252) !important;
  border-color: rgb(226, 232, 240) !important;
  filter: none !important;

  position: relative;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  transition:
    transform 140ms ease,
    box-shadow 140ms ease,
    border-color 140ms ease,
    background-color 140ms ease;
}

.btnFx:hover{
  background: rgb(241, 245, 249) !important;
  border-color: rgb(203, 213, 225) !important;
  opacity: 1 !important;
  filter: none !important;

  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.10);
}

.btnFx:active{
  background: rgb(226, 232, 240) !important;
  opacity: 1 !important;
  filter: none !important;

  transform: translateY(0) scale(0.97);
  box-shadow: 0 6px 12px rgba(15, 23, 42, 0.08);
}


.btn.primary.btnFx{
  background: rgb(239, 246, 255) !important;
  border-color: rgb(191, 219, 254) !important;
  color: rgb(37, 99, 235) !important;
}

.btn.primary.btnFx:hover{
  background: rgb(219, 234, 254) !important;
  border-color: rgb(147, 197, 253) !important;
}

.btn.primary.btnFx:active{
  background: rgb(191, 219, 254) !important;
}

.btnFx:disabled,
.btnFx[aria-disabled="true"]{
  transform: none !important;
  box-shadow: none !important;
  cursor: not-allowed;
  opacity: 0.6 !important;
  filter: none !important;
}
</style>