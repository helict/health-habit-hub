<template>
  <div class="card page">
    <!-- Header / Toolbar -->
    <div class="top">
      <div class="topLeft">
        <div class="title">Live feed (latest per text)</div>
        <div class="sub muted">
          Fetches <code>/recommend/history/latest</code>. Deduped by <code>text_signature</code>; only the latest
          recommendation for each text is shown.
        </div>

        <div class="metaLine muted" v-if="lastRefreshed">
          Last refreshed: <code>{{ lastRefreshed }}</code>
          <span v-if="total > 0" style="margin-left:10px">Total: <code>{{ total }}</code></span>
        </div>
      </div>

      <div class="topRight">
        <button class="btn" @click="refresh" :disabled="loading">
          {{ loading ? "Loading..." : "Refresh" }}
        </button>
        <button class="btn" @click="loadMore" :disabled="loading || items.length >= total">
          Load more
        </button>
      </div>
    </div>

    <!-- Error -->
    <div v-if="errorObj" class="alert error">
      <div class="errTitle">
        {{ errorObj.title || "Request failed" }}
        <span v-if="errorObj.code" class="muted" style="margin-left:8px">({{ errorObj.code }})</span>
      </div>
      <div class="muted" style="margin-top:6px; white-space:pre-wrap">{{ errorObj.message }}</div>
      <details v-if="errorObj.raw" class="details" style="margin-top:10px">
        <summary><span class="muted">Raw (debug)</span></summary>
        <pre class="pre">{{ JSON.stringify(errorObj.raw, null, 2) }}</pre>
      </details>
    </div>

    <!-- Empty -->
    <div v-if="!loading && !errorObj && items.length === 0" class="empty">
      <div class="emptyTitle">No data yet</div>
      <div class="muted">Run <code>/recommend</code> at least once, then click refresh.</div>
    </div>

    <!-- List -->
    <div v-else class="list">
      <article v-for="(it, idx) in items" :key="it.text_signature || idx" class="feedItem">
        <!-- Item header -->
        <div class="itemHead">
          <div class="headMain">
            <div class="textTitle">{{ it.text || "(empty text)" }}</div>
            <div class="headSub muted">
              <span v-if="it.updated_at">updated_at: <code>{{ it.updated_at }}</code></span>
              <span v-else>latest snapshot</span>
            </div>
          </div>

          <div class="badges">
            <span v-if="it.theory_name" class="badge">
              <span class="badgeK">Theory</span>
              <span class="badgeV">{{ it.theory_name }}</span>
            </span>

            <span class="badge">
              <span class="badgeK">Habits</span>
              <span class="badgeV">{{ (it.selected_habits || []).length }}</span>
            </span>

            <span class="badge" :class="ragBadgeClass(it.rag_assessment)">
              <span class="badgeK">RAG</span>
              <span class="badgeV">{{ ragBadgeText(it.rag_assessment) }}</span>
            </span>

            <span class="badge" :class="it.comment ? 'badgeOk' : 'badgeMuted'">
              <span class="badgeK">Comment</span>
              <span class="badgeV">{{ it.comment ? "yes" : "no" }}</span>
            </span>
          </div>
        </div>

        <!-- Recommendation (always visible) -->
        <div class="recBox">
          <div class="recTitle">Recommendation</div>
          <div v-if="it.recommendation_text" class="recText">{{ it.recommendation_text }}</div>
          <div v-else class="muted">No <code>recommendation_text</code>.</div>
        </div>

        <!-- Accordions -->
        <div class="accordion">
          <!-- Profile summary -->
          <details class="acc" :open="false">
            <summary class="accSum">
              <span>Profile summary</span>
              <span class="accHint muted">(click to expand)</span>
            </summary>
            <div class="accBody">
              <div v-if="it.profile_summary" class="mono">{{ it.profile_summary }}</div>
              <div v-else class="muted">No <code>profile_summary</code>.</div>
            </div>
          </details>

          <!-- LLM meta (Meta and RAG separate) -->
          <details class="acc" :open="false">
            <summary class="accSum">
              <span>LLM meta</span>
              <span class="accHint muted">(how it was generated)</span>
            </summary>
            <div class="accBody">
              <div class="kv">
                <div class="k">Provider</div>
                <div class="v"><code>{{ it.llm_meta?.provider || "-" }}</code></div>
              </div>
              <div class="kv">
                <div class="k">Model</div>
                <div class="v"><code>{{ it.llm_meta?.model || "-" }}</code></div>
              </div>
              <div class="kv">
                <div class="k">Temperature</div>
                <div class="v"><code>{{ it.llm_meta?.temperature ?? "-" }}</code></div>
              </div>
              <div class="kv">
                <div class="k">Max tokens</div>
                <div class="v"><code>{{ it.llm_meta?.max_tokens ?? "-" }}</code></div>
              </div>
            </div>
          </details>

          <!-- Selected habits -->
          <details class="acc" :open="false">
            <summary class="accSum">
              <span>Selected habits</span>
              <span class="accHint muted">({{ (it.selected_habits || []).length }})</span>
            </summary>
            <div class="accBody">
              <div v-if="(it.selected_habits || []).length === 0" class="muted">No selected habits.</div>

              <div v-else class="habits">
                <details v-for="(h, hi) in it.selected_habits" :key="h.habit_key || hi" class="habit">
                  <summary class="habitSum">
                    <div class="habitTitle">{{ h.habit || "(no habit text)" }}</div>
                    <div class="muted habitMeta">
                      score: <code>{{ formatScore(h.score) }}</code>
                      <span v-if="h.habit_key" style="margin-left:10px">key: <code>{{ shortKey(h.habit_key) }}</code></span>
                    </div>
                  </summary>

                  <div class="habitBody">
                    <div v-if="h.reason" class="kv">
                      <div class="k">Why</div>
                      <div class="v mono">{{ h.reason }}</div>
                    </div>

                    <div class="kv">
                      <div class="k">Contexts</div>
                      <div class="v">
                        <div v-if="contextsToPairs(h.contexts).length === 0" class="muted">No contexts.</div>
                        <ul v-else class="ctxList">
                          <li v-for="c in contextsToPairs(h.contexts)" :key="c.label" class="ctxItem">
                            <span class="ctxTag">{{ c.label }}</span>
                            <span class="ctxVal">{{ c.value }}</span>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </details>
              </div>
            </div>
          </details>

          <!-- Used evidence (RAG info ABOVE the quotes) -->
          <details class="acc" :open="false">
            <summary class="accSum">
              <span>Used evidence (RAG)</span>
              <span class="accHint muted">({{ (it.used_evidence_rag || []).length }})</span>
            </summary>

            <div class="accBody">
              <!-- RAG assessment first -->
              <div class="ragPanel">
                <div class="ragTitle">RAG assessment</div>
                <div class="kv">
                  <div class="k">rag_available</div>
                  <div class="v"><code>{{ it.rag_assessment?.rag_available ?? "-" }}</code></div>
                </div>
                <div class="kv">
                  <div class="k">rag_actionable</div>
                  <div class="v"><code>{{ it.rag_assessment?.rag_actionable ?? "-" }}</code></div>
                </div>
                <div class="kv">
                  <div class="k">reason</div>
                  <div class="v mono">{{ it.rag_assessment?.reason || "-" }}</div>
                </div>
              </div>

              <!-- Quotes -->
              <div v-if="(it.used_evidence_rag || []).length === 0" class="muted" style="margin-top:10px">
                No RAG quotes used.
              </div>

              <div v-else class="quotes">
                <div v-for="(q, qi) in it.used_evidence_rag" :key="qi" class="quote">
                  <!-- show title + page (no K) -->
                  <div class="quoteHead">
                    <div class="quoteTitle">
                      {{ q.doc_title || "(no title)" }}
                    </div>
                    <div class="quoteMeta muted">
                      page <code>{{ q.page_number ?? "-" }}</code>
                    </div>
                  </div>

                  <div class="quoteText">{{ q.quote || "" }}</div>
                </div>
              </div>
            </div>
          </details>

          <!-- Comment -->
          <details class="acc" :open="false">
            <summary class="accSum">
              <span>Comment</span>
              <span class="accHint muted">{{ it.comment ? "(available)" : "(none)" }}</span>
            </summary>
            <div class="accBody">
              <div v-if="it.comment" class="mono">{{ it.comment }}</div>
              <div v-else class="muted">No comment for this recommendation.</div>
            </div>
          </details>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const API_BASE = import.meta.env.VITE_HHH_API_BASE || "http://127.0.0.1:8081";

type ErrorView = {
  title?: string;
  code?: string;
  message: string;
  raw?: any;
};

type RagQuote = {
  quote?: string | null;
  doc_title?: string | null;
  page_number?: number | null;
  // backend may still include these; we just ignore in UI
  k?: string | null;
  doc_id?: string | null;
  chunk_id?: number | null;
  domain?: string | null;
  score?: number | null;
};

type RecommendationLatestItem = {
  text_signature: string;
  request_uuid: string;
  updated_at?: string | null;

  text?: string;
  profile_summary?: string;
  selected_habits?: any[];

  recommendation_text?: string;
  llm_meta?: Record<string, any>;
  rag_assessment?: Record<string, any>;
  used_evidence_rag?: RagQuote[];

  comment?: string | null;
  theory_name?: string | null;
};

type RecommendationLatestOut = {
  ok: boolean;
  total: number;
  items: RecommendationLatestItem[];
};

const limit = ref<number>(50);
const skip = ref<number>(0);

const total = ref<number>(0);
const items = ref<RecommendationLatestItem[]>([]);
const loading = ref<boolean>(false);
const errorObj = ref<ErrorView | null>(null);
const lastRefreshed = ref<string>("");

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

function nowLocal() {
  const d = new Date();
  return d.toLocaleString();
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

  if (detail && typeof detail === "object") {
    return {
      title: status === 422 ? "Validation error" : "Request failed",
      code: typeof detail.error === "string" ? detail.error : undefined,
      message: detail.message ? String(detail.message) : JSON.stringify(detail),
      raw: data,
    };
  }

  if (typeof detail === "string" && detail.trim()) {
    return { title: "Request failed", message: detail, raw: data };
  }

  return { title: "Request failed", message: `HTTP ${status}`, raw: data };
}

function ragBadgeText(rag: any) {
  const a = rag?.rag_actionable;
  const av = rag?.rag_available;

  if (av === false) return "unavailable";
  if (a === true) return "actionable";
  if (a === false) return "not actionable";
  return "unknown";
}

function ragBadgeClass(rag: any) {
  const a = rag?.rag_actionable;
  const av = rag?.rag_available;

  if (av === false) return "badgeMuted";
  if (a === true) return "badgeOk";
  if (a === false) return "badgeWarn";
  return "badgeMuted";
}

async function fetchLatest(reset: boolean) {
  errorObj.value = null;
  loading.value = true;

  try {
    const useSkip = reset ? 0 : skip.value;
    const r = await fetch(`${API_BASE}/recommend/history/latest?limit=${limit.value}&skip=${useSkip}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    const data = (await r.json().catch(() => null)) as RecommendationLatestOut | null;

    if (!r.ok) {
      errorObj.value = parseBackendError(data, r.status);
      return;
    }

    const got = Array.isArray(data?.items) ? data!.items : [];
    total.value = Number(data?.total ?? got.length) || 0;

    if (reset) {
      items.value = got;
      skip.value = got.length;
    } else {
      items.value = [...items.value, ...got];
      skip.value = items.value.length;
    }

    lastRefreshed.value = nowLocal();
  } catch (e: any) {
    errorObj.value = {
      title: "Network / runtime error",
      message: String(e?.message || e),
      raw: e,
    };
  } finally {
    loading.value = false;
  }
}

async function refresh() {
  await fetchLatest(true);
}

async function loadMore() {
  await fetchLatest(false);
}

// initial load (manual is fine, but better UX to load once)
fetchLatest(true);
</script>

<style scoped>
.page {
  padding: 16px 16px;
}

/* Header */
.top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 14px;
}
.topLeft {
  min-width: 0;
}
.title {
  font-weight: 950;
  font-size: 18px;
  letter-spacing: 0.2px;
}
.sub {
  margin-top: 4px;
  font-size: 13px;
  line-height: 1.45;
}
.metaLine {
  margin-top: 10px;
  font-size: 12px;
}
.topRight {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* Error / empty */
.alert.error {
  border: 1px solid rgba(220, 38, 38, 0.35);
  background: rgba(220, 38, 38, 0.06);
  border-radius: 16px;
  padding: 12px 12px;
  margin-bottom: 14px;
}
.errTitle {
  font-weight: 950;
}
.empty {
  border: 1px dashed rgba(15, 23, 42, 0.2);
  border-radius: 18px;
  padding: 18px 16px;
  background: rgba(248, 250, 252, 0.7);
}
.emptyTitle {
  font-weight: 950;
  margin-bottom: 6px;
}

/* List items */
.list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feedItem {
  border: 1px solid rgba(15, 23, 42, 0.10);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 18px;
  padding: 14px 14px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}

.itemHead {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
}
.headMain {
  min-width: 0;
}
.textTitle {
  font-weight: 950;
  font-size: 15px;
  line-height: 1.35;
  word-break: break-word;
}
.headSub {
  margin-top: 4px;
  font-size: 12px;
}

/* Badges */
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: flex-end;
  align-items: center;
  flex-shrink: 0;
}
.badge {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(15, 23, 42, 0.12);
  background: rgba(248, 250, 252, 0.85);
  font-size: 12px;
  line-height: 1;
}
.badgeK {
  font-weight: 800;
  color: rgba(15, 23, 42, 0.6);
}
.badgeV {
  font-weight: 900;
  color: rgba(15, 23, 42, 0.86);
}
.badgeOk {
  border-color: rgba(16, 185, 129, 0.35);
  background: rgba(16, 185, 129, 0.08);
}
.badgeWarn {
  border-color: rgba(245, 158, 11, 0.35);
  background: rgba(245, 158, 11, 0.10);
}
.badgeMuted {
  opacity: 0.75;
}

/* Recommendation */
.recBox {
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 16px;
  background: rgba(248, 250, 252, 0.75);
  padding: 12px 12px;
  margin-bottom: 10px;
}
.recTitle {
  font-weight: 950;
  font-size: 13px;
  margin-bottom: 6px;
}
.recText {
  white-space: pre-wrap;
  line-height: 1.55;
  font-size: 13px;
}

/* Accordion */
.accordion {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.acc {
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.92);
  padding: 10px 12px;
}
.acc summary {
  cursor: pointer;
  list-style: none;
}
.acc summary::-webkit-details-marker {
  display: none;
}
.accSum {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 10px;
  font-weight: 950;
  font-size: 13px;
}
.accHint {
  font-weight: 800;
  font-size: 12px;
}
.accBody {
  margin-top: 10px;
}

/* KV */
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
  font-weight: 900;
  font-size: 12px;
  color: rgba(15, 23, 42, 0.7);
}
.v {
  font-size: 13px;
}

/* Habits */
.habits {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.habit {
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 14px;
  background: rgba(248, 250, 252, 0.70);
  padding: 10px 12px;
}
.habit summary {
  cursor: pointer;
  list-style: none;
}
.habit summary::-webkit-details-marker {
  display: none;
}
.habitSum {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.habitTitle {
  font-weight: 950;
  font-size: 13px;
  line-height: 1.35;
}
.habitMeta {
  font-size: 12px;
}
.habitBody {
  margin-top: 10px;
}

.ctxList {
  margin: 0;
  padding-left: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.ctxItem {
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.ctxTag {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(15, 23, 42, 0.12);
  background: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  font-weight: 900;
  color: rgba(15, 23, 42, 0.7);
}
.ctxVal {
  font-size: 13px;
  line-height: 1.45;
}

/* RAG section */
.ragPanel {
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 14px;
  background: rgba(248, 250, 252, 0.75);
  padding: 10px 12px;
}
.ragTitle {
  font-weight: 950;
  font-size: 12px;
  margin-bottom: 6px;
  color: rgba(15, 23, 42, 0.8);
}

.quotes {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.quote {
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
  padding: 10px 12px;
}

/* ✅ NEW: title + page */
.quoteHead {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 8px;
}
.quoteTitle {
  font-weight: 950;
  font-size: 13px;
  line-height: 1.25;
  color: rgba(15, 23, 42, 0.85);
  min-width: 0;
  word-break: break-word;
}
.quoteMeta {
  font-size: 12px;
  white-space: nowrap;
}
.quoteText {
  white-space: pre-wrap;
  line-height: 1.5;
  font-size: 13px;
}

/* Debug */
.details {
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.92);
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

.mono {
  white-space: pre-wrap;
  line-height: 1.55;
  font-size: 13px;
}
</style>
