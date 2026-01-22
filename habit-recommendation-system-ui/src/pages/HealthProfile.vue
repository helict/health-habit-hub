<!-- src/pages/HealthProfile.vue -->
<template>
  <div class="hp">
    <div class="card">
      <div class="header">
        <div class="titleBlock">
          <h2>Health Profile</h2>
          <p class="sub">
            Switch between <b>Basic</b> / <b>SLIQ</b> / <b>RAND-36</b>. Backend stores only the latest submission
            per
            form.
          </p>
        </div>

        <div class="right">
          <div class="tabs">
            <button class="btn" :class="{ primary: active === 'basic' }" @click="active = 'basic'">Basic</button>
            <button class="btn" :class="{ primary: active === 'sliq' }" @click="active = 'sliq'">SLIQ</button>
            <button class="btn" :class="{ primary: active === 'rand36' }"
              @click="active = 'rand36'">RAND-36</button>
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
import type { ProfileFormKey, ProfileLatestGetOut, ProfileLatestUpsertOut, ProfileAnswerItem } from "../api/types";


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
  description: "This prototype implements the SLIQ structure and scoring scheme based on Godwin et al. (2008). On-screen item wording is an author-created paraphrase/translation and is not reproduced verbatim from the original questionnaire text. For research/prototyping use only (not for clinical decision-making).",
  showQuestionNumbers: "off",

  elements: [
    // =====================
    // DIET (past year) - 3 questions
    // values: 0..5
    // =====================
    {
  type: "html",
  name: "sliq_citation",
  html:
    `<div style="padding:12px 14px;border:1px solid rgba(15,23,42,0.12);border-radius:12px;background:rgba(15,23,42,0.03);line-height:1.5">
      <b>Source</b>:
      <a
        href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2293321/"
        target="_blank"
        rel="noopener noreferrer"
        style="color:#0f172a; font-weight:700; text-decoration:underline; text-underline-offset:2px;"
      >
        Godwin et al. (2008)
      </a>
      <span style="opacity:0.9;"> (SLIQ structure & scoring scheme)</span>
    </div>`
},
    {
      type: "panel",
      name: "diet_panel",
      title: "Diet (past year)",
      elements: [
        {
          type: "radiogroup",
          name: "sliq_diet_q1",
          title:
            "Over the past year, how often did you eat leafy salad/greens (with or without other vegetables)?",
          isRequired: true,
          choices: [
            { value: 0, text: "Less than 1/week" },
            { value: 1, text: "1/week" },
            { value: 2, text: "2–3 times/week" },
            { value: 3, text: "4–6 times/week" },
            { value: 4, text: "1/day" },
            { value: 5, text: "2+ times/day" }
          ]
        },
        {
          type: "radiogroup",
          name: "sliq_diet_q2",
          title:
            "Over the past year, how often did you eat fruit (fresh/canned/frozen), excluding juices?",
          isRequired: true,
          choices: [
            { value: 0, text: "Less than 1/week" },
            { value: 1, text: "1/week" },
            { value: 2, text: "2–3 times/week" },
            { value: 3, text: "4–6 times/week" },
            { value: 4, text: "1/day" },
            { value: 5, text: "2+ times/day" }
          ]
        },
        {
          type: "radiogroup",
          name: "sliq_diet_q3",
          title:
            "Over the past year, how often did you eat high-fibre cereals / oatmeal / whole-grain breads?",
          isRequired: true,
          choices: [
            { value: 0, text: "Less than 1/week" },
            { value: 1, text: "1/week" },
            { value: 2, text: "2–3 times/week" },
            { value: 3, text: "4–6 times/week" },
            { value: 4, text: "1/day" },
            { value: 5, text: "2+ times/day" }
          ]
        }
      ]
    },

    // =====================
    // EXERCISE (per week, >=30 min each) - 3 questions
    // values per paper:
    // light:   0, 2, 3, 4
    // moderate:0, 4, 6, 8
    // vigorous:0, 6, 9, 12
    // =====================
    {
      type: "panel",
      name: "activity_panel",
      title: "Physical activity (per week, ≥30 minutes each time)",
      elements: [
        {
          type: "radiogroup",
          name: "sliq_act_q1_light",
          title:
            "Light activity (e.g., easy chores, leisurely walking). How many times per week?",
          isRequired: true,
          choices: [
            { value: 0, text: "0/week" },
            { value: 2, text: "1–3 times/week" },
            { value: 3, text: "4–7 times/week" },
            { value: 4, text: "8+ times/week" }
          ]
        },
        {
          type: "radiogroup",
          name: "sliq_act_q2_moderate",
          title:
            "Moderate activity (e.g., brisk walking, cycling, swimming). How many times per week?",
          isRequired: true,
          choices: [
            { value: 0, text: "0/week" },
            { value: 4, text: "1–3 times/week" },
            { value: 6, text: "4–7 times/week" },
            { value: 8, text: "8+ times/week" }
          ]
        },
        {
          type: "radiogroup",
          name: "sliq_act_q3_vigorous",
          title:
            "Vigorous activity (e.g., running/aerobics/weight training). How many times per week?",
          isRequired: true,
          choices: [
            { value: 0, text: "0/week" },
            { value: 6, text: "1–3 times/week" },
            { value: 9, text: "4–7 times/week" },
            { value: 12, text: "8+ times/week" }
          ]
        }
      ]
    },

    // =====================
    // ALCOHOL (average week) - 3 questions (numeric)
    // =====================
    {
      type: "panel",
      name: "alcohol_panel",
      title: "Alcohol consumption (average week)",
      elements: [
        {
          type: "text",
          name: "sliq_alc_wine",
          title: "Wine: drinks per week (approx. 3–5 oz each)",
          isRequired: true,
          inputType: "number",
          min: 0,
          step: 1,
          defaultValue: 0
        },
        {
          type: "text",
          name: "sliq_alc_beer",
          title: "Beer: drinks per week (approx. 10–12 oz / 1 bottle)",
          isRequired: true,
          inputType: "number",
          min: 0,
          step: 1,
          defaultValue: 0
        },
        {
          type: "text",
          name: "sliq_alc_spirits",
          title: "Spirits: drinks per week (approx. 1–1.5 oz each)",
          isRequired: true,
          inputType: "number",
          min: 0,
          step: 1,
          defaultValue: 0
        }
      ]
    },

    // =====================
    // SMOKING - 2 questions (conditional)
    // scoring:
    // smoker yes => 0
    // smoker no + former yes => 1
    // smoker no + former no  => 2
    // =====================
    {
      type: "panel",
      name: "smoking_panel",
      title: "Smoking",
      elements: [
        {
          type: "radiogroup",
          name: "sliq_smoke_current",
          title: "Do you currently smoke?",
          isRequired: true,
          choices: [
            { value: "yes", text: "Yes" },
            { value: "no", text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "sliq_smoke_former",
          title: "If you do not smoke now: have you smoked in the past?",
          visibleIf: "{sliq_smoke_current} = 'no'",
          isRequired: true,
          choices: [
            { value: "yes", text: "Yes" },
            { value: "no", text: "No" }
          ]
        }
      ]
    },

    // =====================
    // STRESS - 1 question
    // options shown as 6..1 (6=not stressful, 1=very stressful)
    // =====================
    {
      type: "panel",
      name: "stress_panel",
      title: "Life stress",
      elements: [
        {
          type: "radiogroup",
          name: "sliq_stress",
          title: "How stressful is your everyday life?",
          isRequired: true,
          choices: [
            { value: 6, text: "6 — Not at all stressful" },
            { value: 5, text: "5" },
            { value: 4, text: "4" },
            { value: 3, text: "3" },
            { value: 2, text: "2" },
            { value: 1, text: "1 — Very stressful" }
          ]
        }
      ]
    },

    // =====================
    // Optional: score preview (you can delete this panel if not needed)
    // =====================
    {
      type: "html",
      name: "sliq_score_preview",
      html:
        `<div style="padding:10px 12px;border:1px solid rgba(15,23,42,0.08);border-radius:12px;background:rgba(15,23,42,0.02);line-height:1.6">
          <b>Diet</b>: raw {diet_raw}, cat {diet_cat}<br/>
          <b>Activity</b>: raw {act_raw}, cat {act_cat}<br/>
          <b>Alcohol</b>: raw {alc_raw}, cat {alc_cat}<br/>
          <b>Smoking</b>: cat {smoke_cat}<br/>
          <b>Stress</b>: raw {stress_raw}, cat {stress_cat}<br/>
          <hr style="border:none;border-top:1px solid rgba(15,23,42,0.12)"/>
          <b>SLIQ total (0–10)</b>: {sliq_total}
        </div>`
    }
  ],

  // =====================
  // Scoring (raw + category + total 0..10), per paper's Figure scoring template
  // =====================
  calculatedValues: [
    // Diet
    { name: "diet_raw", expression: "{sliq_diet_q1}+{sliq_diet_q2}+{sliq_diet_q3}" },
    { name: "diet_cat", expression: "iif({diet_raw}<=5,0,iif({diet_raw}<=10,1,2))" },

    // Activity
    { name: "act_raw", expression: "{sliq_act_q1_light}+{sliq_act_q2_moderate}+{sliq_act_q3_vigorous}" },
    { name: "act_cat", expression: "iif({sliq_act_q3_vigorous}>0,2,iif({sliq_act_q2_moderate}>0,1,0))" },

    // Alcohol
    {
      name: "alc_raw",
      expression:
        "toNumber({sliq_alc_wine}) + toNumber({sliq_alc_beer}) + toNumber({sliq_alc_spirits})"
    },
    { name: "alc_cat", expression: "iif({alc_raw}>=14,0,iif({alc_raw}>=8,1,2))" },

    // Smoking (category same as raw mapping)
    {
      name: "smoke_cat",
      expression:
        "iif({sliq_smoke_current}='yes',0,iif({sliq_smoke_former}='yes',1,2))"
    },

    // Stress
    { name: "stress_raw", expression: "{sliq_stress}" },
    { name: "stress_cat", expression: "iif({stress_raw}<=2,0,iif({stress_raw}<=4,1,2))" },

    // Total SLIQ
    { name: "sliq_total", expression: "{diet_cat}+{act_cat}+{alc_cat}+{smoke_cat}+{stress_cat}" }
  ]
};


// RAND 36-Item Health Survey 1.0 (RAND-36) — SurveyJS JSON + scoring
// Source: RAND MOS SF-36 / RAND-36 questionnaire items & RAND scoring tables.
// - Terms: changes allowed but must be identified; include credit line when distributing.
// - Scoring: recode items to 0–100 (Table 1), then average items per scale (Table 2).

const rand36Json = {
  title: "RAND 36-Item Health Survey (RAND-36) v1.0",
  description:
    "This prototype implements the RAND 36-Item Health Survey 1.0 (RAND-36 / MOS SF-36 items) and scoring according to RAND (Table 1 item recoding to 0–100; Table 2 scale averaging). Item wording shown on screen follows the standard English item wording; any deviations will be explicitly marked. For research/prototyping use only (not for clinical decision-making). When printing/distributing, include the RAND credit line: Developed at RAND as part of the Medical Outcomes Study (MOS).",
  showQuestionNumbers: "off",

  elements: [
    // =====================
    // Citation / terms / scoring note (UI)
    // =====================
    {
      type: "html",
      name: "rand36_citation",
      html: `
        <div style="padding:12px 14px;border:1px solid rgba(15,23,42,0.12);border-radius:12px;background:rgba(15,23,42,0.03);line-height:1.5">
          <b>Source (RAND-36)</b>:
          <a
            href="https://www.rand.org/health/surveys/mos/36-item-short-form/scoring.html"
            target="_blank"
            rel="noopener noreferrer"
            style="color:#0f172a; font-weight:700; text-decoration:underline; text-underline-offset:2px;"
          >RAND Scoring Instructions</a>
          <span style="opacity:0.9;"> (Table 1 recoding; Table 2 scales)</span>
          <br/>
          <b>Terms</b>:
          <a
            href="https://www.rand.org/health/surveys/mos/36-item-short-form/terms.html"
            target="_blank"
            rel="noopener noreferrer"
            style="color:#0f172a; font-weight:700; text-decoration:underline; text-underline-offset:2px;"
          >RAND Terms & Conditions</a>
          <br/>
        </div>
      `
    },

    // =====================
    // GENERAL HEALTH (Items 1–2)
    // =====================
    {
      type: "panel",
      name: "rand36_general_health_panel",
      title: "General health",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q01",
          title: "1. In general, would you say your health is:",
          isRequired: true,
          choices: [
            { value: 1, text: "Excellent" },
            { value: 2, text: "Very good" },
            { value: 3, text: "Good" },
            { value: 4, text: "Fair" },
            { value: 5, text: "Poor" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q02",
          title:
            "2. Compared to one year ago, how would you rate your health in general now?",
          isRequired: true,
          choices: [
            { value: 1, text: "Much better now than one year ago" },
            { value: 2, text: "Somewhat better now than one year ago" },
            { value: 3, text: "About the same" },
            { value: 4, text: "Somewhat worse now than one year ago" },
            { value: 5, text: "Much worse now than one year ago" }
          ]
        }
      ]
    },

    // =====================
    // PHYSICAL FUNCTIONING (Items 3–12)
    // =====================
    {
      type: "panel",
      name: "rand36_pf_panel",
      title:
        "Physical functioning (typical day) — Does your health now limit you in these activities? If so, how much?",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q03",
          title:
            "3. Vigorous activities, such as running, lifting heavy objects, participating in strenuous sports",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q04",
          title:
            "4. Moderate activities, such as moving a table, pushing a vacuum cleaner, bowling, or playing golf",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q05",
          title: "5. Lifting or carrying groceries",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q06",
          title: "6. Climbing several flights of stairs",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q07",
          title: "7. Climbing one flight of stairs",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q08",
          title: "8. Bending, kneeling, or stooping",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q09",
          title: "9. Walking more than a mile",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q10",
          title: "10. Walking several blocks",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q11",
          title: "11. Walking one block",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q12",
          title: "12. Bathing or dressing yourself",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes, limited a lot" },
            { value: 2, text: "Yes, limited a little" },
            { value: 3, text: "No, not limited at all" }
          ]
        }
      ]
    },

    // =====================
    // ROLE LIMITATIONS — PHYSICAL (Items 13–16)
    // =====================
    {
      type: "panel",
      name: "rand36_rp_panel",
      title:
        "Role limitations (physical) — During the past 4 weeks, have you had any of the following problems with your work or other regular daily activities as a result of your physical health?",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q13",
          title:
            "13. Cut down the amount of time you spent on work or other activities",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q14",
          title: "14. Accomplished less than you would like",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q15",
          title: "15. Were limited in the kind of work or other activities",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q16",
          title:
            "16. Had difficulty performing the work or other activities (for example, it took extra effort)",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        }
      ]
    },

    // =====================
    // ROLE LIMITATIONS — EMOTIONAL (Items 17–19)
    // =====================
    {
      type: "panel",
      name: "rand36_re_panel",
      title:
        "Role limitations (emotional) — During the past 4 weeks, have you had any of the following problems with your work or other regular daily activities as a result of any emotional problems (such as feeling depressed or anxious)?",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q17",
          title:
            "17. Cut down the amount of time you spent on work or other activities",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q18",
          title: "18. Accomplished less than you would like",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q19",
          title: "19. Didn't do work or other activities as carefully as usual",
          isRequired: true,
          choices: [
            { value: 1, text: "Yes" },
            { value: 2, text: "No" }
          ]
        }
      ]
    },

    // =====================
    // SOCIAL FUNCTIONING (Item 20) + PAIN (Items 21–22)
    // =====================
    {
      type: "panel",
      name: "rand36_social_pain_panel",
      title: "Social functioning & pain (past 4 weeks)",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q20",
          title:
            "20. During the past 4 weeks, to what extent has your physical health or emotional problems interfered with your normal social activities with family, friends, neighbors, or groups?",
          isRequired: true,
          choices: [
            { value: 1, text: "Not at all" },
            { value: 2, text: "Slightly" },
            { value: 3, text: "Moderately" },
            { value: 4, text: "Quite a bit" },
            { value: 5, text: "Extremely" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q21",
          title: "21. How much bodily pain have you had during the past 4 weeks?",
          isRequired: true,
          choices: [
            { value: 1, text: "None" },
            { value: 2, text: "Very mild" },
            { value: 3, text: "Mild" },
            { value: 4, text: "Moderate" },
            { value: 5, text: "Severe" },
            { value: 6, text: "Very severe" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q22",
          title:
            "22. During the past 4 weeks, how much did pain interfere with your normal work (including both work outside the home and housework)?",
          isRequired: true,
          choices: [
            { value: 1, text: "Not at all" },
            { value: 2, text: "A little bit" },
            { value: 3, text: "Moderately" },
            { value: 4, text: "Quite a bit" },
            { value: 5, text: "Extremely" }
          ]
        }
      ]
    },

    // =====================
    // FEELINGS (Items 23–31)
    // =====================
    {
      type: "panel",
      name: "rand36_feelings_panel",
      title:
        "Feelings (past 4 weeks) — How much of the time during the past 4 weeks…",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q23",
          title: "23. Did you feel full of pep?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q24",
          title: "24. Have you been a very nervous person?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q25",
          title:
            "25. Have you felt so down in the dumps that nothing could cheer you up?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q26",
          title: "26. Have you felt calm and peaceful?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q27",
          title: "27. Did you have a lot of energy?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q28",
          title: "28. Have you felt downhearted and blue?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q29",
          title: "29. Did you feel worn out?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q30",
          title: "30. Have you been a happy person?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q31",
          title: "31. Did you feel tired?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "A good bit of the time" },
            { value: 4, text: "Some of the time" },
            { value: 5, text: "A little of the time" },
            { value: 6, text: "None of the time" }
          ]
        }
      ]
    },

    // =====================
    // SOCIAL FUNCTIONING (Item 32)
    // =====================
    {
      type: "panel",
      name: "rand36_q32_panel",
      title: "Social activities interference (past 4 weeks)",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q32",
          title:
            "32. During the past 4 weeks, how much of the time has your physical health or emotional problems interfered with your social activities (like visiting with friends, relatives, etc.)?",
          isRequired: true,
          choices: [
            { value: 1, text: "All of the time" },
            { value: 2, text: "Most of the time" },
            { value: 3, text: "Some of the time" },
            { value: 4, text: "A little of the time" },
            { value: 5, text: "None of the time" }
          ]
        }
      ]
    },

    // =====================
    // GENERAL HEALTH PERCEPTIONS (Items 33–36)
    // =====================
    {
      type: "panel",
      name: "rand36_ghp_panel",
      title: "General health perceptions",
      elements: [
        {
          type: "radiogroup",
          name: "rand36_q33",
          title: "33. I seem to get sick a little easier than other people",
          isRequired: true,
          choices: [
            { value: 1, text: "Definitely true" },
            { value: 2, text: "Mostly true" },
            { value: 3, text: "Don't know" },
            { value: 4, text: "Mostly false" },
            { value: 5, text: "Definitely false" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q34",
          title: "34. I am as healthy as anybody I know",
          isRequired: true,
          choices: [
            { value: 1, text: "Definitely true" },
            { value: 2, text: "Mostly true" },
            { value: 3, text: "Don't know" },
            { value: 4, text: "Mostly false" },
            { value: 5, text: "Definitely false" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q35",
          title: "35. I expect my health to get worse",
          isRequired: true,
          choices: [
            { value: 1, text: "Definitely true" },
            { value: 2, text: "Mostly true" },
            { value: 3, text: "Don't know" },
            { value: 4, text: "Mostly false" },
            { value: 5, text: "Definitely false" }
          ]
        },
        {
          type: "radiogroup",
          name: "rand36_q36",
          title: "36. My health is excellent",
          isRequired: true,
          choices: [
            { value: 1, text: "Definitely true" },
            { value: 2, text: "Mostly true" },
            { value: 3, text: "Don't know" },
            { value: 4, text: "Mostly false" },
            { value: 5, text: "Definitely false" }
          ]
        }
      ]
    },

    // =====================
    // Optional: score preview
    // =====================
    {
      type: "html",
      name: "rand36_score_preview",
      html: `
        <div style="padding:10px 12px;border:1px solid rgba(15,23,42,0.08);border-radius:12px;background:rgba(15,23,42,0.02);line-height:1.6">
          <b>RAND-36 Scale Scores (0–100)</b><br/>
          Physical Functioning (PF): <b>{rand36_pf}</b><br/>
          Role Limitations — Physical (RP): <b>{rand36_rp}</b><br/>
          Role Limitations — Emotional (RE): <b>{rand36_re}</b><br/>
          Energy/Fatigue (VT): <b>{rand36_vt}</b><br/>
          Emotional Well-Being (MH): <b>{rand36_mh}</b><br/>
          Social Functioning (SF): <b>{rand36_sf}</b><br/>
          Pain (BP): <b>{rand36_bp}</b><br/>
          General Health (GH): <b>{rand36_gh}</b><br/>
          <hr style="border:none;border-top:1px solid rgba(15,23,42,0.12)"/>
          Health Change (HC, item 2 only): <b>{rand36_hc}</b>
        </div>
      `
    }
  ],

  // =====================
  // Scoring per RAND:
  // Step 1: recode items to 0..100 (Table 1)
  // Step 2: average items per scale (Table 2)
  // =====================
  calculatedValues: [
    // --- Table 1 mappings (inline) ---

    // Items 1,2,20,22,34,36: 1→100, 2→75, 3→50, 4→25, 5→0
    {
      name: "rand36_r01",
      expression:
        "iif({rand36_q01}=1,100,iif({rand36_q01}=2,75,iif({rand36_q01}=3,50,iif({rand36_q01}=4,25,0))))"
    },
    {
      name: "rand36_r02",
      expression:
        "iif({rand36_q02}=1,100,iif({rand36_q02}=2,75,iif({rand36_q02}=3,50,iif({rand36_q02}=4,25,0))))"
    },
    {
      name: "rand36_r20",
      expression:
        "iif({rand36_q20}=1,100,iif({rand36_q20}=2,75,iif({rand36_q20}=3,50,iif({rand36_q20}=4,25,0))))"
    },
    {
      name: "rand36_r22",
      expression:
        "iif({rand36_q22}=1,100,iif({rand36_q22}=2,75,iif({rand36_q22}=3,50,iif({rand36_q22}=4,25,0))))"
    },
    {
      name: "rand36_r34",
      expression:
        "iif({rand36_q34}=1,100,iif({rand36_q34}=2,75,iif({rand36_q34}=3,50,iif({rand36_q34}=4,25,0))))"
    },
    {
      name: "rand36_r36",
      expression:
        "iif({rand36_q36}=1,100,iif({rand36_q36}=2,75,iif({rand36_q36}=3,50,iif({rand36_q36}=4,25,0))))"
    },

    // Items 3–12: 1→0, 2→50, 3→100
    { name: "rand36_r03", expression: "iif({rand36_q03}=1,0,iif({rand36_q03}=2,50,100))" },
    { name: "rand36_r04", expression: "iif({rand36_q04}=1,0,iif({rand36_q04}=2,50,100))" },
    { name: "rand36_r05", expression: "iif({rand36_q05}=1,0,iif({rand36_q05}=2,50,100))" },
    { name: "rand36_r06", expression: "iif({rand36_q06}=1,0,iif({rand36_q06}=2,50,100))" },
    { name: "rand36_r07", expression: "iif({rand36_q07}=1,0,iif({rand36_q07}=2,50,100))" },
    { name: "rand36_r08", expression: "iif({rand36_q08}=1,0,iif({rand36_q08}=2,50,100))" },
    { name: "rand36_r09", expression: "iif({rand36_q09}=1,0,iif({rand36_q09}=2,50,100))" },
    { name: "rand36_r10", expression: "iif({rand36_q10}=1,0,iif({rand36_q10}=2,50,100))" },
    { name: "rand36_r11", expression: "iif({rand36_q11}=1,0,iif({rand36_q11}=2,50,100))" },
    { name: "rand36_r12", expression: "iif({rand36_q12}=1,0,iif({rand36_q12}=2,50,100))" },

    // Items 13–19: 1→0, 2→100 (Yes/No)
    { name: "rand36_r13", expression: "iif({rand36_q13}=1,0,100)" },
    { name: "rand36_r14", expression: "iif({rand36_q14}=1,0,100)" },
    { name: "rand36_r15", expression: "iif({rand36_q15}=1,0,100)" },
    { name: "rand36_r16", expression: "iif({rand36_q16}=1,0,100)" },
    { name: "rand36_r17", expression: "iif({rand36_q17}=1,0,100)" },
    { name: "rand36_r18", expression: "iif({rand36_q18}=1,0,100)" },
    { name: "rand36_r19", expression: "iif({rand36_q19}=1,0,100)" },

    // Items 21,23,26,27,30: 1→100,2→80,3→60,4→40,5→20,6→0
    {
      name: "rand36_r21",
      expression:
        "iif({rand36_q21}=1,100,iif({rand36_q21}=2,80,iif({rand36_q21}=3,60,iif({rand36_q21}=4,40,iif({rand36_q21}=5,20,0)))))"
    },
    {
      name: "rand36_r23",
      expression:
        "iif({rand36_q23}=1,100,iif({rand36_q23}=2,80,iif({rand36_q23}=3,60,iif({rand36_q23}=4,40,iif({rand36_q23}=5,20,0)))))"
    },
    {
      name: "rand36_r26",
      expression:
        "iif({rand36_q26}=1,100,iif({rand36_q26}=2,80,iif({rand36_q26}=3,60,iif({rand36_q26}=4,40,iif({rand36_q26}=5,20,0)))))"
    },
    {
      name: "rand36_r27",
      expression:
        "iif({rand36_q27}=1,100,iif({rand36_q27}=2,80,iif({rand36_q27}=3,60,iif({rand36_q27}=4,40,iif({rand36_q27}=5,20,0)))))"
    },
    {
      name: "rand36_r30",
      expression:
        "iif({rand36_q30}=1,100,iif({rand36_q30}=2,80,iif({rand36_q30}=3,60,iif({rand36_q30}=4,40,iif({rand36_q30}=5,20,0)))))"
    },

    // Items 24,25,28,29,31: 1→0,2→20,3→40,4→60,5→80,6→100
    {
      name: "rand36_r24",
      expression:
        "iif({rand36_q24}=1,0,iif({rand36_q24}=2,20,iif({rand36_q24}=3,40,iif({rand36_q24}=4,60,iif({rand36_q24}=5,80,100)))))"
    },
    {
      name: "rand36_r25",
      expression:
        "iif({rand36_q25}=1,0,iif({rand36_q25}=2,20,iif({rand36_q25}=3,40,iif({rand36_q25}=4,60,iif({rand36_q25}=5,80,100)))))"
    },
    {
      name: "rand36_r28",
      expression:
        "iif({rand36_q28}=1,0,iif({rand36_q28}=2,20,iif({rand36_q28}=3,40,iif({rand36_q28}=4,60,iif({rand36_q28}=5,80,100)))))"
    },
    {
      name: "rand36_r29",
      expression:
        "iif({rand36_q29}=1,0,iif({rand36_q29}=2,20,iif({rand36_q29}=3,40,iif({rand36_q29}=4,60,iif({rand36_q29}=5,80,100)))))"
    },
    {
      name: "rand36_r31",
      expression:
        "iif({rand36_q31}=1,0,iif({rand36_q31}=2,20,iif({rand36_q31}=3,40,iif({rand36_q31}=4,60,iif({rand36_q31}=5,80,100)))))"
    },

    // Items 32,33,35: 1→0,2→25,3→50,4→75,5→100
    {
      name: "rand36_r32",
      expression:
        "iif({rand36_q32}=1,0,iif({rand36_q32}=2,25,iif({rand36_q32}=3,50,iif({rand36_q32}=4,75,100))))"
    },
    {
      name: "rand36_r33",
      expression:
        "iif({rand36_q33}=1,0,iif({rand36_q33}=2,25,iif({rand36_q33}=3,50,iif({rand36_q33}=4,75,100))))"
    },
    {
      name: "rand36_r35",
      expression:
        "iif({rand36_q35}=1,0,iif({rand36_q35}=2,25,iif({rand36_q35}=3,50,iif({rand36_q35}=4,75,100))))"
    },

    // --- Table 2 scales (average items after recoding) ---

    // Physical functioning (PF): items 3–12 (10)
    {
      name: "rand36_pf",
      expression:
        "({rand36_r03}+{rand36_r04}+{rand36_r05}+{rand36_r06}+{rand36_r07}+{rand36_r08}+{rand36_r09}+{rand36_r10}+{rand36_r11}+{rand36_r12})/10"
    },

    // Role limitations due to physical health (RP): items 13–16 (4)
    {
      name: "rand36_rp",
      expression: "({rand36_r13}+{rand36_r14}+{rand36_r15}+{rand36_r16})/4"
    },

    // Role limitations due to emotional problems (RE): items 17–19 (3)
    {
      name: "rand36_re",
      expression: "({rand36_r17}+{rand36_r18}+{rand36_r19})/3"
    },

    // Energy/fatigue (VT): items 23,27,29,31 (4)
    {
      name: "rand36_vt",
      expression: "({rand36_r23}+{rand36_r27}+{rand36_r29}+{rand36_r31})/4"
    },

    // Emotional well-being (MH): items 24,25,26,28,30 (5)
    {
      name: "rand36_mh",
      expression:
        "({rand36_r24}+{rand36_r25}+{rand36_r26}+{rand36_r28}+{rand36_r30})/5"
    },

    // Social functioning (SF): items 20,32 (2)
    {
      name: "rand36_sf",
      expression: "({rand36_r20}+{rand36_r32})/2"
    },

    // Pain (BP): items 21,22 (2)
    {
      name: "rand36_bp",
      expression: "({rand36_r21}+{rand36_r22})/2"
    },

    // General health (GH): items 1,33,34,35,36 (5)
    {
      name: "rand36_gh",
      expression:
        "({rand36_r01}+{rand36_r33}+{rand36_r34}+{rand36_r35}+{rand36_r36})/5"
    },

    // Health change (HC): item 2 only (recoded)
    { name: "rand36_hc", expression: "{rand36_r02}" }
  ]
};


// -----------------------------
// One Model per form (keep state)
// -----------------------------
const basicModel = new Model(basicJson);
const sliqModel = new Model(sliqJson);
const rand36Model = new Model(rand36Json);

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

[basicModel, sliqModel, rand36Model].forEach((m) => {
  m.applyTheme(theme);
  m.completeText = "Save";
  // Avoid completion screen
  (m as any).showCompletedPage = false;
  (m as any).completedHtml = "";
});

function modelByForm(f: ProfileFormKey): Model {
  if (f === "basic") return basicModel;
  if (f === "sliq") return sliqModel;
  return rand36Model;
}

// -----------------------------
// Load latest (once per form unless forced)
// -----------------------------
const loaded = ref<Record<ProfileFormKey, boolean>>({
  basic: false,
  sliq: false,
  rand36: false,
});

function extractFormData(r: ProfileLatestGetOut): Record<string, any> | null {
  const payload: any = (r as any)?.data ?? null;
  if (!payload) return null;

  if (typeof payload === "object" && "data" in payload) {
    const d = (payload as any).data ?? null;

    // NEW: backend returns list[{id,value,...}] -> convert to SurveyJS map
    if (Array.isArray(d)) {
      const m: Record<string, any> = {};
      for (const it of d) {
        if (it && typeof it === "object" && "id" in it) m[String((it as any).id)] = (it as any).value;
      }
      return m;
    }

    // legacy: object map
    if (typeof d === "object" && d) return d;
  }

  return null;
}

function buildAnswerItems(m: Model): ProfileAnswerItem[] {
  const out: ProfileAnswerItem[] = [];
  const qs: any[] = (m as any).getAllQuestions?.() ?? [];

  for (const q of qs) {
    const id = String(q?.name ?? "");
    if (!id) continue;

    const val = q?.value;
    if (val === undefined || val === null || val === "") continue;

    const question = String(q?.title ?? q?.fullTitle ?? id);

    let label: string | null = null;
    try {
      const dv = q?.displayValue ?? (typeof q?.getDisplayValue === "function" ? q.getDisplayValue(false) : undefined);
      if (Array.isArray(dv)) label = dv.join(", ");
      else if (dv !== undefined && dv !== null && dv !== "") label = String(dv);
    } catch {}

    if (!label) label = typeof val === "string" ? val : JSON.stringify(val);

    out.push({ id, question, value: val, label });
  }

  return out;
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
async function save(form: ProfileFormKey, items: ProfileAnswerItem[]) {
  status.value = { kind: "saving", text: "Saving..." };

  try {
    const r = (await putProfileLatest(profileUuid, form, items)) as ProfileLatestUpsertOut;
    lastResp.value = r;
  } catch (e) {
    status.value = { kind: "error", text: "Save failed" };
    console.error("PUT failed:", e);
    return;
  }

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

function wireSave(m: Model, form: ProfileFormKey) {
  (m as any).onCompleting.add((sender: any, opt: any) => {
    if (opt) opt.allowComplete = false;
    save(form, buildAnswerItems(sender));
  });
}

wireSave(basicModel, "basic");
wireSave(sliqModel, "sliq");
wireSave(rand36Model, "rand36");

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
