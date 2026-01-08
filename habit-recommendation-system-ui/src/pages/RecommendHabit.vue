<template>
  <div class="card">
    <div class="row" style="justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:12px">
      <div>
        <div style="font-weight:900; font-size:18px">Recommendation</div>
        <div class="muted" style="font-size:13px; margin-top:4px">
          Provide text (and optional theory). The system will generate a recommendation with explainable evidence.
        </div>
      </div>
    </div>

    <!-- Inputs -->
    <div class="grid2" style="margin-bottom:10px">
      <div>
        <div class="label">Theory (optional)</div>
        <select v-model="theoryName" class="input">
          <option :value="''">(None)</option>
          <option value="COM-B">COM-B</option>
          <option value="TTM">TTM</option>
          <option value="SCT">SCT</option>
        </select>
      </div>
    </div>

    <div class="label">Text</div>
    <div class="textBlock">
      <textarea
        v-model="text"
        class="textarea"
        rows="7"
        placeholder="e.g., I want to improve my sleep quality. I work rotating shifts and often use screens in bed..."
      />

      <div class="textActions">
        <button class="btn" @click="clearAll" :disabled="busy || commentBusy">Clear</button>
        <button class="btn primary" @click="submit" :disabled="busy || commentBusy || !text.trim()">
          {{ busy ? "Running..." : "Recommend" }}
        </button>
      </div>
    </div>

    <!-- Progress -->
    <div v-if="busy" class="progressWrap" style="margin-top:12px">
      <div class="progressTop">
        <div class="muted" style="font-size:12px">{{ progressLabel }}</div>
        <div class="muted" style="font-size:12px">{{ progress }}%</div>
      </div>
      <div class="progressBar">
        <div class="progressFill" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="muted" style="font-size:12px; margin-top:6px">
        Note: progress is estimated until the backend returns.
      </div>
    </div>

    <!-- Error (better display) -->
    <div v-if="errorObj" class="alert error" style="margin-top:12px">
      <div style="font-weight:900">
        {{ errorObj.title || "Error" }}
        <span v-if="errorObj.code" class="muted" style="font-weight:800; margin-left:8px">
          ({{ errorObj.code }})
        </span>
      </div>

      <div class="muted" style="margin-top:6px; white-space:pre-wrap">
        {{ errorObj.message }}
      </div>

      <ul v-if="errorObj.hints && errorObj.hints.length" class="ul" style="margin-top:10px">
        <li v-for="(h, i) in errorObj.hints" :key="i">
          <span class="chip">Hint</span>
          <span style="margin-left:8px">{{ h }}</span>
        </li>
      </ul>

      <details v-if="errorObj.raw" class="details" style="margin-top:10px">
        <summary><span class="muted">Raw error (debug)</span></summary>
        <pre class="pre">{{ JSON.stringify(errorObj.raw, null, 2) }}</pre>
      </details>
    </div>

    <!-- Output -->
    <div v-if="resp && !busy && !errorObj" class="out" style="margin-top:14px">
      <!-- 0) Input summary -->
      <div class="section">
        <div class="sectionTitle">Input</div>
        <div class="box">
          <div class="kv">
            <div class="k">Text</div>
            <div class="v" style="white-space:pre-wrap">{{ userText }}</div>
          </div>
        </div>
      </div>

      <!-- 1) Recommendation -->
      <div class="section">
        <div class="sectionTitle">Recommendation</div>
        <div class="box">
          <div v-if="recommendationText" style="white-space:pre-wrap; line-height:1.55">
            {{ recommendationText }}
          </div>
          <div v-else class="muted">No recommendation_text found in response.</div>
        </div>
      </div>

      <!-- 2) LLM meta -->
      <div class="section">
        <div class="sectionTitle">How it was generated (LLM meta)</div>
        <div class="box">
          <div class="kv">
            <div class="k">Provider</div>
            <div class="v"><code>{{ llmMeta.provider || "-" }}</code></div>
          </div>
          <div class="kv">
            <div class="k">Model</div>
            <div class="v"><code>{{ llmMeta.model || "-" }}</code></div>
          </div>
          <div class="kv">
            <div class="k">Temperature</div>
            <div class="v"><code>{{ llmMeta.temperature ?? "-" }}</code></div>
          </div>
          <div class="kv">
            <div class="k">Max tokens</div>
            <div class="v"><code>{{ llmMeta.max_tokens ?? "-" }}</code></div>
          </div>

          <div class="muted" style="font-size:12px; margin-top:8px">
            This recommendation was generated based on your text + the built profile + selected habits + retrieved evidence.
          </div>
        </div>
      </div>

      <!-- 3) profile_detailed -->
      <div class="section">
        <div class="sectionTitle">Profile used for recommendation (LLM-generated)</div>
        <details class="details" open>
          <summary>
            <span class="muted">profile_detailed (click to collapse/expand)</span>
          </summary>
          <div class="box" style="margin-top:10px">
            <div v-if="profileDetailed" style="white-space:pre-wrap; line-height:1.55">
              {{ profileDetailed }}
            </div>
            <div v-else class="muted">No profile_detailed found.</div>
          </div>
        </details>
      </div>

      <!-- 4) selected_habits -->
      <div class="section">
        <div class="sectionTitle">Selected habits (used with context)</div>

        <div v-if="selectedHabits.length === 0" class="muted">
          No selected_habits found.
        </div>

        <div v-else class="stack">
          <details v-for="(h, idx) in selectedHabits" :key="h.habit_key || idx" class="details">
            <summary>
              <div class="sumRow">
                <div class="sumMain">
                  <div class="sumTitle">{{ h.habit || "(no habit text)" }}</div>
                  <div class="muted" style="font-size:12px">
                    score: <code>{{ h.score }}</code>
                    <span v-if="h.habit_key" style="margin-left:10px">
                      habit_key: <code>{{ shortKey(h.habit_key) }}</code>
                    </span>
                  </div>
                </div>
              </div>
            </summary>

            <div class="box" style="margin-top:10px">
              <div class="kv" v-if="h.reason">
                <div class="k">Why selected</div>
                <div class="v" style="white-space:pre-wrap">{{ h.reason }}</div>
              </div>

              <div class="kv">
                <div class="k">Contexts</div>
                <div class="v">
                  <div v-if="contextsToPairs(h.contexts).length === 0" class="muted">No contexts.</div>
                  <ul v-else class="ul">
                    <li v-for="c in contextsToPairs(h.contexts)" :key="c.label">
                      <span class="chip">{{ c.label }}</span>
                      <span style="margin-left:8px">{{ c.value }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </details>
        </div>
      </div>

      <!-- 5) RAG evidence + assessment -->
      <div class="section">
        <div class="sectionTitle">Retrieved evidence (RAG)</div>

        <div v-if="ragAssessment" class="box" style="margin-bottom:10px">
          <div class="muted" style="font-weight:900; font-size:12px; margin-bottom:6px">
            RAG assessment
          </div>

          <div class="kv">
            <div class="k">rag_available</div>
            <div class="v"><code>{{ ragAssessment.rag_available ?? "-" }}</code></div>
          </div>
          <div class="kv">
            <div class="k">rag_actionable</div>
            <div class="v"><code>{{ ragAssessment.rag_actionable ?? "-" }}</code></div>
          </div>
          <div class="kv">
            <div class="k">reason</div>
            <div class="v" style="white-space:pre-wrap">{{ ragAssessment.reason || "-" }}</div>
          </div>
        </div>

        <div v-if="ragEvidence.length === 0" class="muted">
          <span v-if="ragAssessment && ragAssessment.rag_actionable === false">
            No quotes were used because <code>rag_actionable=false</code>.
          </span>
          <span v-else>No used_evidence.rag items.</span>
        </div>

        <div v-else class="stack">
          <details v-for="(e, idx) in ragEvidence" :key="idx" class="details" open>
            <summary>
              <div class="sumRow">
                <div class="sumMain">
                  <div class="sumTitle">{{ e.doc_title || "(no doc_title)" }}</div>
                  <div class="muted" style="font-size:12px">
                    domain: <code>{{ e.domain || "-" }}</code>
                    <span style="margin-left:10px">score: <code>{{ formatScore(e.score) }}</code></span>
                    <span style="margin-left:10px">page: <code>{{ e.page_number ?? "-" }}</code></span>
                    <span v-if="e.k" style="margin-left:10px">ref: <code>{{ e.k }}</code></span>
                  </div>
                </div>
              </div>
            </summary>

            <div class="box" style="margin-top:10px">
              <div class="kv">
                <div class="k">Quote</div>
                <div class="v" style="white-space:pre-wrap">{{ e.quote || "(empty quote)" }}</div>
              </div>
            </div>
          </details>
        </div>
      </div>

      <!-- 6) Feedback (one-time) -->
      <div class="section">
        <div class="sectionTitle">Feedback (one-time)</div>

        <div class="box">
          <div class="muted" style="font-size:12px; margin-bottom:8px">
            You can submit a single comment for this recommendation. It will be stored with a stable id (<code>_id=request_uuid</code>).
          </div>

          <!-- comment API error -->
          <div v-if="commentErrorObj" class="alert error" style="margin-bottom:10px">
            <div style="font-weight:900">
              {{ commentErrorObj.title || "Comment error" }}
              <span v-if="commentErrorObj.code" class="muted" style="font-weight:800; margin-left:8px">
                ({{ commentErrorObj.code }})
              </span>
            </div>
            <div class="muted" style="margin-top:6px; white-space:pre-wrap">{{ commentErrorObj.message }}</div>
            <ul v-if="commentErrorObj.hints && commentErrorObj.hints.length" class="ul" style="margin-top:10px">
              <li v-for="(h, i) in commentErrorObj.hints" :key="i">
                <span class="chip">Hint</span>
                <span style="margin-left:8px">{{ h }}</span>
              </li>
            </ul>
          </div>

          <!-- success -->
          <div v-if="commentSubmitted && commentResp" class="muted" style="white-space:pre-wrap; line-height:1.5">
            Submitted!
            <!-- <div style="margin-top:6px">
              created_at: <code>{{ commentResp?.data?.created_at || "-" }}</code>
            </div> -->
          </div>

          <!-- input -->
          <div v-else>
            <div class="label" style="margin-top:0">Your comment</div>
            <textarea
              v-model="commentText"
              class="textarea"
              rows="3"
              placeholder="Write a short comment (required). e.g., This recommendation is clear and actionable / not helpful because..."
              :disabled="commentBusy || commentLocked"
              style="min-height:90px"
            />

            <div class="textActions" style="margin-top:8px">
              <button class="btn" @click="commentText = ''" :disabled="commentBusy || commentLocked">
                Clear comment
              </button>
              <button
                class="btn primary"
                @click="submitComment"
                :disabled="commentBusy || commentLocked || !commentText.trim() || !commentReady"
              >
                {{ commentBusy ? "Submitting..." : "Submit comment" }}
              </button>
            </div>

            <div v-if="!commentReady" class="muted" style="font-size:12px; margin-top:8px">
              Comment API is enabled only when <code>request_uuid</code> + <code>text_signature</code> are available from /recommend.
            </div>

            <div v-if="commentLocked" class="muted" style="font-size:12px; margin-top:8px">
              🔒 Locked: this request_uuid has already been commented (one-time only).
            </div>
          </div>
        </div>
      </div>

      <!-- Debug -->
      <details class="details" style="margin-top:12px">
        <summary><span class="muted">Raw response (debug)</span></summary>
        <pre class="pre">{{ prettyResp }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

const API_BASE = import.meta.env.VITE_HHH_API_BASE || "http://127.0.0.1:8081";

type TheoryName = "" | "COM-B" | "TTM" | "SCT";
type RecommendReq = { text: string; theory_name?: string | null };

const CONTEXT_LABELS = [
  "TIME",
  "PHYSICAL SETTING",
  "PRIOR BEHAVIOR",
  "OTHER PEOPLE",
  "INTERNAL STATE",
  "BEHAVIOR",
  "REASONING",
] as const;

type ContextLabel = (typeof CONTEXT_LABELS)[number];
type ContextPair = { label: ContextLabel; value: string };

type ErrorView = {
  title?: string;
  code?: string;
  message: string;
  hints?: string[];
  raw?: any;
};

type RecommendCommentReq = {
  request_uuid: string;
  text: string;
  text_signature: string;
  comment: string;
};

const text = ref("");
const theoryName = ref<TheoryName>("COM-B");

const busy = ref(false);
const resp = ref<any | null>(null);
const requestUuid = ref<string>("");

const errorObj = ref<ErrorView | null>(null);

/** progress */
const progress = ref<number>(0);
const progressLabel = ref<string>("Preparing...");
let progressTimer: number | null = null;

const prettyResp = computed(() => (resp.value ? JSON.stringify(resp.value, null, 2) : ""));

const userText = computed(() => {
  return (
    resp.value?.profiles_build?.text ||
    resp.value?.habit_db_select?.text ||
    resp.value?.kb_query?.query ||
    text.value.trim()
  );
});

const recommendationText = computed(() => {
  const r = resp.value;
  return r?.recommendation?.recommendation?.recommendation_text || r?.recommendation?.recommendation_text || "";
});

const ragAssessment = computed(() => {
  const r = resp.value;
  return r?.recommendation?.rag_assessment || r?.recommendation?.recommendation?.rag_assessment || null;
});

const llmMeta = computed(() => {
  const r = resp.value;
  return r?.recommendation?.llm_meta || r?.recommendation?.recommendation?.llm_meta || {};
});

const profileDetailed = computed(() => resp.value?.profiles_build?.profile_detailed || "");

type SelectedHabit = {
  habit: string;
  habit_key: string;
  score: number;
  reason?: string;
  contexts?: any;
};
const selectedHabits = computed<SelectedHabit[]>(() => {
  const xs = resp.value?.habit_db_select?.selected_habits;
  return Array.isArray(xs) ? xs : [];
});

type RagEvidenceView = {
  k?: string;
  quote?: string;
  page_number?: number | null;
  doc_title?: string | null;
  domain?: string | null;
  score?: number | null;
};
const ragEvidence = computed<RagEvidenceView[]>(() => {
  const r = resp.value;
  const rag =
    r?.recommendation?.recommendation?.used_evidence?.rag ||
    r?.recommendation?.used_evidence?.rag ||
    [];
  const hits = r?.kb_query?.hits;

  if (!Array.isArray(rag)) return [];
  const out: RagEvidenceView[] = [];

  for (const it of rag) {
    const k = String(it?.k ?? "");
    const quote = String(it?.quote ?? "");

    let meta: any = null;
    const m = k.match(/^K(\d+)$/i);
    if (m && Array.isArray(hits)) {
      const idx = Number(m[1]) - 1;
      if (Number.isFinite(idx) && idx >= 0 && idx < hits.length) meta = hits[idx];
    }

    out.push({
      k: k || undefined,
      quote: quote || undefined,
      page_number: meta?.page_number ?? null,
      doc_title: meta?.doc_title ?? null,
      domain: meta?.domain ?? null,
      score: meta?.score ?? null,
    });
  }
  return out;
});

/** text_signature for comment API (take from /recommend response) */
const textSignature = computed(() => {
  return (
    resp.value?.profiles_build?.signatures?.text_signature ||
    resp.value?.habit_db_select?.signatures?.text_signature ||
    ""
  );
});

const commentReady = computed(() => {
  return Boolean(requestUuid.value && textSignature.value && userText.value.trim());
});

/* -------------------------
   Comment state + submit
-------------------------- */
const commentText = ref<string>(""); // default empty (OK). Only submit when user typed.
const commentBusy = ref(false);
const commentSubmitted = ref(false);
const commentLocked = ref(false);
const commentResp = ref<any | null>(null);
const commentErrorObj = ref<ErrorView | null>(null);

function clearAll() {
  errorObj.value = null;
  resp.value = null;
  requestUuid.value = "";

  // reset comment state
  commentText.value = "";
  commentBusy.value = false;
  commentSubmitted.value = false;
  commentLocked.value = false;
  commentResp.value = null;
  commentErrorObj.value = null;

  stopProgress();
}

function startProgress() {
  stopProgress();
  progress.value = 5;
  progressLabel.value = "Sending request to backend...";

  let phase = 0;

  progressTimer = window.setInterval(() => {
    if (!busy.value) return;

    if (progress.value < 25 && phase === 0) {
      progress.value += 2;
      if (progress.value >= 25) {
        phase = 1;
        progressLabel.value = "Running workflow (profiles + habits + KB query)...";
      }
      return;
    }

    if (progress.value < 55 && phase === 1) {
      progress.value += 1;
      if (progress.value >= 55) {
        phase = 2;
        progressLabel.value = "Generating recommendation (LLM)...";
      }
      return;
    }

    if (progress.value < 85 && phase === 2) {
      progress.value += 1;
      if (progress.value >= 85) {
        phase = 3;
        progressLabel.value = "Finalizing response...";
      }
      return;
    }

    if (phase === 3 && progress.value < 90) {
      progress.value += 1;
    }
  }, 160);
}

function finishProgressOk() {
  progressLabel.value = "Done";
  progress.value = 100;
  window.setTimeout(() => stopProgress(), 400);
}

function stopProgress() {
  if (progressTimer !== null) {
    window.clearInterval(progressTimer);
    progressTimer = null;
  }
  progress.value = 0;
  progressLabel.value = "Preparing...";
}

function shortKey(s: string) {
  if (!s) return "";
  return s.length <= 16 ? s : `${s.slice(0, 8)}…${s.slice(-6)}`;
}

function formatScore(v: any) {
  const n = Number(v);
  if (!Number.isFinite(n)) return "-";
  return n.toFixed(3);
}

function contextsToPairs(contexts: any): ContextPair[] {
  const out: ContextPair[] = [];

  if (Array.isArray(contexts)) {
    for (const [i, label] of CONTEXT_LABELS.entries()) {
      const val = contexts?.[i];
      if (val === null || val === undefined) continue;
      const s = String(val).trim();
      if (!s) continue;
      out.push({ label, value: s });
    }
    return out;
  }

  if (contexts && typeof contexts === "object") {
    for (const label of CONTEXT_LABELS) {
      const v = (contexts as any)[label] ?? (contexts as any)[String(label).toLowerCase()] ?? null;
      if (v === null || v === undefined) continue;
      const s = String(v).trim();
      if (!s) continue;
      out.push({ label, value: s });
    }
    return out;
  }

  return out;
}

function parseBackendError(data: any, status: number): ErrorView {
  const detail = data?.detail;

  // 422: NO_SELECTED_HABITS
  if (status === 422 && detail && typeof detail === "object" && detail.error === "NO_SELECTED_HABITS") {
    return {
      title: "No habits selected",
      code: "NO_SELECTED_HABITS",
      message:
        detail.message ||
        "No habits were selected/provided. Please enrich the habit library and run habit selection before calling /recommend.",
      hints: Array.isArray(detail.hint) ? detail.hint : undefined,
      raw: data,
    };
  }

  // 409: comment already exists
  if (status === 409 && detail && typeof detail === "object" && detail.error === "COMMENT_ALREADY_EXISTS") {
    return {
      title: "Already submitted",
      code: "COMMENT_ALREADY_EXISTS",
      message: detail.message || "A comment for this request_uuid already exists (one-time only).",
      hints: Array.isArray(detail.hint) ? detail.hint : undefined,
      raw: data,
    };
  }

  if (detail && typeof detail === "object") {
    return {
      title: status === 422 ? "Validation error" : "Request failed",
      code: typeof detail.error === "string" ? detail.error : undefined,
      message: detail.message ? String(detail.message) : JSON.stringify(detail),
      hints: Array.isArray(detail.hint) ? detail.hint : undefined,
      raw: data,
    };
  }

  if (typeof detail === "string" && detail.trim()) {
    return { title: "Request failed", message: detail, raw: data };
  }

  if (typeof data?.message === "string" && data.message.trim()) {
    return { title: "Request failed", message: data.message, raw: data };
  }

  return { title: "Request failed", message: `HTTP ${status}`, raw: data };
}

async function submit() {
  errorObj.value = null;
  resp.value = null;
  requestUuid.value = "";

  // reset comment state on each new recommendation
  commentText.value = "";
  commentBusy.value = false;
  commentSubmitted.value = false;
  commentLocked.value = false;
  commentResp.value = null;
  commentErrorObj.value = null;

  const payload: RecommendReq = {
    text: text.value.trim(),
    theory_name: theoryName.value ? theoryName.value : null,
  };

  busy.value = true;
  startProgress();

  try {
    const r = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await r.json().catch(() => null);

    if (!r.ok) {
      errorObj.value = parseBackendError(data, r.status);
      stopProgress();
      return;
    }

    resp.value = data;

    requestUuid.value =
      data?.recommendation?.request_uuid ||
      data?.profiles_build?.request_uuid ||
      data?.habit_db_select?.request_uuid ||
      "";

    finishProgressOk();
  } catch (e: any) {
    errorObj.value = {
      title: "Network / runtime error",
      message: String(e?.message || e),
      raw: e,
    };
    stopProgress();
  } finally {
    busy.value = false;
  }
}

async function submitComment() {
  commentErrorObj.value = null;
  commentResp.value = null;

  if (!commentReady.value) {
    commentErrorObj.value = {
      title: "Not ready",
      message: "Missing request_uuid or text_signature from /recommend response.",
    };
    return;
  }

  const req: RecommendCommentReq = {
    request_uuid: requestUuid.value,
    text: userText.value, // send original text; backend verifies via normalize+sha1
    text_signature: textSignature.value,
    comment: commentText.value.trim(),
  };

  commentBusy.value = true;

  try {
    const r = await fetch(`${API_BASE}/recommend/comment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });

    const data = await r.json().catch(() => null);

    if (!r.ok) {
      const ev = parseBackendError(data, r.status);
      commentErrorObj.value = ev;

      // if backend says already exists, lock UI
      if (r.status === 409 && ev.code === "COMMENT_ALREADY_EXISTS") {
        commentLocked.value = true;
      }
      return;
    }

    commentResp.value = data;
    commentSubmitted.value = true;
    commentLocked.value = true; // one-time only
  } catch (e: any) {
    commentErrorObj.value = {
      title: "Network / runtime error",
      message: String(e?.message || e),
      raw: e,
    };
  } finally {
    commentBusy.value = false;
  }
}
</script>

<style scoped>
.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
@media (max-width: 900px) {
  .grid2 {
    grid-template-columns: 1fr;
  }
}

.label {
  font-weight: 800;
  font-size: 13px;
  margin-bottom: 6px;
}

.input {
  width: 100%;
  box-sizing: border-box;
  border-radius: 12px;
  border: 1px solid rgba(15, 23, 42, 0.14);
  padding: 10px 10px;
  font-size: 14px;
  outline: none;
  background: white;
}
.input:focus {
  border-color: rgba(59, 130, 246, 0.55);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
}

.textBlock {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.textActions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.textarea {
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  border-radius: 14px;
  border: 1px solid rgba(15, 23, 42, 0.14);
  padding: 10px 12px;
  font-size: 14px;
  outline: none;
  background: white;
  min-height: 140px;
}
.textarea:focus {
  border-color: rgba(59, 130, 246, 0.55);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
}

/* Progress */
.progressWrap {
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.9);
}
.progressTop {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.progressBar {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.1);
  overflow: hidden;
}
.progressFill {
  height: 100%;
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.7);
  transition: width 120ms linear;
}

/* Output layout */
.section {
  margin-top: 14px;
}
.sectionTitle {
  font-weight: 900;
  font-size: 14px;
  margin-bottom: 8px;
}
.box {
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.92);
}
.kv {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 10px;
  padding: 6px 0;
}
@media (max-width: 900px) {
  .kv {
    grid-template-columns: 1fr;
  }
}
.k {
  font-weight: 800;
  font-size: 12px;
  color: rgba(15, 23, 42, 0.75);
}
.v {
  font-size: 13px;
}
.stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.details {
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.92);
}
.details summary {
  cursor: pointer;
  list-style: none;
}
.details summary::-webkit-details-marker {
  display: none;
}

.sumRow {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}
.sumMain {
  min-width: 0;
}
.sumTitle {
  font-weight: 900;
  font-size: 13px;
  line-height: 1.35;
}

.ul {
  margin: 0;
  padding-left: 18px;
}
.chip {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid rgba(15, 23, 42, 0.14);
  background: rgba(248, 250, 252, 0.9);
  font-size: 12px;
  font-weight: 700;
}

.pre {
  margin-top: 8px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(15, 23, 42, 0.12);
  background: rgba(248, 250, 252, 0.9);
  overflow: auto;
  font-size: 12px;
  line-height: 1.4;
}

.alert.error {
  border: 1px solid rgba(220, 38, 38, 0.35);
  background: rgba(220, 38, 38, 0.06);
  border-radius: 14px;
  padding: 10px 12px;
}
</style>
