<!-- src/pages/HealthProfile.vue -->
<template>
  <div class="hp">
    <div class="card">
      <div class="header">
        <div class="titleBlock">
          <h2>Health Profile</h2>
          <p class="sub">
            Switch between <b>Basic</b> / <b>SLIQ</b> / <b>WHOQOL-BREF</b>. Backend stores only the latest submission
            per
            form.
          </p>
        </div>

        <div class="right">
          <div class="tabs">
            <button class="btn" :class="{ primary: active === 'basic' }" @click="active = 'basic'">Basic</button>
            <button class="btn" :class="{ primary: active === 'sliq' }" @click="active = 'sliq'">SLIQ</button>
            <button class="btn" :class="{ primary: active === 'whoqol' }"
              @click="active = 'whoqol'">WHOQOL-BREF</button>
          </div>

          <div class="metaRow">
            <span class="label">profile_uuid</span>
            <code class="mono">{{ profileUuid }}</code>

            <span v-if="status.kind !== 'idle'" class="status" :class="status.kind">
              <span class="dot"></span>
              <span>{{ status.text }}</span>
            </span>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="body">
        <keep-alive>
          <SurveyComponent :model="currentModel" />
        </keep-alive>
      </div>

      <details v-if="lastResp" class="debug">
        <summary>Last API response</summary>
        <pre>{{ JSON.stringify(lastResp, null, 2) }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { Model } from "survey-core";
import { SurveyComponent } from "survey-vue3-ui";
import * as SurveyThemes from "survey-core/themes";
import "survey-core/survey-core.css";

import { getProfileLatest, putProfileLatest } from "../api/hhh";
import type { ProfileFormKey, ProfileLatestGetOut, ProfileLatestUpsertOut } from "../api/types";

// -----------------------------
// profile_uuid (anonymous device id)
// -----------------------------
function getOrCreateProfileUuid(): string {
  const k = "profile_uuid";
  const ex = localStorage.getItem(k);
  if (ex) return ex;
  const u = crypto.randomUUID();
  localStorage.setItem(k, u);
  return u;
}

const profileUuid = getOrCreateProfileUuid();
const active = ref<ProfileFormKey>("basic");
const lastResp = ref<any>(null);

const status = ref<{ kind: "idle" | "saving" | "saved" | "error"; text: string }>({
  kind: "idle",
  text: "",
});

// -----------------------------
// Survey JSONs (placeholders)
// -----------------------------
const basicJson = {
  title: "Basic Health Profile",
  showQuestionNumbers: "off",
  elements: [
    // --------------------
    // Required
    // --------------------
    { type: "text", name: "age", title: "Age", isRequired: true, inputType: "number", min: 16, max: 120 },

    {
      type: "dropdown",
      name: "sex",
      title: "Sex / Gender",
      isRequired: true,
      choices: [
        { value: "female", text: "Female" },
        { value: "male", text: "Male" },
        { value: "diverse", text: "Diverse" },
        { value: "prefer_not_say", text: "Prefer not to say" },
      ],
    },

    // {
    //   type: "dropdown",
    //   name: "primary_goal",
    //   title: "Primary goal",
    //   isRequired: true,
    //   choices: [
    //     { value: "sleep", text: "Improve sleep" },
    //     { value: "stress", text: "Reduce stress" },
    //     { value: "fitness", text: "Increase fitness" },
    //     { value: "diet", text: "Eat healthier" },
    //     { value: "weight", text: "Weight management" },
    //     { value: "general", text: "General health" },
    //   ],
    // },


    { type: "text", name: "height_cm", title: "Height (cm)", isRequired: true, inputType: "number", min: 100, max: 230 },

    { type: "text", name: "weight_kg", title: "Weight (kg)", isRequired: true, inputType: "number", min: 30, max: 250 },


    {
      type: "dropdown",
      name: "limitations",
      title: "Physical limitations",
      isRequired: true,
      choices: [
        { value: "none", text: "None" },
        { value: "knee", text: "Knee problems" },
        { value: "back", text: "Back problems" },
        { value: "cardio", text: "Cardiovascular limitations" },
        { value: "other", text: "Other" },
      ],
    },

    {
      type: "text",
      name: "limitations_other",
      title: "If other, please specify",
      isRequired: true,
      visibleIf: "{limitations} = 'other'",
      placeholder: "e.g., shoulder injury, asthma, etc.",
    },

    {
      type: "dropdown",
      name: "time_budget",
      title: "Daily time budget for new behavior changes",
      isRequired: true,
      choices: [
        { value: "lt5", text: "< 5 minutes" },
        { value: "5_10", text: "5–10 minutes" },
        { value: "10_20", text: "10–20 minutes" },
        { value: "20_30", text: "20–30 minutes" },
        { value: "30_plus", text: "30+ minutes" },
      ],
    },

    {
  type: "html",
  name: "additional_info_hint",
  html:
    `<div style="padding:10px 12px;border:1px solid rgba(15,23,42,0.08);border-radius:12px;background:rgba(15,23,42,0.02);">
      <b>Additional info (optional)</b><br/>
      If the questions above feel limited, you can add anything you think is relevant for better recommendations.
      <ul style="margin:8px 0 0 18px;">
        <li>NCD history (e.g., diabetes, hypertension, CVD, COPD, cancer)</li>
        <li>Current medication, allergies, injuries/limitations</li>
        <li>Diet preferences, daily routine constraints, what has/hasn't worked for you</li>
      </ul>
      <span style="opacity:0.75;">Please avoid sharing personal identifiers (names, exact addresses, etc.).</span>
    </div>`,
},

    // --------------------
    // Optional
    // --------------------
{
  type: "comment",
  name: "additional_notes",
  title: "Free notes (optional)",
  isRequired: false,
  placeholder:
    "E.g., I have hypertension and take medication; I prefer low-impact activities; night shifts; allergies; main barriers; etc.",
  rows: 6,
  autoGrow: true,
  maxLength: 2000,
},
  ],
};

const sliqJson = {
  title: "SLIQ (Lifestyle)",
  description: "Replace item wording with your approved/licensed text.",
  showQuestionNumbers: "off",
  elements: [
    { type: "radiogroup", name: "sliq_q1", title: "SLIQ Q1", isRequired: true, choices: [1, 2, 3, 4, 5] },
    { type: "radiogroup", name: "sliq_q2", title: "SLIQ Q2", isRequired: true, choices: [1, 2, 3, 4, 5] },
  ],
};

const whoqolJson = {
  title: "WHOQOL-BREF",
  description: "26 items, 1–5 scale. Replace item wording with your approved/licensed text.",
  showQuestionNumbers: "off",
  elements: Array.from({ length: 26 }, (_, i) => ({
    type: "radiogroup",
    name: `whoqol_q${i + 1}`,
    title: `WHOQOL Q${i + 1}`,
    isRequired: true,
    choices: [1, 2, 3, 4, 5],
  })),
};

// -----------------------------
// One Model per form (keep state)
// -----------------------------
const basicModel = new Model(basicJson);
const sliqModel = new Model(sliqJson);
const whoqolModel = new Model(whoqolJson);

// Theme: base + CSS variables
const base = (SurveyThemes as any).FlatLightPanelless ?? (SurveyThemes as any).LayeredLightPanelless;
const theme: any = JSON.parse(JSON.stringify(base));
theme.cssVariables = {
  ...(theme.cssVariables || {}),
  "--sjs-primary-backcolor": "rgb(219,234,254)",
  "--sjs-primary-forecolor": "rgb(30,64,175)",
  "--sjs-primary-backcolor-light": "rgb(239,246,255)",
  "--sjs-primary-backcolor-dark": "rgb(191,219,254)",
  "--sjs-font-family": "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial",
  "--sjs-font-size": "14px",
  "--sjs-corner-radius": "12px",
  "--sjs-base-unit": "8px",
  "--sjs-general-backcolor": "#fff",
  "--sjs-general-backcolor-dim": "#fff",
  "--sjs-shadow-small": "0 10px 30px rgba(15,23,42,0.06)",
};

[basicModel, sliqModel, whoqolModel].forEach((m) => {
  m.applyTheme(theme);
  m.completeText = "Save";
  // Avoid completion screen
  (m as any).showCompletedPage = false;
  (m as any).completedHtml = "";
});

function modelByForm(f: ProfileFormKey): Model {
  if (f === "basic") return basicModel;
  if (f === "sliq") return sliqModel;
  return whoqolModel;
}

// -----------------------------
// Load latest (once per form unless forced)
// -----------------------------
const loaded = ref<Record<ProfileFormKey, boolean>>({
  basic: false,
  sliq: false,
  whoqol: false,
});

function extractFormData(r: ProfileLatestGetOut): Record<string, any> | null {
  const payload: any = (r as any)?.data ?? null;
  if (!payload) return null;
  if (typeof payload === "object" && "data" in payload) return (payload as any).data ?? {};
  return null;
}

async function loadLatest(form: ProfileFormKey, opts?: { force?: boolean }) {
  const force = !!opts?.force;
  if (!force && loaded.value[form]) return;

  status.value = { kind: "saving", text: "Loading..." };
  try {
    const r = (await getProfileLatest(profileUuid, form)) as ProfileLatestGetOut;
    lastResp.value = r;

    const data = extractFormData(r);
    modelByForm(form).data = data ?? {};

    loaded.value[form] = true;
    status.value = { kind: "idle", text: "" };
  } catch (e) {
    status.value = { kind: "error", text: "Load failed" };
    console.error("Load failed:", e);
  }
}

// -----------------------------
// Save (PUT latest), then re-load (optional)
// -----------------------------
async function save(form: ProfileFormKey, data: Record<string, any>) {
  status.value = { kind: "saving", text: "Saving..." };

  // 1) PUT: save
  try {
    const r = (await putProfileLatest(profileUuid, form, data)) as ProfileLatestUpsertOut;
    lastResp.value = r;
  } catch (e) {
    status.value = { kind: "error", text: "Save failed" };
    console.error("PUT failed:", e);
    return;
  }

  // 2) GET again: keep UI == DB latest (if GET fails, don't mark save as failed)
  try {
    await loadLatest(form, { force: true });
  } catch (e) {
    console.warn("Reload failed (but save succeeded):", e);
  }

  status.value = { kind: "saved", text: "Saved" };
  setTimeout(() => {
    if (status.value.kind === "saved") status.value = { kind: "idle", text: "" };
  }, 1200);
}

// -----------------------------
// Wire "Save" button WITHOUT completing survey
// -----------------------------
function wireSave(m: Model, form: ProfileFormKey) {
  // IMPORTANT: use onCompleting to prevent "completed" state
  (m as any).onCompleting.add((sender: any, opt: any) => {
    if (opt) opt.allowComplete = false; // block completion
    save(form, sender.data);
  });
}

wireSave(basicModel, "basic");
wireSave(sliqModel, "sliq");
wireSave(whoqolModel, "whoqol");

// -----------------------------
// Lifecycle
// -----------------------------
onMounted(() => loadLatest(active.value));
watch(active, (f) => loadLatest(f));

const currentModel = computed(() => modelByForm(active.value));
</script>

<style scoped>
.hp {
  max-width: 1100px;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 18px;
  padding: 16px 18px 18px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.titleBlock h2 {
  margin: 0;
  font-size: 22px;
  letter-spacing: -0.01em;
}

.sub {
  margin: 6px 0 0;
  opacity: 0.75;
  font-size: 13px;
  line-height: 1.35;
}

.right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  min-width: 360px;
}

.tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn {
  position: relative;
  padding: 10px 13px;
  border-radius: 999px;
  border: 1px solid rgba(17, 24, 39, 0.1);
  background: rgba(17, 24, 39, 0.03);
  font-weight: 850;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
  user-select: none;
  transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease, background-color 120ms ease;
}

.btn.primary {
  background: rgba(59, 130, 246, 0.12);
  border-color: rgba(59, 130, 246, 0.28);
  color: rgba(37, 99, 235, 0.98);
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
}

.btn:active {
  transform: translateY(0px) scale(0.98);
  box-shadow: 0 6px 12px rgba(15, 23, 42, 0.06);
}

.btn:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.7);
  outline-offset: 2px;
}

.metaRow {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label {
  font-size: 12px;
  opacity: 0.7;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  background: rgba(15, 23, 42, 0.04);
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 9px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  background: rgba(17, 24, 39, 0.03);
}

.status .dot {
  width: 7px;
  height: 7px;
  border-radius: 99px;
  background: rgba(100, 116, 139, 0.9);
}

.status.saving {
  background: rgba(59, 130, 246, 0.08);
  border-color: rgba(59, 130, 246, 0.18);
}

.status.saving .dot {
  background: rgba(37, 99, 235, 0.9);
}

.status.saved {
  background: rgba(34, 197, 94, 0.08);
  border-color: rgba(34, 197, 94, 0.18);
}

.status.saved .dot {
  background: rgba(22, 163, 74, 0.9);
}

.status.error {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.18);
}

.status.error .dot {
  background: rgba(220, 38, 38, 0.9);
}

.divider {
  height: 1px;
  background: rgba(15, 23, 42, 0.08);
  margin: 14px 0;
}

.body {
  padding: 6px 2px 0;
  padding-bottom: 22px;
  /* sticky nav spacing */
}

/* =========================================================
   SurveyJS polish (deep)
   ========================================================= */
:deep(.sd-root-modern),
:deep(.sv-root-modern) {
  width: 100%;
}

:deep(.sd-container-modern),
:deep(.sv-container-modern) {
  max-width: 760px;
  margin: 0 auto;
  padding: 0 !important;
}

:deep(.sd-title),
:deep(.sv-title) {
  font-size: 18px !important;
  font-weight: 900 !important;
  color: rgb(15, 23, 42) !important;
  margin-bottom: 10px !important;
}

:deep(.sd-question__title),
:deep(.sv-question__title) {
  font-weight: 800 !important;
  color: rgb(15, 23, 42) !important;
}

/* inputs */
:deep(input.sd-input),
:deep(textarea.sd-input),
:deep(.sd-dropdown),
:deep(.sd-text),
:deep(.sv_q_text_root input),
:deep(.sv_q_dropdown_control) {
  border-radius: 12px !important;
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  background: #fff !important;
  box-shadow: none !important;
  padding: 10px 12px !important;
}

/* save button */
:deep(.sd-btn),
:deep(.sv-btn) {
  border-radius: 12px !important;
  font-weight: 850 !important;
  padding: 10px 14px !important;
  transition: transform 120ms ease, box-shadow 120ms ease, background-color 120ms ease, border-color 120ms ease !important;
}

:deep(.sd-btn:hover),
:deep(.sv-btn:hover) {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.10);
}

:deep(.sd-btn:active),
:deep(.sv-btn:active) {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 6px 12px rgba(15, 23, 42, 0.08);
}

/* navigation right-bottom + sticky */
:deep(.sd-body__navigation),
:deep(.sd-navigation),
:deep(.sv_nav) {
  display: flex !important;
  justify-content: flex-end !important;
  align-items: center !important;
  width: 100% !important;

  position: sticky;
  bottom: 0;
  z-index: 5;

  padding-top: 12px;
  background: linear-gradient(to top, #fff 70%, rgba(255, 255, 255, 0));
}

/* push complete/save to right */
:deep(.sd-navigation__complete-btn),
:deep(.sd-navigation__complete-btn .sd-btn),
:deep(.sv_complete_btn),
:deep(.sv_complete_btn .sv-btn) {
  margin-left: auto !important;
}


/* debug */
.debug {
  margin-top: 14px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.02);
}

.debug summary {
  cursor: pointer;
  font-weight: 800;
  font-size: 13px;
  opacity: 0.8;
}

pre {
  margin: 10px 0 0;
  white-space: pre-wrap;
  font-size: 12px;
}
</style>
